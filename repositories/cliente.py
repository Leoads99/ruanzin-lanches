from models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db):
        self.__db = db

    def get(self, id=None):
        cursor = self.__db.connection.cursor()
        if (id):
            sql_command = "SELECT id, nome, cpf from cliente WHERE id = %s"

            cursor.execute(sql_command, (id,))

            tupla = cursor.fetchone()

            clientes = Cliente(tupla[1], tupla[2], id=tupla[0])
        else:
            sql_command = "SELECT id, nome, cpf from cliente"
            cursor.execute(sql_command)
            clientes = self.transform_cliente(cursor.fetchall())

        return clientes

    def save(self, cliente):
        cursor = self.__db.connection.cursor()

        if(cliente.id):
            sql_command = "UPDATE cliente SET nome=%s, cpf=%s where id=%s"
            cursor.execute(sql_command, (cliente.nome,
                                         cliente.cpf, cliente.id))
        else:
            sql_command = "INSERT INTO cliente(nome, cpf) VALUES (%s, %s)"
            cursor.execute(sql_command, (cliente.nome,
                                         cliente.cpf))

        self.__db.connection.commit()

        return cliente

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        sql_command = "DELETE FROM cliente WHERE id = %s"
        cursor.execute(sql_command, (id,))

        self.__db.connection.commit()

    def transform_cliente(self, clientes):
        def create_cliente_tuple(tupla):
            return Cliente(tupla[1], tupla[2], id=tupla[0])
        return list(map(create_cliente_tuple, clientes))
