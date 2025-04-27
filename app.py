from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir acesso da página HTML (diferente porta)

DATABASE = 'survey.db'

def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/', methods=['GET'])
def index():
    return "🚀 Servidor rodando com sucesso! Backend online!"

@app.route('/submit', methods=['POST'])
def submit_survey():
    data = request.json
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO survey_responses (industry, company_time, knowledge_level, products, needs_help, full_name, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['industry'],
            data['company_time'],
            data['knowledge_level'],
            data['products'],
            data['needs_help'],
            data['full_name'],
            data['email']
        ))
        conn.commit()
        return jsonify({'message': 'Resposta salva com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
