"""
Allen - Bichinho Virtual Alienígena
Módulo: pet.py
Lógica do pet alienígena com estatísticas, estágios de vida e interações.
"""

import json
import os
import random
import time


class AlienPet:
    """
    Representa um bichinho virtual alienígena com necessidades e estágios de vida.
    """

    STAGES = ["ovo", "bebe", "adolescente", "adulto", "idoso", "morto"]

    def __init__(self, nome="Zorg", especie="Xenomorfo"):
        self.nome = nome
        self.especie = especie
        self.nascimento = time.time()
        self.idade_segundos = 0
        self.estagio = "ovo"

        self.fome = 50
        self.energia = 80
        self.felicidade = 50
        self.saude = 100
        self.higiene = 70

        self.refeicoes = 0
        self.brincadeiras = 0
        self.sonecas = 0

        self.vivo = True
        self.dormindo = False
        self.doente = False

        self.taxa_fome = 0.05
        self.taxa_energia = 0.03
        self.taxa_felicidade = 0.04
        self.taxa_higiene = 0.02

    def atualizar(self, dt):
        if not self.vivo or self.estagio == "morto":
            return

        self.idade_segundos += dt
        self._atualizar_estagio()

        if self.dormindo:
            self.energia = min(100, self.energia + 0.1 * dt)
            self.fome = min(100, self.fome + 0.03 * dt)
            self.felicidade = max(0, self.felicidade - 0.02 * dt)
        else:
            self.fome = min(100, self.fome + self.taxa_fome * dt)
            self.energia = max(0, self.energia - self.taxa_energia * dt)
            self.felicidade = max(0, self.felicidade - self.taxa_felicidade * dt)
            self.higiene = max(0, self.higiene - self.taxa_higiene * dt)

        if self.fome >= 90:
            self.saude = max(0, self.saude - 0.05 * dt)
        if self.energia <= 10:
            self.saude = max(0, self.saude - 0.03 * dt)
        if self.felicidade <= 10:
            self.saude = max(0, self.saude - 0.04 * dt)
        if self.higiene <= 20:
            self.doente = True
            self.saude = max(0, self.saude - 0.02 * dt)
        else:
            self.doente = False

        if self.saude <= 0:
            self.morrer()

    def _atualizar_estagio(self):
        idade = self.idade_segundos
        if idade < 30:
            self.estagio = "ovo"
        elif idade < 120:
            self.estagio = "bebe"
        elif idade < 300:
            self.estagio = "adolescente"
        elif idade < 600:
            self.estagio = "adulto"
        elif idade < 900:
            self.estagio = "idoso"
        else:
            self.estagio = "idoso"

    def alimentar(self):
        if not self.vivo or self.dormindo:
            return False
        self.fome = max(0, self.fome - 25)
        self.felicidade = min(100, self.felicidade + 5)
        self.refeicoes += 1
        return True

    def brincar(self):
        if not self.vivo or self.dormindo or self.energia < 20:
            return False
        self.felicidade = min(100, self.felicidade + 15)
        self.fome = min(100, self.fome + 10)
        self.energia = max(0, self.energia - 10)
        self.brincadeiras += 1
        return True

    def dormir(self):
        if not self.vivo:
            return False
        self.dormindo = not self.dormindo
        if self.dormindo:
            self.sonecas += 1
        return self.dormindo

    def curar(self):
        if not self.vivo:
            return False
        self.doente = False
        self.saude = min(100, self.saude + 20)
        self.higiene = min(100, self.higiene + 30)
        return True

    def morrer(self):
        self.vivo = False
        self.estagio = "morto"

    def esta_doente(self):
        return self.doente

    def precisa_atencao(self):
        return self.fome > 80 or self.energia < 20 or self.felicidade < 20 or self.saude < 50

    def get_status_texto(self):
        if not self.vivo:
            return "MORTO"
        if self.dormindo:
            return "DORMINDO"
        if self.doente:
            return "DOENTE"
        if self.precisa_atencao():
            return "PRECISA DE ATENÇÃO"
        return "BEM"

    def to_dict(self):
        return {
            "nome": self.nome,
            "especie": self.especie,
            "nascimento": self.nascimento,
            "idade_segundos": self.idade_segundos,
            "estagio": self.estagio,
            "fome": self.fome,
            "energia": self.energia,
            "felicidade": self.felicidade,
            "saude": self.saude,
            "higiene": self.higiene,
            "refeicoes": self.refeicoes,
            "brincadeiras": self.brincadeiras,
            "sonecas": self.sonecas,
            "vivo": self.vivo,
            "dormindo": self.dormindo,
            "doente": self.doente,
        }

    @classmethod
    def from_dict(cls, data):
        pet = cls(nome=data.get("nome", "Zorg"), especie=data.get("especie", "Xenomorfo"))
        pet.nascimento = data.get("nascimento", time.time())
        pet.idade_segundos = data.get("idade_segundos", 0)
        pet.estagio = data.get("estagio", "ovo")
        pet.fome = data.get("fome", 50)
        pet.energia = data.get("energia", 80)
        pet.felicidade = data.get("felicidade", 50)
        pet.saude = data.get("saude", 100)
        pet.higiene = data.get("higiene", 70)
        pet.refeicoes = data.get("refeicoes", 0)
        pet.brincadeiras = data.get("brincadeiras", 0)
        pet.sonecas = data.get("sonecas", 0)
        pet.vivo = data.get("vivo", True)
        pet.dormindo = data.get("dormindo", False)
        pet.doente = data.get("doente", False)
        return pet


def salvar_pet(pet, caminho="savegame.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(pet.to_dict(), f, indent=2, ensure_ascii=False)


def carregar_pet(caminho="savegame.json"):
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        data = json.load(f)
    return AlienPet.from_dict(data)
