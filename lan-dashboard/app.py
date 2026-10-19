import socket
import speedtest
import requests
import subprocess
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_gateway():
    try:
        res = subprocess.check_output(['ip', 'route'], stderr=subprocess.STDOUT).decode()
        for line in res.split('\n'):
            if 'default via' in line:
                return line.split()[2]
    except:
        return "Não disponível"

def get_dns():
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    return line.split()[1]
    except:
        return "Não disponível"

def get_mac():
    try:
        res = subprocess.check_output(['cat', '/sys/class/net/wlan0/address'], stderr=subprocess.STDOUT).decode()
        return res.strip()
    except:
        return "Não disponível"

def get_network_info():
    try:
        hostname = socket.gethostname()
    except:
        hostname = "Desconhecido"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "Não disponível"
    
    # Upgrade: Usando ip-api.com para pegar IP + Geo
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            public_ip = data['query']
            geo = {
                "country": data.get('country', 'N/A'),
                "city": data.get('city', 'N/A'),
                "isp": data.get('isp', 'N/A'),
                "lat": data.get('lat', 'N/A'),
                "lon": data.get('lon', 'N/A')
            }
        else:
            public_ip = "Não disponível"
            geo = {}
    except:
        public_ip = "Não disponível"
        geo = {}

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "public_ip": public_ip,
        "gateway": get_gateway(),
        "dns": get_dns(),
        "mac": get_mac(),
        "geo": geo
    }

