from sqlalchemy.orm import Session
from .models import Tarefa
from .schemas import TarefaCreate, TarefaUpdate

def criar_tarefa(db: Session, tarefa: TarefaCreate):
    nova_tarefa = Tarefa(**tarefa.dict())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def listar_tarefas(db: Session, estado: str = None, skip: int = 0, limit: int = 10):
    query = db.query(Tarefa)
    if estado:
        query = query.filter(Tarefa.estado == estado)
    total = query.count()
    tarefas = query.offset(skip).limit(limit).all()
    return tarefas, total

def buscar_tarefa_por_id(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaUpdate):
    tarefa_existente = buscar_tarefa_por_id(db, tarefa_id)
    if tarefa_existente:
        for key, value in tarefa.dict(exclude_unset=True).items():
            setattr(tarefa_existente, key, value)
        db.commit()
        db.refresh(tarefa_existente)
    return tarefa_existente

def deletar_tarefa(db: Session, tarefa_id: int):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if tarefa:
        db.delete(tarefa)
        db.commit()
    return tarefa
