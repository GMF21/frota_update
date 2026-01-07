from frota import Frota
from veiculo import Veiculo, EletricCar

frota = Frota()

v1 = Veiculo("Ferrari", 250000)
v2 = Veiculo("Pagani", 4565000)
v3 = EletricCar("Tesla", 50000, 410)

frota.adicionarVeiculo(v1)
frota.adicionarVeiculo(v2)
frota.adicionarVeiculo(v3)

print("\nVeiculos Ferrari:")
for v in frota.filter("Ferrari"):
    print(v)

print("\nDesconto 10%")
frota.aplicar_desconto(10)

for v in frota.veiculos:print(v)

frota.export_inventory()