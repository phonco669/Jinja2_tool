from flask import Flask, render_template, request, jsonify
from jinja2 import Template, TemplateSyntaxError
import json
import webbrowser
from threading import Timer

app = Flask(__name__)

# 固定主题色系定义
THEME_VARIANTS = {
    'info': {
        'bg': '#e6f4ff',
        'border': '#1677ff',
        'title': '#0958d9',
        'text': '#595959',
        'icon': 'ℹ️',
    },
    'success': {
        'bg': '#f6ffed',
        'border': '#52c41a',
        'title': '#237804',
        'text': '#595959',
        'icon': '✅',
    },
    'warning': {
        'bg': '#fffbe6',
        'border': '#faad14',
        'title': '#d46b08',
        'text': '#595959',
        'icon': '⚠️',
    },
    'error': {
        'bg': '#fff1f0',
        'border': '#ff4d4f',
        'title': '#a8071a',
        'text': '#595959',
        'icon': '⛔',
    },
    'clear': {
        'bg': '#ffffff',
        'border': '#d9d9d9',
        'title': '#262626',
        'text': '#595959',
        'icon': '🧹',
    },
}

def apply_theme_to_template(template_code: str, theme: dict) -> str:
    """
    将用户模板中的常见内联颜色替换为选中主题的颜色值。

    参数:
        template_code: 模板源码字符串
        theme: 选中主题字典，包含 bg/border/title/text/icon

    返回:
        替换后的模板字符串
    """
    try:
        code = template_code
        code = code.replace('border-left:4px solid #faad14', f"border-left:4px solid {theme['border']}")
        code = code.replace('background:#fffbe6', f"background:{theme['bg']}")
        code = code.replace('color:#d46b08', f"color:{theme['title']}")
        code = code.replace('color:#595959', f"color:{theme['text']}")
        code = code.replace('⚠️', theme.get('icon', ''))
        return code
    except Exception:
        return template_code

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
    variant = data.get('variant', 'info')
    apply_adapter = bool(data.get('applyAdapter', False))
    
    context = {}
    if context_str.strip():
        try:
            context = json.loads(context_str)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'JSON Context Error: {str(e)}'}), 400

    # 选中主题并注入上下文
    theme = THEME_VARIANTS.get(variant, THEME_VARIANTS['info'])
    context['theme'] = theme

    # 可选适配器：将常见内联样式替换为当前主题值
    if apply_adapter:
        template_code = apply_theme_to_template(template_code, theme)

    try:
        template = Template(template_code)
        rendered_html = template.render(**context)
        return jsonify({'result': rendered_html})
    except TemplateSyntaxError as e:
        return jsonify({'error': f'Jinja2 Syntax Error: Line {e.lineno}: {e.message}'}), 400
    except Exception as e:
        return jsonify({'error': f'Render Error: {str(e)}'}), 500

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000)
