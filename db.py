# db.py
from pymongo import MongoClient

def get_db():
    uri = "mongodb+srv://bibliotecaluizcarlos:dqgFXFlBUGfNw8ky@cluster0.vlfmpuv.mongodb.net/"
    client = MongoClient(uri)
    db = client["fardas"]

    return {
        "usuarios": db["fardasDB"],
        "cadastro": db["cadastro"],
        "produtos": db["produtos"],
        "movimentacao": db["movimentacao"],
        "alunos": db["alunos"],
        "movimentacao_aluno": db["movimentacao_aluno"]
    }
