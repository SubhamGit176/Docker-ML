from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

LLM_URL = os.environ.get('LLM_URL', 'http://host.docker.internal:8080/v1/chat/completions')
DEFAULT_MODEL = os.environ.get('MODEL', 'gpt-5')
MODEL_OPTIONS = os.environ.get('MODEL_OPTIONS', 'gpt-5,gpt-5-mini,gpt-4o').split(',')
MAX_TOKENS = int(os.environ.get('MAX_TOKENS', '1024'))
KEEP_ALIVE = os.environ.get('KEEP_ALIVE', '30m')


def build_payload(prompt, model, max_tokens):
    return {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'keep_alive': KEEP_ALIVE,
    }


def parse_response(text):
    if not text:
        return ''
    try:
        obj = json.loads(text)
    except Exception:
        return text

    choices = obj.get('choices') or []
    if choices:
        first = choices[0]
        msg = first.get('message')
        if msg and isinstance(msg, dict):
            return msg.get('content', '')
        if 'text' in first:
            return first['text']

    if 'output' in obj:
        return obj['output']

    return json.dumps(obj, indent=2)


@app.route('/config')
def config():
    return jsonify({
        'default_model': DEFAULT_MODEL,
        'model_options': MODEL_OPTIONS,
        'llm_url': LLM_URL,
        'max_tokens': MAX_TOKENS,
        'keep_alive': KEEP_ALIVE,
    })


@app.route('/health', methods=['GET'])
def health():
    llm_url = request.args.get('llm_url', LLM_URL)
    payload = build_payload('ping', DEFAULT_MODEL, 1)
    try:
        resp = requests.post(llm_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=15)
        return jsonify({'status': resp.status_code, 'body': resp.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 502


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400

    model = data.get('model', DEFAULT_MODEL)
    max_tokens = int(data.get('max_tokens', MAX_TOKENS))
    llm_url = data.get('llm_url', LLM_URL)
    extra_headers = data.get('headers', {}) or {}

    payload = build_payload(prompt, model, max_tokens)
    headers = {**extra_headers, 'Content-Type': 'application/json'}

    try:
        resp = requests.post(llm_url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        raw_text = resp.text
        reply = parse_response(raw_text)
        raw = None
        try:
            raw = resp.json()
        except Exception:
            raw = raw_text
        return jsonify({'reply': reply, 'raw': raw, 'model': model, 'llm_url': llm_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 502


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
