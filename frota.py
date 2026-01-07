import csv
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
        return [v for v in self.veiculos if v.marca == marca]

    def aplicar_desconto(self, percentagem):
        desconto = lambda preco: preco * (1 - percentagem/100)
        for v in self.veiculos:
            v.preco = desconto(v.preco)
    
    def export_inventory(self, ficheiro="inventario_frota.csv"):
        with open(ficheiro, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Marca", "Preco", "Tipo", "Autonomia"])
            for v in self.veiculos:
                if isinstance(v, EletricCar):
                    writer.writerow([v.marca, v.preco, "Elétrico", v.autonomia])
                else:
                    writer.writerow([v.marca, v.preco, "Convencional", "N/A"])
            