#!/usr/bin/env python3
"""Ecossistema Simulação 2.0

Projeto modernizado: uso de dataclasses, type hints, e Rich para visualização
colorida e fluida no terminal.

Requisitos:
  pip install rich

Execute com: python ecossistema.py
"""

import random
import time
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

# ================== CONFIGURAÇÕES DO MUNDO ==================
LARGURA: int = 35
ALTURA: int = 18
TEMPO_ENTRE_CICLOS: float = 0.25  # segundos entre cada ciclo
CICLOS_POR_DIA: int = 12          # quanto tempo dura o ciclo dia‑noite

# REGRAS DE VIDA
CHANCE_PLANTA_NASCE: float = 0.09
ENERGIA_POR_PLANTA: int = 3
CUSTO_MOVER_DIA: int = 1
CUSTO_MOVER_NOITE: float = 0.7
ENERGIA_INICIAL_PEIXE: int = 10
ENERGIA_INICIAL_HERBIVORO: int = 14
ENERGIA_INICIAL_PREDADOR: int = 18
REPRODUCAO_PEIXE: float = 0.15
REPRODUCAO_HERBIVORO: float = 0.12
REPRODUCAO_PREDADOR: float = 0.09
CHANCE_MORRE_PEIXE: float = 0.02
CHANCE_MORRE_HERBIVORO: float = 0.015
CHANCE_MORRE_PREDADOR: float = 0.01

# SÍMBOLOS DO MAPA (usando Rich para colorir)
SIMBOLO_VAZIO = "·"
SIMBOLO_PLANTA = "🌿"
SIMBOLO_PEIXE = "🐟"
SIMBOLO_HERBIVORO = "🐸"
SIMBOLO_PREDADOR = "🦈"
SIMBOLO_RIO = "🌊"
SIMBOLO_MONTANHA = "⛰️"

# TIPOS DE TERRENO
TERRENO_PASSAGEM = 0
TERRENO_RIO = 1
TERRENO_MONTANHA = 2

# ================== ENTIDADES ==================
@dataclass
class Entidade:
    tipo: str
    energia: int = 0

@dataclass
class Planta(Entidade):
    tipo: str = "planta"

@dataclass
class Peixe(Entidade):
    tipo: str = "peixe"
    energia: int = ENERGIA_INICIAL_PEIXE

@dataclass
class Herbivoro(Entidade):
    tipo: str = "herbivoro"
    energia: int = ENERGIA_INICIAL_HERBIVORO

@dataclass
class Predador(Entidade):
    tipo: str = "predador"
    energia: int = ENERGIA_INICIAL_PREDADOR

# ================== FUNÇÕES DE AMBIENTE ==================
def criar_mapa() -> List[List[Optional[Entidade]]]:
    """Mapa vazio (sem entidades)."""
    return [[None for _ in range(LARGURA)] for _ in range(ALTURA)]

def criar_terreno() -> List[List[int]]:
    """Gera rios e montanhas como obstáculos intransponíveis."""
    terreno = [[TERRENO_PASSAGEM for _ in range(LARGURA)] for _ in range(ALTURA)]
    # Rio vertical central
    rio_x = LARGURA // 2
    for y in range(ALTURA):
        terreno[y][rio_x] = TERRENO_RIO
        if random.random() < 0.3:
            terreno[y][max(rio_x - 1, 0)] = TERRENO_RIO
    # Montanhas aleatórias
    for _ in range(6):
        mx = random.randint(0, LARGURA - 1)
        my = random.randint(0, ALTURA - 1)
        tamanho = random.randint(1, 3)
        for dy in range(-tamanho, tamanho + 1):
            for dx in range(-tamanho, tamanho + 1):
                ny, nx = my + dy, mx + dx
                if 0 <= ny < ALTURA and 0 <= nx < LARGURA:
                    if abs(dx) + abs(dy) <= tamanho:
                        terreno[ny][nx] = TERRENO_MONTANHA
    return terreno

def eh_passavel(x: int, y: int, terreno: List[List[int]]) -> bool:
    return 0 <= y < ALTURA and 0 <= x < LARGURA and terreno[y][x] == TERRENO_PASSAGEM

def vizinhos(x: int, y: int, terreno: List[List[int]]) -> List[Tuple[int, int]]:
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]
    result = []
    for dy, dx in dirs:
        nx, ny = x + dx, y + dy
        if eh_passavel(nx, ny, terreno):
            result.append((nx, ny))
    return result

# ================== ESTATÍSTICAS ==================
def contar_estatisticas(mapa: List[List[Optional[Entidade]]]) -> Dict[str, int]:
    est = defaultdict(int)
    for linha in mapa:
        for celula in linha:
            if not celula:
                continue
            est[celula.tipo] += 1
    return dict(est)

