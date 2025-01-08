from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app.schemas import Tarefa, TarefaCreate, TarefaUpdate
from app.crud import criar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa

# Inicializa as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Função para gerenciar sessões de banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tarefas/", response_model=Tarefa)
def criar_nova_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return criar_tarefa(db, tarefa)

@app.get("/tarefas/", response_model=list[Tarefa])
def listar_todas_as_tarefas(db: Session = Depends(get_db)):
    return listar_tarefas(db)

@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def visualizar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa_existente(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    tarefa_atualizada = atualizar_tarefa(db, tarefa_id, tarefa)
    if not tarefa_atualizada:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa_atualizada

@app.delete("/tarefas/{tarefa_id}")
def deletar_uma_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa_deletada = deletar_tarefa(db, tarefa_id)
    if not tarefa_deletada:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"detail": "Tarefa deletada com sucesso"}
