"""
Allen - Bichinho Virtual Alienígena
Módulo: ui.py
Interface do usuário: botões, barras de status, mensagens e HUD.
"""

import pygame
from renderer import (
    desenhar_barra_status, desenhar_texto,
    COR_UI, COR_ALERTA, COR_FUNDO, COR_CORPO, COR_OLHO, COR_ANTENA
)


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor=COR_UI):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.hover = False

    def desenhar(self, surface, fonte):
        cor = (min(255, self.cor[0] + 40),
               min(255, self.cor[1] + 40),
               min(255, self.cor[2] + 40)) if self.hover else self.cor
        pygame.draw.rect(surface, cor, self.rect, 2)
        desenhar_texto(surface, self.texto,
                       self.rect.x + 10, self.rect.y + 8, fonte, cor)

    def clicado(self, pos):
        return self.rect.collidepoint(pos)

    def atualizar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)


class HUD:
    def __init__(self, largura_tela, altura_tela):
        self.largura = largura_tela
        self.altura = altura_tela
        self.fonte = pygame.font.SysFont("monospace", 18, bold=True)
        self.fonte_pequena = pygame.font.SysFont("monospace", 14)

    def desenhar(self, surface, pet):
        y_inicial = 20
        espacamento = 50

        desenhar_texto(surface, f"> {pet.nome.upper()} [{pet.especie}]",
                       20, y_inicial, self.fonte, COR_UI)

        estagio_txt = f"ESTÁGIO: {pet.estagio.upper()}"
        cor_estagio = COR_ALERTA if pet.estagio == "morto" else COR_UI
        desenhar_texto(surface, estagio_txt, 20, y_inicial + 25, self.fonte_pequena, cor_estagio)

        barras = [
            ("FOME", pet.fome, COR_ALERTA if pet.fome > 70 else COR_UI),
            ("ENERGIA", pet.energia, COR_UI if pet.energia > 30 else COR_ALERTA),
            ("FELICIDADE", pet.felicidade, COR_UI if pet.felicidade > 40 else COR_ALERTA),
            ("SAÚDE", pet.saude, COR_UI if pet.saude > 60 else COR_ALERTA),
            ("HIGIENE", pet.higiene, COR_UI if pet.higiene > 40 else COR_ALERTA),
        ]

        for i, (label, valor, cor) in enumerate(barras):
            y = y_inicial + 60 + i * espacamento
            desenhar_texto(surface, label, 20, y, self.fonte_pequena, cor)
            desenhar_barra_status(surface, 100, y, 200, 12, valor, cor)
            desenhar_texto(surface, f"{valor:.0f}%", 310, y - 2, self.fonte_pequena, cor)

        status = pet.get_status_texto()
        cor_status = COR_ALERTA if status in ("PRECISA DE ATENÇÃO", "DOENTE", "MORTO") else COR_UI
        desenhar_texto(surface, f"STATUS: {status}", 20, y_inicial + 60 + len(barras) * espacamento + 10,
                       self.fonte, cor_status)

        idade_min = int(pet.idade_segundos // 60)
        idade_seg = int(pet.idade_segundos % 60)
        desenhar_texto(surface, f"IDADE: {idade_min}m {idade_seg:02d}s",
                       20, y_inicial + 60 + len(barras) * espacamento + 40, self.fonte_pequena, COR_UI)

        desenhar_texto(surface, f"REFEIÇÕES: {pet.refeicoes}  BRINCADEIRAS: {pet.brincadeiras}  SONECAS: {pet.sonecas}",
                       20, y_inicial + 60 + len(barras) * espacamento + 60, self.fonte_pequena, COR_UI)

        if pet.doente:
            desenhar_texto(surface, "! ALERTA: PET DOENTE !", 20,
                           y_inicial + 60 + len(barras) * espacamento + 85,
                           self.fonte, COR_ALERTA)
        if pet.dormindo:
            desenhar_texto(surface, "Zzz... DORMINDO", 20,
                           y_inicial + 60 + len(barras) * espacamento + 105,
                           self.fonte, COR_UI)


class PainelBotoes:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.botoes = []
        self._criar_botoes()

    def _criar_botoes(self):
        bw, bh = 120, 40
        espacamento = 15
        colunas = 2
        linhas = 3

        labels = [
            ("ALIMENTAR", "alimentar"),
            ("BRINCAR", "brincar"),
            ("DORMIR", "dormir"),
            ("CURAR", "curar"),
            ("SALVAR", "salvar"),
            ("SAIR", "sair"),
        ]

        for i, (label, acao) in enumerate(labels):
            col = i % colunas
            linha = i // colunas
            bx = self.x + col * (bw + espacamento) + 10
            by = self.y + linha * (bh + espacamento) + 10
            self.botoes.append(Botao(bx, by, bw, bh, label))

    def desenhar(self, surface, fonte):
        pygame.draw.rect(surface, COR_UI, (self.x, self.y, self.largura, self.altura), 2)
        desenhar_texto(surface, "COMANDOS", self.x + 10, self.y + 10, fonte, COR_UI)

        for botao in self.botoes:
            botao.desenhar(surface, fonte)

    def atualizar_hover(self, pos):
        for botao in self.botoes:
            botao.atualizar_hover(pos)

    def clicar(self, pos):
        for botao in self.botoes:
            if botao.clicado(pos):
                return botao.texto.lower()
        return None
