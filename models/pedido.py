from datetime import date

class Pedido:
    def __init__(self, Cliente, Items, id=None):
        self.id = id
        self.Cliente = Cliente
        self.Items = Items
        self.data = date.today()
