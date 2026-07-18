from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from datetime import datetime

import requests
import logging

LOGGER = logging.getLogger("devops")
LOGGER.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
file_handler   = logging.FileHandler(f"{LOGGER.name}.log", encoding='utf-8')
formatador     = logging.Formatter(fmt="%(name)s | %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s")

stream_handler.setFormatter(formatador)
file_handler.setFormatter(formatador)
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(file_handler)


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

def verificar_existencia_tarefa(id: int):
    """Função auxiliar para verificar a existência de uma tarefa com base no seu ID"""
    for tarefa in LISTA_TAREFAS:
        if id == tarefa['id']:
            return True
    return False

@APP.get("/")
def index():
    LOGGER.info("Acesso à rota GET /")
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    LOGGER.info("Acesso à rota GET /tarefas")

    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []

    for tarefa in LISTA_TAREFAS:
        tarefas.append({
            "id": tarefa["id"],
            "titulo": tarefa["titulo"]
        })

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    LOGGER.info("GET /tarefas/%s", id)

    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}
    if len(LISTA_TAREFAS) == 0:
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao

# Implementar!
# @APP.post("/tarefas")
# Rota /tarefas (POST)
#   Entrada: id da tarefa (int), titulo da tarefa (str) e descrição da tarefa (str)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Cria uma nova tarefa usando a função `nova_tarefa`
#       - Adiciona nova tarefa a LISTA_TAREFAS
#   # Saída:
#       - Retorna "OK" se a tarefa foi criada
#       - Se a tarefa existir, retornar "TAREFA JÁ EXISTE"

@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    LOGGER.info(
        "POST /tarefas | id=%s titulo='%s' descricao='%s'",
        id,
        titulo,
        descricao
    )

    if tarefa_existe:
        ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
        raise ex
    
    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    return {"mensagem": "OK"}

# @APP.put("/tarefas/{id}")
# Rota /tarefas/{id} (PUT)
#   Entrada: id da tarefa (int), titulo da tarefa (str), descrição da tarefa (str) e concluido (bool)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Atualiza informações da tarefa de id específico
#   # Saída:
#       - Retorna "OK" se a tarefa foi atualizada
#       - Se a tarefa NÃO existir, retornar "TAREFA NÃO EXISTE"
@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    LOGGER.info(
        "PUT /tarefas/%s | titulo='%s' descricao='%s' concluido=%s",
        id,
        titulo,
        descricao,
        concluido
    )


    if not tarefa_existe:
        return {"mensagem": "TAREFA NÃO EXISTE!"}
    
    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    if titulo != "":
        LISTA_TAREFAS[indice]['titulo'] = titulo
    
    if descricao !=  "":
        LISTA_TAREFAS[indice]['descricao'] = descricao
    
    if concluido == True:
        requests.post(
            f"http://notificacoes:8000/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}",
            timeout=10
        )

    LISTA_TAREFAS[indice]['concluido'] = concluido

    return {"mensagem": "OK"}

# @APP.delete("/tarefas")
# Rota /tarefas/{id} (DELETE)
#   Entrada: id da tarefa (int)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Busca pela tarefa com base no ID
#       - Se tarefa existir, remover de LISTA_TAREFAS
#       - Se NÃO existir, retorna "TAREFA NÃO EXISTE"
#   # Saída:
#       - Retorna "OK" se a tarefa foi removida
#       - Se a tarefa NÃO existir, retornar "TAREFA NÃO EXISTE"
@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    LOGGER.info("DELETE /tarefas/%s", id)

    if not verificar_existencia_tarefa(id):
        LOGGER.warning("Tentativa de remover tarefa inexistente. id=%s", id)
        return {"mensagem": "TAREFA NÃO EXISTE"}

    for indice, tarefa in enumerate(LISTA_TAREFAS):
        if tarefa["id"] == id:
            break

    LOGGER.info("Removendo tarefa '%s'", tarefa["titulo"])

    LISTA_TAREFAS.pop(indice)

    LOGGER.info("Tarefa %s removida com sucesso.", id)

    return {"mensagem": "OK"}