# 🚀 Deployment-Anleitung - Light-Autom8 Vector Store

## Option 1: Render.com (Empfohlen)

### Schritt 1: GitHub Repository erstellen
```bash
# Git Repository initialisieren (falls noch nicht geschehen)
git init
git add .
git commit -m "Initial commit for deployment"

# GitHub Repository erstellen und pushen
git remote add origin https://github.com/[DEIN-USERNAME]/light-autom8-vector-store.git
git push -u origin main
```

### Schritt 2: Render.com Setup
1. Gehe zu [render.com](https://render.com)
2. Erstelle einen kostenlosen Account
3. Klicke "New +" → "Web Service"
4. Verbinde dein GitHub Repository
5. Wähle "light-autom8-vector-store" aus

### Schritt 3: Konfiguration
- **Name**: `light-autom8-vector-store`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### Schritt 4: Umgebungsvariablen setzen
In Render Dashboard → Environment:
```
OPENAI_API_KEY=dein_openai_api_key
GEMINI_API_KEY=dein_gemini_api_key
FLASK_ENV=production
```

### Schritt 5: Deploy!
- Klicke "Create Web Service"
- Warte 2-3 Minuten
- Deine App ist live! 🎉

---

## Option 2: Heroku (Alternative)

### Schritt 1: Heroku CLI installieren
```bash
# macOS
brew install heroku/brew/heroku

# Oder Download von https://devcenter.heroku.com/articles/heroku-cli
```

### Schritt 2: Heroku App erstellen
```bash
heroku login
heroku create light-autom8-vector-store
```

### Schritt 3: Umgebungsvariablen setzen
```bash
heroku config:set OPENAI_API_KEY=dein_openai_api_key
heroku config:set GEMINI_API_KEY=dein_gemini_api_key
heroku config:set FLASK_ENV=production
```

### Schritt 4: Deploy
```bash
git push heroku main
```

---

## Option 3: Netlify + Serverless (Für Frontend)

Falls du nur das Frontend deployen möchtest:

1. Gehe zu [netlify.com](https://netlify.com)
2. Drag & Drop deinen `templates/` Ordner
3. Oder verbinde GitHub Repository
4. Setze Build Command: `python -m http.server 8000`

---

## 🔧 Lokale Entwicklung

```bash
# Dependencies installieren
pip install -r requirements.txt

# Lokal starten
python app.py

# Oder mit npm
npm run start
```

## 📝 Wichtige Hinweise

- **API Keys**: Niemals in Git committen!
- **Production**: Debug-Modus ist automatisch deaktiviert
- **HTTPS**: Alle Plattformen bieten automatisches HTTPS
- **Skalierung**: Render und Heroku skalieren automatisch

## 🆘 Troubleshooting

### Port-Problem
```python
# In app.py ist bereits konfiguriert:
port = int(os.environ.get('PORT', 8000))
```

### Dependencies-Problem
```bash
# Stelle sicher, dass alle Pakete in requirements.txt stehen
pip freeze > requirements.txt
```

### Umgebungsvariablen-Problem
- Prüfe, ob alle API Keys korrekt gesetzt sind
- Verwende die .env-Datei nur lokal, nicht in Production
