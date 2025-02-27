from flask import Flask, jsonify, request
from flask_cors import CORS  # Importe a biblioteca CORS
import mysql.connector


USER = "root"
PASSWORD = "my5ql"
DATABASE = "pizzaria"
HOST = "localhost"

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas


# Função para conectar ao banco de dados (mesma função do exemplo anterior)
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return conexao
    except mysql.connector.Error as err:
        return None

# Rota para consultar pedidos por cliente
@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    cliente_id = request.args.get('cliente_id')  # Obtém o cliente_id da query string
    if not cliente_id:
        return jsonify({"error": "cliente_id é obrigatório"}), 400

    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
            SELECT p.PedidoID, p.DataPedido, p.Status, p.Total, c.Nome AS Cliente
            FROM Pedidos p
            JOIN Clientes c ON p.ClienteID = c.ClienteID
            WHERE p.ClienteID = %s
            """
            cursor.execute(query, (cliente_id,))
            resultados = cursor.fetchall()

            if resultados:
                return jsonify(resultados)  # Retorna os resultados em JSON
            else:
                return jsonify([])  # Retorna uma lista vazia
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conexao.close()
    else:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)