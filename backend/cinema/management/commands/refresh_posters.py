import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Movie

API_KEY = "be071106a7d116eb087c1512c6ddfc01"
BASE_URL = "https://api.themoviedb.org/3"

# (movie_id_in_db, tmdb_id) pairs - exact list from the audit output,
# using the database primary key to target each row precisely
BROKEN_MOVIES = [
    (658, 1726), (660, 10138), (661, 10195), (662, 22136), (663, 24428),
    (665, 76338), (666, 100402), (668, 99861), (669, 102899), (670, 271110),
    (672, 283995), (676, 363088), (680, 497698), (686, 505642), (687, 640146),
    (689, 609681), (691, 49521), (693, 297761), (694, 297762), (695, 141052),
    (697, 287947), (699, 715931), (704, 572802), (705, 36657), (706, 36668),
    (707, 36669), (708, 127585), (709, 49538), (710, 100770), (711, 127526),
    (712, 182127), (713, 246655), (716, 320288), (720, 674), (721, 675),
    (722, 767), (723, 12444), (724, 12445), (725, 259316), (726, 338952),
    (727, 899112), (729, 1894), (731, 348350), (735, 1892), (740, 121),
    (743, 57529), (744, 122917), (746, 293167), (747, 373571), (751, 330),
    (752, 331), (753, 135397), (754, 351286), (756, 9799), (757, 584),
    (758, 9615), (759, 51497), (760, 82992), (761, 168259), (762, 337339),
    (763, 463906), (767, 324552), (769, 954), (770, 955), (772, 56292),
    (773, 177677), (777, 604), (778, 605), (779, 624860), (783, 324786),
    (786, 523427), (787, 259693), (789, 22), (790, 58), (791, 285),
    (792, 1865), (793, 166426), (794, 839033), (795, 882598), (796, 1075794),
    (797, 912349), (798, 1087822), (800, 1399), (802, 2190), (803, 1438),
    (804, 60574), (805, 60059), (808, 46648), (810, 67744), (816, 95479),
    (818, 108978), (819, 120089), (820, 1405), (821, 100088), (822, 85271),
    (825, 92782), (826, 88329), (827, 202555), (828, 82856), (829, 114461),
    (830, 92830), (831, 77875), (832, 128858), (833, 127529), (834, 139880),
    (835, 154112), (837, 255709), (838, 339877), (839, 564147), (840, 587412),
    (841, 690957), (843, 791373), (845, 66573), (847, 67178), (848, 76479),
    (850, 60735), (851, 79008), (852, 122226), (853, 801688), (854, 843307),
]


def fetch_current_data(tmdb_id, media_type, max_attempts=4):
    """Direct lookup by tmdb_id - not a search, not a guess. This is
    TMDB's own current record for an ID we already know is correct."""
    for attempt in range(max_attempts):
        session = requests.Session()
        try:
            r = session.get(
                f"{BASE_URL}/{media_type}/{tmdb_id}",
                params={"api_key": API_KEY},
                timeout=20,
            )
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                return None
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
            time.sleep(3 * (attempt + 1))
            continue
        finally:
            session.close()
    return "FAILED"


class Command(BaseCommand):
    help = "Refresh poster/backdrop paths for the 120 confirmed-broken movies via direct TMDB lookup"

    def handle(self, *args, **options):
        fixed = 0
        still_broken = []
        network_failures = []

        self.stdout.write(self.style.SUCCESS(f"\nRefreshing {len(BROKEN_MOVIES)} broken posters via direct TMDB lookup...\n"))

        for i, (db_id, tmdb_id) in enumerate(BROKEN_MOVIES, 1):
            movie = Movie.objects.filter(pk=db_id).first()
            if not movie:
                self.stdout.write(self.style.WARNING(f"  [{i}/{len(BROKEN_MOVIES)}] DB row not found: pk={db_id}"))
                continue

            media_type = "tv" if movie.type == "series" else "movie"
            data = fetch_current_data(tmdb_id, media_type)

            if data == "FAILED":
                network_failures.append(movie.title)
                self.stdout.write(self.style.WARNING(f"  [{i}/{len(BROKEN_MOVIES)}] Network failure: {movie.title}"))
                continue

            if data is None:
                still_broken.append(movie.title)
                self.stdout.write(self.style.ERROR(f"  [{i}/{len(BROKEN_MOVIES)}] tmdb_id no longer exists: {movie.title}"))
                continue

            new_poster = data.get("poster_path", "")
            new_backdrop = data.get("backdrop_path", "")

            if not new_poster and not new_backdrop:
                still_broken.append(movie.title)
                self.stdout.write(self.style.WARNING(f"  [{i}/{len(BROKEN_MOVIES)}] TMDB has no images for: {movie.title}"))
                continue

            movie.poster_path = new_poster or movie.poster_path
            movie.backdrop_path = new_backdrop or movie.backdrop_path
            movie.save()
            fixed += 1
            self.stdout.write(self.style.SUCCESS(f"  [{i}/{len(BROKEN_MOVIES)}] REFRESHED: {movie.title}"))

            time.sleep(0.2)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Refreshed:        {fixed}"))
        self.stdout.write(self.style.WARNING(f"Network failures: {len(network_failures)} (re-run to retry)"))
        self.stdout.write(self.style.ERROR(f"Still no image:   {len(still_broken)} (will use gradient fallback)"))
        if network_failures:
            self.stdout.write(f"\nRetry these: {network_failures}")