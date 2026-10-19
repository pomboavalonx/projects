# Projeto 3dcube-raycast

## Decisões de Discovery
- **Stack**: Python 3, `pygame` (para janela e desenho), `numpy` (opcional para vetores e matrizes). 
- **Objetivo**: Renderizar um cubo wireframe 3D giratório usando raycasting puro (projeção de pontos 3D para 2D). 
- **Arquitetura**: Projeto simples, estrutura modular:
  - `src/main.py` – ponto de entrada, loop principal do pygame.
  - `src/cube.py` – definição da geometria do cubo e cálculo das arestas.
  - `src/raycaster.py` – funções de projeção (perspectiva) e rotação.
- **Dependências externas**: `pygame` (instalar via `pip install pygame`). `numpy` opcional, mas usado para simplificar cálculos.
- **Testes**: Não necessários para este protótipo rápido.
- **CI/CD**: Não configurado.
- **Licença**: MIT (padrão).

## TODOs
- Implementar rotação contínua.
- Ajustar parâmetros de câmera (fov, distância).
- Documentar funções.
- **Adicionar efeito de zoom (cubo se afasta e se aproxima) implementado.**
- Implementar rotação contínua.
- Ajustar parâmetros de câmera (fov, distância).
- Documentar funções.

## Changelog
- 2026-10-17: Projeto criado, decisões definidas.
