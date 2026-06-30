from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

app = FastAPI(title="API Diagnostico Dados")

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["alunos"]

class Aluno(BaseModel):
    nome: str
    nota: float
    turma: str

@app.get("/")
def read_root():
    return {"status": "API OK"}

@app.get("/alunos")
def listar_alunos():
    alunos = list(collection.find({}, {"_id": 0}))
    return alunos

@app.post("/alunos")
def criar_aluno(aluno: Aluno):
    collection.insert_one(aluno.dict())
    return {"mensagem": "Aluno criado com sucesso"}