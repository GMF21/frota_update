class Veiculo:
    def __init__(self, marca, modelo, ano, preco):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.preco = preco

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.preco:.2f}€"


class EletricCar(Veiculo):
    def __init__(self, marca, modelo, ano, preco, autonomia):
        super().__init__(marca, modelo, ano, preco)
        self.autonomia = autonomia

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) (Elétrico) - {self.preco:.2f}€ | Autonomia: {self.autonomia} km"
