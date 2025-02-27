from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel
from typing import List

USER = "root"
PASSWORD = "my5ql"
DATABASE = "pizzaria"
HOST = "localhost"

# Configuração do FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_methods=["GET"],  # Métodos permitidos
    allow_headers=["*"],  # Cabeçalhos permitidos
)


class Pedido(BaseModel):
    """ Modelo de representação de um pedido"""
    PedidoID: int
    DataPedido: str
    Status: str
    Total: float
    Cliente: str


def conectar_banco():
    """ Conecta ao banco de dados"""
    try:
        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return conexao
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco de dados: {err}")

@app.get("/api/pedidos", response_model=List[Pedido])
def get_pedidos(cliente_id: int = Query(..., description="ID do cliente")):
    """ Rota para consultar pedidos de clientes"""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """
            SELECT p.PedidoID AS PedidoID, DATE_FORMAT(p.DataPedido, %s)
            AS DataPedido,
            p.Status AS Status, CAST(p.Total AS DECIMAL(10, 2)) AS Total,
            c.Nome AS Cliente
            FROM Pedidos p
            JOIN Clientes c ON p.ClienteID = c.ClienteID
            WHERE p.ClienteID = %s
            """
            # Passa o valor de cliente_id como uma tupla
            cursor.execute(query, ('%Y-%m-%d %H:%i:%s', cliente_id,))
    
            resultados = cursor.fetchall()

            if resultados:
                return resultados  # FastAPI automaticamente converte para JSON
            else:
                return []  # Retorna uma lista vazia em JSON
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Erro ao executar a consulta: {err}")
        finally:
            cursor.close()
            conexao.close()
    else:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")


# Iniciar o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,)