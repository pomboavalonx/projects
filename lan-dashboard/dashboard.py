import socket
import speedtest
import requests
import subprocess
import argparse
import os
from datetime import datetime

# --- Configurações de Cores (ANSI) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def get_gateway():
    try:
        # No Android/Termux, 'ip route' é a forma mais confiável
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
        # Tenta pegar o MAC da interface wlan0
        res = subprocess.check_output(['cat', '/sys/class/net/wlan0/address'], stderr=subprocess.STDOUT).decode()
        return res.strip()
    except:
        return "Não disponível"

def get_network_info():
    # Hostname
    try:
        hostname = socket.gethostname()
    except:
        hostname = "Desconhecido"

    # IP Local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "Não disponível"
    
    # IP Público
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
    except:
        public_ip = "Não disponível"

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "public_ip": public_ip,
        "gateway": get_gateway(),
        "dns": get_dns(),
        "mac": get_mac()
    }

def check_speed():
    print(f"\n{Colors.YELLOW}⚡ Medindo velocidade da internet... Isso pode demorar.{Colors.END}")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        return {"download": download, "upload": upload, "ping": ping}
    except Exception as e:
        return {"error": str(e)}

def print_dashboard(info, speed=None):
    print(f"\n{Colors.BOLD}{Colors.CYAN}============================================")
    print(f"   🌐 LAN-DASHBOARD | SYSTEM RECON")
    print(f"============================================{Colors.END}")
    
    print(f"{Colors.GREEN}[+] Identificação{Colors.END}")
    print(f"    Hostname: {Colors.BOLD}{info['hostname']}{Colors.END}")
    print(f"    MAC Addr:  {Colors.BOLD}{info['mac']}{Colors.END}")
    
    print(f"\n{Colors.GREEN}[+] Endereçamento{Colors.END}")
    print(f"    IP Local:  {Colors.BOLD}{info['local_ip']}{Colors.END}")
    print(f"    IP Público: {Colors.BOLD}{info['public_ip']}{Colors.END}")
    print(f"    Gateway:   {Colors.BOLD}{info['gateway']}{Colors.END}")
    print(f"    DNS:       {Colors.BOLD}{info['dns']}{Colors.END}")
    
    if speed:
        print(f"\n{Colors.GREEN}[+] Performance{Colors.END}")
        if "error" in speed:
            print(f"    {Colors.RED}Erro: {speed['error']}{Colors.END}")
        else:
            print(f"    Download: {Colors.BOLD}{speed['download']:.2f} Mbps{Colors.END}")
            print(f"    Upload:   {Colors.BOLD}{speed['upload']:.2f} Mbps{Colors.END}")
            print(f"    Ping:     {Colors.BOLD}{speed['ping']:.2f} ms{Colors.END}")
    
    print(f"\n{Colors.CYAN}============================================{Colors.END}")
    print(f" {Colors.BLUE}Scan finalizado em: {datetime.now().strftime('%H:%M:%S')}{Colors.END}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LAN-Dashboard: Network Recon Tool")
    parser.add_argument('--full', action='store_true', help="Executa o scan completo incluindo Speedtest")
    args = parser.parse_args()

    info = get_network_info()
    speed_data = None
    if args.full:
        speed_data = check_speed()
    
    print_dashboard(info, speed_data)
