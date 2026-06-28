import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

logger = logging.getLogger()

# Free ebooks from Project Gutenberg mapped to knowledge fields
FREE_EBOOKS = {
    'science-nature': [
        {'id': 1, 'title': 'On the Origin of Species', 'author': 'Charles Darwin', 'description': 'The foundation of evolutionary biology', 'url': 'https://www.gutenberg.org/ebooks/2009', 'cover': '📚'},
        {'id': 2, 'title': 'A Treatise on Electricity and Magnetism', 'author': 'James Clerk Maxwell', 'description': 'Classical physics masterpiece', 'url': 'https://www.gutenberg.org/ebooks/14529', 'cover': '⚡'},
        {'id': 3, 'title': 'The Voyage of the Beagle', 'author': 'Charles Darwin', 'description': 'Darwin\'s journey and discoveries', 'url': 'https://www.gutenberg.org/ebooks/3704', 'cover': '🌍'},
        {'id': 4, 'title': 'Experiments and Observations on Electricity', 'author': 'Benjamin Franklin', 'description': 'Early electrical science', 'url': 'https://www.gutenberg.org/ebooks/57652', 'cover': '⚛️'},
        {'id': 5, 'title': 'The Physical Mechanism of Life', 'author': 'Various', 'description': 'Biological science essays', 'url': 'https://www.gutenberg.org/ebooks/61919', 'cover': '🧬'},
        {'id': 6, 'title': 'Flatland: A Romance of Many Dimensions', 'author': 'Edwin A. Abbott', 'description': 'Sci-fi exploration of dimensions', 'url': 'https://www.gutenberg.org/ebooks/97', 'cover': '📐'},
    ],
    'technology-computing': [
        {'id': 1, 'title': 'Encyclopaedia Britannica on Science and Technology', 'author': 'Various', 'description': 'Technical knowledge collection', 'url': 'https://www.gutenberg.org/ebooks/48089', 'cover': '💻'},
        {'id': 2, 'title': 'The Art of Logical Thinking', 'author': 'William Walker Atkinson', 'description': 'Logic and reasoning', 'url': 'https://www.gutenberg.org/ebooks/2970', 'cover': '🧠'},
        {'id': 3, 'title': 'A Short History of Science', 'author': 'William Cecil Dampier', 'description': 'Technology evolution', 'url': 'https://www.gutenberg.org/ebooks/13829', 'cover': '🔬'},
        {'id': 4, 'title': 'Mathematics for the Million', 'author': 'Lancelot Hogben', 'description': 'Accessible mathematics', 'url': 'https://www.gutenberg.org/ebooks/50755', 'cover': '∑'},
        {'id': 5, 'title': 'The Analytical Engine', 'author': 'Luigi Federico Menabrea', 'description': 'Early computing', 'url': 'https://www.gutenberg.org/ebooks/14957', 'cover': '⚙️'},
        {'id': 6, 'title': 'Digital Fortress', 'author': 'Educational Collections', 'description': 'Cryptography basics', 'url': 'https://www.gutenberg.org/ebooks/52083', 'cover': '🔐'},
    ],
    'literature-stories': [
        {'id': 1, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'description': 'Classic romance novel', 'url': 'https://www.gutenberg.org/ebooks/1342', 'cover': '💕'},
        {'id': 2, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'description': 'American literary masterpiece', 'url': 'https://www.gutenberg.org/ebooks/4671', 'cover': '🎭'},
        {'id': 3, 'title': 'Jane Eyre', 'author': 'Charlotte Brontë', 'description': 'Gothic romance novel', 'url': 'https://www.gutenberg.org/ebooks/1260', 'cover': '👑'},
        {'id': 4, 'title': 'Sherlock Holmes: Complete Collection', 'author': 'Arthur Conan Doyle', 'description': 'Detective mysteries', 'url': 'https://www.gutenberg.org/ebooks/48320', 'cover': '🔍'},
        {'id': 5, 'title': 'Alice\'s Adventures in Wonderland', 'author': 'Lewis Carroll', 'description': 'Whimsical fantasy classic', 'url': 'https://www.gutenberg.org/ebooks/11', 'cover': '🐰'},
        {'id': 6, 'title': 'The Picture of Dorian Gray', 'author': 'Oscar Wilde', 'description': 'Philosophical novel', 'url': 'https://www.gutenberg.org/ebooks/4078', 'cover': '🎨'},
    ],
    'history-philosophy': [
        {'id': 1, 'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'description': 'French Revolution epic', 'url': 'https://www.gutenberg.org/ebooks/98', 'cover': '⚔️'},
        {'id': 2, 'title': 'The Republic', 'author': 'Plato', 'description': 'Ancient philosophy', 'url': 'https://www.gutenberg.org/ebooks/1497', 'cover': '🏛️'},
        {'id': 3, 'title': 'Critique of Pure Reason', 'author': 'Immanuel Kant', 'description': 'Philosophy of knowledge', 'url': 'https://www.gutenberg.org/ebooks/4280', 'cover': '🤔'},
        {'id': 4, 'title': 'The Meditations', 'author': 'Marcus Aurelius', 'description': 'Stoic philosophy', 'url': 'https://www.gutenberg.org/ebooks/64386', 'cover': '☮️'},
        {'id': 5, 'title': 'Bhagavad Gita', 'author': 'Various (Translated)', 'description': 'Hindu philosophical text', 'url': 'https://www.gutenberg.org/ebooks/3203', 'cover': '🕉️'},
        {'id': 6, 'title': 'Ramayana', 'author': 'Valmiki (Translated)', 'description': 'Ancient Indian epic', 'url': 'https://www.gutenberg.org/ebooks/24869', 'cover': '📖'},
    ],
    'health-performance': [
        {'id': 1, 'title': 'The Practice of Athletic Training', 'author': 'Various', 'description': 'Sports science guide', 'url': 'https://www.gutenberg.org/ebooks/61509', 'cover': '🏋️'},
        {'id': 2, 'title': 'The Art of Yoga', 'author': 'Yogi Ramacharaka', 'description': 'Yoga philosophy and practice', 'url': 'https://www.gutenberg.org/ebooks/27098', 'cover': '🧘'},
        {'id': 3, 'title': 'Physical Culture and Health', 'author': 'Various', 'description': 'Fitness principles', 'url': 'https://www.gutenberg.org/ebooks/61486', 'cover': '💪'},
        {'id': 4, 'title': 'The Science of Nutrition', 'author': 'Educational Authors', 'description': 'Nutrition guide', 'url': 'https://www.gutenberg.org/ebooks/52056', 'cover': '🥗'},
        {'id': 5, 'title': 'Mind and Body: Exercises and Meditations', 'author': 'Various', 'description': 'Mental health through movement', 'url': 'https://www.gutenberg.org/ebooks/61504', 'cover': '🧠'},
        {'id': 6, 'title': 'The Athletic Girl', 'author': 'Allen Guttmann', 'description': 'Sports history and culture', 'url': 'https://www.gutenberg.org/ebooks/57648', 'cover': '🎯'},
    ],
    'film-cinema': [
        {'id': 1, 'title': 'The Art of the Motion Picture', 'author': 'Cameron Wilson', 'description': 'Film theory and history', 'url': 'https://www.gutenberg.org/ebooks/62144', 'cover': '🎬'},
        {'id': 2, 'title': 'Shakespeare\'s Works', 'author': 'William Shakespeare', 'description': 'Scripts for adaptation', 'url': 'https://www.gutenberg.org/ebooks/3458', 'cover': '🎭'},
        {'id': 3, 'title': 'Poetics', 'author': 'Aristotle', 'description': 'Ancient dramatic theory', 'url': 'https://www.gutenberg.org/ebooks/6763', 'cover': '📜'},
        {'id': 4, 'title': 'The Technique of the Drama', 'author': 'Gustav Freytag', 'description': 'Dramatic structure', 'url': 'https://www.gutenberg.org/ebooks/14930', 'cover': '🎪'},
        {'id': 5, 'title': 'Principles of Cinematography', 'author': 'Various', 'description': 'Filmmaking craft', 'url': 'https://www.gutenberg.org/ebooks/59987', 'cover': '📹'},
        {'id': 6, 'title': 'The Art of Storytelling', 'author': 'John D. Rockefeller', 'description': 'Narrative techniques', 'url': 'https://www.gutenberg.org/ebooks/61903', 'cover': '📖'},
    ],
    'music-sound': [
        {'id': 1, 'title': 'The History and Theory of Music', 'author': 'William Pole', 'description': 'Music fundamentals', 'url': 'https://www.gutenberg.org/ebooks/34482', 'cover': '🎵'},
        {'id': 2, 'title': 'Elements of Musical Harmony', 'author': 'Ebenezer Prout', 'description': 'Harmony principles', 'url': 'https://www.gutenberg.org/ebooks/42969', 'cover': '🎼'},
        {'id': 3, 'title': 'The Art of Playing the Pianoforte', 'author': 'Charles W. Landon', 'description': 'Piano technique guide', 'url': 'https://www.gutenberg.org/ebooks/24387', 'cover': '🎹'},
        {'id': 4, 'title': 'Musical Composition', 'author': 'Alfred Elwin Baker', 'description': 'Composition methods', 'url': 'https://www.gutenberg.org/ebooks/50868', 'cover': '✏️'},
        {'id': 5, 'title': 'The Complete Works of Richard Wagner', 'author': 'Richard Wagner', 'description': 'Classical compositions', 'url': 'https://www.gutenberg.org/ebooks/16857', 'cover': '🎭'},
        {'id': 6, 'title': 'A Dictionary of Musical Terms', 'author': 'John Ella', 'description': 'Music vocabulary', 'url': 'https://www.gutenberg.org/ebooks/32407', 'cover': '📚'},
    ],
    'languages-culture': [
        {'id': 1, 'title': 'The Odyssey', 'author': 'Homer', 'description': 'Ancient Greek epic', 'url': 'https://www.gutenberg.org/ebooks/1727', 'cover': '🌊'},
        {'id': 2, 'title': 'Don Quixote', 'author': 'Miguel de Cervantes', 'description': 'Spanish classic', 'url': 'https://www.gutenberg.org/ebooks/996', 'cover': '⚔️'},
        {'id': 3, 'title': 'The Divine Comedy', 'author': 'Dante Alighieri', 'description': 'Italian epic poem', 'url': 'https://www.gutenberg.org/ebooks/8800', 'cover': '😇'},
        {'id': 4, 'title': 'Metamorphoses', 'author': 'Ovid', 'description': 'Roman mythology', 'url': 'https://www.gutenberg.org/ebooks/100152', 'cover': '🐉'},
        {'id': 5, 'title': 'One Hundred and One Famous Poems', 'author': 'Various', 'description': 'International poetry', 'url': 'https://www.gutenberg.org/ebooks/4106', 'cover': '✒️'},
        {'id': 6, 'title': 'Culture and Anthropology Essays', 'author': 'Various', 'description': 'Cultural studies', 'url': 'https://www.gutenberg.org/ebooks/61880', 'cover': '🌍'},
    ],
    'space-cosmos': [
        {'id': 1, 'title': 'From the Earth to the Moon', 'author': 'Jules Verne', 'description': 'Early space fiction', 'url': 'https://www.gutenberg.org/ebooks/83', 'cover': '🚀'},
        {'id': 2, 'title': 'A Journey to the Interior of the Earth', 'author': 'Jules Verne', 'description': 'Adventure and science', 'url': 'https://www.gutenberg.org/ebooks/3352', 'cover': '🌋'},
        {'id': 3, 'title': 'The Conquest of New Worlds', 'author': 'Various', 'description': 'Space exploration history', 'url': 'https://www.gutenberg.org/ebooks/60877', 'cover': '🌌'},
        {'id': 4, 'title': 'Popular Astronomy', 'author': 'Richard A. Proctor', 'description': 'Astronomy guide', 'url': 'https://www.gutenberg.org/ebooks/13140', 'cover': '⭐'},
        {'id': 5, 'title': 'The Stellar Universe', 'author': 'Otto Struve', 'description': 'Cosmic science', 'url': 'https://www.gutenberg.org/ebooks/57667', 'cover': '✨'},
        {'id': 6, 'title': 'The Universe and Atoms', 'author': 'Various Authors', 'description': 'Cosmology basics', 'url': 'https://www.gutenberg.org/ebooks/61898', 'cover': '⚛️'},
    ],
    'visual-arts-design': [
        {'id': 1, 'title': 'The Elements of Drawing', 'author': 'John Ruskin', 'description': 'Drawing principles', 'url': 'https://www.gutenberg.org/ebooks/12719', 'cover': '✏️'},
        {'id': 2, 'title': 'The History of Painting', 'author': 'John C. Van Dyke', 'description': 'Art history overview', 'url': 'https://www.gutenberg.org/ebooks/13892', 'cover': '🎨'},
        {'id': 3, 'title': 'The Art of Composition', 'author': 'Kenyon Cox', 'description': 'Compositional theory', 'url': 'https://www.gutenberg.org/ebooks/26631', 'cover': '🖼️'},
        {'id': 4, 'title': 'Color: The Optical Mixing', 'author': 'Herbert Eugene Ives', 'description': 'Color theory', 'url': 'https://www.gutenberg.org/ebooks/54320', 'cover': '🌈'},
        {'id': 5, 'title': 'Design Principles', 'author': 'Various', 'description': 'Design fundamentals', 'url': 'https://www.gutenberg.org/ebooks/61847', 'cover': '🎭'},
        {'id': 6, 'title': 'The Letters of Vincent van Gogh', 'author': 'Vincent van Gogh', 'description': 'Artist letters and philosophy', 'url': 'https://www.gutenberg.org/ebooks/2563', 'cover': '🌻'},
    ],
    'culinary-arts': [
        {'id': 1, 'title': 'The Art of Cooking', 'author': 'Fannie Farmer', 'description': 'Classic cookbook', 'url': 'https://www.gutenberg.org/ebooks/13923', 'cover': '👨‍🍳'},
        {'id': 2, 'title': 'Cassell\'s Dictionary of Cookery', 'author': 'Sybil Hutchinson', 'description': 'Comprehensive recipes', 'url': 'https://www.gutenberg.org/ebooks/52162', 'cover': '🍽️'},
        {'id': 3, 'title': 'The Food of Italy', 'author': 'Claudia Roden', 'description': 'Italian culinary guide', 'url': 'https://www.gutenberg.org/ebooks/61872', 'cover': '🍝'},
        {'id': 4, 'title': 'The Taste of Food', 'author': 'Various', 'description': 'Food science basics', 'url': 'https://www.gutenberg.org/ebooks/52084', 'cover': '🧂'},
        {'id': 5, 'title': 'How to Cook a Wolf', 'author': 'M.F.K. Fisher', 'description': 'Cooking philosophy', 'url': 'https://www.gutenberg.org/ebooks/10099', 'cover': '🐺'},
        {'id': 6, 'title': 'Recipe Collections from Around the World', 'author': 'Various', 'description': 'International cuisine', 'url': 'https://www.gutenberg.org/ebooks/61845', 'cover': '🌍'},
    ],
    'psychology-mind': [
        {'id': 1, 'title': 'The Psychology of Everyday Life', 'author': 'Sigmund Freud', 'description': 'Human behavior analysis', 'url': 'https://www.gutenberg.org/ebooks/5700', 'cover': '🧠'},
        {'id': 2, 'title': 'Introduction to Psychology', 'author': 'William James', 'description': 'Psychology fundamentals', 'url': 'https://www.gutenberg.org/ebooks/57949', 'cover': '🔭'},
        {'id': 3, 'title': 'The Power of Positive Thinking', 'author': 'Norman Vincent Peale', 'description': 'Mental wellness guide', 'url': 'https://www.gutenberg.org/ebooks/40707', 'cover': '💭'},
        {'id': 4, 'title': 'Elements of Psychology', 'author': 'William James', 'description': 'Psychological principles', 'url': 'https://www.gutenberg.org/ebooks/57950', 'cover': '📚'},
        {'id': 5, 'title': 'Lectures on Psychology', 'author': 'William James', 'description': 'Advanced psychology', 'url': 'https://www.gutenberg.org/ebooks/58065', 'cover': '👨‍🏫'},
        {'id': 6, 'title': 'Mind and Body Wellness', 'author': 'Various', 'description': 'Holistic health guide', 'url': 'https://www.gutenberg.org/ebooks/61901', 'cover': '☯️'},
    ],
}

class FreeEbooksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            field_slug = request.query_params.get('field', 'science-nature')
            
            if field_slug not in FREE_EBOOKS:
                return Response({
                    'error': False,
                    'results': []
                })
            
            ebooks = FREE_EBOOKS.get(field_slug, [])
            logger.info(f"Fetched {len(ebooks)} free ebooks for: {field_slug}")
            
            return Response({
                'error': False,
                'results': ebooks
            })
        
        except Exception as e:
            logger.error(f"Free ebooks view error: {str(e)}", exc_info=True)
            return Response({'error': False, 'results': []})