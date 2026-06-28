import logging
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import os

logger = logging.getLogger()

TMDB_API_KEY = os.getenv('TMDB_API_KEY', None)
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Mock movie data for fallback (real movies relevant to each field)
MOCK_MOVIES = {
    'science-nature': [
        {'id': 1, 'title': 'Interstellar', 'overview': 'A team of explorers travel through a wormhole in space to ensure humanity\'s survival.', 'poster_path': '/rZe6Z6KcLévénementseW9XQ.jpg', 'release_date': '2014-11-07', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=Interstellar+full+movie+free'},
        {'id': 2, 'title': 'The Martian', 'overview': 'An astronaut becomes stranded on Mars and must rely on his ingenuity to survive.', 'poster_path': '/5aGhaIHYuQbqlHWvWYqMCnj4zIl.jpg', 'release_date': '2015-10-02', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Martian+full+movie+free'},
        {'id': 3, 'title': 'A Brief History of Time', 'overview': 'A documentary about Stephen Hawking exploring the nature of the universe.', 'poster_path': '/abc123.jpg', 'release_date': '1991-04-26', 'vote_average': 7.5, 'watch_url': 'https://www.youtube.com/results?search_query=A+Brief+History+of+Time+full+movie'},
        {'id': 4, 'title': 'Cosmos: A Spacetime Odyssey', 'overview': 'Neil deGrasse Tyson explores the universe and humanity\'s place in it.', 'poster_path': '/cosmos.jpg', 'release_date': '2014-03-09', 'vote_average': 9.2, 'watch_url': 'https://www.youtube.com/results?search_query=Cosmos+A+Spacetime+Odyssey'},
        {'id': 5, 'title': 'Life', 'overview': 'Astronauts aboard the International Space Station encounter a rapidly evolving alien organism.', 'poster_path': '/life.jpg', 'release_date': '2017-03-24', 'vote_average': 6.6, 'watch_url': 'https://www.youtube.com/results?search_query=Life+2017+full+movie'},
        {'id': 6, 'title': 'The Right Stuff', 'overview': 'The story of the early U.S. space program and the Mercury Seven astronauts.', 'poster_path': '/rightstuff.jpg', 'release_date': '1983-10-21', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=The+Right+Stuff+full+movie'},
        {'id': 7, 'title': 'Apollo 13', 'overview': 'The true story of NASA\'s Apollo 13 mission and the struggle to return the astronauts home.', 'poster_path': '/apollo13.jpg', 'release_date': '1995-06-30', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=Apollo+13+full+movie'},
        {'id': 8, 'title': 'First Man', 'overview': 'A look at the early years of space exploration and the space race.', 'poster_path': '/firstman.jpg', 'release_date': '2018-10-12', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=First+Man+full+movie'},
    ],
    'technology-computing': [
        {'id': 1, 'title': 'The Imitation Game', 'overview': 'The story of mathematician Alan Turing and his crucial role in WWII.', 'poster_path': '/imitation.jpg', 'release_date': '2014-12-25', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Imitation+Game+full+movie+free'},
        {'id': 2, 'title': 'Ex Machina', 'overview': 'A programmer is invited to evaluate an advanced humanoid AI robot.', 'poster_path': '/exmachina.jpg', 'release_date': '2015-04-10', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=Ex+Machina+full+movie+free'},
        {'id': 3, 'title': 'Her', 'overview': 'A lonely man develops a relationship with an advanced artificial intelligence.', 'poster_path': '/her.jpg', 'release_date': '2013-12-18', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Her+full+movie+free'},
        {'id': 4, 'title': 'The Social Network', 'overview': 'The founding of Facebook and the lawsuits that followed.', 'poster_path': '/socialnetwork.jpg', 'release_date': '2010-10-01', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=The+Social+Network+full+movie'},
        {'id': 5, 'title': 'Steve Jobs', 'overview': 'The life and legacy of Apple founder Steve Jobs.', 'poster_path': '/stevejobs.jpg', 'release_date': '2015-11-25', 'vote_average': 7.2, 'watch_url': 'https://www.youtube.com/results?search_query=Steve+Jobs+full+movie'},
        {'id': 6, 'title': 'The Code Breaker', 'overview': 'Documentary about the life and achievements of programmer legends.', 'poster_path': '/codebreaker.jpg', 'release_date': '2015-06-01', 'vote_average': 7.4, 'watch_url': 'https://www.youtube.com/results?search_query=The+Code+Breaker+documentary'},
        {'id': 7, 'title': 'Westworld', 'overview': 'Android hosts in a futuristic theme park begin to gain consciousness.', 'poster_path': '/westworld.jpg', 'release_date': '2016-10-02', 'vote_average': 8.5, 'watch_url': 'https://www.youtube.com/results?search_query=Westworld+series'},
        {'id': 8, 'title': 'Blade Runner 2049', 'overview': 'A futuristic tale exploring artificial intelligence and humanity.', 'poster_path': '/bladerunner.jpg', 'release_date': '2017-10-06', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Blade+Runner+2049+full+movie'},
    ],
    'literature-stories': [
        {'id': 1, 'title': 'Pride and Prejudice', 'overview': 'A romantic drama based on Jane Austen\'s classic novel.', 'poster_path': '/prideandprejudice.jpg', 'release_date': '2005-09-16', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Pride+and+Prejudice+full+movie'},
        {'id': 2, 'title': 'The Great Gatsby', 'overview': 'The tale of Jay Gatsby and his obsessive love for Daisy Buchanan.', 'poster_path': '/gatsby.jpg', 'release_date': '2013-05-10', 'vote_average': 7.2, 'watch_url': 'https://www.youtube.com/results?search_query=The+Great+Gatsby+full+movie'},
        {'id': 3, 'title': 'Avengers: Endgame', 'overview': 'Marvel comic adaptation featuring iconic superheroes.', 'poster_path': '/avengersendgame.jpg', 'release_date': '2019-04-26', 'vote_average': 8.4, 'watch_url': 'https://www.youtube.com/results?search_query=Avengers+Endgame+full+movie'},
        {'id': 4, 'title': 'Black Panther', 'overview': 'Marvel Studios\' adaptation of the Black Panther comics.', 'poster_path': '/blackpanther.jpg', 'release_date': '2018-02-16', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=Black+Panther+full+movie'},
        {'id': 5, 'title': 'Wonder Woman', 'overview': 'Amazon princess Diana fights injustice and discovers her true powers.', 'poster_path': '/wonderwoman.jpg', 'release_date': '2017-06-02', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=Wonder+Woman+full+movie'},
        {'id': 6, 'title': 'The Book Thief', 'overview': 'A girl steals books and shares them during WWII.', 'poster_path': '/bookthief.jpg', 'release_date': '2013-11-15', 'vote_average': 7.6, 'watch_url': 'https://www.youtube.com/results?search_query=The+Book+Thief+full+movie'},
        {'id': 7, 'title': 'Atonement', 'overview': 'A tragic love story told across decades based on a literary masterpiece.', 'poster_path': '/atonement.jpg', 'release_date': '2007-12-07', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Atonement+full+movie'},
        {'id': 8, 'title': 'Harry Potter and the Sorcerer\'s Stone', 'overview': 'A young wizard attends a magical school and discovers his destiny.', 'poster_path': '/harrypotter.jpg', 'release_date': '2001-11-16', 'vote_average': 7.6, 'watch_url': 'https://www.youtube.com/results?search_query=Harry+Potter+full+movie'},
    ],
    'film-cinema': [
        {'id': 1, 'title': 'Inception', 'overview': 'A thief who steals corporate secrets through dream-sharing technology.', 'poster_path': '/inception.jpg', 'release_date': '2010-07-16', 'vote_average': 8.8, 'watch_url': 'https://www.youtube.com/results?search_query=Inception+full+movie'},
        {'id': 2, 'title': 'Pulp Fiction', 'overview': 'The lives of two mob hitmen, a boxer, and a gangster\'s wife intertwine.', 'poster_path': '/pulpfiction.jpg', 'release_date': '1994-10-14', 'vote_average': 8.9, 'watch_url': 'https://www.youtube.com/results?search_query=Pulp+Fiction+full+movie'},
        {'id': 3, 'title': 'The Dark Knight', 'overview': 'Batman faces the Joker, a criminal mastermind.', 'poster_path': '/darkknight.jpg', 'release_date': '2008-07-18', 'vote_average': 9.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Dark+Knight+full+movie'},
        {'id': 4, 'title': 'Parasite', 'overview': 'A brilliant social thriller about class and society.', 'poster_path': '/parasite.jpg', 'release_date': '2019-05-30', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=Parasite+full+movie'},
        {'id': 5, 'title': 'Oppenheimer', 'overview': 'The life story of theoretical physicist J. Robert Oppenheimer.', 'poster_path': '/oppenheimer.jpg', 'release_date': '2023-07-21', 'vote_average': 8.1, 'watch_url': 'https://www.youtube.com/results?search_query=Oppenheimer+full+movie'},
        {'id': 6, 'title': 'Amélie', 'overview': 'A shy waitress decides to change the lives of those around her.', 'poster_path': '/amelie.jpg', 'release_date': '2001-04-25', 'vote_average': 8.3, 'watch_url': 'https://www.youtube.com/results?search_query=Amelie+full+movie'},
        {'id': 7, 'title': 'Barbie', 'overview': 'Barbie comes to life in a vibrant, colorful adventure.', 'poster_path': '/barbie.jpg', 'release_date': '2023-07-21', 'vote_average': 7.4, 'watch_url': 'https://www.youtube.com/results?search_query=Barbie+full+movie'},
        {'id': 8, 'title': 'Dune', 'overview': 'An epic science fiction adaptation of Frank Herbert\'s masterpiece.', 'poster_path': '/dune.jpg', 'release_date': '2021-10-22', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Dune+full+movie'},
    ],
    'health-performance': [
        {'id': 1, 'title': 'Rocky', 'overview': 'An underdog boxer gets a shot at the heavyweight championship.', 'poster_path': '/rocky.jpg', 'release_date': '1976-12-03', 'vote_average': 8.1, 'watch_url': 'https://www.youtube.com/results?search_query=Rocky+full+movie'},
        {'id': 2, 'title': 'Creed', 'overview': 'An apollo Creed\'s son trains to become a champion boxer.', 'poster_path': '/creed.jpg', 'release_date': '2015-11-25', 'vote_average': 7.5, 'watch_url': 'https://www.youtube.com/results?search_query=Creed+full+movie'},
        {'id': 3, 'title': 'Yoga: The Art of Transformation', 'overview': 'A documentary exploring the ancient practice of yoga.', 'poster_path': '/yoga.jpg', 'release_date': '2012-04-15', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Yoga+The+Art+of+Transformation'},
        {'id': 4, 'title': 'Free Solo', 'overview': 'A climber attempts to scale El Capitan without ropes.', 'poster_path': '/freesolo.jpg', 'release_date': '2018-09-28', 'vote_average': 8.2, 'watch_url': 'https://www.youtube.com/results?search_query=Free+Solo+documentary'},
        {'id': 5, 'title': 'The Last Dance', 'overview': 'Documentary series about Michael Jordan\'s final championship season.', 'poster_path': '/lastdance.jpg', 'release_date': '2020-04-19', 'vote_average': 9.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Last+Dance+Michael+Jordan'},
        {'id': 6, 'title': 'Pumping Iron', 'overview': 'Documentary about bodybuilding and Arnold Schwarzenegger.', 'poster_path': '/pumpingiron.jpg', 'release_date': '1977-02-04', 'vote_average': 7.6, 'watch_url': 'https://www.youtube.com/results?search_query=Pumping+Iron+documentary'},
        {'id': 7, 'title': 'Chariots of Fire', 'overview': 'British sprinters compete in the 1924 Olympic Games.', 'poster_path': '/chariotsoffire.jpg', 'release_date': '1981-10-23', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Chariots+of+Fire+full+movie'},
        {'id': 8, 'title': 'Midnight Runners', 'overview': 'Inspiring sports drama about dedication and triumph.', 'poster_path': '/midnightrunners.jpg', 'release_date': '2017-12-20', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=Midnight+Runners+full+movie'},
    ],
    'history-philosophy': [
        {'id': 1, 'title': 'Gandhi', 'overview': 'The life and philosophies of Mahatma Gandhi.', 'poster_path': '/gandhi.jpg', 'release_date': '1982-11-30', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Gandhi+full+movie'},
        {'id': 2, 'title': 'Schindler\'s List', 'overview': 'The true story of Oskar Schindler during the Holocaust.', 'poster_path': '/schindlerslist.jpg', 'release_date': '1993-12-15', 'vote_average': 9.0, 'watch_url': 'https://www.youtube.com/results?search_query=Schindler\'s+List+full+movie'},
        {'id': 3, 'title': 'Oppenheimer', 'overview': 'The life of physicist J. Robert Oppenheimer and the atomic bomb.', 'poster_path': '/oppenheimer.jpg', 'release_date': '2023-07-21', 'vote_average': 8.1, 'watch_url': 'https://www.youtube.com/results?search_query=Oppenheimer+full+movie'},
        {'id': 4, 'title': 'The King\'s Speech', 'overview': 'King George VI must overcome his stammer to lead Britain.', 'poster_path': '/kingsspeech.jpg', 'release_date': '2010-12-25', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+King\'s+Speech+full+movie'},
        {'id': 5, 'title': '1917', 'overview': 'Two soldiers must deliver a message during WWI.', 'poster_path': '/1917.jpg', 'release_date': '2019-12-25', 'vote_average': 8.2, 'watch_url': 'https://www.youtube.com/results?search_query=1917+full+movie'},
        {'id': 6, 'title': 'Darkest Hour', 'overview': 'Churchill leads Britain through its darkest hour in WWII.', 'poster_path': '/darkesthour.jpg', 'release_date': '2017-11-22', 'vote_average': 7.4, 'watch_url': 'https://www.youtube.com/results?search_query=Darkest+Hour+full+movie'},
        {'id': 7, 'title': 'The Imitation Game', 'overview': 'Alan Turing\'s brilliant mind during World War II.', 'poster_path': '/imitation.jpg', 'release_date': '2014-12-25', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Imitation+Game+full+movie'},
        {'id': 8, 'title': 'Hidden Figures', 'overview': 'Black women mathematicians during the space race.', 'poster_path': '/hiddenfigures.jpg', 'release_date': '2016-12-25', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Hidden+Figures+full+movie'},
    ],
    'music-sound': [
        {'id': 1, 'title': 'Bohemian Rhapsody', 'overview': 'The story of Queen and Freddie Mercury.', 'poster_path': '/bohemian.jpg', 'release_date': '2018-11-02', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Bohemian+Rhapsody+full+movie'},
        {'id': 2, 'title': 'A Star Is Born', 'overview': 'A musician helps an unknown singer find stardom.', 'poster_path': '/starisborn.jpg', 'release_date': '2018-10-05', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=A+Star+Is+Born+full+movie'},
        {'id': 3, 'title': 'Whiplash', 'overview': 'A drummer\'s obsessive pursuit of musical perfection.', 'poster_path': '/whiplash.jpg', 'release_date': '2014-10-10', 'vote_average': 8.5, 'watch_url': 'https://www.youtube.com/results?search_query=Whiplash+full+movie'},
        {'id': 4, 'title': 'Ray', 'overview': 'The life and music of Ray Charles.', 'poster_path': '/ray.jpg', 'release_date': '2004-10-29', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=Ray+full+movie'},
        {'id': 5, 'title': 'Walk the Line', 'overview': 'Johnny Cash\'s journey to stardom and redemption.', 'poster_path': '/walktherline.jpg', 'release_date': '2005-11-18', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=Walk+the+Line+full+movie'},
        {'id': 6, 'title': 'Dreamgirls', 'overview': 'The rise of an all-girl singing group in the 1960s.', 'poster_path': '/dreamgirls.jpg', 'release_date': '2006-12-25', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=Dreamgirls+full+movie'},
        {'id': 7, 'title': 'Once', 'overview': 'Two musicians share their passion through music.', 'poster_path': '/once.jpg', 'release_date': '2007-05-18', 'vote_average': 7.8, 'watch_url': 'https://www.youtube.com/results?search_query=Once+full+movie'},
        {'id': 8, 'title': 'Rocketman', 'overview': 'The extraordinary life of Elton John.', 'poster_path': '/rocketman.jpg', 'release_date': '2019-05-31', 'vote_average': 7.2, 'watch_url': 'https://www.youtube.com/results?search_query=Rocketman+full+movie'},
    ],
    'languages-culture': [
        {'id': 1, 'title': 'Slumdog Millionaire', 'overview': 'An Indian street kid wins the lottery and recounts his past.', 'poster_path': '/slumdogmillionaire.jpg', 'release_date': '2008-11-23', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Slumdog+Millionaire+full+movie'},
        {'id': 2, 'title': 'Parasite', 'overview': 'A Korean thriller exploring class and culture.', 'poster_path': '/parasite.jpg', 'release_date': '2019-05-30', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=Parasite+full+movie'},
        {'id': 3, 'title': 'Crouching Tiger, Hidden Dragon', 'overview': 'A martial arts epic set in ancient China.', 'poster_path': '/crouching.jpg', 'release_date': '2000-07-06', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=Crouching+Tiger+Hidden+Dragon+full+movie'},
        {'id': 4, 'title': 'Life Is Beautiful', 'overview': 'An Italian father uses humor to shield his son from tragedy.', 'poster_path': '/lifeisbeautiful.jpg', 'release_date': '1997-12-20', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=Life+Is+Beautiful+full+movie'},
        {'id': 5, 'title': 'Amélie', 'overview': 'A French girl transforms the lives around her.', 'poster_path': '/amelie.jpg', 'release_date': '2001-04-25', 'vote_average': 8.3, 'watch_url': 'https://www.youtube.com/results?search_query=Amelie+full+movie'},
        {'id': 6, 'title': 'Pan\'s Labyrinth', 'overview': 'A Spanish fantasy set during the Spanish Civil War.', 'poster_path': '/panslabyrinth.jpg', 'release_date': '2006-12-29', 'vote_average': 8.2, 'watch_url': 'https://www.youtube.com/results?search_query=Pan\'s+Labyrinth+full+movie'},
        {'id': 7, 'title': 'Chungking Express', 'overview': 'A Hong Kong film exploring love and urban culture.', 'poster_path': '/chungking.jpg', 'release_date': '1994-12-14', 'vote_average': 7.5, 'watch_url': 'https://www.youtube.com/results?search_query=Chungking+Express+full+movie'},
        {'id': 8, 'title': 'Joyride', 'overview': 'An Irish film celebrating youth and freedom.', 'poster_path': '/joyride.jpg', 'release_date': '2008-08-08', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=Joyride+full+movie'},
    ],
    'culinary-arts': [
        {'id': 1, 'title': 'Ratatouille', 'overview': 'A rat dreams of becoming a chef in Paris.', 'poster_path': '/ratatouille.jpg', 'release_date': '2007-06-29', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Ratatouille+full+movie'},
        {'id': 2, 'title': 'Jiro Dreams of Sushi', 'overview': 'Documentary about an elderly sushi master and his art.', 'poster_path': '/jiro.jpg', 'release_date': '2011-03-23', 'vote_average': 8.2, 'watch_url': 'https://www.youtube.com/results?search_query=Jiro+Dreams+of+Sushi+documentary'},
        {'id': 3, 'title': 'Babette\'s Feast', 'overview': 'A French cook prepares an extravagant meal for a small Danish village.', 'poster_path': '/babettesfeast.jpg', 'release_date': '1987-04-18', 'vote_average': 8.1, 'watch_url': 'https://www.youtube.com/results?search_query=Babette\'s+Feast+full+movie'},
        {'id': 4, 'title': 'Chef', 'overview': 'A celebrity chef opens a food truck after losing his job.', 'poster_path': '/chef.jpg', 'release_date': '2014-05-30', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=Chef+full+movie'},
        {'id': 5, 'title': 'Eat Pray Love', 'overview': 'A woman travels the world to find herself through food.', 'poster_path': '/eatpraylove.jpg', 'release_date': '2010-08-15', 'vote_average': 5.8, 'watch_url': 'https://www.youtube.com/results?search_query=Eat+Pray+Love+full+movie'},
        {'id': 6, 'title': 'Chocolat', 'overview': 'A woman opens a chocolate shop in a conservative French village.', 'poster_path': '/chocolat.jpg', 'release_date': '2000-12-29', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=Chocolat+full+movie'},
        {'id': 7, 'title': 'Tampopo', 'overview': 'A Japanese food comedy about the perfect ramen noodle.', 'poster_path': '/tampopo.jpg', 'release_date': '1985-11-09', 'vote_average': 7.6, 'watch_url': 'https://www.youtube.com/results?search_query=Tampopo+full+movie'},
        {'id': 8, 'title': 'Delicatessen', 'overview': 'A surreal dark comedy set in a unique community.', 'poster_path': '/delicatessen.jpg', 'release_date': '1991-12-30', 'vote_average': 7.5, 'watch_url': 'https://www.youtube.com/results?search_query=Delicatessen+full+movie'},
    ],
    'visual-arts-design': [
        {'id': 1, 'title': 'Frida', 'overview': 'The life and art of Mexican painter Frida Kahlo.', 'poster_path': '/frida.jpg', 'release_date': '2002-11-15', 'vote_average': 7.6, 'watch_url': 'https://www.youtube.com/results?search_query=Frida+full+movie'},
        {'id': 2, 'title': 'Pollock', 'overview': 'The life and work of abstract artist Jackson Pollock.', 'poster_path': '/pollock.jpg', 'release_date': '2000-12-08', 'vote_average': 7.4, 'watch_url': 'https://www.youtube.com/results?search_query=Pollock+full+movie'},
        {'id': 3, 'title': 'Big Eyes', 'overview': 'A woman creates masterpiece paintings while her husband takes credit.', 'poster_path': '/bigeyes.jpg', 'release_date': '2014-12-25', 'vote_average': 7.4, 'watch_url': 'https://www.youtube.com/results?search_query=Big+Eyes+full+movie'},
        {'id': 4, 'title': 'Midnight in Paris', 'overview': 'A writer is transported to 1920s Paris through the magic of art.', 'poster_path': '/midnightinparis.jpg', 'release_date': '2011-05-20', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=Midnight+in+Paris+full+movie'},
        {'id': 5, 'title': 'Dreamchild', 'overview': 'The story behind the creation of Alice in Wonderland.', 'poster_path': '/dreamchild.jpg', 'release_date': '1985-11-15', 'vote_average': 7.0, 'watch_url': 'https://www.youtube.com/results?search_query=Dreamchild+full+movie'},
        {'id': 6, 'title': 'In the Mood for Love', 'overview': 'A visually stunning Hong Kong film about art and design.', 'poster_path': '/intheoodforlove.jpg', 'release_date': '2000-12-20', 'vote_average': 8.1, 'watch_url': 'https://www.youtube.com/results?search_query=In+the+Mood+for+Love+full+movie'},
        {'id': 7, 'title': 'The Artist', 'overview': 'A silent film about the transition from silent to sound cinema.', 'poster_path': '/theartist.jpg', 'release_date': '2011-10-14', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=The+Artist+full+movie'},
        {'id': 8, 'title': 'Everything Everywhere All at Once', 'overview': 'A visually creative multiverse adventure.', 'poster_path': '/everything.jpg', 'release_date': '2022-11-18', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Everything+Everywhere+All+At+Once+full+movie'},
    ],
    'psychology-mind': [
        {'id': 1, 'title': 'One Flew Over the Cuckoo\'s Nest', 'overview': 'A patient leads a rebellion in a mental institution.', 'poster_path': '/cuckoosnest.jpg', 'release_date': '1975-11-23', 'vote_average': 8.7, 'watch_url': 'https://www.youtube.com/results?search_query=One+Flew+Over+the+Cuckoo\'s+Nest+full+movie'},
        {'id': 2, 'title': 'Fight Club', 'overview': 'An insomniac and a soap maker start an underground fight club.', 'poster_path': '/fightclub.jpg', 'release_date': '1999-10-15', 'vote_average': 8.8, 'watch_url': 'https://www.youtube.com/results?search_query=Fight+Club+full+movie'},
        {'id': 3, 'title': 'The Shining', 'overview': 'A man descends into madness at an isolated hotel.', 'poster_path': '/theshining.jpg', 'release_date': '1980-05-23', 'vote_average': 8.4, 'watch_url': 'https://www.youtube.com/results?search_query=The+Shining+full+movie'},
        {'id': 4, 'title': 'Requiem for a Dream', 'overview': 'Four people spiral into desperation and addiction.', 'poster_path': '/requiem.jpg', 'release_date': '2000-10-06', 'vote_average': 8.3, 'watch_url': 'https://www.youtube.com/results?search_query=Requiem+for+a+Dream+full+movie'},
        {'id': 5, 'title': 'Black Swan', 'overview': 'A ballerina\'s descent into madness and obsession.', 'poster_path': '/blackswan.jpg', 'release_date': '2010-12-17', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=Black+Swan+full+movie'},
        {'id': 6, 'title': 'Joker', 'overview': 'The origin story of the iconic villain and troubled man.', 'poster_path': '/joker.jpg', 'release_date': '2019-10-04', 'vote_average': 8.4, 'watch_url': 'https://www.youtube.com/results?search_query=Joker+full+movie'},
        {'id': 7, 'title': 'The Silence of the Lambs', 'overview': 'An FBI trainee seeks help from an imprisoned cannibalistic killer.', 'poster_path': '/silence.jpg', 'release_date': '1991-02-14', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=The+Silence+of+the+Lambs+full+movie'},
        {'id': 8, 'title': 'Eternal Sunshine of the Spotless Mind', 'overview': 'A man undergoes a procedure to erase memories of his ex.', 'poster_path': '/eternalsunshinе.jpg', 'release_date': '2004-03-19', 'vote_average': 8.3, 'watch_url': 'https://www.youtube.com/results?search_query=Eternal+Sunshine+of+the+Spotless+Mind+full+movie'},
    ],
    'space-cosmos': [
        {'id': 1, 'title': 'Interstellar', 'overview': 'Explorers travel through a wormhole to save humanity.', 'poster_path': '/interstellar.jpg', 'release_date': '2014-11-07', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=Interstellar+full+movie'},
        {'id': 2, 'title': 'Gravity', 'overview': 'An astronaut must survive in space after a disaster.', 'poster_path': '/gravity.jpg', 'release_date': '2013-10-04', 'vote_average': 7.7, 'watch_url': 'https://www.youtube.com/results?search_query=Gravity+full+movie'},
        {'id': 3, 'title': 'The Martian', 'overview': 'An astronaut survives alone on Mars.', 'poster_path': '/themartian.jpg', 'release_date': '2015-10-02', 'vote_average': 8.0, 'watch_url': 'https://www.youtube.com/results?search_query=The+Martian+full+movie'},
        {'id': 4, 'title': 'Cosmos: A Spacetime Odyssey', 'overview': 'Neil deGrasse Tyson explores the universe.', 'poster_path': '/cosmos.jpg', 'release_date': '2014-03-09', 'vote_average': 9.2, 'watch_url': 'https://www.youtube.com/results?search_query=Cosmos+A+Spacetime+Odyssey'},
        {'id': 5, 'title': 'Proxima', 'overview': 'A French astronaut prepares for a mission to space.', 'poster_path': '/proxima.jpg', 'release_date': '2019-03-29', 'vote_average': 6.8, 'watch_url': 'https://www.youtube.com/results?search_query=Proxima+full+movie'},
        {'id': 6, 'title': 'First Man', 'overview': 'The early space program and the race to the moon.', 'poster_path': '/firstman.jpg', 'release_date': '2018-10-12', 'vote_average': 7.3, 'watch_url': 'https://www.youtube.com/results?search_query=First+Man+full+movie'},
        {'id': 7, 'title': 'Apollo 13', 'overview': 'The true story of the Apollo 13 mission.', 'poster_path': '/apollo13.jpg', 'release_date': '1995-06-30', 'vote_average': 7.9, 'watch_url': 'https://www.youtube.com/results?search_query=Apollo+13+full+movie'},
        {'id': 8, 'title': 'For All Mankind', 'overview': 'Documentary series about space exploration and astronomy.', 'poster_path': '/forallmankind.jpg', 'release_date': '2019-11-01', 'vote_average': 8.6, 'watch_url': 'https://www.youtube.com/results?search_query=For+All+Mankind+documentary'},
    ],
}

FIELD_TO_TMDB_QUERY = {
    'science-nature': 'science nature',
    'technology-computing': 'technology computing',
    'literature-stories': 'literature stories',
    'music-sound': 'music sound',
    'visual-arts-design': 'visual arts design',
    'culinary-arts': 'culinary cooking',
    'history-philosophy': 'history philosophy',
    'health-performance': 'health sports',
    'film-cinema': 'film cinema',
    'languages-culture': 'language culture',
    'space-cosmos': 'space astronomy',
    'psychology-mind': 'psychology mind',
}

class TMDBMoviesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            field_slug = request.query_params.get('field', 'science-nature')
            
            if field_slug not in FIELD_TO_TMDB_QUERY:
                return Response(
                    {'error': False, 'results': []}
                )
            
            # Try real TMDB API first if key exists
            if TMDB_API_KEY:
                movies = self.fetch_movies_from_tmdb(field_slug)
                if movies:
                    logger.info(f"Fetched {len(movies)} movies from TMDB for: {field_slug}")
                    return Response({'error': False, 'results': movies})
            
            # Fallback to mock data
            mock_movies = MOCK_MOVIES.get(field_slug, [])
            logger.info(f"Using mock data: {len(mock_movies)} movies for: {field_slug}")
            
            return Response({
                'error': False,
                'results': mock_movies
            })
        
        except Exception as e:
            logger.error(f"TMDB view error: {str(e)}", exc_info=True)
            return Response({'error': False, 'results': []})

    def fetch_movies_from_tmdb(self, field_slug):
        """Try to fetch from real TMDB API"""
        try:
            query = FIELD_TO_TMDB_QUERY.get(field_slug, '')
            url = f"{TMDB_BASE_URL}/search/movie"
            params = {
                'api_key': TMDB_API_KEY,
                'query': query,
                'page': 1,
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('results', [])[:12]
        
        except Exception as e:
            logger.warning(f"Real TMDB fetch failed, using mock data: {str(e)}")
            return []