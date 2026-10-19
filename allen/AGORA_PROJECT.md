# AGORA_PROJECT - Allen

## Decisões de Arquitetura
- **Stack:** Python 3 + Pygame 2.x
- **Objetivo:** Bichinho virtual (Tamagotchi-like) com estética wireframe e temática alienígena
- **Dependências externas:** pygame (via pip)
- **Padrão de arquitetura:** Modular (separação de lógica de jogo, renderização e UI)
- **Testes:** Não definido (opcional)
- **CI/CD:** Não definido (opcional)
- **Licença:** MIT

## Funcionalidades Implementadas
- Classe AlienPet com atributos: fome, energia, felicidade, saúde, idade, estágio de vida
- Renderização wireframe (apenas linhas, sem preenchimento) usando pygame.draw.line / pygame.draw.lines
- Temática alienígena: cores neon (verde, ciano, magenta), olhos grandes, antenas, formas orgânicas geométricas
- Interações: alimentar, brincar, dormir, curar
- Sistema de estágios: Ovo → Bebê → Adolescente → Adulto → Idoso → Morto
- Barra de status com estatísticas visuais em wireframe
- Loop principal com clock, eventos de teclado e mouse
- Salvamento de estado (JSON)
- HUD com barras de status e avisos visuais
- Painel de botões clicáveis na interface
- **Animações por interação:**
  - Comer: pulso vertical + cor amarelada
  - Brincar: tremulação rápida + cor magenta
  - Dormir: descida lenta + cor azulada
  - Curar: pulso de escala + cor ciano
  - Morrer: queda + cor vermelha + X nos olhos

## TODOs
- [x] Criar main.py com loop principal
- [x] Criar pet.py com lógica do alien
- [x] Criar renderer.py com desenho wireframe + animações
- [x] Criar ui.py com barras de status e botões
- [x] Criar requirements.txt
- [x] Criar start.sh
- [x] Verificação de sintaxe (py_compile OK)
- [ ] Testar execução com display (sem servidor X11 no Termux headless)
- [ ] Sync com GitHub

## Changelog
- 2026-10-16: Projeto inicializado, discovery concluído
- 2026-10-16: Todos os módulos criados e verificados (py_compile OK)
- 2026-10-16: Pygame 2.6.1 já instalado no Termux
- 2026-10-16: Adicionado sistema de animações por interação (comer, brincar, dormir, curar, morrer)
- 2026-10-16: Adicionado script start.sh
