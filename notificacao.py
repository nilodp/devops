from fastapi import FastAPI
from datetime import datetime

APP_NOTIFICACAO = FastAPI()

# Criar uma rota para receber tarefa finalizada
# APP_NOTIFICACAO.post("/notificar")
# Entrada:
#   - Recebe título da tarefa e data de finalização da tarefa
# Saída:
#   - print no terminal

@APP_NOTIFICACAO.post("/notificar")
def notificar_tarefa(titulo: str, dataFinalizacao: datetime):
    print(f"Tarefa finalizada: {titulo}")
    print(f"Data de finalização: {dataFinalizacao}")

    return {"mensagem": "OK"}