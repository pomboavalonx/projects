from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import requests
import urllib.parse
import random
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configurações de Caminho
SAVE_PATH = "/data/data/com.termux/files/home/storage/pictures/Polix/"
HISTORY_FILE = os.path.expanduser("~/polix_history.json")

# API Keys e Endpoints
OLLAMA_LOCAL_URL = "http://localhost:11434/api/generate"
OLLAMA_SITE_URL = "https://ollama.com/api/generate" 
OLLAMA_API_KEY = "bc71d4c6cc26495cad706faea2669c8b.JPKG0esSNh3ygYDdMLudjpoh"
OLLAMA_MODEL = "gemma4:cloud"

# Prompt Negativo Padrão
DEFAULT_NEGATIVE_PROMPT = (
    "extra fingers, mutated hands, poorly drawn hands, deformed fingers, "
    "missing fingers, fused fingers, extra limbs, malformed limbs, "
    "missing arms, missing legs, extra arms, extra legs, mutated feet, "
    "poorly drawn feet, long neck, cloned face, gross proportions, "
    "morphed limbs, bad anatomy"
)

# Presets de Estilo
STYLE_PRESETS = {
    "none": "",
    "cyberpunk": "cyberpunk aesthetic, neon lighting, futuristic city, synthwave color palette, high tech, volumetric fog, cinematic lighting, hyper-detailed, 8k, unreal engine 5",
    "photoreal": "photorealistic, raw photo, 8k uhd, fujifilm xt4, depth of field, sharp focus, highly detailed skin pores, natural lighting, cinematic composition, masterpiece, shot on 35mm lens",
    "anime": "anime style, studio ghibli aesthetic, makoto shinkai art, vibrant colors, clean lines, detailed background, cel shaded, high quality anime art, 4k",
    "oil_painting": "oil painting, canvas texture, heavy brushstrokes, classical art, museum quality, rich colors, chiaroscuro lighting, artistic masterpiece",
    "concept_art": "digital illustration, concept art, artstation trending, intricate details, epic composition, sharp edges, smooth gradients, fantasy art, professional color grading"
}

