from fastapi import FastAPI
from datetime import datetime

LISTA_TAREFAS = []
APP = FastAPI()

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

@APP.get("/")
def index():
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []
    
    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}
    if len(LISTA_TAREFAS) == 0:
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao

# Implementar!
# @APP.post("/tarefas")
@APP.post("/tarefas")
def criar_tarefa(id: int, titulo: str, descricao: str):

    # Verifica se já existe uma tarefa com o mesmo ID
    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            return {"mensagem": "TAREFA JÁ EXISTE"}

    tarefa = nova_tarefa(id, titulo, descricao)
    LISTA_TAREFAS.append(tarefa)

    return {"mensagem": "OK"}

# @APP.put("/tarefas/{id}")
@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str, descricao: str, concluido: bool):

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            tarefa["titulo"] = titulo
            tarefa["descricao"] = descricao
            tarefa["concluido"] = concluido

            return {"mensagem": "OK"}

    return {"mensagem": "TAREFA NÃO EXISTE"}

# @APP.delete("/tarefas")
@APP.delete("/tarefas/{id}")
def deletar_tarefa_especifica(id: int):
    if len(LISTA_TAREFAS) == 0:
        return {"mensagem": "Não existe nenhuma tarefa"}

    # Verifica se o índice existe
    if 0 <= id < len(LISTA_TAREFAS):
        del LISTA_TAREFAS[id]
        return {"mensagem": "Tarefa excluída com sucesso"}

    return {"mensagem": "Tarefa não encontrada"}