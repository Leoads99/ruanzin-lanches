from models.pedido import Pedido
from models.item import Item


class PedidoRepository:
    def __init__(self, db):
        self.__db = db

    def get(self, id=None):
        cursor = self.__db.connection.cursor()
        if (id):
            sql_command = "SELECT p.id, c.id, pr.nome, i.quantidade from pedido p INNER JOIN cliente c ON c.id = p.id_cliente INNER JOIN item_pedido ip on ip.id_pedido = p.id INNER JOIN item i on i.id = ip.id_item INNER JOIN produto pr on pr.id = i.id_produto WHERE p.id = %s"

            cursor.execute(sql_command, (id,))

            pedido = self.transform_pedido_unique(cursor.fetchall())
        else:
            sql_command = "SELECT p.id, c.nome from pedido p INNER JOIN cliente c ON c.id = p.id_cliente WHERE p.ativo = 1"
            cursor.execute(sql_command)
            pedido = self.transform_pedido(cursor.fetchall())

        return pedido

    def save(self, pedido):
        cursor = self.__db.connection.cursor()

        if(pedido.id):
            sql_command = "UPDATE pedido SET nome=%s, cpf=%s where id=%s"
            cursor.execute(sql_command, (pedido.nome,
                                         pedido.cpf, pedido.id))
        else:
            sql_command = "INSERT INTO pedido(id_cliente, data, ativo) VALUES (%s, %s, %s)"
            cursor.execute(sql_command, (pedido.Cliente,
                                         pedido.data, 1))
            pedidoId = cursor.lastrowid
            for item in pedido.Items:
                sql_command = "INSERT INTO item(id_produto, quantidade) VALUES(%s, %s)"

                cursor.execute(sql_command, (item['produtoId'], item['qtd']))
                itemId = cursor.lastrowid

                sql_command = "INSERT INTO item_pedido(id_item, id_pedido) VALUES (%s, %s)"
                cursor.execute(sql_command, (itemId, pedidoId))

        self.__db.connection.commit()

        return pedido

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        sql_command = "UPDATE pedido SET ativo = 0 WHERE id = %s"
        cursor.execute(sql_command, (id,))

        self.__db.connection.commit()

    def transform_pedido_unique(self, pedidos):
        def create_pedido_tuple(tupla):
            return Pedido(tupla[1], Items=[tupla[2], tupla[3]], id=tupla[0])
        return list(map(create_pedido_tuple, pedidos))

    def transform_pedido(self, pedidos):
        def create_pedido_tuple(tupla):
            return Pedido(tupla[1], Items=None, id=tupla[0])
        return list(map(create_pedido_tuple, pedidos))