def safe_translate(text: str, target: str = 'en') -> str:
    """Traduz texto de forma resiliente, com User-Agent real e fallback limpo."""
    if not text or not text.strip():
        return ''
    text = text.strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
    }
    # 1. Tentativa via Google Translate endpoint web com User-Agent adequado
    try:
        r = requests.get(
            'https://translate.google.com/m',
            params={'tl': target, 'sl': 'auto', 'q': text},
            headers=headers,
            timeout=8
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            el = soup.find('div', {'class': 'result-container'}) or soup.find('div', {'class': 't0'})
            if el and el.text:
                result_text = el.text.strip()
                if not result_text.startswith('Error ') and "That’s an error" not in result_text:
                    return result_text
    except Exception:
        pass

    # 2. Tentativa via deep_translator
    try:
        translated = GoogleTranslator(source='auto', target=target).translate(text)
        if translated and not translated.startswith('Error ') and "That’s an error" not in translated:
            return translated
    except Exception:
        pass

    # 3. Fallback: retorna o texto original sem quebrar o fluxo
    return text

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [item for item in data if 'Error%20500' not in item.get('url', '') and 'Error 500' not in item.get('url', '')]
        except Exception:
            return []
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(load_history())

@app.route('/clear_history', methods=['POST'])
def clear_history():
    save_history([])
    return jsonify({'message': 'Histórico obliterado com sucesso!'})

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    data = request.get_json(silent=True) or {}
    image_base64 = data.get('image', '')
    engine = data.get('engine', 'local')
    
    if not image_base64:
        return jsonify({'error': 'Nenhuma imagem recebida!'}), 400

    # Limpa prefixo Data URI se presente
    if ',' in image_base64:
        image_base64 = image_base64.split(',', 1)[1]

    try:
        url = OLLAMA_SITE_URL if engine == 'site' else OLLAMA_LOCAL_URL
        headers = {"Authorization": f"Bearer {OLLAMA_API_KEY}"} if engine == 'site' else {}
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": (
                "Analyze this image. Provide a detailed description for an AI image generator. "
                "Format your response exactly like this: PT: [Portuguese Description] | EN: [English Description]. "
                "Be precise and descriptive. No conversational text."
            ),
            "stream": False,
            "images": [image_base64]
        }
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        try:
            result = response.json()
        except Exception:
            return jsonify({'error': f"Resposta inválida do Ollama ({response.status_code}): {response.text[:200]}"}), 502

        if response.status_code != 200 or 'error' in result:
            err_msg = result.get('error', f"HTTP {response.status_code}")
            return jsonify({'error': f"Ollama ({engine}): {err_msg}"}), 502

        full_response = result.get('response', '').strip()
        if not full_response:
            return jsonify({'error': 'Ollama não gerou descrição para a imagem informada.'}), 502

        if "|" in full_response:
            parts = full_response.split("|", 1)
            pt_desc = parts[0].replace("PT:", "").strip()
            en_desc = parts[1].replace("EN:", "").strip()
        else:
            en_desc = full_response
            pt_desc = safe_translate(en_desc, target='pt')

        return jsonify({'prompt': en_desc, 'description_pt': pt_desc})
    except requests.exceptions.Timeout:
        return jsonify({'error': f"Tempo limite excedido ao conectar com Ollama ({engine})."}), 504
    except Exception as e:
        return jsonify({'error': f"Erro no Olho Digital ({engine}): {str(e)}"}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(silent=True) or {}
    prompt_pt = data.get('prompt', '').strip()
    negative_prompt_pt = data.get('negative', '').strip()
    aspect_ratio = data.get('ratio', '1:1')
    style_key = data.get('style', 'none')

    if not prompt_pt:
        return jsonify({'error': 'Por favor, digite um prompt para gerar a imagem!'}), 400

    try:
        # 1. Tradução resiliente do prompt
        prompt_en = safe_translate(prompt_pt, target='en')
        
        # 2. Aplicação de estilo artístico
        style_tokens = STYLE_PRESETS.get(style_key, "")
        if style_tokens:
            prompt_en = f"{prompt_en}, {style_tokens}"

        # 3. Prompt negativo
        if not negative_prompt_pt:
            neg_en = DEFAULT_NEGATIVE_PROMPT
        else:
            neg_en = safe_translate(negative_prompt_pt, target='en')

        # 4. Parâmetros de resolução
        ratio_params = []
        if aspect_ratio == '16:9':
            ratio_params = ['width=1280', 'height=720']
        elif aspect_ratio == '9:16':
            ratio_params = ['width=720', 'height=1280']
        else:
            ratio_params = ['width=1024', 'height=1024']

        # 5. Codificação URL segura com seed aleatório para evitar cache estático
        seed = random.randint(1, 99999999)
        prompt_encoded = urllib.parse.quote(prompt_en.strip(), safe='')
        neg_encoded = urllib.parse.quote(neg_en.strip(), safe='')

        query_parts = [
            f"seed={seed}",
            "nologo=true",
            f"nprop={neg_encoded}"
        ] + ratio_params

        query_string = "&".join(query_parts)
        url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?{query_string}"

        # 6. Salva no histórico
        history = load_history()
        history.append({
            'url': url,
            'prompt': prompt_pt,
            'translated': prompt_en,
            'timestamp': datetime.now().isoformat()
        })
        save_history(history[-50:])

        # 7. Feedback tátil se em ambiente Termux
        try:
            os.system('termux-vibrate -d 150 >/dev/null 2>&1')
        except Exception:
            pass

        return jsonify({'url': url, 'translated': prompt_en, 'prompt': prompt_pt})
    except Exception as e:
        return jsonify({'error': f"Erro ao gerar imagem: {str(e)}"}), 500

@app.route('/save', methods=['POST'])
def save_image():
    data = request.get_json(silent=True) or {}
    image_url = data.get('url', '').strip()
    
    if not image_url or not image_url.startswith('http'):
        return jsonify({'error': 'URL da imagem não fornecida ou inválida!'}), 400

    try:
        # Prepara diretório de salvamento com fallback para pasta local se storage falhar
        save_dir = SAVE_PATH
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception:
            save_dir = os.path.expanduser("~/polix_pictures/")
            os.makedirs(save_dir, exist_ok=True)

        filename = f"polix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        full_path = os.path.join(save_dir, filename)

        response = requests.get(image_url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)

            # Notifica o Android para atualizar a galeria imediatamente
            try:
                os.system(f'termux-media-scan "{full_path}" >/dev/null 2>&1')
            except Exception:
                pass

            return jsonify({'message': f'Imagem salva com sucesso em: {full_path}'})
        else:
            return jsonify({'error': f'Falha ao baixar imagem do motor AI (Código HTTP {response.status_code}).'}), 502
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Tempo limite excedido ao baixar a imagem gerada.'}), 504
    except Exception as e:
        return jsonify({'error': f'Erro ao salvar arquivo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
