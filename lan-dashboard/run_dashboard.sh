#!/bin/bash

# Cores para o menu
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

clear
echo -e "${CYAN}============================================"
echo -e "       🚀 LAN-DASHBOARD LAUNCHER"
echo -e "============================================${NC}"
echo -e "${YELLOW}Como você quer rodar o scan hoje?${NC}"
echo -e "1) ${GREEN}Padrão${NC} (Apenas IPs e Rede - Rápido)"
echo -e "2) ${GREEN}Full${NC} (Rede + Speedtest - Demorado)"
echo -e "3) ${RED}Sair${NC}"
echo -e "${CYAN}--------------------------------------------${NC}"

read -p "Escolha uma opção [1-3]: " option

case $option in
    1)
        echo -e "\n${YELLOW}Iniciando scan padrão...${NC}"
        python ~/lan-dashboard/dashboard.py
        ;;
    2)
        echo -e "\n${YELLOW}Iniciando scan completo...${NC}"
        python ~/lan-dashboard/dashboard.py --full
        ;;
    3)
        echo -e "\n${CYAN}Saindo... Fui!${NC}"
        exit 0
        ;;
    *)
        echo -e "\n${RED}Opção inválida! Digita 1, 2 ou 3, porra.${NC}"
        $0 # Reinicia o script
        ;;
esac

echo -e "\n${CYAN}============================================${NC}"
echo -e "   Scan finalizado. Voltando ao terminal..."