def check_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        return {
            "download": round(st.download() / 1_000_000, 2),
            "upload": round(st.upload() / 1_000_000, 2),
            "ping": round(st.results.ping, 2)
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/stats')
def stats():
    info = get_network_info()
    speed = check_speed()
    return jsonify({"network": info, "speed": speed})

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LAN-Dashboard Pro</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0f172a">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
        .neon-text { text-shadow: 0 0 10px rgba(34, 211, 238, 0.8); }
        .loader { border-top-color: #22d3ee; animation: spinner 1.5s linear infinite; }
        @keyframes spinner { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <header class="flex justify-between items-center mb-8">
            <div class="flex items-center gap-3">
                <div class="p-2 bg-cyan-500 rounded-lg shadow-[0_0_15px_rgba(34,211,238,0.5)]">
                    <i class="fas fa-satellite-dish text-slate-900 text-xl"></i>
                </div>
                <div>
                    <h1 class="text-3xl font-bold text-cyan-400 neon-text">LAN-DASHBOARD <span class="text-xs bg-cyan-500 text-slate-900 px-2 py-0.5 rounded-full ml-2">PRO</span></h1>
                    <p class="text-slate-400 text-sm">Advanced System Recon & Network Intelligence</p>
                </div>
            </div>
            <button onclick="fetchData()" class="glass p-3 rounded-full hover:bg-cyan-500/20 transition-all active:scale-90">
                <i class="fas fa-sync-alt" id="refresh-icon"></i>
            </button>
        </header>

        <div id="loading" class="flex flex-col items-center justify-center py-20">
            <div class="loader w-12 h-12 border-4 border-slate-700 rounded-full mb-4"></div>
            <p class="text-slate-400 animate-pulse">Sincronizando com o hardware e satélites...</p>
        </div>

        <div id="content" class="hidden grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Network Card -->
            <div class="glass p-6 rounded-2xl">
                <div class="flex items-center mb-4 text-cyan-400">
                    <i class="fas fa-network-wired mr-2"></i>
                    <h2 class="text-xl font-semibold">Identificação</h2>
                </div>
                <div class="space-y-4">
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">Hostname</span>
                        <span id="hostname" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">IP Local</span>
                        <span id="local_ip" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">IP Público</span>
                        <span id="public_ip" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">Gateway</span>
                        <span id="gateway" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">DNS</span>
                        <span id="dns" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">MAC Address</span>
                        <span id="mac" class="font-mono text-white">-</span>
                    </div>
                </div>
            </div>

            <!-- Geo Card -->
            <div class="glass p-6 rounded-2xl">
                <div class="flex items-center mb-4 text-purple-400">
                    <i class="fas fa-globe-americas mr-2"></i>
                    <h2 class="text-xl font-semibold">Geolocalização</h2>
                </div>
                <div class="space-y-4">
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">País</span>
                        <span id="geo_country" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">Cidade</span>
                        <span id="geo_city" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">ISP</span>
                        <span id="geo_isp" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700 pb-2">
                        <span class="text-slate-400">Latitude</span>
                        <span id="geo_lat" class="font-mono text-white">-</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">Longitude</span>
                        <span id="geo_lon" class="font-mono text-white">-</span>
                    </div>
                </div>
            </div>

            <!-- Speed Card -->
            <div class="glass p-6 rounded-2xl">
                <div class="flex items-center mb-4 text-emerald-400">
                    <i class="fas fa-tachometer-alt mr-2"></i>
                    <h2 class="text-xl font-semibold">Performance</h2>
                </div>
                <div class="grid grid-cols-1 gap-4">
                    <div class="bg-slate-800/50 p-4 rounded-xl text-center border border-slate-700">
                        <p class="text-slate-400 text-xs uppercase mb-1">Download</p>
                        <p class="text-3xl font-bold text-emerald-400"><span id="download">-</span> <small class="text-sm">Mbps</small></p>
                    </div>
                    <div class="bg-slate-800/50 p-4 rounded-xl text-center border border-slate-700">
                        <p class="text-slate-400 text-xs uppercase mb-1">Upload</p>
                        <p class="text-3xl font-bold text-emerald-400"><span id="upload">-</span> <small class="text-sm">Mbps</small></p>
                    </div>
                    <div class="bg-slate-800/50 p-4 rounded-xl text-center border border-slate-700">
                        <p class="text-slate-400 text-xs uppercase mb-1">Ping</p>
                        <p class="text-3xl font-bold text-emerald-400"><span id="ping">-</span> <small class="text-sm">ms</small></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function fetchData() {
            const icon = document.getElementById('refresh-icon');
            const loading = document.getElementById('loading');
            const content = document.getElementById('content');
            
            icon.classList.add('fa-spin');
            loading.classList.remove('hidden');
            content.classList.add('hidden');

            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                // Network
                document.getElementById('hostname').innerText = data.network.hostname;
                document.getElementById('local_ip').innerText = data.network.local_ip;
                document.getElementById('public_ip').innerText = data.network.public_ip;
                document.getElementById('gateway').innerText = data.network.gateway;
                document.getElementById('dns').innerText = data.network.dns;
                document.getElementById('mac').innerText = data.network.mac;

                // Geo
                const geo = data.network.geo || {};
                document.getElementById('geo_country').innerText = geo.country || 'N/A';
                document.getElementById('geo_city').innerText = geo.city || 'N/A';
                document.getElementById('geo_isp').innerText = geo.isp || 'N/A';
                document.getElementById('geo_lat').innerText = geo.lat || 'N/A';
                document.getElementById('geo_lon').innerText = geo.lon || 'N/A';

                // Speed
                if (data.speed.error) {
                    document.getElementById('download').innerText = 'ERR';
                    document.getElementById('upload').innerText = 'ERR';
                    document.getElementById('ping').innerText = 'ERR';
                } else {
                    document.getElementById('download').innerText = data.speed.download;
                    document.getElementById('upload').innerText = data.speed.upload;
                    document.getElementById('ping').innerText = data.speed.ping;
                }

                loading.classList.add('hidden');
                content.classList.remove('hidden');
            } catch (e) {
                alert("Erro ao buscar dados do servidor!");
            } finally {
                icon.classList.remove('fa-spin');
            }
        }

        window.onload = fetchData;
    </script>
</body>
</html>
'''

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "LAN-Dashboard Pro",
        "short_name": "LAN-Dash Pro",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#0f172a",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/2885/2885417.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
