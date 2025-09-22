#!/bin/bash

# Light-Autom8 Private Deployment Script
echo "🚀 Light-Autom8 Private Deployment gestartet..."

# Prüfe ob Repository-URL angegeben wurde
if [ -z "$1" ]; then
    echo "❌ Fehler: Repository-URL erforderlich"
    echo "Verwendung: ./deploy-private.sh https://github.com/alstra11/light-autom8-private.git"
    exit 1
fi

REPO_URL=$1
echo "📦 Repository: $REPO_URL"

# Git Remote hinzufügen
echo "🔗 Private Repository als Remote hinzufügen..."
git remote add private $REPO_URL

# Alle Änderungen committen
echo "💾 Änderungen committen..."
git add .
git commit -m "CP-004: Private Deployment vorbereitet

- render-private.yaml Konfiguration erstellt
- README.md für privates Deployment aktualisiert
- Deployment-Skript hinzugefügt
- Sichere API Key Verwaltung implementiert"

# Code zum privaten Repository pushen
echo "📤 Code zum privaten Repository pushen..."
git push private main

echo "✅ Private Repository erfolgreich erstellt und konfiguriert!"
echo ""
echo "🎯 Nächste Schritte für Render.com Deployment:"
echo "1. Gehen Sie zu https://dashboard.render.com"
echo "2. Klicken Sie 'New +' → 'Web Service'"
echo "3. Verbinden Sie das private Repository: $REPO_URL"
echo "4. Konfiguration:"
echo "   - Name: light-autom8-private"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python app.py"
echo "5. Umgebungsvariablen setzen:"
echo "   - OPENAI_API_KEY=your_key"
echo "   - GEMINI_API_KEY=your_key"
echo "   - FLASK_ENV=production"
echo ""
echo "🔒 Ihr privates Deployment ist bereit!"
