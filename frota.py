import csv
import os
from decoradores import log_operacao
from veiculo import Veiculo, EletricCar


class Frota:
    def __init__(self):
        self.veiculos = []

    @log_operacao
    def adicionarVeiculo(self, veiculo):
        self.veiculos.append(veiculo)

    @log_operacao
    def removeVeiculo(self, veiculo):
        self.veiculos.remove(veiculo)

    def filter(self, marca):
        marca = (marca or "").strip().lower()
        return [v for v in self.veiculos if marca in v.marca.strip().lower()]

    def aplicar_desconto(self, percentagem):
        desconto = lambda preco: preco * (1 - percentagem / 100)
        for v in self.veiculos:
            v.preco = desconto(v.preco)

    def load_inventory(self, ficheiro="inventario_frota.csv"):
        if not os.path.exists(ficheiro):
            return

        self.veiculos = []

        with open(ficheiro, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    marca = (row.get("Marca") or "").strip()
                    modelo = (row.get("Modelo") or "").strip()
                    ano_txt = (row.get("Ano") or "").strip()
                    preco_txt = (row.get("Preco") or "").strip().replace(",", ".")
                    tipo = (row.get("Tipo") or "").strip().lower()
                    autonomia_txt = (row.get("Autonomia") or "").strip()

                    if not marca or not modelo or not ano_txt or not preco_txt:
                        continue

                    ano = int(ano_txt)
                    preco = float(preco_txt)

                    if "elétrico" in tipo or "eletrico" in tipo:
                        autonomia = int(autonomia_txt) if autonomia_txt and autonomia_txt != "N/A" else 0
                        self.veiculos.append(EletricCar(marca, modelo, ano, preco, autonomia))
                    else:
                        self.veiculos.append(Veiculo(marca, modelo, ano, preco))
                except:
                    continue

    def export_inventory(self, ficheiro="inventario_frota.csv"):
        with open(ficheiro, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Marca", "Modelo", "Ano", "Preco", "Tipo", "Autonomia"])
            for v in self.veiculos:
                if isinstance(v, EletricCar):
                    writer.writerow([v.marca, v.modelo, v.ano, v.preco, "Elétrico", v.autonomia])
                else:
                    writer.writerow([v.marca, v.modelo, v.ano, v.preco, "Convencional", "N/A"])
