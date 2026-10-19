#!/bin/bash
# Script para iniciar o chr$doom

echo "🚀 Iniciando chr\$doom..."
cd ~/projects/chr-doom
# Adiciona a pasta atual ao PYTHONPATH para que o Python encontre o pacote 'src'
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 src/main.py
