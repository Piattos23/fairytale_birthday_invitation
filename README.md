# Fairytale Birthday Invitation

A responsive, fairytale-inspired birthday invitation built with Flask, SQLite/PostgreSQL, HTML, CSS and vanilla JavaScript.

## Project structure

```text
fairytale_birthday_invitation/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
├── rsvp.db                 # created automatically when using SQLite
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── admin.html
└── static/
    ├── style.css
    └── script.js
```

## Run locally (PyCharm / Windows)

1. Open this folder in PyCharm.
2. Create and activate a virtual environment.
3. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

4. Optional but recommended: set your local secrets in PowerShell:

   ```powershell
   $env:SECRET_KEY="a-long-random-secret-value"
   $env:ADMIN_PASSWORD="choose-a-strong-password"
   ```

5. Run `app.py` in PyCharm, or:

   ```powershell
   python app.py
   ```

6. Open `http://127.0.0.1:5000`.

Admin page: `http://127.0.0.1:5000/admin`

## Customize the party details

Edit the `PARTY` dictionary near the top of `app.py`:

- `host`
- `age`
- `date`
- `time`
- `place`
- `dress_code`
- `message`
- `rsvp_by`

## Admin login

Default local admin password is `admin123` if `ADMIN_PASSWORD` is not set. Change it before sharing or deploying the site.

## Database and deployment

- Without `DATABASE_URL`, the app uses a local SQLite database (`rsvp.db`).
- With `DATABASE_URL`, the app uses PostgreSQL via psycopg.
- Existing SQLite and PostgreSQL `responses` table layouts are retained.
- `Procfile` is provided for platforms that use it.
- `render.yaml` is an optional Render blueprint for a web service and PostgreSQL database.

For production, set a strong `SECRET_KEY`, set a strong `ADMIN_PASSWORD`, set `FLASK_DEBUG=0`, and use HTTPS. Do not commit secrets or a production database file to GitHub.

## Effects included

- Click-to-open invitation envelope
- Mouse-following sparkles and ambient twinkles
- Floating hearts and floral symbols
- Confetti burst when a guest chooses “Yes”
- Gentle 3D card tilt on desktop
- Responsive layout and reduced-motion accessibility support

Google Fonts are loaded from Google Fonts; the page falls back to local system fonts if unavailable.
