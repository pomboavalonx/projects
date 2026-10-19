#!/data/data/com.termux/files/usr/bin/bash

# LAN-Dashboard Startup Script
# Operação: Nébula

echo -e "\033[1;36m[+] Iniciando LAN-Dashboard...\033[0m"

# Verifica se as dependências estão instaladas
echo -e "\033[0;33m[*] Verificando dependências...\033[0m"
pip install flask flask-cors speedtest-cli requests --quiet

echo -e "\033[1;32m[+] Servidor subindo na porta 5050...\033[0m"
echo -e "\033[0;34m[i] Acesse: http://localhost:5050\033[0m"
echo -e "\033[0;31m[!] Pressione CTRL+C para encerrar\033[0m"
echo "--------------------------------------------"

python /data/data/com.termux/files/home/lan-dashboard/app.py
