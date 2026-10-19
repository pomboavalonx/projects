"""
Allen - Bichinho Virtual Alienígena
Módulo: renderer.py
Renderização wireframe do alienígena com animações por interação.
"""

import math
import pygame


COR_CORPO = (0, 255, 128)
COR_OLHO = (0, 255, 255)
COR_ANTENA = (255, 0, 255)
COR_FUNDO = (10, 10, 20)
COR_UI = (0, 255, 255)
COR_ALERTA = (255, 0, 128)


class AnimationManager:
    """
    Gerencia animações temporárias do alienígena wireframe.
    Cada animação tem duração e modifica parâmetros visuais durante esse tempo.
    """

    def __init__(self):
        self.active = None      # nome da animação ativa
        self.timer = 0.0        # tempo restante em segundos
        self.duration = 0.0     # duração total
        self.intensity = 1.0    # intensidade da animação (0 a 1)

    def start(self, nome, duracao=0.8):
        """Inicia uma animação."""
        self.active = nome
        self.timer = duracao
        self.duration = duracao
        self.intensity = 1.0

    def update(self, dt):
        """Atualiza o temporizador da animação."""
        if self.active is None:
            return
        self.timer -= dt
        if self.timer <= 0:
            self.active = None
            self.timer = 0
            self.intensity = 0
        else:
            self.intensity = self.timer / self.duration

    def get_offset(self):
        """Retorna deslocamento (dx, dy) baseado na animação ativa."""
        if self.active is None:
            return 0, 0
        i = self.intensity
        if self.active == "comer":
            # Pulso para cima e para baixo
            return 0, -10 * math.sin(i * math.pi)
        elif self.active == "brincar":
            # Tremulação rápida
            return (5 * math.sin(i * 40 * math.pi),
                    5 * math.cos(i * 40 * math.pi))
        elif self.active == "dormir":
            # Desce devagar
            return 0, 5 * (1 - i)
        elif self.active == "curar":
            # Brilho/pulso para fora
            return 0, 0
        elif self.active == "morrer":
            # Cai para baixo
            return 0, 20 * (1 - i)
        return 0, 0

    def get_scale(self):
        """Retorna escala baseada na animação."""
        if self.active is None:
            return 1.0
        i = self.intensity
        if self.active == "comer":
            return 1.0 + 0.1 * math.sin(i * math.pi)
        elif self.active == "brincar":
            return 1.0 + 0.15 * math.sin(i * 30 * math.pi)
        elif self.active == "dormir":
            return 1.0 - 0.05 * (1 - i)
        elif self.active == "curar":
            return 1.0 + 0.1 * math.sin(i * 20 * math.pi)
        elif self.active == "morrer":
            return 1.0 - 0.3 * (1 - i)
        return 1.0

    def get_color_mod(self):
        """Retorna modificador de cor (r, g, b) baseado na animação."""
        if self.active is None:
            return 0, 0, 0
        i = self.intensity
        if self.active == "comer":
            return int(50 * i), int(100 * i), 0
        elif self.active == "brincar":
            return int(100 * i), 0, int(100 * i)
        elif self.active == "dormir":
            return 0, 0, int(50 * i)
        elif self.active == "curar":
            return 0, int(100 * i), int(100 * i)
        elif self.active == "morrer":
            return int(100 * i), 0, 0
        return 0, 0, 0


