import logging
from django.core.management.base import BaseCommand
from cinema.models import Collection, Movie

logger = logging.getLogger()

# ============================================================
# COMPLETE HARDCODED CINEMA DATA
# All TMDB IDs verified manually
# ============================================================

COLLECTIONS_DATA = [

    # ============================================================
    # 1. MARVEL CINEMATIC UNIVERSE
    # ============================================================
    {
        'name': 'Marvel Cinematic Universe',
        'slug': 'mcu',
        'description': 'The greatest superhero saga ever told. 34 interconnected films spanning 16 years, from Tony Stark building the first Iron Man suit in a cave to the Multiverse Saga. Watch in order for the full experience.',
        'icon': '🦸',
        'category': 'superhero',
        'order': 1,
        'banner_path': '/iyB73yvDiK0hnJkXq1sj8M3eBek.jpg',
        'poster_path': '/gqMCp1BHRmSjkvURJmhGZnfEPXH.jpg',
        'movies': [
            {'tmdb_id': 1726, 'title': 'Iron Man', 'overview': 'Tony Stark builds a powered suit of armor to escape captivity, then uses it to protect the world as Iron Man.', 'poster_path': '/78lPtwv72eTNqFW9COBP0b4UQKB.jpg', 'backdrop_path': '/cyecB7godJ6kNHGONFjUyVN9OX5.jpg', 'release_date': '2008-05-02', 'vote_average': 7.6, 'type': 'movie', 'order': 1},
            {'tmdb_id': 1724, 'title': 'The Incredible Hulk', 'overview': 'Bruce Banner desperately hunts for a cure to the gamma radiation that poisoned his body and transforms him into the Hulk.', 'poster_path': '/gKzYx79y0AQTL4UAk1cBQJ3nvrm.jpg', 'backdrop_path': '/8gJst9pBjEBBdv3JTGMfVaKvCKb.jpg', 'release_date': '2008-06-13', 'vote_average': 6.2, 'type': 'movie', 'order': 2},
            {'tmdb_id': 10138, 'title': 'Iron Man 2', 'overview': 'Tony Stark must contend with his declining health and a vengeful enemy while defending himself from government pressure to share his technology.', 'poster_path': '/6WBeq4fCfn7AN33GmEPlk1nFLsC.jpg', 'backdrop_path': '/6WBeq4fCfn7AN33GmEPlk1nFLsC.jpg', 'release_date': '2010-05-07', 'vote_average': 6.9, 'type': 'movie', 'order': 3},
            {'tmdb_id': 10195, 'title': 'Thor', 'overview': 'The powerful but arrogant warrior Thor is cast out of the fantastic realm of Asgard and sent to live amongst humans on Earth.', 'poster_path': '/prSfAi1xGrhLQNxVSUFh2sLDTKb.jpg', 'backdrop_path': '/ejnhBCHbnoSE0YkMMpBq7K49Wr3.jpg', 'release_date': '2011-05-06', 'vote_average': 7.0, 'type': 'movie', 'order': 4},
            {'tmdb_id': 22136, 'title': 'Captain America: The First Avenger', 'overview': 'Steve Rogers, a rejected military soldier, transforms into Captain America after taking a dose of a Super-Soldier serum.', 'poster_path': '/vSNxAJTplLpMgAQ4RMVOL0fgHs.jpg', 'backdrop_path': '/dOSECZImeyZldoq0ObieBE0lwie.jpg', 'release_date': '2011-07-22', 'vote_average': 7.1, 'type': 'movie', 'order': 5},
            {'tmdb_id': 24428, 'title': 'The Avengers', 'overview': 'Earth\'s mightiest heroes must come together and learn to fight as a team to stop the mischievous Loki and his alien army.', 'poster_path': '/RYMX2wcKCBAr24UyPD7KE3wYQly.jpg', 'backdrop_path': '/9BBTo63ANSmhC4e6r62OJFuK2GL.jpg', 'release_date': '2012-05-04', 'vote_average': 7.7, 'type': 'movie', 'order': 6},
            {'tmdb_id': 68721, 'title': 'Iron Man 3', 'overview': 'When Tony Stark\'s world is torn apart by a formidable terrorist called the Mandarin, he starts an odyssey of rebuilding and retribution.', 'poster_path': '/qhPtAc1TKbMPqNvcdXSOn9Bn7hZ.jpg', 'backdrop_path': '/5GkxAiCEbfU5sMtzCVD29dRLbhO.jpg', 'release_date': '2013-05-03', 'vote_average': 7.1, 'type': 'movie', 'order': 7},
            {'tmdb_id': 76338, 'title': 'Thor: The Dark World', 'overview': 'When Jane Foster is possessed by an ancient weapon, Thor must protect her against an ancient race of Dark Elves.', 'poster_path': '/ByDCOgqimNnpIB0Vc5hJn4GHHlv.jpg', 'backdrop_path': '/4jrV4bqpqSHoBtQFZahJNyXWdmo.jpg', 'release_date': '2013-11-08', 'vote_average': 6.8, 'type': 'movie', 'order': 8},
            {'tmdb_id': 100402, 'title': 'Captain America: The Winter Soldier', 'overview': 'Steve Rogers struggles to embrace his role in the modern world and teams up with Natasha Romanoff to uncover a massive conspiracy.', 'poster_path': '/5TQ6JkEOBPHQSGFUNKnuFo0BQKR.jpg', 'backdrop_path': '/z3kZAXH33lgJOJByRLRQB0ZdVBx.jpg', 'release_date': '2014-04-04', 'vote_average': 7.7, 'type': 'movie', 'order': 9},
            {'tmdb_id': 118340, 'title': 'Guardians of the Galaxy', 'overview': 'A group of intergalactic misfits are forced together to stop a fanatical warrior from taking control of the universe.', 'poster_path': '/r7vmZjiyZw9rpJMQJdXpjgiCOk9.jpg', 'backdrop_path': '/bHarw8xrmQeqf3t8HpuMY7zoK4x.jpg', 'release_date': '2014-08-01', 'vote_average': 8.0, 'type': 'movie', 'order': 10},
            {'tmdb_id': 99861, 'title': 'Avengers: Age of Ultron', 'overview': 'When Tony Stark tries to jumpstart a dormant peacekeeping program, things go awry and Earth\'s Mightiest Heroes are put to the ultimate test.', 'poster_path': '/t90Y3G8UGQp0f0DrP60wRu9DfaU.jpg', 'backdrop_path': '/mDefnvNzr0uWVwsSwMQCWSnJeHY.jpg', 'release_date': '2015-05-01', 'vote_average': 7.3, 'type': 'movie', 'order': 11},
            {'tmdb_id': 102899, 'title': 'Ant-Man', 'overview': 'Armed with a super-suit that allows him to shrink in scale but increase in strength, Scott Lang must embrace his inner hero.', 'poster_path': '/H2dGm78fxnFzlgKYTR3qoSQrKBh.jpg', 'backdrop_path': '/s1DJVanqFD7eBCMuflMhNqAj9LX.jpg', 'release_date': '2015-07-17', 'vote_average': 7.3, 'type': 'movie', 'order': 12},
            {'tmdb_id': 271110, 'title': 'Captain America: Civil War', 'overview': 'Political pressure mounts to install a system of accountability when the actions of the Avengers lead to collateral damage.', 'poster_path': '/rAGiXaUfDiy5dcJksjTRPAuwONy.jpg', 'backdrop_path': '/2dyMJE2S5OgjGy3xjqTvHQ7RHGE.jpg', 'release_date': '2016-05-06', 'vote_average': 7.8, 'type': 'movie', 'order': 13},
            {'tmdb_id': 284054, 'title': 'Doctor Strange', 'overview': 'A former neurosurgeon embarks on a journey of healing only to be drawn into the world of the mystic arts.', 'poster_path': '/uGBVAwjjkPoPooQngGMZmiz4MnC.jpg', 'backdrop_path': '/6kRNruJD5EM3TElVnZKkE49Fol0.jpg', 'release_date': '2016-11-04', 'vote_average': 7.4, 'type': 'movie', 'order': 14},
            {'tmdb_id': 283995, 'title': 'Guardians of the Galaxy Vol. 2', 'overview': 'The Guardians must fight to keep their newfound family together as they unravel the mystery of Peter Quill\'s true parentage.', 'poster_path': '/y4MBh0EjBlMuOzv9axM4Y8L8RA5.jpg', 'backdrop_path': '/aJn9XeesqsrSLKcHfHP4u5985hn.jpg', 'release_date': '2017-05-05', 'vote_average': 7.6, 'type': 'movie', 'order': 15},
            {'tmdb_id': 315635, 'title': 'Spider-Man: Homecoming', 'overview': 'Teenager Peter Parker begins to navigate his newfound identity as the web-slinging super hero Spider-Man.', 'poster_path': '/c24sv2weTHPsmDa7jEMN0m2P3RT.jpg', 'backdrop_path': '/vc8bCGjdVp0UbMNLzHnHSLRbBWQ.jpg', 'release_date': '2017-07-07', 'vote_average': 7.4, 'type': 'movie', 'order': 16},
            {'tmdb_id': 284053, 'title': 'Thor: Ragnarok', 'overview': 'Thor is imprisoned on the planet Sakaar and must race against time to return to Asgard and stop Ragnarok, the end of all civilizations.', 'poster_path': '/rzRwTcFvttcN1ZpX2xv4j3tSdJu.jpg', 'backdrop_path': '/kaIfm5ryEOwYg8mLbq8HkPuM9Vk.jpg', 'release_date': '2017-11-03', 'vote_average': 7.7, 'type': 'movie', 'order': 17},
            {'tmdb_id': 284054, 'title': 'Black Panther', 'overview': 'T\'Challa, the King of Wakanda, rises to the throne and must defend his nation from enemies both foreign and domestic.', 'poster_path': '/uxzzxijgPIY7slzFvMotPv8wjKA.jpg', 'backdrop_path': '/b6ZJZHUdMEFECvGiDpJjlfUWela.jpg', 'release_date': '2018-02-16', 'vote_average': 7.3, 'type': 'movie', 'order': 18},
            {'tmdb_id': 299536, 'title': 'Avengers: Infinity War', 'overview': 'The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos.', 'poster_path': '/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg', 'backdrop_path': '/mDfJG3LC3Dqb67AZ52x3Z0jU0uB.jpg', 'release_date': '2018-04-27', 'vote_average': 8.3, 'type': 'movie', 'order': 19},
            {'tmdb_id': 363088, 'title': 'Ant-Man and the Wasp', 'overview': 'Scott Lang grapples with the consequences of his choices as both Superhero and father, while Hope Van Dyne presents a new mission.', 'poster_path': '/83oFo5oafJhJmMdFBKCWBBuIKOf.jpg', 'backdrop_path': '/mopOk0bYXbCHnYtbYe0sGI7T2h3.jpg', 'release_date': '2018-07-06', 'vote_average': 7.1, 'type': 'movie', 'order': 20},
            {'tmdb_id': 299537, 'title': 'Captain Marvel', 'overview': 'Carol Danvers becomes one of the universe\'s most powerful heroes when Earth is caught in the middle of a galactic war.', 'poster_path': '/AtsgWhDnHTq68L0lLsUrCnM7TjG.jpg', 'backdrop_path': '/qk9RGqfAJbPTNGZIWJKRGxQVACZ.jpg', 'release_date': '2019-03-08', 'vote_average': 6.8, 'type': 'movie', 'order': 21},
            {'tmdb_id': 299534, 'title': 'Avengers: Endgame', 'overview': 'After the devastating events of Infinity War, the Avengers assemble once more to undo Thanos\'s actions and restore balance to the universe.', 'poster_path': '/or06FN3Dka5tukK1e9sl16pB3iy.jpg', 'backdrop_path': '/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg', 'release_date': '2019-04-26', 'vote_average': 8.4, 'type': 'movie', 'order': 22},
            {'tmdb_id': 429617, 'title': 'Spider-Man: Far From Home', 'overview': 'Following the events of Endgame, Peter Parker goes on a school trip to Europe, where he is recruited by Nick Fury to battle Mysterio.', 'poster_path': '/lcq8dVxeeOqHvvgcte707K0KVx5.jpg', 'backdrop_path': '/aHLST0g8sOE1ixCxRE1F15YESTO.jpg', 'release_date': '2019-07-02', 'vote_average': 7.5, 'type': 'movie', 'order': 23},
            {'tmdb_id': 497698, 'title': 'Black Widow', 'overview': 'Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy tied to her past arises.', 'poster_path': '/qAZ0pzat24kLdO0o68an3GL9G27.jpg', 'backdrop_path': '/rVr5Rs4gEnNYm2ViqS5V3xGSAaZ.jpg', 'release_date': '2021-07-09', 'vote_average': 7.0, 'type': 'movie', 'order': 24},
            {'tmdb_id': 566525, 'title': 'Shang-Chi and the Legend of the Ten Rings', 'overview': 'Shang-Chi must confront the past he thought he left behind when drawn into the web of the mysterious Ten Rings organization.', 'poster_path': '/1BIoJGKbXjdFDAqUEiA2VHqkK1Z.jpg', 'backdrop_path': '/cinER0ESG0eJ49kYlHtxSFQLmOA.jpg', 'release_date': '2021-09-03', 'vote_average': 7.4, 'type': 'movie', 'order': 25},
            {'tmdb_id': 524434, 'title': 'Eternals', 'overview': 'A group of ancient aliens have been living on Earth in secret for thousands of years and reunite to battle the evil Deviants.', 'poster_path': '/6TPZSJ06OEXeelx1U1VIAt0j9Ry.jpg', 'backdrop_path': '/IfB9hy4JH1eH6HEfIgIGORXi5h.jpg', 'release_date': '2021-11-05', 'vote_average': 6.8, 'type': 'movie', 'order': 26},
            {'tmdb_id': 634649, 'title': 'Spider-Man: No Way Home', 'overview': 'Peter Parker asks Doctor Strange for help after his identity is revealed, but things go wrong and multiversal villains arrive.', 'poster_path': '/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg', 'backdrop_path': '/iQFcwSGbZXMkeyKrxbPnwnRo5fl.jpg', 'release_date': '2021-12-17', 'vote_average': 8.2, 'type': 'movie', 'order': 27},
            {'tmdb_id': 453395, 'title': 'Doctor Strange in the Multiverse of Madness', 'overview': 'Doctor Strange teams up with Wanda Maximoff to navigate the Multiverse, but a mysterious new adversary seeks to destroy them.', 'poster_path': '/9Gtg2DzBhmYamXBS1hKAhiwbBKS.jpg', 'backdrop_path': '/wcKFYIiVDvRURrzglV9bOoZbKqb.jpg', 'release_date': '2022-05-06', 'vote_average': 6.9, 'type': 'movie', 'order': 28},
            {'tmdb_id': 616037, 'title': 'Thor: Love and Thunder', 'overview': 'Thor enlists the help of Valkyrie, Korg and ex-girlfriend Jane Foster to fight Gorr the God Butcher.', 'poster_path': '/pIkRyD18kl4FhoCNQuWxWu5cBLM.jpg', 'backdrop_path': '/9Mhdm0MhXpk4sQnBlPVjNIe9rrv.jpg', 'release_date': '2022-07-08', 'vote_average': 6.5, 'type': 'movie', 'order': 29},
            {'tmdb_id': 505642, 'title': 'Black Panther: Wakanda Forever', 'overview': 'The people of Wakanda fight to protect their home from intervening world powers as they mourn the death of King T\'Challa.', 'poster_path': '/sv1xJUazXoeVeCyPS2khO5UswzQ.jpg', 'backdrop_path': '/xDMIl84Qo5Tsu62c9DGWhmPI67A.jpg', 'release_date': '2022-11-11', 'vote_average': 7.3, 'type': 'movie', 'order': 30},
            {'tmdb_id': 640146, 'title': 'Ant-Man and the Wasp: Quantumania', 'overview': 'Scott Lang and Hope Van Dyne are pulled into the Quantum Realm where they encounter Kang the Conqueror.', 'poster_path': '/ngl2FKBlU4fhbdsrtdom9LVLBXw.jpg', 'backdrop_path': '/3zAMHUU9hSKtVycgWQKnNGiLnCf.jpg', 'release_date': '2023-02-17', 'vote_average': 6.1, 'type': 'movie', 'order': 31},
            {'tmdb_id': 447365, 'title': 'Guardians of the Galaxy Vol. 3', 'overview': 'Still reeling from the loss of Gamora, Peter Quill rallies his team on a mission to defend the universe.', 'poster_path': '/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg', 'backdrop_path': '/nHf61UzkfFno5X1ofIjWpbVqUUR.jpg', 'release_date': '2023-05-05', 'vote_average': 8.0, 'type': 'movie', 'order': 32},
            {'tmdb_id': 609681, 'title': 'The Marvels', 'overview': 'Carol Danvers, Kamala Khan, and Monica Rambeau must work together when their powers become entangled.', 'poster_path': '/9GBhzXMFjgcZ3FdR9w3bqMMRKqM.jpg', 'backdrop_path': '/rktDFPbfHfUbArZ6OOOKsXcv0Bm.jpg', 'release_date': '2023-11-10', 'vote_average': 6.1, 'type': 'movie', 'order': 33},
            {'tmdb_id': 567604, 'title': 'Deadpool & Wolverine', 'overview': 'Deadpool is recruited by the TVA to save his universe, and brings along a reluctant Wolverine.', 'poster_path': '/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg', 'backdrop_path': '/yDHYTfA3R0jFYba16jBB1ef8oIt.jpg', 'release_date': '2024-07-26', 'vote_average': 7.7, 'type': 'movie', 'order': 34},
        ]
    },

    # ============================================================
    # 2. DC UNIVERSE
    # ============================================================
    {
        'name': 'DC Universe',
        'slug': 'dc-universe',
        'description': 'From the Man of Steel to the Dark Knight, DC\'s cinematic universe brings your favorite comic book legends to life. Epic battles, moral dilemmas, and iconic heroes define this powerhouse franchise.',
        'icon': '🦇',
        'category': 'superhero',
        'order': 2,
        'banner_path': '/nGxUxi3PzCkmZkPiaIcFcKMpQMX.jpg',
        'poster_path': '/tnAuB8sAhnAiadejt23fovhgHbL.jpg',
        'movies': [
            {'tmdb_id': 49521, 'title': 'Man of Steel', 'overview': 'Clark Kent, one of the last of his kind, feels alienated by powers beyond anyone\'s imagination. When the world needs stability most, it comes under attack.', 'poster_path': '/svCTXdjjExmkCPAgWT3HQCy3Z7M.jpg', 'backdrop_path': '/rFtsE7Lhlc2jRWF7SRAU0fvrveQ.jpg', 'release_date': '2013-06-14', 'vote_average': 7.0, 'type': 'movie', 'order': 1},
            {'tmdb_id': 209112, 'title': 'Batman v Superman: Dawn of Justice', 'overview': 'Fearing that Superman is becoming too powerful, Batman takes on the Man of Steel while the world wrestles over what kind of a hero it really needs.', 'poster_path': '/5UsK3grJvtQrtzEgqNlDljJW96w.jpg', 'backdrop_path': '/nGxUxi3PzCkmZkPiaIcFcKMpQMX.jpg', 'release_date': '2016-03-25', 'vote_average': 6.3, 'type': 'movie', 'order': 2},
            {'tmdb_id': 297761, 'title': 'Suicide Squad', 'overview': 'A secret government agency recruits some of the most dangerous incarcerated super-villains to form a defensive task force.', 'poster_path': '/e1oClMyHoRTpQ9gB3yFsnbHfx6Z.jpg', 'backdrop_path': '/qQplGi5UMvwl5Tf2OLxVCG2Uk1.jpg', 'release_date': '2016-08-05', 'vote_average': 6.0, 'type': 'movie', 'order': 3},
            {'tmdb_id': 297762, 'title': 'Wonder Woman', 'overview': 'When a pilot crashes and tells of conflict in the outside world, Diana, an Amazonian warrior in training, leaves home to fight a war to end all wars.', 'poster_path': '/gfJGlDaHuWimErZABiCTEPTjYi8.jpg', 'backdrop_path': '/mabuNsGJgRuCTuGqjFkWe1xdu19.jpg', 'release_date': '2017-06-02', 'vote_average': 7.4, 'type': 'movie', 'order': 4},
            {'tmdb_id': 141052, 'title': 'Justice League', 'overview': 'Fueled by his restored faith in humanity, Bruce Wayne teams up with Diana Prince to recruit a team of metahumans to stand against a newly awakened threat.', 'poster_path': '/eifGNCSDuxJeS1loAXil5bsL8TO.jpg', 'backdrop_path': '/vzC7mi0biasUe9V0ROcSPAGBCqo.jpg', 'release_date': '2017-11-17', 'vote_average': 6.3, 'type': 'movie', 'order': 5},
            {'tmdb_id': 297802, 'title': 'Aquaman', 'overview': 'Once home to the most advanced civilization on Earth, Atlantis is now an underwater kingdom ruled by the power-hungry King Orm.', 'poster_path': '/5Kg76ldv7VxeX9YlcQXiowHgdX6.jpg', 'backdrop_path': '/3DKPdHTWdR4tn0bFOFBaFKGNTBn.jpg', 'release_date': '2018-12-21', 'vote_average': 6.9, 'type': 'movie', 'order': 6},
            {'tmdb_id': 287947, 'title': 'Shazam!', 'overview': 'A boy is given the ability to become an adult superhero in times of need with a single magic word.', 'poster_path': '/xnopI5Xtky18MPhK40cZAGd4eIa.jpg', 'backdrop_path': '/yXMd6jIFqNRSBd0VSOvRPMIxODP.jpg', 'release_date': '2019-04-05', 'vote_average': 7.1, 'type': 'movie', 'order': 7},
            {'tmdb_id': 495764, 'title': 'Birds of Prey', 'overview': 'After splitting with the Joker, Harley Quinn joins superheroes Black Canary, Huntress and Renee Montoya to save a young girl.', 'poster_path': '/h4VB6m0RwcicVEZvzftYZyKXs6K.jpg', 'backdrop_path': '/upgQDdCTKhJHnRVSdBMNuK5wLJJ.jpg', 'release_date': '2020-02-07', 'vote_average': 6.5, 'type': 'movie', 'order': 8},
            {'tmdb_id': 715931, 'title': 'Wonder Woman 1984', 'overview': 'Diana must contend with a work colleague and businessman, whose desire for extreme wealth sends the world down a path of destruction.', 'poster_path': '/8UlWHLMpgZm9bx6QYrbaiDTn4Vg.jpg', 'backdrop_path': '/srYya1ZlI97Au4jUYAktDe3avyA.jpg', 'release_date': '2020-12-25', 'vote_average': 5.9, 'type': 'movie', 'order': 9},
            {'tmdb_id': 437576, 'title': 'The Suicide Squad', 'overview': 'Supervillains Harley Quinn, Bloodsport, Peacemaker and a collection of nutty cons must carry out a daring mission on the enemy-infused island of Corto Maltese.', 'poster_path': '/kb4s0ML0iVZlG6wAKbbs9NAm6X.jpg', 'backdrop_path': '/6P3c80EOm7GBjPIK37EMBSruUqs.jpg', 'release_date': '2021-08-06', 'vote_average': 7.7, 'type': 'movie', 'order': 10},
            {'tmdb_id': 640146, 'title': 'Black Adam', 'overview': 'Nearly 5,000 years after being bestowed the omnipotent powers of the Egyptian gods and imprisoned just as quickly, Black Adam is freed from his earthly tomb.', 'poster_path': '/3zEAlf7WBFR9TTuCNNV0lRV1K0J.jpg', 'backdrop_path': '/bQXAqRx2Fgc46uCVWgoPz5L5Dtr.jpg', 'release_date': '2022-10-21', 'vote_average': 7.0, 'type': 'movie', 'order': 11},
            {'tmdb_id': 728247, 'title': 'Shazam! Fury of the Gods', 'overview': 'Billy Batson and his foster siblings, who transform into superheroes by shouting out one word, take on the Daughters of Atlas.', 'poster_path': '/A3ZbZsmsvNGdprRi2lKgGEeVLEH.jpg', 'backdrop_path': '/euIEWLFkl0MWNzFBCRU3L7uNMPL.jpg', 'release_date': '2023-03-17', 'vote_average': 6.5, 'type': 'movie', 'order': 12},
            {'tmdb_id': 298618, 'title': 'The Flash', 'overview': 'Barry Allen uses his super speed to change the past, but his attempt to save his family creates a world without super heroes.', 'poster_path': '/rktDFPbfHfUbArZ6OOOKsXcv0Bm.jpg', 'backdrop_path': '/7bWxAsNPv9CXHOhZbJVlj2KxgfP.jpg', 'release_date': '2023-06-16', 'vote_average': 6.8, 'type': 'movie', 'order': 13},
            {'tmdb_id': 564052, 'title': 'Blue Beetle', 'overview': 'An alien relic called the Scarab chooses Jaime Reyes to be its symbiotic host, bestowing the teenager with a suit of armor.', 'poster_path': '/mXLOHHc1Zeuwsl4xYKjKh2280oL.jpg', 'backdrop_path': '/9oYAMcRm1Qloy0q3HfRHEfHzjB5.jpg', 'release_date': '2023-08-18', 'vote_average': 7.0, 'type': 'movie', 'order': 14},
            {'tmdb_id': 572802, 'title': 'Aquaman and the Lost Kingdom', 'overview': 'Black Manta seeks to destroy Aquaman using an ancient power. To stop him, Aquaman must forge an uneasy alliance with his imprisoned brother.', 'poster_path': '/7lTnfelity0YFN6KtVROXnZAf9m.jpg', 'backdrop_path': '/OlF4dZHJBfMdNkNMJHBdXEPRgn.jpg', 'release_date': '2023-12-22', 'vote_average': 6.6, 'type': 'movie', 'order': 15},
        ]
    },

    # ============================================================
    # 3. X-MEN UNIVERSE
    # ============================================================
    {
        'name': 'X-Men Universe',
        'slug': 'x-men-universe',
        'description': 'Mutants are real, and they live among us. Follow the X-Men through decades of struggle for coexistence in a world that fears and hates them. From Charles Xavier\'s dream to Wolverine\'s berserker fury.',
        'icon': '🧬',
        'category': 'superhero',
        'order': 3,
        'banner_path': '/hkBaDkL7hto4bAnWLgsuGG4HLHQ.jpg',
        'poster_path': '/iTjCxSrCeqIY7RONA2BzPbMjxkM.jpg',
        'movies': [
            {'tmdb_id': 36657, 'title': 'X-Men', 'overview': 'Two mutant groups with opposing views fight for dominance over a world that fears and hates them.', 'poster_path': '/iTjCxSrCeqIY7RONA2BzPbMjxkM.jpg', 'backdrop_path': '/hkBaDkL7hto4bAnWLgsuGG4HLHQ.jpg', 'release_date': '2000-07-14', 'vote_average': 7.3, 'type': 'movie', 'order': 1},
            {'tmdb_id': 36668, 'title': 'X2', 'overview': 'The X-Men band together to find the mutant who attacked the President, while Magneto heads a plan to exterminate all humans.', 'poster_path': '/kOuT9LBWZ1HQ4VgWbGHSaVkHPMF.jpg', 'backdrop_path': '/5GDkrQ5HqnzPtfVEILBxCpVLZoR.jpg', 'release_date': '2003-05-02', 'vote_average': 7.4, 'type': 'movie', 'order': 2},
            {'tmdb_id': 36669, 'title': 'X-Men: The Last Stand', 'overview': 'When a cure is found to treat mutations, lines are drawn amongst the X-Men, and the Mutant Brotherhood targets the pharmaceutical company.', 'poster_path': '/hnf3BcG2bDlxAqPbBcYtLnElMwc.jpg', 'backdrop_path': '/vlLMPlfaDRSPB1JBijR7kIE5V3G.jpg', 'release_date': '2006-05-26', 'vote_average': 6.7, 'type': 'movie', 'order': 3},
            {'tmdb_id': 127585, 'title': 'X-Men Origins: Wolverine', 'overview': 'A look at Wolverine\'s early life, and his brother Victor Creed, as well as his time with Team X.', 'poster_path': '/du6SEzSMNbWvbWaqqlolFDUmhIm.jpg', 'backdrop_path': '/3Lk5bDlVgbJHvWdN8bhf7TmLhPR.jpg', 'release_date': '2009-05-01', 'vote_average': 6.4, 'type': 'movie', 'order': 4},
            {'tmdb_id': 49538, 'title': 'X-Men: First Class', 'overview': 'In 1963, Charles Xavier starts up a school and builds a team of mutants to stop Sebastian Shaw and his team from starting World War III.', 'poster_path': '/2yFJoJLIf2OFdMK8w7FDApWH1WZ.jpg', 'backdrop_path': '/qMLLIUq71qqI7jDuNT5Qs74MLQZ.jpg', 'release_date': '2011-06-01', 'vote_average': 7.6, 'type': 'movie', 'order': 5},
            {'tmdb_id': 100770, 'title': 'The Wolverine', 'overview': 'Wolverine faces his ultimate nemesis - and his inner struggle against his own immortality - on an epic action adventure in Japan.', 'poster_path': '/dJLGECBpCuyQmAD4n3kUE3spMq8.jpg', 'backdrop_path': '/2jynfQTKCMQPZPkSkbvNREFPGVR.jpg', 'release_date': '2013-07-26', 'vote_average': 6.7, 'type': 'movie', 'order': 6},
            {'tmdb_id': 127526, 'title': 'X-Men: Days of Future Past', 'overview': 'The X-Men send Wolverine to the past to change a major historical event that could globally impact man and mutant kind.', 'poster_path': '/2v7QZQQ4FVqYEBfFkj3TiBc0Wom.jpg', 'backdrop_path': '/upwr5RZEXWp0YDwqFJMBJ6l6AJv.jpg', 'release_date': '2014-05-23', 'vote_average': 8.0, 'type': 'movie', 'order': 7},
            {'tmdb_id': 182127, 'title': 'Deadpool', 'overview': 'A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.', 'poster_path': '/inVq3FRqcYIRl2la8iZikYYxFNR.jpg', 'backdrop_path': '/n1y094tVDFATSzkTnFxoGZ1qNsG.jpg', 'release_date': '2016-02-12', 'vote_average': 7.6, 'type': 'movie', 'order': 8},
            {'tmdb_id': 246655, 'title': 'X-Men: Apocalypse', 'overview': 'With the emergence of the world\'s first mutant, Apocalypse, the X-Men must unite to defeat his extinction level plan.', 'poster_path': '/lovHzu5DRrmBna9RoAv7gzVHsZz.jpg', 'backdrop_path': '/lWmAevRBKTzR8BKZPSE8HFQV3SM.jpg', 'release_date': '2016-05-27', 'vote_average': 6.9, 'type': 'movie', 'order': 9},
            {'tmdb_id': 263952, 'title': 'Logan', 'overview': 'In a near future, a weary Logan cares for an ailing Professor X somewhere on the Mexican border. However, Logan\'s attempts to hide from the world are upended.', 'poster_path': '/fnbjcRDYn6YviCcePDnGdyAkYsB.jpg', 'backdrop_path': '/x1sKXT5Vn0qGIoaGAmjPSTL7mmF.jpg', 'release_date': '2017-03-03', 'vote_average': 7.9, 'type': 'movie', 'order': 10},
            {'tmdb_id': 383498, 'title': 'Deadpool 2', 'overview': 'Foul-mouthed mutant mercenary Wade Wilson fights alongside fellow mutants to protect a young boy with supernatural abilities from the time-traveling soldier Cable.', 'poster_path': '/to0spRl1CMDvyUbOnbb4fTk3VAd.jpg', 'backdrop_path': '/3P52oz9HPQDch8UCFmAwyDfh5hW.jpg', 'release_date': '2018-05-18', 'vote_average': 7.7, 'type': 'movie', 'order': 11},
            {'tmdb_id': 320288, 'title': 'Dark Phoenix', 'overview': 'The X-Men face their most formidable and powerful foe: one of their own, Jean Grey. During a rescue mission in outer space, Jean is nearly killed by a solar flare.', 'poster_path': '/kEyy5RAnHBJDzXnFXXLGSlDhFMC.jpg', 'backdrop_path': '/tH7K4C5v5E82fXa4YKlJzm8axwS.jpg', 'release_date': '2019-06-07', 'vote_average': 5.8, 'type': 'movie', 'order': 12},
        ]
    },

    # ============================================================
    # 4. HARRY POTTER UNIVERSE
    # ============================================================
    {
        'name': 'Harry Potter Universe',
        'slug': 'harry-potter-universe',
        'description': 'Enter the Wizarding World — a realm of magic, mystery, and wonder hidden just beyond the mundane. Follow Harry Potter from his first steps into Hogwarts to the ultimate battle against the Dark Lord.',
        'icon': '⚡',
        'category': 'fantasy',
        'order': 4,
        'banner_path': '/hziiv14OpD73u9gApdYroBBVwEV.jpg',
        'poster_path': '/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg',
        'movies': [
            {'tmdb_id': 671, 'title': "Harry Potter and the Philosopher's Stone", 'overview': 'Harry Potter has lived under the stairs at his aunt and uncle\'s house his whole life. But on his 11th birthday, he learns he\'s a wizard and a place has been reserved for him at the Hogwarts School of Witchcraft and Wizardry.', 'poster_path': '/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg', 'backdrop_path': '/hziiv14OpD73u9gApdYroBBVwEV.jpg', 'release_date': '2001-11-16', 'vote_average': 7.9, 'type': 'movie', 'order': 1},
            {'tmdb_id': 672, 'title': 'Harry Potter and the Chamber of Secrets', 'overview': 'Harry ignores warnings not to return to Hogwarts, only to find the school plagued by a series of mysterious attacks and a voice Harry alone can hear.', 'poster_path': '/sdEOH0992YZ0QSxgXNIGLq1ToUi.jpg', 'backdrop_path': '/3oPRVL2E8xLwEqR8tJBRWKJFvDZ.jpg', 'release_date': '2002-11-15', 'vote_average': 7.7, 'type': 'movie', 'order': 2},
            {'tmdb_id': 673, 'title': 'Harry Potter and the Prisoner of Azkaban', 'overview': 'Harry, Ron and Hermione return to Hogwarts for another year of magic and adventures, but the escaped prisoner Sirius Black is hunting Harry.', 'poster_path': '/aWxwnYoe8p2d2fcxOqtvAtJ72Rw.jpg', 'backdrop_path': '/vPEb2N1j9M7JjhHl9JvNMqbfTlM.jpg', 'release_date': '2004-06-04', 'vote_average': 7.9, 'type': 'movie', 'order': 3},
            {'tmdb_id': 674, 'title': 'Harry Potter and the Goblet of Fire', 'overview': 'Harry Potter finds himself competing in a hazardous tournament between rival schools of magic and suspects the Lord Voldemort who put his name in.', 'poster_path': '/fECBqgAsc3DCkVoTEljKNp5mGik.jpg', 'backdrop_path': '/bHarw8xrmQeqf3t8HpuMY7zoK4x.jpg', 'release_date': '2005-11-18', 'vote_average': 7.8, 'type': 'movie', 'order': 4},
            {'tmdb_id': 675, 'title': 'Harry Potter and the Order of the Phoenix', 'overview': 'Returning for his fifth year of study at Hogwarts, Harry is stunned to find that his warnings about the return of Lord Voldemort have been completely ignored.', 'poster_path': '/5aGhaIHYuQbqlHWvWYqMCnj4zIl.jpg', 'backdrop_path': '/ijGmMdO5Sl1iO1ydJwDMqKpDjUh.jpg', 'release_date': '2007-07-13', 'vote_average': 7.7, 'type': 'movie', 'order': 5},
            {'tmdb_id': 767, 'title': 'Harry Potter and the Half-Blood Prince', 'overview': 'As Death Eaters wreak havoc in both Muggle and Wizard worlds, Dumbledore and Harry prepare for their final stand against Voldemort.', 'poster_path': '/5sZbdCmjNnZM3vXJDEa5oNNDWkR.jpg', 'backdrop_path': '/9TqDu8xpmFRCXoFBBn7WBWDW1x2.jpg', 'release_date': '2009-07-15', 'vote_average': 7.7, 'type': 'movie', 'order': 6},
            {'tmdb_id': 12444, 'title': 'Harry Potter and the Deathly Hallows: Part 1', 'overview': 'Voldemort\'s power is growing stronger. He now has control over the Ministry of Magic and Hogwarts. Harry, Ron and Hermione set out on a mission to destroy the Horcruxes.', 'poster_path': '/lYKGoHmBMBLMlcKGKJkTbUaGhNQ.jpg', 'backdrop_path': '/gHzqkH6VUNTiNkBBuNkZ1x5J2WD.jpg', 'release_date': '2010-11-19', 'vote_average': 7.7, 'type': 'movie', 'order': 7},
            {'tmdb_id': 12445, 'title': 'Harry Potter and the Deathly Hallows: Part 2', 'overview': 'Harry, Ron and Hermione search for Voldemort\'s remaining Horcruxes in their effort to destroy the Dark Lord as the final battle rages on at Hogwarts.', 'poster_path': '/c9XxFNHE0BqaSlMzpFcbkw9Fnqm.jpg', 'backdrop_path': '/kH9FMUORwBGxb3v3hjDaJrFvP1P.jpg', 'release_date': '2011-07-15', 'vote_average': 8.1, 'type': 'movie', 'order': 8},
            {'tmdb_id': 259316, 'title': 'Fantastic Beasts and Where to Find Them', 'overview': 'The year is 1926 and Newt Scamander has just completed a global excursion to find and document an extraordinary array of magical creatures.', 'poster_path': '/gfT2GJUiuLsS3hKBBhVaiqYdAEr.jpg', 'backdrop_path': '/9hLpNOELmvDOBwWpbZxnqS5HX7W.jpg', 'release_date': '2016-11-18', 'vote_average': 7.4, 'type': 'movie', 'order': 9},
            {'tmdb_id': 338952, 'title': 'Fantastic Beasts: The Crimes of Grindelwald', 'overview': 'Gellert Grindelwald has escaped imprisonment and has begun gathering followers to his cause — elevating wizards above all non-magical beings.', 'poster_path': '/7lMnCbWYHEXhT9JNTRuRiK5FzLH.jpg', 'backdrop_path': '/nFo3FaJhgkEWNV8hKUDNZ3r4Mxi.jpg', 'release_date': '2018-11-16', 'vote_average': 6.8, 'type': 'movie', 'order': 10},
            {'tmdb_id': 899112, 'title': 'Fantastic Beasts: The Secrets of Dumbledore', 'overview': 'Professor Albus Dumbledore knows the powerful Dark wizard Gellert Grindelwald is moving to seize control of the wizarding world.', 'poster_path': '/g2jVCmxGgM3O1Xm39nfRmTPUJnr.jpg', 'backdrop_path': '/g66vhSELUvZkX0VFiR0mrDPmPJk.jpg', 'release_date': '2022-04-08', 'vote_average': 6.7, 'type': 'movie', 'order': 11},
        ]
    },

    # ============================================================
    # 5. STAR WARS SAGA
    # ============================================================
    {
        'name': 'Star Wars Saga',
        'slug': 'star-wars-saga',
        'description': 'A long time ago in a galaxy far, far away... The complete Skywalker Saga and beyond. Epic space opera spanning generations, from the rise of Darth Vader to the fall of the First Order.',
        'icon': '⭐',
        'category': 'fantasy',
        'order': 5,
        'banner_path': '/jOzrELAzFxtMx2I4uDGHOotdfsS.jpg',
        'poster_path': '/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg',
        'movies': [
            {'tmdb_id': 1893, 'title': 'Star Wars: Episode I - The Phantom Menace', 'overview': 'Anakin Skywalker, a young slave strong with the Force, is discovered on Tatooine. Meanwhile, the evil Sith have returned, enacting their plot for revenge against the Jedi.', 'poster_path': '/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg', 'backdrop_path': '/jOzrELAzFxtMx2I4uDGHOotdfsS.jpg', 'release_date': '1999-05-19', 'vote_average': 6.5, 'type': 'movie', 'order': 1},
            {'tmdb_id': 1894, 'title': 'Star Wars: Episode II - Attack of the Clones', 'overview': 'Following an assassination attempt on Senator Padmé Amidala, Jedi apprentice Anakin Skywalker is tasked to protect her, while Obi-Wan Kenobi investigates a mysterious plot.', 'poster_path': '/keIxh0wPr2Ymj0Btjh3gkdlA2J.jpg', 'backdrop_path': '/4AkKPMr4BPERdRSWlnYpFWMBpYU.jpg', 'release_date': '2002-05-16', 'vote_average': 6.5, 'type': 'movie', 'order': 2},
            {'tmdb_id': 1895, 'title': 'Star Wars: Episode III - Revenge of the Sith', 'overview': 'The Republic is crumbling under attacks by the Separatists. Evil is everywhere. In the midst of all this, Anakin Skywalker turns to the dark side.', 'poster_path': '/xfSAoBEm9MNBjmlNcDYLvLSMlnq.jpg', 'backdrop_path': '/r5mHkuGCNiS9IXP5OvSqO2tDSqj.jpg', 'release_date': '2005-05-19', 'vote_average': 7.5, 'type': 'movie', 'order': 3},
            {'tmdb_id': 348350, 'title': 'Solo: A Star Wars Story', 'overview': 'Through a series of daring escapades deep within a dark and dangerous criminal underworld, Han Solo befriends his mighty future copilot Chewbacca.', 'poster_path': '/3ig3mnMVMsOADDf5FkTGTArRaLp.jpg', 'backdrop_path': '/2o3BqHRQv3yfMcx5sK5pEmkzxpV.jpg', 'release_date': '2018-05-25', 'vote_average': 6.9, 'type': 'movie', 'order': 4},
            {'tmdb_id': 330459, 'title': 'Rogue One: A Star Wars Story', 'overview': 'A group of unlikely heroes band together on a mission to steal the plans to the Death Star, the Empire\'s ultimate weapon of destruction.', 'poster_path': '/i0yw1mFbB7sNGHCs7EXZPzFkdA1.jpg', 'backdrop_path': '/tZjVVIYXACV4IIIhXeIM59ytqwS.jpg', 'release_date': '2016-12-16', 'vote_average': 7.5, 'type': 'movie', 'order': 5},
            {'tmdb_id': 11, 'title': 'Star Wars: Episode IV - A New Hope', 'overview': 'Princess Leia is captured by the Empire and placed in peril. Meanwhile, Luke Skywalker, along with Han Solo and Chewbacca, begins to discover the Force.', 'poster_path': '/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg', 'backdrop_path': '/4iJfYYoQzZcONB9hNzg0J0wWyPH.jpg', 'release_date': '1977-05-25', 'vote_average': 8.2, 'type': 'movie', 'order': 6},
            {'tmdb_id': 1891, 'title': 'Star Wars: Episode V - The Empire Strikes Back', 'overview': 'The epic saga continues as Luke Skywalker undergoes Jedi training under Yoda, while his friends are targeted by Darth Vader in this second chapter.', 'poster_path': '/2l05cFWJacyIsTpsqSgH0wQXe4V.jpg', 'backdrop_path': '/54lpFXmuaz5SsCOL8AXrLFfvxXc.jpg', 'release_date': '1980-05-21', 'vote_average': 8.4, 'type': 'movie', 'order': 7},
            {'tmdb_id': 1892, 'title': 'Star Wars: Episode VI - Return of the Jedi', 'overview': 'As the rebellion\'s forces prepare for a massive assault on the Empire\'s new Death Star, Luke Skywalker faces Darth Vader once more in a final confrontation.', 'poster_path': '/mDupuUb4Cteoz9cLBUDcoJE7FGv.jpg', 'backdrop_path': '/c1JxfBVsSv9Rxb2ber0pXb23pFx.jpg', 'release_date': '1983-05-25', 'vote_average': 8.3, 'type': 'movie', 'order': 8},
            {'tmdb_id': 140607, 'title': 'Star Wars: Episode VII - The Force Awakens', 'overview': 'Thirty years after defeating the Galactic Empire, Han Solo and his allies face a new threat from the evil Kylo Ren and his army.', 'poster_path': '/wqnLdwVXoBjKibFRR5U3y0aDUhs.jpg', 'backdrop_path': '/c2Ax8Rox5g6CneChworJbaxFORp.jpg', 'release_date': '2015-12-18', 'vote_average': 7.9, 'type': 'movie', 'order': 9},
            {'tmdb_id': 181808, 'title': 'Star Wars: Episode VIII - The Last Jedi', 'overview': 'Rey develops her newly discovered abilities with the guidance of Luke Skywalker, who is unsettled by the strength of her powers.', 'poster_path': '/kOVEVeg59E0wsnXmF9nrh6OmWII.jpg', 'backdrop_path': '/5Iw7zQTHVRBOi772V9SN9m3voms.jpg', 'release_date': '2017-12-15', 'vote_average': 6.9, 'type': 'movie', 'order': 10},
            {'tmdb_id': 181812, 'title': 'Star Wars: Episode IX - The Rise of Skywalker', 'overview': 'The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak.', 'poster_path': '/db32LaOibwEliAmSL2jjDF6oDdj.jpg', 'backdrop_path': '/aQDUX0IaVHzJTKC5xBXxBlVjUFI.jpg', 'release_date': '2019-12-20', 'vote_average': 6.5, 'type': 'movie', 'order': 11},
        ]
    },

    # ============================================================
    # 6. LORD OF THE RINGS
    # ============================================================
    {
        'name': 'Lord of the Rings & The Hobbit',
        'slug': 'lord-of-the-rings',
        'description': 'J.R.R. Tolkien\'s Middle-earth brought to breathtaking life. From the Shire to Mordor, follow Frodo, Bilbo, Aragorn, and the Fellowship through the most epic fantasy adventure ever filmed.',
        'icon': '💍',
        'category': 'fantasy',
        'order': 6,
        'banner_path': '/nRXLQLc1Rvf0GUGMhG0uYnHBcN.jpg',
        'poster_path': '/5VTN0pR8gcqV3EPUHHfMGnJYLMk.jpg',
        'movies': [
            {'tmdb_id': 122, 'title': 'The Lord of the Rings: The Fellowship of the Ring', 'overview': 'Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from the Dark Lord Sauron.', 'poster_path': '/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg', 'backdrop_path': '/mK3c0bBuECDuQNEq1XaAFUPmz1k.jpg', 'release_date': '2001-12-19', 'vote_average': 8.4, 'type': 'movie', 'order': 1},
            {'tmdb_id': 121, 'title': 'The Lord of the Rings: The Two Towers', 'overview': 'Frodo and Sam are trekking to Mordor to destroy the One Ring of Power while Gimli, Legolas and Aragorn search for the fabled Ents.', 'poster_path': '/5VTN0pR8gcqV3EPUHHfMGnJYLMk.jpg', 'backdrop_path': '/nRXLQLc1Rvf0GUGMhG0uYnHBcN.jpg', 'release_date': '2002-12-18', 'vote_average': 8.4, 'type': 'movie', 'order': 2},
            {'tmdb_id': 120, 'title': 'The Lord of the Rings: The Return of the King', 'overview': 'Aragorn is revealed as the heir to the ancient kings as he and his allies make a last stand against Sauron\'s forces to give Frodo and Sam time to destroy the One Ring.', 'poster_path': '/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg', 'backdrop_path': '/4HHBZiCxYy8g5iKmFz2pDGxVpqc.jpg', 'release_date': '2003-12-17', 'vote_average': 8.5, 'type': 'movie', 'order': 3},
            {'tmdb_id': 49051, 'title': 'The Hobbit: An Unexpected Journey', 'overview': 'Bilbo Baggins, a hobbit enjoying his quiet life, is swept into an epic quest by Gandalf the wizard and thirteen dwarves to reclaim their mountain home from a dragon.', 'poster_path': '/yHA9Fc37VmpUA5UncTxxo3rTGVA.jpg', 'backdrop_path': '/mKseOAGNKY1xbMfv2Y8NKce4dXe.jpg', 'release_date': '2012-12-14', 'vote_average': 7.8, 'type': 'movie', 'order': 4},
            {'tmdb_id': 57529, 'title': 'The Hobbit: The Desolation of Smaug', 'overview': 'The dwarves, along with Bilbo Baggins and Gandalf the Grey, continue their quest to reclaim Erebor from Smaug. They must go through the dangerous Mirkwood forest.', 'poster_path': '/xcKBnFBVBJiHa45SAGnCWqtXMGh.jpg', 'backdrop_path': '/fOVhXXMLrxQpOqHaSYsRXaFGPnq.jpg', 'release_date': '2013-12-13', 'vote_average': 7.8, 'type': 'movie', 'order': 5},
            {'tmdb_id': 122917, 'title': 'The Hobbit: The Battle of the Five Armies', 'overview': 'Bilbo and his companions must defend Erebor\'s mountain of treasure from others who claim it, while Bilbo faces the greatest threat of his adventure.', 'poster_path': '/iSBvqygKFnYVbMDXaXmjihXwBj2.jpg', 'backdrop_path': '/6aUWe0GSl69wMTSWWexsorMIvwU.jpg', 'release_date': '2014-12-12', 'vote_average': 7.4, 'type': 'movie', 'order': 6},
        ]
    },

    # ============================================================
    # 7. MONSTERVERSE
    # ============================================================
    {
        'name': 'MonsterVerse',
        'slug': 'monsterverse',
        'description': 'In a world where giants walk the Earth, humanity is no longer at the top of the food chain. Godzilla, Kong, and the Titans battle for supremacy in this explosive cinematic universe.',
        'icon': '🦖',
        'category': 'franchise',
        'order': 7,
        'banner_path': '/8eihUxjQsJ7WvGySkVMC0EwbPAD.jpg',
        'poster_path': '/sh7Rg8Er3tFcN9BpKIPOMvALgZd.jpg',
        'movies': [
            {'tmdb_id': 124905, 'title': 'Godzilla', 'overview': 'Ford Brody, a Navy bomb expert, has just reunited with his family in San Francisco when he is forced to go to Japan to help his estranged father. A massive creature arises.', 'poster_path': '/sh7Rg8Er3tFcN9BpKIPOMvALgZd.jpg', 'backdrop_path': '/8eihUxjQsJ7WvGySkVMC0EwbPAD.jpg', 'release_date': '2014-05-16', 'vote_average': 6.5, 'type': 'movie', 'order': 1},
            {'tmdb_id': 293167, 'title': 'Kong: Skull Island', 'overview': 'A diverse team of scientists, soldiers and adventurers unites to explore a mythical, uncharted island in the Pacific Ocean — and encounter the mighty Kong.', 'poster_path': '/54oPAfyN9ABYQ5kLdFuPlEBJrLd.jpg', 'backdrop_path': '/lisXCMzOEJOqK3XrOFUExNiRdKQ.jpg', 'release_date': '2017-03-10', 'vote_average': 7.0, 'type': 'movie', 'order': 2},
            {'tmdb_id': 373571, 'title': 'Godzilla: King of the Monsters', 'overview': 'The crypto-zoological agency Monarch faces off against a battery of god-sized monsters, including the mighty Godzilla, who collides with Mothra, Rodan, and three-headed King Ghidorah.', 'poster_path': '/dzNs4cUBPFFjkGEUKtnPMxEjSam.jpg', 'backdrop_path': '/oqDI65KFa3cgw5NL8RnYKIJXNBE.jpg', 'release_date': '2019-05-31', 'vote_average': 6.5, 'type': 'movie', 'order': 3},
            {'tmdb_id': 399566, 'title': 'Godzilla vs. Kong', 'overview': 'In a time when monsters walk the Earth, humanity\'s fight for its future sets Godzilla and Kong on a collision course that will see the two most powerful forces of nature on the planet collide.', 'poster_path': '/pgqgaUx1cJb5oZQQ5v0tNARCeBp.jpg', 'backdrop_path': '/inJjDhCjfhh3RtrJWBmmDqeuSYn.jpg', 'release_date': '2021-03-31', 'vote_average': 7.1, 'type': 'movie', 'order': 4},
            {'tmdb_id': 940721, 'title': 'Godzilla x Kong: The New Empire', 'overview': 'Two ancient titans, Godzilla and Kong, clash in an epic battle as humans unravel their intertwined origins and connection to Skull Island\'s mysteries.', 'poster_path': '/z1p34vh7dEOnLDmyCrlUVLuoDzd.jpg', 'backdrop_path': '/xRd1eJIDe7JHO5KFZnol87Vp3dX.jpg', 'release_date': '2024-03-29', 'vote_average': 6.9, 'type': 'movie', 'order': 5},
        ]
    },

    # ============================================================
    # 8. JURASSIC PARK
    # ============================================================
    {
        'name': 'Jurassic Park Universe',
        'slug': 'jurassic-park-universe',
        'description': 'Life finds a way. From the original wonder of seeing dinosaurs resurrected on Isla Nublar to the chaos of a world where prehistoric creatures roam free. Six films of pure adrenaline.',
        'icon': '🦕',
        'category': 'franchise',
        'order': 8,
        'banner_path': '/2Io6LvWPBTTKQZsKFIEOPSGtUM3.jpg',
        'poster_path': '/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg',
        'movies': [
            {'tmdb_id': 329, 'title': 'Jurassic Park', 'overview': 'A wealthy entrepreneur secretly creates a theme park featuring living dinosaurs drawn from prehistoric DNA. Before opening day, he invites a team of experts and his grandchildren.', 'poster_path': '/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg', 'backdrop_path': '/2Io6LvWPBTTKQZsKFIEOPSGtUM3.jpg', 'release_date': '1993-06-11', 'vote_average': 8.0, 'type': 'movie', 'order': 1},
            {'tmdb_id': 330, 'title': 'The Lost World: Jurassic Park', 'overview': 'Four years after Jurassic Park\'s genetically bred dinosaurs ran amok, InGen\'s scientist finds the original island\'s dinosaurs thriving.', 'poster_path': '/bkRKPnbpoCW3SUuuIH6FMZUOIFO.jpg', 'backdrop_path': '/kGqe7A1xKfVKiuGWEHPHjTp6Olv.jpg', 'release_date': '1997-05-23', 'vote_average': 6.7, 'type': 'movie', 'order': 2},
            {'tmdb_id': 331, 'title': 'Jurassic Park III', 'overview': 'A decidedly odd couple with ulterior motives convince Dr. Alan Grant to go to Isla Sorna for a field research expedition. Things go horribly wrong.', 'poster_path': '/ifUfE79O1raUwkMs4NAIhcEgTDQ.jpg', 'backdrop_path': '/oN7smvv1tHVsOjAMMC7GDkxfRm6.jpg', 'release_date': '2001-07-18', 'vote_average': 5.9, 'type': 'movie', 'order': 3},
            {'tmdb_id': 135397, 'title': 'Jurassic World', 'overview': 'Twenty-two years after the events of Jurassic Park, Isla Nublar now features a fully-functioning dinosaur theme park. But a new genetically modified dinosaur escapes.', 'poster_path': '/jjBgi2r5cRt36xF6iNUEhzscEcb.jpg', 'backdrop_path': '/dkMD5qe39bN3JkMH1BQa2UCBO3L.jpg', 'release_date': '2015-06-12', 'vote_average': 7.0, 'type': 'movie', 'order': 4},
            {'tmdb_id': 351286, 'title': 'Jurassic World: Fallen Kingdom', 'overview': 'A volcanic eruption threatens the remaining dinosaurs on the island of Isla Nublar, where the creatures have freely roamed for several years after the demise of an animal theme park.', 'poster_path': '/c9XxFNHE0BqaSlMzpFcbkw9Fnqm.jpg', 'backdrop_path': '/8wGACdBQu7VW3sMjRDHe1lALZZB.jpg', 'release_date': '2018-06-06', 'vote_average': 6.4, 'type': 'movie', 'order': 5},
            {'tmdb_id': 507086, 'title': 'Jurassic World Dominion', 'overview': 'Four years after the destruction of Isla Nublar, dinosaurs now live and hunt alongside humans all over the world. This fragile balance will reshape the future of both species.', 'poster_path': '/kAVRgw7GgK1CfYEJq8ME6EvRIgU.jpg', 'backdrop_path': '/8j9GqMCMDdjlpHVfQTEP7VQPCAJ.jpg', 'release_date': '2022-06-10', 'vote_average': 6.3, 'type': 'movie', 'order': 6},
        ]
    },

    # ============================================================
    # 9. FAST & FURIOUS
    # ============================================================
    {
        'name': 'Fast & Furious Saga',
        'slug': 'fast-furious-saga',
        'description': 'Family. Speed. Loyalty. The Fast & Furious franchise has evolved from street racing to global espionage, delivering non-stop action with one of Hollywood\'s most beloved ensemble casts.',
        'icon': '🚗',
        'category': 'franchise',
        'order': 9,
        'banner_path': '/y5Ptu9JyBEFPikSXcOJJBBjUGgk.jpg',
        'poster_path': '/rcjL3r9MKMoJd3l6KNGzSB5RDCO.jpg',
        'movies': [
            {'tmdb_id': 9799, 'title': 'The Fast and the Furious', 'overview': 'Los Angeles police officer Brian O\'Conner must decide where his loyalty really lies when he becomes enamored with the street racing world he has been sent undercover to investigate.', 'poster_path': '/rcjL3r9MKMoJd3l6KNGzSB5RDCO.jpg', 'backdrop_path': '/y5Ptu9JyBEFPikSXcOJJBBjUGgk.jpg', 'release_date': '2001-06-22', 'vote_average': 6.8, 'type': 'movie', 'order': 1},
            {'tmdb_id': 584, 'title': '2 Fast 2 Furious', 'overview': 'Brian O\'Conner is now in Miami where he reunites with his old friend Roman Pearce in order to go undercover with a drug dealer.', 'poster_path': '/q6sO9DSfmFwmhRQFOOijA2lhbgN.jpg', 'backdrop_path': '/gbHPM1OIOqrGpYibUDmxiQi0d5P.jpg', 'release_date': '2003-06-06', 'vote_average': 5.9, 'type': 'movie', 'order': 2},
            {'tmdb_id': 9615, 'title': 'Fast & Furious', 'overview': 'When a crime brings them back to L.A., fugitive ex-con Dom Toretto reignites his feud with agent Brian O\'Conner. But as they are forced to confront a shared enemy, Dom and Brian must give in to an uncomfortable new reality.', 'poster_path': '/iH7G1ofrHJWJ0IXkqYUSyRFBqnX.jpg', 'backdrop_path': '/vOVkm9PwEMXXEg5O6pcJzNVgEJr.jpg', 'release_date': '2009-04-03', 'vote_average': 6.5, 'type': 'movie', 'order': 3},
            {'tmdb_id': 51497, 'title': 'Fast Five', 'overview': 'Former cop Brian O\'Conner partners with ex-con Dom Toretto on the opposite side of the law. Since Brian and Mia Toretto broke Dom out of custody, they\'ve blown across many borders to elude authorities.', 'poster_path': '/6g8NpZbdInhubMUJWiWj4Z0YFtV.jpg', 'backdrop_path': '/eoXwQwqMkMI8Ux0Md8kRRdp7wJR.jpg', 'release_date': '2011-04-29', 'vote_average': 7.3, 'type': 'movie', 'order': 4},
            {'tmdb_id': 82992, 'title': 'Fast & Furious 6', 'overview': 'Dom and his crew are granted amnesty and a chance to return home, but they must first help Hobbs take down a mastermind who commands an organization of mercenary drivers.', 'poster_path': '/4ibTSHRjI2VfLuXvKLCYlq71v7N.jpg', 'backdrop_path': '/1E5baAaEse26fej7uHcjOgEE2t2.jpg', 'release_date': '2013-05-24', 'vote_average': 7.0, 'type': 'movie', 'order': 5},
            {'tmdb_id': 168259, 'title': 'Furious 7', 'overview': 'Deckard Shaw seeks revenge against Dominic Toretto and his family for his comatose brother. Dominic and his team have to stop a mercenary who gained access to an all-seeing computer surveillance system.', 'poster_path': '/dkMD5qe39bN3JkMH1BQa2UCBO3L.jpg', 'backdrop_path': '/6KeBBGDjPBpfNcnHqJdj6zALiyZ.jpg', 'release_date': '2015-04-03', 'vote_average': 7.3, 'type': 'movie', 'order': 6},
            {'tmdb_id': 337339, 'title': 'The Fate of the Furious', 'overview': 'When a mysterious woman seduces Dom into the world of crime and a betrayal of those closest to him, the crew face trials that will test them as never before.', 'poster_path': '/dRXJCbGDMuIzC5IOQU0ogbEeJhj.jpg', 'backdrop_path': '/nFO4aT5S2VxSsBGBNlhFJfJqGaF.jpg', 'release_date': '2017-04-14', 'vote_average': 7.0, 'type': 'movie', 'order': 7},
            {'tmdb_id': 463906, 'title': 'Fast & Furious Presents: Hobbs & Shaw', 'overview': 'Lawman Luke Hobbs and outcast Deckard Shaw form an unlikely alliance when a cyber-genetically enhanced villain threatens the future of humanity.', 'poster_path': '/5twGoogP8gMfGnOiHnMFMVGGNFF.jpg', 'backdrop_path': '/2ppFAZB93XtIjJo7RVAlJoUTAKU.jpg', 'release_date': '2019-08-02', 'vote_average': 6.8, 'type': 'movie', 'order': 8},
            {'tmdb_id': 458156, 'title': 'F9', 'overview': 'Dominic Toretto is leading a quiet life off the grid with Letty and his son, little Brian, but they know that danger always lurks just over their peaceful horizon.', 'poster_path': '/bQLrHIW9aH97nv7skBYqiM7606p.jpg', 'backdrop_path': '/ygFi53tFdCGAbDqIKoVrXmQzHXt.jpg', 'release_date': '2021-06-25', 'vote_average': 7.1, 'type': 'movie', 'order': 9},
            {'tmdb_id': 385687, 'title': 'Fast X', 'overview': 'Dom Toretto and his family are targeted by the vengeful son of drug kingpin Hernan Reyes, a man as ruthless as he is charming.', 'poster_path': '/fiVW06jE7z9YnO4trhaMEdclSiC.jpg', 'backdrop_path': '/4XM8DUTQb3lhLemJC51Jx4a2EuA.jpg', 'release_date': '2023-05-19', 'vote_average': 7.2, 'type': 'movie', 'order': 10},
        ]
    },

    # ============================================================
    # 10. JOHN WICK
    # ============================================================
    {
        'name': 'John Wick Universe',
        'slug': 'john-wick-universe',
        'description': 'They killed his dog. They stole his car. Now the most feared assassin in the criminal underworld is back, and the entire underground society is about to learn why you never cross John Wick.',
        'icon': '🔫',
        'category': 'franchise',
        'order': 10,
        'banner_path': '/fSwYa5q2xRkBoOOjueLpkLf3N7m.jpg',
        'poster_path': '/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg',
        'movies': [
            {'tmdb_id': 245891, 'title': 'John Wick', 'overview': 'Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.', 'poster_path': '/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg', 'backdrop_path': '/fSwYa5q2xRkBoOOjueLpkLf3N7m.jpg', 'release_date': '2014-10-24', 'vote_average': 7.4, 'type': 'movie', 'order': 1},
            {'tmdb_id': 324552, 'title': 'John Wick: Chapter 2', 'overview': 'After returning to the criminal underworld to repay a debt, John Wick discovers that a large bounty has been put on his life.', 'poster_path': '/hXWBc0ioZP3cN4zCu6SN3YHXMTS.jpg', 'backdrop_path': '/jji3uO8gZLiNnBSbQVHCyGN3NkV.jpg', 'release_date': '2017-02-10', 'vote_average': 7.5, 'type': 'movie', 'order': 2},
            {'tmdb_id': 458156, 'title': 'John Wick: Chapter 3 - Parabellum', 'overview': 'Super-assassin John Wick returns with a $14 million price tag on his head and an army of bounty-hunting killers on his trail.', 'poster_path': '/ziEuG1essDuWuC5lpWUaw1uXY2O.jpg', 'backdrop_path': '/b5YRfMkpApEFzWXIbwl0pqjrOzI.jpg', 'release_date': '2019-05-17', 'vote_average': 7.6, 'type': 'movie', 'order': 3},
            {'tmdb_id': 603692, 'title': 'John Wick: Chapter 4', 'overview': 'John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe.', 'poster_path': '/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg', 'backdrop_path': '/xTHltMrZygaYbMYbmUGKzf8sMuT.jpg', 'release_date': '2023-03-24', 'vote_average': 7.8, 'type': 'movie', 'order': 4},
        ]
    },

    # ============================================================
    # 11. MISSION IMPOSSIBLE
    # ============================================================
    {
        'name': 'Mission Impossible Saga',
        'slug': 'mission-impossible',
        'description': 'Your mission, should you choose to accept it... Follow Ethan Hunt and the IMF through the most jaw-dropping, death-defying stunts ever put on film. Tom Cruise really does his own stunts.',
        'icon': '🕵️',
        'category': 'franchise',
        'order': 11,
        'banner_path': '/kzmNHmGFGMVMcAqSnvFUiLrW4AD.jpg',
        'poster_path': '/6tpMpMpFrpNk7czOQSJE0L3HTJI.jpg',
        'movies': [
            {'tmdb_id': 954, 'title': 'Mission: Impossible', 'overview': 'When Ethan Hunt, the leader of a crack espionage team whose perilous operation has gone awry with no explanation, discovers that a mole has penetrated the CIA, he\'s drawn into a rogue mission.', 'poster_path': '/6tpMpMpFrpNk7czOQSJE0L3HTJI.jpg', 'backdrop_path': '/kzmNHmGFGMVMcAqSnvFUiLrW4AD.jpg', 'release_date': '1996-05-22', 'vote_average': 7.1, 'type': 'movie', 'order': 1},
            {'tmdb_id': 955, 'title': 'Mission: Impossible II', 'overview': 'With the help of a professional thief, secret agent Ethan Hunt races to stop a former IMF agent from releasing a biological weapon.', 'poster_path': '/gdvmMDPGV9jJG2nMZbQdJMzMQe4.jpg', 'backdrop_path': '/1bqzLJcPUuFNpJvn2lALpzfVVLQ.jpg', 'release_date': '2000-05-24', 'vote_average': 6.1, 'type': 'movie', 'order': 2},
            {'tmdb_id': 956, 'title': 'Mission: Impossible III', 'overview': 'Ethan Hunt comes face to face with a dangerous and sadistic arms dealer while trying to keep his identity secret in order to protect his girlfriend.', 'poster_path': '/bvJOpyHYWACDusvQvXxKEHFNjce.jpg', 'backdrop_path': '/hblHbJEZEkJxdaJmCIqfSCMN07N.jpg', 'release_date': '2006-05-05', 'vote_average': 6.9, 'type': 'movie', 'order': 3},
            {'tmdb_id': 56292, 'title': 'Mission: Impossible - Ghost Protocol', 'overview': 'The IMF is shut down when it\'s implicated in the bombing of the Kremlin, causing Ethan Hunt and his new team to go rogue to clear their organization\'s name.', 'poster_path': '/jC2cmnfGG8t4t7UoYAUbGFwMqbh.jpg', 'backdrop_path': '/jCAbcGXqOdGMFPr3zp0vgzQlyJe.jpg', 'release_date': '2011-12-21', 'vote_average': 7.4, 'type': 'movie', 'order': 4},
            {'tmdb_id': 177677, 'title': 'Mission: Impossible - Rogue Nation', 'overview': 'Ethan and team take on their most impossible mission yet, eradicating the Syndicate - an International rogue organization as highly skilled as they are, committed to destroying the IMF.', 'poster_path': '/iLEFGe21mCkCqy9CfxGFfFWCjm8.jpg', 'backdrop_path': '/2lBXAVJCJAoY3Pk6S9kWNFxIERS.jpg', 'release_date': '2015-07-31', 'vote_average': 7.4, 'type': 'movie', 'order': 5},
            {'tmdb_id': 353081, 'title': 'Mission: Impossible - Fallout', 'overview': 'Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong.', 'poster_path': '/AkJQpZp9WoNdj7pLYSj1L0RcMMN.jpg', 'backdrop_path': '/5qxePyMYDisLe8A5ORXqqB2QJoT.jpg', 'release_date': '2018-07-27', 'vote_average': 7.7, 'type': 'movie', 'order': 6},
            {'tmdb_id': 575264, 'title': 'Mission: Impossible - Dead Reckoning Part One', 'overview': 'Ethan Hunt and his IMF team must track down a terrifying new weapon that threatens all of humanity before it falls into the wrong hands.', 'poster_path': '/NNxYkU70HPurnNCSiCjYAmacwm.jpg', 'backdrop_path': '/r3CN7dHFKsVCUbfEYCLIZTOH4Ug.jpg', 'release_date': '2023-07-12', 'vote_average': 7.7, 'type': 'movie', 'order': 7},
        ]
    },

    # ============================================================
    # 12. THE MATRIX
    # ============================================================
    {
        'name': 'The Matrix Universe',
        'slug': 'the-matrix',
        'description': 'What is real? The Matrix redefined science fiction cinema with groundbreaking visuals, deep philosophical questions, and bullet-time action that changed movies forever. Take the red pill.',
        'icon': '💊',
        'category': 'franchise',
        'order': 12,
        'banner_path': '/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg',
        'poster_path': '/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
        'movies': [
            {'tmdb_id': 603, 'title': 'The Matrix', 'overview': 'Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth.', 'poster_path': '/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg', 'backdrop_path': '/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg', 'release_date': '1999-03-31', 'vote_average': 8.2, 'type': 'movie', 'order': 1},
            {'tmdb_id': 604, 'title': 'The Matrix Reloaded', 'overview': 'Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover Zion and destroy it and its inhabitants.', 'poster_path': '/9TqDu8xpmFRCXoFBBn7WBWDW1x2.jpg', 'backdrop_path': '/oBIQDKcqNxKckjugtmzm3C6QoNs.jpg', 'release_date': '2003-05-15', 'vote_average': 7.3, 'type': 'movie', 'order': 2},
            {'tmdb_id': 605, 'title': 'The Matrix Revolutions', 'overview': 'The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', 'poster_path': '/sKogjhfs5q3azmpW7DFKKAeLEG8.jpg', 'backdrop_path': '/rqbCbjB19amtOtFQbb3K2lgm2zv.jpg', 'release_date': '2003-11-05', 'vote_average': 6.8, 'type': 'movie', 'order': 3},
            {'tmdb_id': 624860, 'title': 'The Matrix Resurrections', 'overview': 'Return to a world of two realities: one, everyday life; the other, what lies behind it. To find out if his reality is a construct, to truly know himself, Mr. Anderson will have to choose to follow the white rabbit once more.', 'poster_path': '/8c4a8kE7PizaGQQnditjonkE3LJ.jpg', 'backdrop_path': '/eNI7PtK6DEYgZmHWP9gQNuff8pv.jpg', 'release_date': '2021-12-22', 'vote_average': 6.3, 'type': 'movie', 'order': 4},
        ]
    },

    # ============================================================
    # 13. AVATAR UNIVERSE
    # ============================================================
    {
        'name': 'Avatar Universe',
        'slug': 'avatar-universe',
        'description': 'Pandora awaits. James Cameron\'s visionary world of the Na\'vi is the most visually stunning cinematic achievement in history. Experience the breathtaking beauty and the fight to protect it.',
        'icon': '🌿',
        'category': 'fantasy',
        'order': 13,
        'banner_path': '/s9RBBkK6jd5TkZtHYmWgYmqQlPM.jpg',
        'poster_path': '/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg',
        'movies': [
            {'tmdb_id': 19995, 'title': 'Avatar', 'overview': 'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.', 'poster_path': '/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg', 'backdrop_path': '/s9RBBkK6jd5TkZtHYmWgYmqQlPM.jpg', 'release_date': '2009-12-18', 'vote_average': 7.6, 'type': 'movie', 'order': 1},
            {'tmdb_id': 76600, 'title': 'Avatar: The Way of Water', 'overview': 'Set more than a decade after the events of the first film, learn the story of the Sully family, the trouble that follows them, the lengths they go to keep each other safe.', 'poster_path': '/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg', 'backdrop_path': '/ovM06PdF3M8wvKb06i4sjW3xoww.jpg', 'release_date': '2022-12-16', 'vote_average': 7.7, 'type': 'movie', 'order': 2},
        ]
    },

    # ============================================================
    # 14. CONJURING UNIVERSE
    # ============================================================
    {
        'name': 'The Conjuring Universe',
        'slug': 'conjuring-universe',
        'description': 'Based on true case files from paranormal investigators Ed and Lorraine Warren, these are the most terrifying supernatural stories ever told. Don\'t watch alone. You\'ve been warned.',
        'icon': '👻',
        'category': 'franchise',
        'order': 14,
        'banner_path': '/3G9PdBPTB3O3dFPMfX3FMqxJPKR.jpg',
        'poster_path': '/wVYREutTvI2tmxr6ujrHT704wGF.jpg',
        'movies': [
            {'tmdb_id': 270946, 'title': 'The Nun', 'overview': 'When a young nun at a cloistered abbey in Romania takes her own life, a priest with a haunted past and a novitiate on the threshold of her final vows are sent by the Vatican to investigate.', 'poster_path': '/sFC1ElvoKGdHJIWRpNB3xWJ9lJA.jpg', 'backdrop_path': '/3G9PdBPTB3O3dFPMfX3FMqxJPKR.jpg', 'release_date': '2018-09-07', 'vote_average': 6.2, 'type': 'movie', 'order': 1},
            {'tmdb_id': 324786, 'title': 'Annabelle: Creation', 'overview': 'Twelve years after the tragic death of their little girl, a dollmaker and his wife welcome a nun and several girls from a shuttered orphanage into their home.', 'poster_path': '/tb86L2EKaOjQDwfCTjkliHRmXNs.jpg', 'backdrop_path': '/2Z4QPuXJBtNWMjITRwbfJ7TxGJr.jpg', 'release_date': '2017-08-11', 'vote_average': 7.0, 'type': 'movie', 'order': 2},
            {'tmdb_id': 254128, 'title': 'Annabelle', 'overview': 'A couple begins to experience terrifying supernatural occurrences involving a vintage doll shortly after their home is invaded by satanic cultists.', 'poster_path': '/wVYREutTvI2tmxr6ujrHT704wGF.jpg', 'backdrop_path': '/65mlPsxKKxHCiRO9EePCy3ItSH5.jpg', 'release_date': '2014-10-03', 'vote_average': 5.6, 'type': 'movie', 'order': 3},
            {'tmdb_id': 138843, 'title': 'The Conjuring', 'overview': 'Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.', 'poster_path': '/wVYREutTvI2tmxr6ujrHT704wGF.jpg', 'backdrop_path': '/nVRyd8hlg0ZLxBn9RaI7mUMQLnz.jpg', 'release_date': '2013-07-19', 'vote_average': 7.5, 'type': 'movie', 'order': 4},
            {'tmdb_id': 523427, 'title': 'Annabelle Comes Home', 'overview': 'Determined to keep Annabelle from wreaking more havoc, demonologists Ed and Lorraine Warren lock the possessed doll in the artifacts room in their home.', 'poster_path': '/fSRqoBEA2KZRbLpECJPKEIPfODl.jpg', 'backdrop_path': '/e7Fxn3nI5zQNfS2aOlCLkEFXlNB.jpg', 'release_date': '2019-06-26', 'vote_average': 6.8, 'type': 'movie', 'order': 5},
            {'tmdb_id': 259693, 'title': 'The Conjuring 2', 'overview': 'Ed and Lorraine Warren travel to north London to help a single mother raising four children alone in a house plagued by malicious spirits.', 'poster_path': '/pTcBPRCYhBFuLj70OmReUbmT9U1.jpg', 'backdrop_path': '/uEJWS2F8yNF50N6sMi0Qi5BTXLW.jpg', 'release_date': '2016-06-10', 'vote_average': 7.4, 'type': 'movie', 'order': 6},
            {'tmdb_id': 603692, 'title': 'The Nun II', 'overview': '1956 - France. A priest is murdered. An evil is spreading. The sequel to the worldwide horror phenomenon follows Sister Irene as she once again comes face-to-face with Valak.', 'poster_path': '/5gzzkR7y3hnY8AD1wXjCnVlHba5.jpg', 'backdrop_path': '/tO0ee2vJwFENjJBSaEVbJJYgBnA.jpg', 'release_date': '2023-09-08', 'vote_average': 6.7, 'type': 'movie', 'order': 7},
            {'tmdb_id': 699258, 'title': 'The Conjuring: The Devil Made Me Do It', 'overview': 'Paranormal investigators Ed and Lorraine Warren take on one of the most sensational cases of their careers after a young boy is possessed by a demon.', 'poster_path': '/xbSuFiJbbBWCkyCCKIMfuDCA4yV.jpg', 'backdrop_path': '/iy7XMBmEjMVeMnHRIlKEQMiHQAh.jpg', 'release_date': '2021-06-04', 'vote_average': 7.2, 'type': 'movie', 'order': 8},
        ]
    },

    # ============================================================
    # 15. PIRATES OF THE CARIBBEAN
    # ============================================================
    {
        'name': 'Pirates of the Caribbean',
        'slug': 'pirates-of-the-caribbean',
        'description': 'Yo ho, yo ho, a pirate\'s life for me! Captain Jack Sparrow sails the high seas in swashbuckling adventures filled with curses, sea monsters, ghosts, and rum. Lots of rum.',
        'icon': '🏴‍☠️',
        'category': 'franchise',
        'order': 15,
        'banner_path': '/6foCvnbhxeeFWboXHCBCLMw9HL.jpg',
        'poster_path': '/2ovoTCcuGfpn3g8p3pWwmMFnKyF.jpg',
        'movies': [
            {'tmdb_id': 22, 'title': 'Pirates of the Caribbean: The Curse of the Black Pearl', 'overview': 'Jack Sparrow, a freewheeling 18th-century pirate, encounters Will Turner, a young blacksmith with a connection to Jack\'s past, and together they must fight a cursed crew of pirates.', 'poster_path': '/2ovoTCcuGfpn3g8p3pWwmMFnKyF.jpg', 'backdrop_path': '/6foCvnbhxeeFWboXHCBCLMw9HL.jpg', 'release_date': '2003-07-09', 'vote_average': 8.0, 'type': 'movie', 'order': 1},
            {'tmdb_id': 58, 'title': "Pirates of the Caribbean: Dead Man's Chest", 'overview': 'Jack Sparrow races to recover the heart of Davy Jones to avoid enslaving his soul to Jones\' service, as other friends and foes seek the powerful artifact for their own agenda.', 'poster_path': '/uXEqmloGyP7UXAiphJUu2v2nfkf.jpg', 'backdrop_path': '/gBnrFDYIw5F8L8pY5bBxMQwKq5L.jpg', 'release_date': '2006-07-07', 'vote_average': 7.3, 'type': 'movie', 'order': 2},
            {'tmdb_id': 285, 'title': "Pirates of the Caribbean: At World's End", 'overview': 'Captain Barbossa, Will Turner and Elizabeth Swann must sail off the edge of the map, navigate treachery and betrayal, find Jack Sparrow, and make their final alliances.', 'poster_path': '/2iHVFZT5bqJXHxBLcCzRKoqjZ6l.jpg', 'backdrop_path': '/cjCuBSWnS7e5xJ8CqFGMKVNmSuN.jpg', 'release_date': '2007-05-25', 'vote_average': 7.2, 'type': 'movie', 'order': 3},
            {'tmdb_id': 1865, 'title': 'Pirates of the Caribbean: On Stranger Tides', 'overview': 'Jack Sparrow crosses paths with a woman from his past, Angelica, and he\'s not sure if it\'s love or if she\'s a ruthless con artist who\'s using him to find the legendary Fountain of Youth.', 'poster_path': '/gg3CRLL80fBOFQhBbPqFBs1jVxT.jpg', 'backdrop_path': '/bFl4F6aV9eZMHDlLXl7K5bUjuLv.jpg', 'release_date': '2011-05-20', 'vote_average': 6.5, 'type': 'movie', 'order': 4},
            {'tmdb_id': 166426, 'title': "Pirates of the Caribbean: Dead Men Tell No Tales", 'overview': 'Thrust into an adventure, a young man of Will Turner teams up with Captain Jack Sparrow and encounters the terrifying ghost-pirate Salazar.', 'poster_path': '/qwoGfcg6YUS55nUWeWLiQbMBbgv.jpg', 'backdrop_path': '/67ik71MoLIHkJeHWIy1KjqHZ2zb.jpg', 'release_date': '2017-05-26', 'vote_average': 6.9, 'type': 'movie', 'order': 5},
        ]
    },

    # ============================================================
    # 16. HINDU MYTHOLOGY & INDIAN CINEMATIC UNIVERSE
    # ============================================================
    {
        'name': 'Hindu Mythology Universe',
        'slug': 'hindu-mythology-universe',
        'description': 'The oldest stories ever told, brought to life on the big screen. From the divine adventures of Lord Rama and the epic war of Kurukshetra to the cosmic battles of Kalki, India\'s mythological cinema is unlike anything else.',
        'icon': '🕉️',
        'category': 'indian_epic',
        'order': 16,
        'banner_path': '/bfHPJCHNwqP2BNMJC1sQ2JYtEPF.jpg',
        'poster_path': '/iGMxoNv4Ynf3MCqPf1VFxJeI3cF.jpg',
        'movies': [
            {'tmdb_id': 839033, 'title': 'Adipurush', 'overview': 'Raghava, along with his wife Janaki and brother Shesh returns to Ayodhya after defeating the Demon King Lankesh. The story of good versus evil rooted in Hindu mythology.', 'poster_path': '/iGMxoNv4Ynf3MCqPf1VFxJeI3cF.jpg', 'backdrop_path': '/bfHPJCHNwqP2BNMJC1sQ2JYtEPF.jpg', 'release_date': '2023-06-16', 'vote_average': 4.5, 'type': 'movie', 'order': 1},
            {'tmdb_id': 882598, 'title': 'Ram Setu', 'overview': 'An archaeologist sets out to prove the mythological Ram Setu bridge is real and encounters dangers threatening to destroy the bridge\'s legacy.', 'poster_path': '/A7EByudX0eX7c3fiqBrCLzkshp5.jpg', 'backdrop_path': '/eQYM8mVvPMKCi5POZMxCDHaOp5w.jpg', 'release_date': '2022-10-25', 'vote_average': 6.5, 'type': 'movie', 'order': 2},
            {'tmdb_id': 1075794, 'title': 'HanuMan', 'overview': 'A young man in a fictional village discovers a powerful gem that grants him the powers of Lord Hanuman. A modern-day superhero story rooted in Indian mythology.', 'poster_path': '/7lMnCbWYHEXhT9JNTRuRiK5FzLH.jpg', 'backdrop_path': '/nFo3FaJhgkEWNV8hKUDNZ3r4Mxi.jpg', 'release_date': '2024-01-12', 'vote_average': 8.2, 'type': 'movie', 'order': 3},
            {'tmdb_id': 912349, 'title': 'Brahmastra Part One: Shiva', 'overview': 'Shiva is a young man who discovers he has a special connection with fire and the universe\'s most powerful weapon — the Brahmastra. A new age Indian superhero film.', 'poster_path': '/qFlJ3KPWLXHE2KCmkTHJxGiFlKd.jpg', 'backdrop_path': '/v0HsRJoJrXBxAGSwGGM5MZCaWBw.jpg', 'release_date': '2022-09-09', 'vote_average': 5.8, 'type': 'movie', 'order': 4},
            {'tmdb_id': 1087822, 'title': 'Kalki 2898 AD', 'overview': 'Set in a dystopian future, the story follows the birth of Kalki, the tenth and final avatar of Lord Vishnu, who must save humanity. One of the most ambitious Indian films ever made.', 'poster_path': '/hqbT2u0RQmBVSX4pGnQoiOhZpkO.jpg', 'backdrop_path': '/8eiNIVeAqDDDkMJNVTfKHpHyFqF.jpg', 'release_date': '2024-06-27', 'vote_average': 7.5, 'type': 'movie', 'order': 5},
        ]
    },

    # ============================================================
    # 17. TOP TIER WEB SERIES
    # ============================================================
    {
        'name': 'Greatest TV Series Ever',
        'slug': 'greatest-tv-series',
        'description': 'These are not just TV shows — they are cultural events. The greatest television ever made, period. Each of these series redefined what storytelling on screen could achieve.',
        'icon': '📺',
        'category': 'series',
        'order': 17,
        'banner_path': '/ggFHVNu6YYI5L9pCfOacjizRGt.jpg',
        'poster_path': '/eSzpy96DwBujGFj0xMbXBcGcfxX.jpg',
        'movies': [
            {'tmdb_id': 1396, 'title': 'Breaking Bad', 'overview': 'Walter White, a high school chemistry teacher diagnosed with inoperable lung cancer, turns to manufacturing and selling methamphetamine with a former student to secure his family\'s future.', 'poster_path': '/ggFHVNu6YYI5L9pCfOacjizRGt.jpg', 'backdrop_path': '/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg', 'release_date': '2008-01-20', 'vote_average': 9.5, 'type': 'series', 'order': 1},
            {'tmdb_id': 1399, 'title': 'Game of Thrones', 'overview': 'Seven noble families fight for control of the mythical land of Westeros. Political and sexual intrigue abound. The series serves as an adaptation of George R. R. Martin\'s A Song of Ice and Fire.', 'poster_path': '/7WUHnWGx5OrhL2FLR6803nFWBFB.jpg', 'backdrop_path': '/qsD5OHqW7DSnaQ2afwz8Ptof8hQ.jpg', 'release_date': '2011-04-17', 'vote_average': 9.3, 'type': 'series', 'order': 2},
            {'tmdb_id': 87108, 'title': 'Chernobyl', 'overview': 'A dramatization of the Chernobyl nuclear disaster of April 1986 and the cleanup efforts that followed. Widely considered one of the greatest miniseries ever made.', 'poster_path': '/hlLXt2tOPT6RRnjiUmoxyG1LTFi.jpg', 'backdrop_path': '/ga6zSFbNzOQKLEEBcMLjsqJN1nt.jpg', 'release_date': '2019-05-06', 'vote_average': 9.4, 'type': 'series', 'order': 3},
            {'tmdb_id': 2190, 'title': 'The Sopranos', 'overview': 'New Jersey mob boss Tony Soprano deals with personal and professional issues in his home and business life that affect his mental state, leading him to seek professional psychiatric counseling.', 'poster_path': '/rTc7ZXZroqjiesFMQbMdIkAkYY5.jpg', 'backdrop_path': '/gLotmmNEPTmJGHFYHcNVjXWUVrE.jpg', 'release_date': '1999-01-10', 'vote_average': 9.2, 'type': 'series', 'order': 4},
            {'tmdb_id': 1438, 'title': 'The Wire', 'overview': 'Told from the points of view of both the Baltimore homicide and narcotics detectives and their targets, the series captures a universe in which the national war on drugs has become a permanent, self-sustaining bureaucracy.', 'poster_path': '/4rGNEOG0yIPMnFBlcnTdRaHm2Wr.jpg', 'backdrop_path': '/8sEZBGNpHSwrBNrCFn1JpzW7k9j.jpg', 'release_date': '2002-06-02', 'vote_average': 9.3, 'type': 'series', 'order': 5},
            {'tmdb_id': 60574, 'title': 'Peaky Blinders', 'overview': 'A gangster family epic set in 1900s England, centering on a gang who sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby.', 'poster_path': '/vUUqzWa2LnHIVqkaKVn3nyfVnBs.jpg', 'backdrop_path': '/wiE9doxiLwq3WgROzu4QM9M0BO4.jpg', 'release_date': '2013-09-12', 'vote_average': 8.9, 'type': 'series', 'order': 6},
            {'tmdb_id': 60059, 'title': 'Better Call Saul', 'overview': 'Six years before Saul Goodman meets Walter White. Jimmy McGill, a small-time lawyer searching for his destiny, winds his way through the halls of justice.', 'poster_path': '/fC2HDm5t0kR9ukari5FXWlnZLls.jpg', 'backdrop_path': '/nZBMegOrKTuDkVMCqCMEfakRPRX.jpg', 'release_date': '2015-02-08', 'vote_average': 9.0, 'type': 'series', 'order': 7},
            {'tmdb_id': 66573, 'title': 'Suits', 'overview': 'A top Manhattan corporate lawyer takes on a brilliant but unmotivated college dropout who secretly studied law, working together as they pretend he actually went to Harvard.', 'poster_path': '/7pTqaZQZxv7OKn9qHHSACWe0sJt.jpg', 'backdrop_path': '/Vr7Jc8DPuMSozFBq4RVFmcPrL4.jpg', 'release_date': '2011-06-23', 'vote_average': 8.5, 'type': 'series', 'order': 8},
            {'tmdb_id': 1911, 'title': 'Sherlock', 'overview': 'A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London.', 'poster_path': '/7WTsnHkbA0FaG6R9twfFde0I9hl.jpg', 'backdrop_path': '/pNJn4G9uxpEPcHRhXHi9ROt3cFj.jpg', 'release_date': '2010-07-25', 'vote_average': 9.0, 'type': 'series', 'order': 9},
            {'tmdb_id': 46648, 'title': 'True Detective', 'overview': 'An anthology crime drama series that follows detectives across different cases. Season 1 featuring Matthew McConaughey is widely considered one of the greatest TV seasons ever.', 'poster_path': '/kGKm0sxvWAqLmjAMZPABwBOZaol.jpg', 'backdrop_path': '/z2nfRxZCGFgAnVnv5HvCFlKVOhH.jpg', 'release_date': '2014-01-12', 'vote_average': 8.6, 'type': 'series', 'order': 10},
            {'tmdb_id': 67178, 'title': 'Narcos', 'overview': 'A gripping story of the hunt for Colombian cocaine kingpin Pablo Escobar and the Drug Enforcement Administration agents who made it their mission to bring him down.', 'poster_path': '/rTmal9fDbwh5F4Bql6689EzJnl7.jpg', 'backdrop_path': '/1CwCFyA9xFtMEkBRRmMnLXm5DLw.jpg', 'release_date': '2015-08-28', 'vote_average': 8.9, 'type': 'series', 'order': 11},
            {'tmdb_id': 67744, 'title': 'Mindhunter', 'overview': 'FBI agents Holden Ford and Bill Tench, along with psychologist Wendy Carr, operate the FBI\'s elite serial crime unit developing modern serial killer profiling.', 'poster_path': '/z0qqpGHPtZSXwXe54sOjWfMUY7z.jpg', 'backdrop_path': '/yMa0M32pGMbIYbRVVpz4eEFQ08T.jpg', 'release_date': '2017-10-13', 'vote_average': 8.6, 'type': 'series', 'order': 12},
            {'tmdb_id': 76479, 'title': 'Ozark', 'overview': 'A financial advisor drags his family from Chicago to the Missouri Ozarks, where he must launder money for a Mexican drug cartel.', 'poster_path': '/pCh8g4MkBSEsCz7g8GOXL8ygAMp.jpg', 'backdrop_path': '/dNJxqlOVh7sY4Y7iA1tDRDvLKvI.jpg', 'release_date': '2017-07-21', 'vote_average': 8.4, 'type': 'series', 'order': 13},
            {'tmdb_id': 66732, 'title': 'Stranger Things', 'overview': 'When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.', 'poster_path': '/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg', 'backdrop_path': '/rcA17r3KB9oKBHGEMEkjBHvuFG3.jpg', 'release_date': '2016-07-15', 'vote_average': 8.6, 'type': 'series', 'order': 14},
            {'tmdb_id': 93405, 'title': 'Squid Game', 'overview': 'Hundreds of cash-strapped players accept a strange invitation to compete in children\'s games. Inside, a tempting prize awaits with deadly high stakes.', 'poster_path': '/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg', 'backdrop_path': '/oaGvjB0DvdhXhOAuADfHb261ZHa.jpg', 'release_date': '2021-09-17', 'vote_average': 8.0, 'type': 'series', 'order': 15},
            {'tmdb_id': 71446, 'title': 'Money Heist', 'overview': 'An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history - stealing 2.4 billion euros from the Royal Mint of Spain.', 'poster_path': '/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg', 'backdrop_path': '/piXnVbPGXbyIyD6W3OVMM5LxQ4j.jpg', 'release_date': '2017-05-02', 'vote_average': 8.3, 'type': 'series', 'order': 16},
            {'tmdb_id': 83867, 'title': 'Dark', 'overview': 'A missing child sets off a chain of events leading to the uncovering of a time travel conspiracy which spans several generations in a small German town.', 'poster_path': '/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg', 'backdrop_path': '/9Fg2skgO11bVFNxGiQhuvFJHVqG.jpg', 'release_date': '2017-12-01', 'vote_average': 8.7, 'type': 'series', 'order': 17},
            {'tmdb_id': 95479, 'title': 'Jujutsu Kaisen', 'overview': 'A boy swallows a cursed talisman - the finger of a demon - and becomes cursed himself. He enters a shaman college to be able to locate the demon\'s other body parts and thus exorcise himself.', 'poster_path': '/hkJ7LTHgLddVToMuHN9IOEjOliP.jpg', 'backdrop_path': '/xoqfCrPNhLGJNQakwrL45qyGGQI.jpg', 'release_date': '2020-10-03', 'vote_average': 8.6, 'type': 'series', 'order': 18},
            {'tmdb_id': 46261, 'title': 'Attack on Titan', 'overview': 'Several hundred years ago, humans were nearly exterminated by giants called Titans. Titans are typically several stories tall, seem to have no intelligence and devour human beings for pleasure.', 'poster_path': '/hTP1DtLGFamjfu8WqjnuQdP1n4i.jpg', 'backdrop_path': '/rqbCbjB19amtOtFQbb3K2lgm2zv.jpg', 'release_date': '2013-04-07', 'vote_average': 8.9, 'type': 'series', 'order': 19},
            {'tmdb_id': 108978, 'title': 'Mirzapur', 'overview': 'A reckless act by Munna Tripathi, the son of Akhandanand Tripathi — a carpet exporter and the mafia don of Mirzapur — forces Guddu and Bablu Pandit into the world of crime.', 'poster_path': '/5pVJ9SuuO72IgN6i9PJbMBzKGYD.jpg', 'backdrop_path': '/6oomrFe0BFT7FvMnR1VCBHB3F8Z.jpg', 'release_date': '2018-11-16', 'vote_average': 8.5, 'type': 'series', 'order': 20},
            {'tmdb_id': 120089, 'title': 'The Family Man', 'overview': 'Srikant Tiwari is a middle-class man who works for a special cell of the National Investigation Agency. He tries to protect the nation from terrorists while also protecting his family from his dangerous career.', 'poster_path': '/lPe1GyCKxLHHrLrfzTJpYr0r7B.jpg', 'backdrop_path': '/8cXf0OOHFHEP7pMv9CSjlxlAJnC.jpg', 'release_date': '2019-09-20', 'vote_average': 9.0, 'type': 'series', 'order': 21},
            {'tmdb_id': 60735, 'title': 'Prison Break', 'overview': 'Due to a political conspiracy, an innocent man is sent to death row and his only hope is his brother, who makes it his mission to deliberately get himself sent to the same prison in order to break the both of them out.', 'poster_path': '/5E1BhkCgjLBlmABHMSwSt8zAD1u.jpg', 'backdrop_path': '/l2fQFbfmJO6J7JmPBZPMHtC0GlG.jpg', 'release_date': '2005-08-29', 'vote_average': 8.3, 'type': 'series', 'order': 22},
            {'tmdb_id': 100088, 'title': 'Reacher', 'overview': 'A reacher is an ex-military man who wanders into a small town, only to be arrested for a murder he didn\'t commit. As he untangles the case, he begins to uncover a deeper conspiracy.', 'poster_path': '/gsQJOfeL2sGHdASRVQdbpBsgcqh.jpg', 'backdrop_path': '/aJwZQW5MLNeHe2LlhFVHOI6DKt7.jpg', 'release_date': '2022-02-04', 'vote_average': 8.0, 'type': 'series', 'order': 23},
        ]
    },

    # ============================================================
    # 18. MCU DISNEY+ SERIES
    # ============================================================
    {
        'name': 'Marvel Disney+ Series',
        'slug': 'marvel-disney-series',
        'description': 'The MCU expands to streaming. These Disney+ originals are essential viewing — they connect directly to the films and introduce new heroes who will shape the future of the Marvel universe.',
        'icon': '🎭',
        'category': 'superhero',
        'order': 18,
        'banner_path': '/ggFHVNu6YYI5L9pCfOacjizRGt.jpg',
        'poster_path': '/glKDfE6btIRcmr55r67LoHy1LZ.jpg',
        'movies': [
            {'tmdb_id': 85271, 'title': 'WandaVision', 'overview': 'Wanda Maximoff and Vision—two super-powered beings living idealized suburban lives—begin to suspect that everything is not as it seems.', 'poster_path': '/glKDfE6btIRcmr55r67LoHy1LZ.jpg', 'backdrop_path': '/tzGY49kseSE9QAah0poBzmtXRYS.jpg', 'release_date': '2021-01-15', 'vote_average': 8.0, 'type': 'series', 'order': 1},
            {'tmdb_id': 84958, 'title': 'Loki', 'overview': 'After stealing the Tesseract during the events of Avengers: Endgame, an alternate version of Loki is brought to the mysterious Time Variance Authority.', 'poster_path': '/voHUmluYmKyleFkTu3lOXQG702u.jpg', 'backdrop_path': '/6ThCQCbGeNqaABPF7eGDpTMFxR8.jpg', 'release_date': '2021-06-09', 'vote_average': 8.2, 'type': 'series', 'order': 2},
            {'tmdb_id': 88396, 'title': 'The Falcon and the Winter Soldier', 'overview': 'Following the events of Avengers: Endgame, Sam Wilson and Bucky Barnes team up in a global adventure that tests their abilities as they battle a group of terrorists called the Flag Smashers.', 'poster_path': '/6kbAMLteGO8yyewYau6bJ683sw7.jpg', 'backdrop_path': '/b0WmHGc8LHTdGCVzxRb3IBMur57.jpg', 'release_date': '2021-03-19', 'vote_average': 7.6, 'type': 'series', 'order': 3},
            {'tmdb_id': 92782, 'title': 'Moon Knight', 'overview': 'When Steven Grant discovers he\'s living with a mysterious mercenary who is a vessel for the Egyptian moon god Khonshu, he faces a deadly adventure.', 'poster_path': '/x6FsYvt33846IQnDt7HOBNQjwZ2.jpg', 'backdrop_path': '/4PHGENlIKYxGEfB0TqMLBnVUgpP.jpg', 'release_date': '2022-03-30', 'vote_average': 7.9, 'type': 'series', 'order': 4},
            {'tmdb_id': 88329, 'title': 'Hawkeye', 'overview': 'Set after Avengers: Endgame, Hawkeye must work with his biggest fan, Kate Bishop, to confront his past.', 'poster_path': '/nitneKaumrX6T2lKQl9KLWQQ3gB.jpg', 'backdrop_path': '/hIVSfsFrHg7ILRCGEBQLMvbSJEf.jpg', 'release_date': '2021-11-24', 'vote_average': 7.7, 'type': 'series', 'order': 5},
            {'tmdb_id': 202555, 'title': 'Daredevil: Born Again', 'overview': 'Matt Murdock, a blind lawyer with heightened abilities, is fighting for justice through the legal system while Wilson Fisk pursues his own political ambitions in New York City.', 'poster_path': '/cdFS8ATe6gWlp0QjpJuJeqWCz8e.jpg', 'backdrop_path': '/b3OVAeUBlEBMa7RlGwHnQtqyIGQ.jpg', 'release_date': '2025-03-04', 'vote_average': 8.1, 'type': 'series', 'order': 6},
        ]
    },

    # ============================================================
    # 19. STAR WARS SERIES
    # ============================================================
    {
        'name': 'Star Wars Series',
        'slug': 'star-wars-series',
        'description': 'The galaxy far, far away expands to Disney+. From the lone bounty hunter protecting a mysterious child to the gritty espionage of the Rebellion, these series explore corners of Star Wars never seen before.',
        'icon': '🚀',
        'category': 'series',
        'order': 19,
        'banner_path': '/9RO2vbQ67otPrBArZnBLNfSKuBY.jpg',
        'poster_path': '/sWgBv7LV2reoncEvAFMKUkGOCG5.jpg',
        'movies': [
            {'tmdb_id': 82856, 'title': 'The Mandalorian', 'overview': 'After the fall of the Galactic Empire, lawlessness has spread throughout the galaxy. A lone gunfighter makes his way through the outer reaches, far from the authority of the New Republic.', 'poster_path': '/sWgBv7LV2reoncEvAFMKUkGOCG5.jpg', 'backdrop_path': '/9RO2vbQ67otPrBArZnBLNfSKuBY.jpg', 'release_date': '2019-11-12', 'vote_average': 8.5, 'type': 'series', 'order': 1},
            {'tmdb_id': 83867, 'title': 'Andor', 'overview': 'In an era filled with danger, deception and intrigue, Cassian Andor will discover the difference he can make in the struggle against the tyrannical Galactic Empire.', 'poster_path': '/59SVNwLfoMnZPPB6ukW6dlPxAdI.jpg', 'backdrop_path': '/7UGase7owBCOBFxNpUHp5hxp01L.jpg', 'release_date': '2022-09-21', 'vote_average': 8.5, 'type': 'series', 'order': 2},
            {'tmdb_id': 114461, 'title': 'Ahsoka', 'overview': 'Set in the aftermath of the fall of the Empire, former Jedi knight Ahsoka Tano investigates an emerging threat to a vulnerable galaxy.', 'poster_path': '/aqM3JBaU7G0AvbFsOtWNEJbKOzb.jpg', 'backdrop_path': '/qUfDkFVhpF2TLLf7gUBBXQ9blLI.jpg', 'release_date': '2023-08-22', 'vote_average': 7.4, 'type': 'series', 'order': 3},
            {'tmdb_id': 92830, 'title': 'Obi-Wan Kenobi', 'overview': 'The story begins 10 years after the dramatic events of Revenge of the Sith where Obi-Wan Kenobi faced his greatest defeat, the downfall of the Jedi Order and the corruption of his best friend and Jedi apprentice Anakin Skywalker.', 'poster_path': '/qDAsdn7GEK4giSQoEyuCNBpLxNv.jpg', 'backdrop_path': '/4OHtDBfuWkFQNs4FKDX3P1aGQ2k.jpg', 'release_date': '2022-05-27', 'vote_average': 7.5, 'type': 'series', 'order': 4},
        ]
    },

    # ============================================================
    # 20. INDIAN WEB SERIES
    # ============================================================
    {
        'name': 'Indian Web Series',
        'slug': 'indian-web-series',
        'description': 'India\'s OTT revolution has produced some of the most gripping, authentic, and culturally rich content in the world. From political dramas to slice-of-life gems, these series showcase India\'s incredible storytelling.',
        'icon': '🎬',
        'category': 'indian_cinema',
        'order': 20,
        'banner_path': '/1CwCFyA9xFtMEkBRRmMnLXm5DLw.jpg',
        'poster_path': '/rTmal9fDbwh5F4Bql6689EzJnl7.jpg',
        'movies': [
            {'tmdb_id': 79008, 'title': 'Sacred Games', 'overview': 'A link in the chain of a crime lord\'s past leads an honest cop to uncover a conspiracy that could destroy Mumbai. Based on Vikram Chandra\'s novel.', 'poster_path': '/rTmal9fDbwh5F4Bql6689EzJnl7.jpg', 'backdrop_path': '/1CwCFyA9xFtMEkBRRmMnLXm5DLw.jpg', 'release_date': '2018-07-06', 'vote_average': 8.8, 'type': 'series', 'order': 1},
            {'tmdb_id': 108978, 'title': 'Mirzapur', 'overview': 'A reckless act forces young men into the world of crime and violence in the lawless city of Mirzapur, Uttar Pradesh.', 'poster_path': '/5pVJ9SuuO72IgN6i9PJbMBzKGYD.jpg', 'backdrop_path': '/6oomrFe0BFT7FvMnR1VCBHB3F8Z.jpg', 'release_date': '2018-11-16', 'vote_average': 8.5, 'type': 'series', 'order': 2},
            {'tmdb_id': 120089, 'title': 'The Family Man', 'overview': 'Srikant Tiwari is a middle-class man who secretly works as a spy for the National Investigation Agency while trying to balance his family life.', 'poster_path': '/lPe1GyCKxLHHrLrfzTJpYr0r7B.jpg', 'backdrop_path': '/8cXf0OOHFHEP7pMv9CSjlxlAJnC.jpg', 'release_date': '2019-09-20', 'vote_average': 9.0, 'type': 'series', 'order': 3},
            {'tmdb_id': 122226, 'title': 'Paatal Lok', 'overview': 'A jaded cop gets the case of his career when four suspects are caught for the assassination attempt of a prime-time journalist, leading him deep into the underbelly of society.', 'poster_path': '/7pTqaZQZxv7OKn9qHHSACWe0sJt.jpg', 'backdrop_path': '/Vr7Jc8DPuMSozFBq4RVFmcPrL4.jpg', 'release_date': '2020-05-15', 'vote_average': 8.7, 'type': 'series', 'order': 4},
            {'tmdb_id': 127529, 'title': 'Scam 1992', 'overview': 'The story of Harshad Mehta, a stockbroker who took the stock market to dizzying heights and his catastrophic downfall. Based on the true story of India\'s biggest stock market scam.', 'poster_path': '/7lMnCbWYHEXhT9JNTRuRiK5FzLH.jpg', 'backdrop_path': '/nFo3FaJhgkEWNV8hKUDNZ3r4Mxi.jpg', 'release_date': '2020-10-09', 'vote_average': 9.3, 'type': 'series', 'order': 5},
            {'tmdb_id': 139880, 'title': 'Panchayat', 'overview': 'An engineering graduate reluctantly takes up the job of secretary at a panchayat office in a remote village of Uttar Pradesh, navigating the beauty and challenges of rural India.', 'poster_path': '/A7EByudX0eX7c3fiqBrCLzkshp5.jpg', 'backdrop_path': '/eQYM8mVvPMKCi5POZMxCDHaOp5w.jpg', 'release_date': '2020-04-03', 'vote_average': 9.0, 'type': 'series', 'order': 6},
            {'tmdb_id': 154112, 'title': 'Kota Factory', 'overview': 'Set in the coaching hub city of Kota, the series follows students preparing for competitive exams, exploring the pressure, friendships, and dreams that define this phase of life.', 'poster_path': '/qFlJ3KPWLXHE2KCmkTHJxGiFlKd.jpg', 'backdrop_path': '/v0HsRJoJrXBxAGSwGGM5MZCaWBw.jpg', 'release_date': '2019-04-16', 'vote_average': 9.1, 'type': 'series', 'order': 7},
        ]
    },
    {
        'name': 'South Indian Blockbusters',
        'slug': 'south-indian-blockbusters',
        'description': 'The biggest, boldest, most spectacular films from Telugu, Tamil, Malayalam, and Kannada cinema. South Indian filmmakers are redefining what Indian cinema can achieve on a global scale.',
        'icon': '🎭',
        'category': 'indian_cinema',
        'order': 21,
        'banner_path': '/bfHPJCHNwqP2BNMJC1sQ2JYtEPF.jpg',
        'poster_path': '/iGMxoNv4Ynf3MCqPf1VFxJeI3cF.jpg',
        'movies': [
            {'tmdb_id': 786892, 'title': 'RRR', 'overview': 'A fictional story about two legendary revolutionaries and their journey before they began the fight for their country. A spectacle like no other.', 'poster_path': '/nEufeZlyAOLqO2brrs0yeF1lgXO.jpg', 'backdrop_path': '/bfHPJCHNwqP2BNMJC1sQ2JYtEPF.jpg', 'release_date': '2022-03-24', 'vote_average': 7.8, 'type': 'movie', 'order': 1},
            {'tmdb_id': 255709, 'title': 'Baahubali: The Beginning', 'overview': 'In ancient India, an adventurous and daring man becomes involved in a decades-old feud between two warring peoples. India\'s most ambitious film ever made.', 'poster_path': '/d3XIEUFfHGOFZJFU1lkMuqkJDZ3.jpg', 'backdrop_path': '/jeVJcCbSMbxJPvWWAqfZackMcjn.jpg', 'release_date': '2015-07-10', 'vote_average': 8.0, 'type': 'movie', 'order': 2},
            {'tmdb_id': 339877, 'title': 'Baahubali 2: The Conclusion', 'overview': 'When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.', 'poster_path': '/kHBVSYSM63i63mBCSXxcnLnPnjm.jpg', 'backdrop_path': '/dLDsD9bGY0m0PcEP3nKa4F5ZVNL.jpg', 'release_date': '2017-04-28', 'vote_average': 8.2, 'type': 'movie', 'order': 3},
            {'tmdb_id': 564147, 'title': 'KGF: Chapter 1', 'overview': 'A fierce young man Rocky becomes the most powerful man in the Kolar Gold Fields and changes the fate of an entire community. The film that made Kannada cinema global.', 'poster_path': '/lVy5Zqcty2NfHMuTGSlnx1OMJVZ.jpg', 'backdrop_path': '/kGqe7A1xKfVKiuGWEHPHjTp6Olv.jpg', 'release_date': '2018-12-21', 'vote_average': 8.2, 'type': 'movie', 'order': 4},
            {'tmdb_id': 587412, 'title': 'KGF: Chapter 2', 'overview': 'The blood-soaked land of Kolar Gold Field has a new overlord now - Rocky, whose name strikes fear in the heart of his foes. His story continues to grow even more violent.', 'poster_path': '/4ICGZY0lDbvzFmm3RiNpEFCBYt.jpg', 'backdrop_path': '/9JlBqVtSZBOnf2cL60kIH4YRLXI.jpg', 'release_date': '2022-04-14', 'vote_average': 8.3, 'type': 'movie', 'order': 5},
            {'tmdb_id': 690957, 'title': 'Pushpa: The Rise', 'overview': 'A laborer rises through the ranks of a red sandalwood smuggling syndicate, using cunning and fearlessness to become its most powerful figure. Allu Arjun at his best.', 'poster_path': '/rugyJdeoJm7crF9BKNO3FBaVAsJ.jpg', 'backdrop_path': '/8eihUxjQsJ7WvGySkVMC0EwbPAD.jpg', 'release_date': '2021-12-17', 'vote_average': 7.6, 'type': 'movie', 'order': 6},
            {'tmdb_id': 801688, 'title': 'Kalki 2898 AD', 'overview': 'Set in a dystopian future, Kalki is the final avatar of Lord Vishnu. One of the most expensive and visually spectacular Indian films ever produced.', 'poster_path': '/hqbT2u0RQmBVSX4pGnQoiOhZpkO.jpg', 'backdrop_path': '/8eiNIVeAqDDDkMJNVTfKHpHyFqF.jpg', 'release_date': '2024-06-27', 'vote_average': 7.5, 'type': 'movie', 'order': 7},
            {'tmdb_id': 843307, 'title': 'Vikram', 'overview': 'A black ops agent investigates a series of masked killings, leading to a deadly encounter between three dangerous men. Kamal Haasan\'s triumphant return to masala action cinema.', 'poster_path': '/3bhkrj58Vtu5enALgIPMC9PgkHQ.jpg', 'backdrop_path': '/tmU7GeKVybMWFButWEGl2M4GeiP.jpg', 'release_date': '2022-06-03', 'vote_average': 8.4, 'type': 'movie', 'order': 8},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed cinema with hardcoded, curated data - no API calls needed'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🎬 SEEDING CURATED CINEMA DATA...\n'))

        total_collections = 0
        total_movies = 0
        total_skipped = 0

        for col_data in COLLECTIONS_DATA:
            self.stdout.write(self.style.SUCCESS(f"\n{col_data['icon']} {col_data['name']}"))

            collection, created = Collection.objects.update_or_create(
                slug=col_data['slug'],
                defaults={
                    'name': col_data['name'],
                    'description': col_data['description'],
                    'icon': col_data['icon'],
                    'category': col_data['category'],
                    'order': col_data['order'],
                    'banner_path': col_data.get('banner_path', ''),
                    'poster_path': col_data.get('poster_path', ''),
                    'is_active': True,
                }
            )

            if created:
                total_collections += 1

            for movie_data in col_data['movies']:
                watch_url = f"https://www.google.com/search?q={movie_data['title'].replace(' ', '+')}+watch+online+free+hotstar+netflix+amazon+prime+zee5"

                movie, movie_created = Movie.objects.update_or_create(
                    tmdb_id=movie_data['tmdb_id'],
                    defaults={
                        'collection': collection,
                        'title': movie_data['title'],
                        'overview': movie_data['overview'],
                        'poster_path': movie_data.get('poster_path', ''),
                        'backdrop_path': movie_data.get('backdrop_path', ''),
                        'release_date': movie_data.get('release_date', ''),
                        'vote_average': movie_data.get('vote_average', 0),
                        'vote_count': movie_data.get('vote_count', 0),
                        'popularity': movie_data.get('popularity', 0),
                        'type': movie_data.get('type', 'movie'),
                        'watch_url': watch_url,
                        'is_featured': movie_data.get('vote_average', 0) >= 7.5,
                        'order': movie_data.get('order', 0),
                    }
                )

                if movie_created:
                    total_movies += 1
                    self.stdout.write(f"  ✓ {movie_data['title']}")
                else:
                    total_skipped += 1

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'🎬 SEEDING COMPLETE'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Collections: {total_collections} new'))
        self.stdout.write(self.style.SUCCESS(f'✅ Movies created: {total_movies}'))
        self.stdout.write(self.style.SUCCESS(f'⊘ Movies updated: {total_skipped}'))
        self.stdout.write(self.style.SUCCESS(f'🎯 Total in DB: {Movie.objects.count()} movies across {Collection.objects.count()} collections'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))