"""
Allen - Bichinho Virtual Alienígena
Arquivo principal: main.py
Loop principal do jogo, integração entre pet, renderer e UI.
Estética wireframe + temática alienígena + animações por interação.
"""

import sys
import pygame

from pet import AlienPet, salvar_pet, carregar_pet
from renderer import WireframeAlien, COR_FUNDO, COR_UI, COR_ALERTA
from ui import HUD, PainelBotoes


LARGURA = 800
ALTURA = 600
FPS = 60


def desenhar_texto_tela(surface, texto, x, y, fonte, cor):
    render = fonte.render(texto, True, cor)
    surface.blit(render, (x, y))


def main():
    pygame.init()
    pygame.display.set_caption("ALLEN - Bichinho Virtual Alienígena")
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    relogio = pygame.time.Clock()

    pet = carregar_pet("savegame.json")
    if pet is None:
        pet = AlienPet(nome="Allen", especie="Xenomorfo Wireframe")

    alien = WireframeAlien(LARGURA // 2, ALTURA // 2 - 50, escala=1.2)

    hud = HUD(LARGURA, ALTURA)
    painel = PainelBotoes(LARGURA - 320, ALTURA - 260, 300, 240)

    fonte_msg = pygame.font.SysFont("monospace", 20, bold=True)
    mensagem = "Bem-vindo, comandante. Cuide do seu alien."
    tempo_mensagem = 0

    rodando = True
    ultimo_tempo = pygame.time.get_ticks()

    while rodando:
        agora = pygame.time.get_ticks()
        dt = (agora - ultimo_tempo) / 1000.0
        ultimo_tempo = agora

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_1:
                    if pet.alimentar():
                        mensagem = f"{pet.nome} foi alimentado!"
                        tempo_mensagem = 180
                        alien.tocar_animacao("comer", 0.8)
                elif evento.key == pygame.K_2:
                    if pet.brincar():
                        mensagem = f"Brincando com {pet.nome}!"
                        tempo_mensagem = 180
                        alien.tocar_animacao("brincar", 0.8)
                elif evento.key == pygame.K_3:
                    dormindo = pet.dormir()
                    mensagem = f"{pet.nome} {'dormiu' if dormindo else 'acordou'}!"
                    tempo_mensagem = 180
                    alien.tocar_animacao("dormir", 1.2)
                elif evento.key == pygame.K_4:
                    if pet.curar():
                        mensagem = f"{pet.nome} foi curado!"
                        tempo_mensagem = 180
                        alien.tocar_animacao("curar", 0.8)
                elif evento.key == pygame.K_s:
                    salvar_pet(pet, "savegame.json")
                    mensagem = "Jogo salvo!"
                    tempo_mensagem = 120

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos = pygame.mouse.get_pos()
                    acao = painel.clicar(pos)
                    if acao == "alimentar":
                        if pet.alimentar():
                            mensagem = f"{pet.nome} foi alimentado!"
                            tempo_mensagem = 180
                            alien.tocar_animacao("comer", 0.8)
                    elif acao == "brincar":
                        if pet.brincar():
                            mensagem = f"Brincando com {pet.nome}!"
                            tempo_mensagem = 180
                            alien.tocar_animacao("brincar", 0.8)
                    elif acao == "dormir":
                        dormindo = pet.dormir()
                        mensagem = f"{pet.nome} {'dormiu' if dormindo else 'acordou'}!"
                        tempo_mensagem = 180
                        alien.tocar_animacao("dormir", 1.2)
                    elif acao == "curar":
                        if pet.curar():
                            mensagem = f"{pet.nome} foi curado!"
                            tempo_mensagem = 180
                            alien.tocar_animacao("curar", 0.8)
                    elif acao == "salvar":
                        salvar_pet(pet, "savegame.json")
                        mensagem = "Jogo salvo!"
                        tempo_mensagem = 120
                    elif acao == "sair":
                        rodando = False

        # Animação de morte se saúde zerar
        if not pet.vivo and pet.estagio == "morto" and alien.anim.active != "morrer":
            alien.tocar_animacao("morrer", 1.5)

        pet.atualizar(dt)
        alien.atualizar(dt)
        painel.atualizar_hover(pygame.mouse.get_pos())

        if tempo_mensagem > 0:
            tempo_mensagem -= 1

        tela.fill(COR_FUNDO)

        for x in range(0, LARGURA, 40):
            pygame.draw.line(tela, (30, 30, 50), (x, 0), (x, ALTURA), 1)
        for y in range(0, ALTURA, 40):
            pygame.draw.line(tela, (30, 30, 50), (0, y), (LARGURA, y), 1)

        alien.desenhar(
            tela,
            estagio=pet.estagio,
            vivo=pet.vivo,
            dormindo=pet.dormindo,
            doente=pet.doente,
        )

        hud.desenhar(tela, pet)
        painel.desenhar(tela, fonte_msg)

        if tempo_mensagem > 0:
            desenhar_texto_tela(tela, mensagem, LARGURA // 2 - 150, 30,
                                fonte_msg, COR_UI)

        desenhar_texto_tela(tela, "Teclas: 1=Alimentar  2=Brincar  3=Dormir  4=Curar  S=Salvar  ESC=Sair",
                            20, ALTURA - 30, pygame.font.SysFont("monospace", 14), (100, 100, 120))

        pygame.display.flip()
        relogio.tick(FPS)

    salvar_pet(pet, "savegame.json")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
