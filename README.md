# Light-Autom8 Vector Store System

Ein modernes Web-Interface für die Verwaltung von OpenAI Vector Stores, entwickelt für Klick2Automade.

## 🔒 Private Deployment

Dieses Repository ist für privates Deployment konfiguriert und enthält:
- Sichere API Key Verwaltung über Umgebungsvariablen
- Render.com Deployment-Konfiguration
- Private GitHub Repository Integration

## 🌐 Live Demo

**🚀 [https://light-autom8-klick2automade.onrender.com](https://light-autom8-klick2automade.onrender.com)**

Die Anwendung ist live auf Render.com verfügbar und kann sofort getestet werden!

## Features

- 🚀 **Vector Store Management**: Erstellen und verwalten von Vector Stores
- 📁 **Datei-Upload**: Hochladen von Dokumenten in Vector Stores
- 🎨 **Moderne UI**: Responsive, benutzerfreundliche Oberfläche
- 🔧 **REST API**: Flask-basierte Backend-API
- 🌐 **Deutsche Lokalisierung**: Vollständig auf Deutsch

## Installation

1. **Dependencies installieren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Umgebungsvariablen konfigurieren:**
   ```bash
   cp env.example .env
   # Bearbeiten Sie .env und fügen Sie Ihren OpenAI API Key hinzu
   ```

3. **Anwendung starten:**
   ```bash
   python app.py
   ```

4. **Im Browser öffnen:**
   ```
   http://localhost:8000
   ```

## Verwendung

### Vector Store erstellen
1. Geben Sie einen Namen für den Vector Store ein
2. Klicken Sie auf "Vector Store erstellen"
3. Die Vector Store ID wird automatisch für den Datei-Upload verwendet

### Datei hochladen
1. Geben Sie die Vector Store ID ein (oder verwenden Sie die automatisch gefüllte)
2. Wählen Sie einen Dateinamen
3. Fügen Sie den Dateiinhalt ein
4. Klicken Sie auf "Datei hochladen"

### Vector Stores verwalten
- Klicken Sie auf "Vector Stores laden" um alle verfügbaren Vector Stores anzuzeigen
- Informationen zu ID, Name, Status und Erstellungsdatum werden angezeigt

## API Endpoints

- `POST /create-vector-store` - Erstellt einen neuen Vector Store
- `POST /upload-file` - Lädt eine Datei in einen Vector Store hoch
- `GET /list-vector-stores` - Listet alle Vector Stores auf

## 🚀 Deployment

Die Anwendung ist automatisch auf **Render.com** deployed:

- **Live URL**: https://light-autom8-klick2automade.onrender.com
- **Dashboard**: https://dashboard.render.com/web/srv-d38t6sbipnbc738f9img
- **Auto-Deploy**: Aktiviert bei Git Push auf `main` Branch
- **Region**: Frankfurt (EU)
- **Plan**: Free Tier

### Deployment-Konfiguration
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Python Version**: 3.11.0
- **Runtime**: Python

## Technologie-Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Integration**: OpenAI API, Google Gemini AI
- **Styling**: Custom CSS mit modernem Design
- **Deployment**: Render.com mit Gunicorn

## Lizenz

MIT License - Klick2Automade