class WireframeAlien:
    def __init__(self, centro_x, centro_y, escala=1.0):
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.escala_base = escala
        self.escala = escala
        self.angulo_rotacao = 0.0
        self.pulso = 0.0

        self.anim = AnimationManager()

        self.cabeca_nos = [
            (-20, -40), (-10, -50), (0, -55), (10, -50), (20, -40),
            (25, -20), (20, 0), (10, 10), (0, 15), (-10, 10), (-20, 0), (-25, -20)
        ]
        self.olho_esquerdo = [(-12, -30), (-8, -30)]
        self.olho_direito = [(8, -30), (12, -30)]
        self.antena_esquerda = [(-15, -55), (-18, -65), (-22, -70)]
        self.antena_direita = [(15, -55), (18, -65), (22, -70)]
        self.corpo_nos = [
            (-15, 10), (-15, 40), (-10, 60), (0, 65), (10, 60), (15, 40), (15, 10)
        ]
        self.braco_esquerdo = [(-15, 20), (-30, 30), (-35, 40)]
        self.braco_direito = [(15, 20), (30, 30), (35, 40)]
        self.perna_esquerda = [(-8, 60), (-12, 80), (-10, 95)]
        self.perna_direita = [(8, 60), (12, 80), (10, 95)]

    def _transformar(self, x, y):
        rad = math.radians(self.angulo_rotacao)
        cos_r = math.cos(rad)
        sin_r = math.sin(rad)
        xr = x * cos_r - y * sin_r
        yr = x * sin_r + y * cos_r
        dx, dy = self.anim.get_offset()
        s = self.anim.get_scale() * self.escala_base
        return (
            self.centro_x + dx + xr * s,
            self.centro_y + dy + yr * s
        )

    def _desenhar_linha(self, surface, cor, p1, p2, largura=2):
        t1 = self._transformar(*p1)
        t2 = self._transformar(*p2)
        pygame.draw.line(surface, cor, t1, t2, largura)

    def _desenhar_poligono_aberto(self, surface, cor, nos, largura=2, fechado=False):
        for i in range(len(nos) - 1):
            self._desenhar_linha(surface, cor, nos[i], nos[i + 1], largura)
        if fechado and len(nos) > 2:
            self._desenhar_linha(surface, cor, nos[-1], nos[0], largura)

    def _desenhar_olho(self, surface, centro_x, centro_y, raio_externo, raio_interno):
        num_segmentos = 16
        for i in range(num_segmentos):
            ang1 = 2 * math.pi * i / num_segmentos
            ang2 = 2 * math.pi * ((i + 1) % num_segmentos) / num_segmentos
            x1 = centro_x + raio_externo * math.cos(ang1)
            y1 = centro_y + raio_externo * math.sin(ang1)
            x2 = centro_x + raio_externo * math.cos(ang2)
            y2 = centro_y + raio_externo * math.sin(ang2)
            self._desenhar_linha(surface, COR_OLHO, (x1, y1), (x2, y2), 2)
            x1i = centro_x + raio_interno * math.cos(ang1)
            y1i = centro_y + raio_interno * math.sin(ang1)
            x2i = centro_x + raio_interno * math.cos(ang2)
            y2i = centro_y + raio_interno * math.sin(ang2)
            self._desenhar_linha(surface, COR_OLHO, (x1i, y1i), (x2i, y2i), 1)

    def atualizar(self, dt):
        self.angulo_rotacao = (self.angulo_rotacao + 20 * dt) % 360
        self.pulso = (self.pulso + dt) % (2 * math.pi)
        self.anim.update(dt)

    def tocar_animacao(self, nome, duracao=0.8):
        """Dispara uma animação de interação."""
        self.anim.start(nome, duracao)

    def desenhar(self, surface, estagio="ovo", vivo=True, dormindo=False, doente=False):
        if not vivo:
            self._desenhar_base(surface, estagio, dormindo, doente)
            # X nos olhos indicando morte
            self._desenhar_linha(surface, COR_ALERTA, (-12, -30), (-8, -26), 3)
            self._desenhar_linha(surface, COR_ALERTA, (-8, -30), (-12, -26), 3)
            self._desenhar_linha(surface, COR_ALERTA, (8, -30), (12, -26), 3)
            self._desenhar_linha(surface, COR_ALERTA, (12, -30), (8, -26), 3)
            return

        self._desenhar_base(surface, estagio, dormindo, doente)

    def _desenhar_base(self, surface, estagio, dormindo, doente):
        cor_corpo = COR_ALERTA if doente else COR_CORPO
        cor_olho = (100, 100, 100) if dormindo else COR_OLHO

        # Aplica modificador de cor da animação
        cr, cg, cb = self.anim.get_color_mod()
        if cr or cg or cb:
            cor_corpo = (
                min(255, cor_corpo[0] + cr),
                min(255, cor_corpo[1] + cg),
                min(255, cor_corpo[2] + cb),
            )

        self._desenhar_poligono_aberto(surface, cor_corpo, self.cabeca_nos, fechado=True)

        offset_olho_y = -30
        if estagio == "ovo":
            offset_olho_y = -45
        elif estagio == "bebe":
            offset_olho_y = -25

        self._desenhar_olho(surface, -12, offset_olho_y, 8, 4)
        self._desenhar_olho(surface, 12, offset_olho_y, 8, 4)

        boca_y = 5 if not dormindo else 8
        self._desenhar_linha(surface, cor_corpo, (-6, boca_y), (6, boca_y), 2)

        self._desenhar_poligono_aberto(surface, COR_ANTENA, self.antena_esquerda)
        self._desenhar_poligono_aberto(surface, COR_ANTENA, self.antena_direita)
        pygame.draw.circle(surface, COR_ANTENA,
                           self._transformar(*self.antena_esquerda[-1]), 3)
        pygame.draw.circle(surface, COR_ANTENA,
                           self._transformar(*self.antena_direita[-1]), 3)

        self._desenhar_poligono_aberto(surface, cor_corpo, self.corpo_nos, fechado=True)

        self._desenhar_poligono_aberto(surface, cor_corpo, self.braco_esquerdo)
        self._desenhar_poligono_aberto(surface, cor_corpo, self.braco_direito)

        self._desenhar_poligono_aberto(surface, cor_corpo, self.perna_esquerda)
        self._desenhar_poligono_aberto(surface, cor_corpo, self.perna_direita)

        self._desenhar_linha(surface, cor_corpo, (-10, 10), (-10, 40), 1)
        self._desenhar_linha(surface, cor_corpo, (10, 10), (10, 40), 1)
        self._desenhar_linha(surface, cor_corpo, (0, 15), (0, 60), 1)


def desenhar_barra_status(surface, x, y, largura, altura, valor, cor, cor_fundo=(40, 40, 60)):
    pygame.draw.rect(surface, cor, (x, y, largura, altura), 2)
    preenchimento = int(largura * (valor / 100.0))
    for i in range(0, preenchimento, 4):
        pygame.draw.line(surface, cor, (x + i, y + 2), (x + i, y + altura - 2), 1)


def desenhar_texto(surface, texto, x, y, fonte, cor=(0, 255, 255)):
    render = fonte.render(texto, True, cor)
    surface.blit(render, (x, y))
