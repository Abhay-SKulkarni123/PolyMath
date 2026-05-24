# Polymath 🧠

> Explore Everything. Know Everything.

Polymath is a premium global knowledge marketplace where vendors 
sell physical products, digital downloads, and knowledge experiences 
organized around fields of human curiosity.

## What Makes Polymath Different

- **Knowledge-first** — browse by field of knowledge, not product type
- **Hybrid products** — physical + digital versions of the same product
- **AI Discovery** — conversational assistant connecting books, courses, 
  products, and movies across any knowledge field
- **Entertainment layer** — movie recommendations with streaming links 
  related to any topic you explore

## Knowledge Fields

🔬 Science & Nature · 💻 Technology · 📖 Literature · 🎵 Music  
🎨 Visual Arts · 🍳 Culinary Arts · 🏛️ History · 🧘 Health  
🎬 Film & Cinema · 🌍 Languages · 🔭 Space · 🧠 Psychology

## Tech Stack

**Backend:** Django 6 · DRF · JWT · PostgreSQL · Redis · Celery · Docker  
**Frontend:** Next.js 14 · Tailwind CSS · shadcn/ui · Framer Motion  
**Integrations:** TMDB API · Anthropic API · Resend

## Product Types

| Type | Description |
|------|-------------|
| Physical | Ships to address |
| Digital | Instant download after purchase |
| Experience | Live workshop or mentoring access |

## API Documentation

Run the server and visit `/api/docs/` for full Swagger documentation.

## Local Development

```bash
git clone https://github.com/yourusername/polymath.git
cd polymath
python -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Roadmap

### Backend
- [x] Custom user model with roles
- [x] JWT authentication
- [x] Vendor and customer profiles
- [x] Product catalog with search
- [x] Cart system
- [x] Order system with transaction safety
- [x] Swagger documentation
- [x] Rate limiting and error handling
- [x] Docker setup
- [ ] Knowledge field model
- [ ] Product type system (physical/digital/experience)
- [ ] Digital file delivery
- [ ] TMDB movie integration

### Frontend
- [ ] Landing page
- [ ] Knowledge field browsing
- [ ] Product pages
- [ ] AI Polymath assistant
- [ ] Cart and checkout
- [ ] Digital delivery
- [ ] Order tracking
- [ ] Vendor dashboard
- [ ] Dark/light mode

## Author

Built by Abhay — a production-grade knowledge marketplace