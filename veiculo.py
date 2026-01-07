class Veiculo:
    def __init__(self, marca, preco):
        self.marca = marca
        self.preco = preco

    def __str__(self):
        return f"{self.marca} - {self.preco:.2f}€"
    
class EletricCar(Veiculo):
    def __init__(self, marca, preco, autonomia):
        super().__init__(marca, preco)
        self.autonomia = autonomia

    def __str__(self):
        return f"{self.marca} (Elétrico) - {self.preco:.2f}€ | Autonomia: {self.autonomia} km"
    