# ================== DESASTRES NATURAIS ==================
console = Console()

def verificar_desastre(ciclo: int, mapa: List[List[Optional[Entidade]]], terreno: List[List[int]]) -> None:
    if ciclo % 50 == 0 and random.random() < 0.35:
        tipo = random.choice(["seca", "tempestade"])
        if tipo == "seca":
            console.log("☀️💀 SECA! Muitas plantas morrem.")
            for y in range(ALTURA):
                for x in range(LARGURA):
                    if mapa[y][x] and mapa[y][x].tipo == "planta" and random.random() < 0.55:
                        mapa[y][x] = None
        else:
            console.log("⛈️🌪️ TEMPESTADE! Inundações e ventos fortes.")
            for y in range(ALTURA):
                for x in range(LARGURA):
                    if mapa[y][x] and random.random() < 0.18:
                        mapa[y][x] = None
        time.sleep(1.5)

# ================== RENDERIZAÇÃO COM RICH ==================

def render_mapa(mapa: List[List[Optional[Entidade]]], terreno: List[List[int]], ciclo: int, estat: Dict[str, int]) -> Panel:
    periodo = "☀️ DIA" if (ciclo // CICLOS_POR_DIA) % 2 == 0 else "🌙 NOITE"
    linhas = []
    for y in range(ALTURA):
        linha = []
        for x in range(LARGURA):
            t = terreno[y][x]
            if t == TERRENO_RIO:
                linha.append(f"[cyan]{SIMBOLO_RIO}[/]")
            elif t == TERRENO_MONTANHA:
                linha.append(f"[magenta]{SIMBOLO_MONTANHA}[/]")
            else:
                ent = mapa[y][x]
                if not ent:
                    linha.append(SIMBOLO_VAZIO)
                elif ent.tipo == "planta":
                    linha.append(f"[green]{SIMBOLO_PLANTA}[/]")
                elif ent.tipo == "peixe":
                    linha.append(f"[blue]{SIMBOLO_PEIXE}[/]")
                elif ent.tipo == "herbivoro":
                    linha.append(f"[yellow]{SIMBOLO_HERBIVORO}[/]")
                elif ent.tipo == "predador":
                    linha.append(f"[red]{SIMBOLO_PREDADOR}[/]")
        linhas.append(" ".join(linha))
    body = "\n".join(linhas)
    header = f"[bold]Ciclo {ciclo} — {periodo}[/]"
    footer = (
        f"[green]Plantas: {estat.get('planta',0)}[/]  "
        f"[blue]Peixes: {estat.get('peixe',0)}[/]  "
        f"[yellow]Herbívoros: {estat.get('herbivoro',0)}[/]  "
        f"[red]Predadores: {estat.get('predador',0)}[/]"
    )
    return Panel(body, title=header, subtitle=footer, border_style="bright_black")

# ================== CICLO DE VIDA ==================

def ciclo_da_vida(mapa: List[List[Optional[Entidade]]], terreno: List[List[int]], ciclo: int) -> List[List[Optional[Entidade]]]:
    novo = criar_mapa()
    eh_dia = (ciclo // CICLOS_POR_DIA) % 2 == 0
    custo = CUSTO_MOVER_DIA if eh_dia else CUSTO_MOVER_NOITE

    # Plantas (apenas de dia)
    for y in range(ALTURA):
        for x in range(LARGURA):
            if not eh_passavel(x, y, terreno):
                continue
            atual = mapa[y][x]
            if atual is None:
                if eh_dia and random.random() < CHANCE_PLANTA_NASCE:
                    novo[y][x] = Planta()
            elif atual.tipo == "planta":
                novo[y][x] = Planta()

    # Função auxiliar de movimentação
    def mover(ent: Entidade, x: int, y: int):
        ent.energia -= custo
        if ent.energia <= 0:
            return  # morre por falta de energia
        # chance de morte aleatória
        if ent.tipo == "peixe" and random.random() < CHANCE_MORRE_PEIXE:
            return
        if ent.tipo == "herbivoro" and random.random() < CHANCE_MORRE_HERBIVORO:
            return
        if ent.tipo == "predador" and random.random() < CHANCE_MORRE_PREDADOR:
            return
        viz = vizinhos(x, y, terreno)
        vazios = [(nx, ny) for nx, ny in viz if novo[ny][nx] is None]
        # Determina alimento
        if ent.tipo in ("peixe", "herbivoro"):
            comida = [(nx, ny) for nx, ny in viz if mapa[ny][nx] and mapa[ny][nx].tipo == "planta"]
        else:  # predador
            comida = [(nx, ny) for nx, ny in viz if mapa[ny][nx] and mapa[ny][nx].tipo in ("peixe", "herbivoro")]
        if comida:
            nx, ny = random.choice(comida)
            ent.energia += ENERGIA_POR_PLANTA
            # Reprodução específica
            if ent.tipo == "peixe" and random.random() < REPRODUCAO_PEIXE and vazios:
                fx, fy = random.choice(vazios)
                novo[fy][fx] = Peixe()
                vazios.remove((fx, fy))
            elif ent.tipo == "herbivoro" and random.random() < REPRODUCAO_HERBIVORO and vazios:
                fx, fy = random.choice(vazios)
                novo[fy][fx] = Herbivoro()
                vazios.remove((fx, fy))
            elif ent.tipo == "predador" and random.random() < REPRODUCAO_PREDADOR and vazios:
                fx, fy = random.choice(vazios)
                novo[fy][fx] = Predador()
                vazios.remove((fx, fy))
            novo[ny][nx] = ent
        elif vazios:
            nx, ny = random.choice(vazios)
            novo[ny][nx] = ent
        else:
            novo[y][x] = ent

    # Processa peixes
    for y in range(ALTURA):
        for x in range(LARGURA):
            ent = mapa[y][x]
            if ent and ent.tipo == "peixe":
                mover(ent, x, y)
    # Herbívoros
    for y in range(ALTURA):
        for x in range(LARGURA):
            ent = mapa[y][x]
            if ent and ent.tipo == "herbivoro":
                mover(ent, x, y)
    # Predadores
    for y in range(ALTURA):
        for x in range(LARGURA):
            ent = mapa[y][x]
            if ent and ent.tipo == "predador":
                mover(ent, x, y)
    return novo

# ================== GRÁFICO POPULAÇÃO ==================
historico: Dict[str, List[int]] = defaultdict(list)

def render_grafico() -> Panel:
    if not any(historico.values()):
        return Panel("Sem dados ainda...", border_style="red")
    span = 20
    chaves = ["planta", "peixe", "herbivoro", "predador"]
    cores = {"planta": "green", "peixe": "blue", "herbivoro": "yellow", "predador": "red"}
    max_val = max((max(historico[k][-span:] or [1]) for k in chaves))
    linhas = []
    for k in chaves:
        vals = historico[k][-span:]
        barra = ""
        for v in vals:
            pct = v / max_val if max_val else 0
            if pct > 0.75:
                barra += "█"
            elif pct > 0.5:
                barra += "▓"
            elif pct > 0.25:
                barra += "▒"
            elif pct > 0.05:
                barra += "░"
            else:
                barra += " "
        símbolo = SIMBOLO_PLANTA if k == "planta" else SIMBOLO_PEIXE if k == "peixe" else SIMBOLO_HERBIVORO if k == "herbivoro" else SIMBOLO_PREDADOR
        linha = f"[{cores[k]}]{símbolo} {k.ljust(10)} {barra} {historico[k][-1] if historico[k] else 0}[/]"
        linhas.append(linha)
    body = "\n".join(linhas)
    return Panel(body, title="📈 Evolução Populacional (últimos 20 ciclos)", border_style="bright_black")

# ================== MAIN ==================
def main() -> None:
    console.print("[bold magenta]🌍 ECOSSISTEMA MODERNO – Iniciando...[/]")
    time.sleep(1)
    mapa = criar_mapa()
    terreno = criar_terreno()
    # População inicial
    for y in range(ALTURA):
        for x in range(LARGURA):
            if not eh_passavel(x, y, terreno):
                continue
            r = random.random()
            if r < 0.11:
                mapa[y][x] = Planta()
            elif r < 0.17:
                mapa[y][x] = Peixe()
            elif r < 0.21:
                mapa[y][x] = Herbivoro()
            elif r < 0.24:
                mapa[y][x] = Predador()
    ciclo = 0
    try:
        with Live(refresh_per_second=4, console=console) as live:
            while True:
                ciclo += 1
                estat = contar_estatisticas(mapa)
                for k, v in estat.items():
                    historico[k].append(v)
                live.update(render_mapa(mapa, terreno, ciclo, estat))
                if ciclo % 5 == 0:
                    console.print(render_grafico())
                verificar_desastre(ciclo, mapa, terreno)
                mapa = ciclo_da_vida(mapa, terreno, ciclo)
                time.sleep(TEMPO_ENTRE_CICLOS)
                if sum(estat.values()) == 0:
                    console.print("[red]💀 Todas as formas de vida desapareceram. Reiniciando...[/]")
                    time.sleep(2)
                    mapa = criar_mapa()
                    historico.clear()
    except KeyboardInterrupt:
        console.clear()
        console.print("[bold green]🌍 Simulação encerrada. Até a próxima![/]")

if __name__ == "__main__":
    main()
