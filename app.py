import os
import tempfile
from flask import Flask, render_template, request, jsonify
from rag_engine import RAGEngine
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Global RAG engine instance
# In a real production app, you might handle this per-session or with a better storage mechanism
rag_engine = RAGEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            status = rag_engine.process_pdf(tmp_path)
            return jsonify({"message": status}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        response, sources = rag_engine.query(question)
        # Prepare source data for frontend
        source_list = [{"content": doc.page_content, "metadata": doc.metadata} for doc in sources]
        return jsonify({
            "response": response,
            "sources": source_list
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
