# Appointment Booking System (Django)

Web aplikacija za upravljanje terminima s tri uloge:
- CLIENT – rezervacija i otkazivanje termina
- STAFF – upravljanje dostupnošću i odobravanje termina
- ADMIN – potpuni uvid i administracija sustava

## Tehnologije
- Python 3.x
- Django
- SQLite
- Bootstrap

## Funkcionalnosti
- Autentikacija i role-based autorizacija
- Generiranje slobodnih termina iz dostupnosti
- Workflow termina (PENDING → APPROVED → DONE)
- Pravilo otkazivanja (24h)
- Django admin panel

## Pokretanje projekta
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
