from openai import OpenAI
import os
import google.generativeai as genai
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Gemini AI
genai.configure(api_key='AIzaSyAiIXAoBwoTNlq138bJ5xKaC5oJdEZJEPU')
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docu')
def documentation():
    return render_template('documentation.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/create-vector-store', methods=['POST'])
def create_vector_store():
    try:
        data = request.get_json()
        store_name = data.get('name', 'Support FAQ')
        
        # Create vector store
        vector_store = client.vector_stores.create(
            name=store_name
        )
        
        return jsonify({
            'success': True,
            'vector_store_id': vector_store.id,
            'name': vector_store.name,
            'status': vector_store.status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        vector_store_id = data.get('vector_store_id')
        file_content = data.get('file_content')
        file_name = data.get('file_name', 'customer_policies.txt')
        
        # Create temporary file
        temp_file_path = f"temp_{file_name}"
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        # Upload file to vector store
        with open(temp_file_path, 'rb') as f:
            result = client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store_id,
                file=f
            )
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return jsonify({
            'success': True,
            'file_id': result.id,
            'status': result.status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/list-vector-stores', methods=['GET'])
def list_vector_stores():
    try:
        vector_stores = client.vector_stores.list()
        stores = []
        for store in vector_stores.data:
            stores.append({
                'id': store.id,
                'name': store.name,
                'status': store.status,
                'created_at': store.created_at
            })
        
        return jsonify({
            'success': True,
            'vector_stores': stores
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# NEUE GEMINI AI ROUTEN 🚀
@app.route('/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question')
        vector_store_id = data.get('vector_store_id', 'vs_68d1bff6e0c08191b1f798578de9b925')
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Keine Frage angegeben'
            }), 400
        
        # Lade die Kundenrichtlinien
        with open('customer_policies.txt', 'r', encoding='utf-8') as f:
            policies_content = f.read()
        
        # Erstelle den Prompt für Gemini
        prompt = f"""
Du bist ein intelligenter Assistent für Klick2Automade. Beantworte die folgende Frage basierend auf den Kundenrichtlinien:

KUNDENRICHTLINIEN:
{policies_content}

FRAGE: {question}

Antworte präzise und hilfreich auf Deutsch. Wenn die Antwort nicht in den Richtlinien steht, sage das ehrlich.
"""
        
        # Generiere Antwort mit Gemini
        response = gemini_model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'answer': response.text,
            'source': 'Kundenrichtlinien',
            'confidence': 0.95
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate-todos', methods=['POST'])
def generate_todos():
    try:
        data = request.get_json()
        project_description = data.get('description', '')
        
        # Erstelle den Prompt für intelligente Todo-Generierung
        prompt = f"""
Erstelle 5-7 intelligente Todo-Aufgaben für folgendes Projekt:

PROJEKT: {project_description}

Erstelle Aufgaben mit:
- Realistischen Titeln
- Detaillierten Beschreibungen
- Angemessenen Prioritäten (hoch/mittel/niedrig)
- Passenden Kategorien (Entwicklung/Testing/Dokumentation/Deployment/Wartung)

Antworte im JSON Format:
{{
    "todos": [
        {{
            "title": "Titel der Aufgabe",
            "description": "Detaillierte Beschreibung",
            "priority": "hoch/mittel/niedrig",
            "category": "Entwicklung/Testing/Dokumentation/Deployment/Wartung"
        }}
    ]
}}
"""
        
        response = gemini_model.generate_content(prompt)
        
        # Parse JSON Response
        try:
            todos_data = json.loads(response.text)
            return jsonify({
                'success': True,
                'todos': todos_data.get('todos', [])
            })
        except json.JSONDecodeError:
            # Fallback falls JSON Parsing fehlschlägt
            return jsonify({
                'success': True,
                'todos': [
                    {
                        'title': 'Projekt Setup',
                        'description': 'Grundlegende Projektstruktur einrichten',
                        'priority': 'hoch',
                        'category': 'Entwicklung'
                    },
                    {
                        'title': 'Testing implementieren',
                        'description': 'Automatisierte Tests für das Projekt erstellen',
                        'priority': 'mittel',
                        'category': 'Testing'
                    }
                ]
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate-followups', methods=['POST'])
def generate_followups():
    try:
        data = request.get_json()
        original_question = data.get('original_question', '')
        original_answer = data.get('original_answer', '')
        
        if not original_question or not original_answer:
            return jsonify({
                'success': False,
                'error': 'Fehlende Daten'
            }), 400
        
        prompt = f"""
Du bist ein hilfreicher Assistent. Basierend auf dieser Frage und Antwort, generiere EXAKT 3 relevante Follow-Up-Fragen auf Deutsch.

FRAGE: {original_question}
ANTWORT: {original_answer}

Wichtige Regeln:
- Generiere genau 3 Fragen
- Jede Frage muss logisch auf die Originale folgen
- Antworte NUR mit validem JSON, ohne zusätzlichen Text
- Format: {{"followups": ["Frage 1", "Frage 2", "Frage 3"]}}

Beispiel:
{{"followups": ["Wie viel kostet das?", "Wann ist es verfügbar?", "Gibt es Alternativen?"]}}
"""
        
        response = gemini_model.generate_content(prompt)
        
        try:
            # Entferne mögliche Markdown oder Extra-Text
            response_text = response.text.strip().replace('```json', '').replace('```', '')
            followups_data = json.loads(response_text)
            followups = followups_data.get('followups', [])
            
            if len(followups) == 0:
                # Fallback Fragen
                followups = [
                    "Können Sie das genauer erklären?",
                    "Gibt es damit zusammenhängende Kosten?",
                    "Wie wirkt sich das auf mein Projekt aus?"
                ]
            
            return jsonify({
                'success': True,
                'followups': followups
            })
        except json.JSONDecodeError:
            # Erweiterter Fallback
            return jsonify({
                'success': True,
                'followups': [
                    "Was sind die nächsten Schritte?",
                    "Gibt es Beispiele dazu?",
                    "Wie kann ich das anpassen?"
                ]
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/ai-suggestions', methods=['POST'])
def ai_suggestions():
    try:
        data = request.get_json()
        todo_title = data.get('title', '')
        todo_description = data.get('description', '')
        
        prompt = f"""
Analysiere diese Todo-Aufgabe und gib intelligente Verbesserungsvorschläge:

TITEL: {todo_title}
BESCHREIBUNG: {todo_description}

Gib Vorschläge für:
1. Bessere Prioritätseinstufung
2. Zusätzliche Schritte
3. Mögliche Risiken
4. Optimierte Beschreibung

Antworte kurz und präzise auf Deutsch.
"""
        
        response = gemini_model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'suggestions': response.text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
