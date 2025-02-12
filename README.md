# join-backend-2025
Backend Django


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