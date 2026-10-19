# ALLEN - Bichinho Virtual Alienígena

Um Tamagotchi-like em Python + Pygame com estética **wireframe** e temática **alienígena**.

## Requisitos
- Python 3.7+
- Pygame 2.1+

## Instalação
```bash
pip install -r requirements.txt
```

## Execução
```bash
python main.py
```

## Controles
| Tecla | Ação |
|-------|------|
| 1 | Alimentar |
| 2 | Brincar |
| 3 | Dormir / Acordar |
| 4 | Curar |
| S | Salvar jogo |
| ESC | Sair |

Clique nos botões da interface para as mesmas ações.

## Funcionalidades
- Estatísticas: fome, energia, felicidade, saúde, higiene
- Estágios de vida: Ovo → Bebê → Adolescente → Adulto → Idoso → Morto
- Renderização 100% wireframe (apenas linhas, sem preenchimento)
- Cores neon alienígenas (verde, ciano, magenta)
- Salvamento automático em JSON
- HUD com barras de status e avisos

## Estrutura
```
allen/
├── main.py          # Loop principal
├── pet.py           # Lógica do pet alienígena
├── renderer.py      # Renderização wireframe
├── ui.py            # Interface (HUD, botões)
├── requirements.txt
├── AGORA_PROJECT.md
└── README.md
```

## Licença
MIT
