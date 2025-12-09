from flask import Flask, render_template, request, jsonify
from jinja2 import Template, TemplateSyntaxError
import json
import webbrowser
from threading import Timer

app = Flask(__name__)

def open_browser():
    """
    Open the default web browser to the application URL.
    """
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/')
def index():
    """
    Serve the main page.
    """
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render():
    """
    Render the Jinja2 template with the provided context data.
    """
    data = request.json
    template_code = data.get('template', '')
    context_str = data.get('context', '{}')
    
    context = {}
    if context_str.strip():
        try:
            context = json.loads(context_str)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'JSON Context Error: {str(e)}'}), 400

    try:
        template = Template(template_code)
        rendered_html = template.render(**context)
        return jsonify({'result': rendered_html})
    except TemplateSyntaxError as e:
        return jsonify({'error': f'Jinja2 Syntax Error: Line {e.lineno}: {e.message}'}), 400
    except Exception as e:
        return jsonify({'error': f'Render Error: {str(e)}'}), 500

if __name__ == '__main__':
    # Automatically open browser after 1 second
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000)
