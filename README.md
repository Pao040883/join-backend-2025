📌 join-backend-2025
Ein Django-Backend für die join-Webanwendung mit Django REST Framework (DRF) und SQLite.

🚀 Über das Projekt
Das join-backend-2025 ist die Backend-API für die join-Webanwendung. Es verwaltet Benutzer, Daten und API-Endpunkte mit Django REST Framework (DRF).

🛠 Technologien & Tools
Backend: Django 4.x, Django REST Framework (DRF)
Datenbank: SQLite
Authentifizierung: DRF Token Authentication
Dokumentation: DRF Browsable API

📂 Projektstruktur
join-backend-2025/
│── backend_join/         # Django-Projektkonfiguration
│   │── __init__.py
│   │── asgi.py
│   │── settings.py
│   │── urls.py
│   │── wsgi.py
│── env/                  # Virtuelle Umgebung (nicht im Repository)
│── join_app/             # Haupt-App
│   │── api/              # API-Module
│   │   │── serializers.py
│   │   │── urls.py
│   │   │── views.py
│   │── migrations/       # Datenbank-Migrationen
│   │── __init__.py
│   │── admin.py
│   │── apps.py
│   │── models.py
│   │── tests.py
│   │── views.py
│── db.sqlite3            # SQLite-Datenbank
│── manage.py             # Django-Befehle
│── README.md             # Diese Datei
│── requirements.txt      # Abhängigkeiten

🔧 Installation & Setup
1️⃣ Projekt klonen
git clone https://github.com/dein-github-username/join-backend-2025.git
cd join-backend-2025

2️⃣ Virtuelle Umgebung erstellen & aktivieren
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate      # Windows

3️⃣ Abhängigkeiten installieren
pip install -r requirements.txt

4️⃣ Datenbank migrieren
python manage.py migrate

5️⃣ Superuser erstellen (optional, für Admin-Zugang)
python manage.py createsuperuser

6️⃣ Server starten
python manage.py runserver
Die API ist jetzt unter http://127.0.0.1:8000/ erreichbar.

🔑 Authentifizierung (DRF Token Authentication)
Das Backend nutzt Token-basierte Authentifizierung von Django REST Framework:

Token erstellen (nach erfolgreicher Anmeldung):
POST /api/auth/token/
Body: { "username": "dein-username", "password": "dein-passwort" }

Antwort:
{
  "token": "abcd1234xyz..."
}

Token-geschützte API-Aufrufe:
Jede Anfrage muss den Token im Authorization-Header senden:

Authorization: Token abcd1234xyz...
📌 API-Endpunkte (Beispiele)
Methode	Endpunkt	Beschreibung
POST	/api/auth/register/	Benutzer registrieren
POST	/api/auth/token/	Authentifizierung & Token abrufen
GET	/api/data/	Beispiel-Endpunkt
POST	/api/data/create/	Daten speichern

🔒 Sicherheit
DRF Token-Authentifizierung
CORS-Unterstützung für API-Zugriffe
Django Middleware für zusätzliche Sicherheit
🚀 Deployment
1️⃣ Umgebungsvariablen setzen (.env Datei)
Falls benötigt, erstelle eine .env Datei für Umgebungsvariablen:

SECRET_KEY=dein-geheimer-schlüssel
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

📄 Lizenz
MIT License – Freie Nutzung und Anpassung erlaubt.

🙌 Mitwirken
Pull Requests sind willkommen! Falls du Fragen hast, erstelle ein Issue.