from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Usuario
from app.schemas import Tarefa, TarefaCreate, TarefaUpdate, UsuarioCreate, UsuarioResponse
from app.crud import criar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa
from app.auth import criar_token_acesso, gerar_hash_senha, verificar_senha, verificar_token

# Inicializa as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

api_key_header = APIKeyHeader(name="Authorization")

app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="API para criar, listar, atualizar e deletar tarefas",
    version="1.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def obter_usuario_atual(authorization: str = Depends(api_key_header)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization header must start with Bearer"
        )
    token = authorization[7:]
    try:
        payload = verificar_token(token) 
        return payload.get("sub")  
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@app.post("/usuarios/", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    usuario_db = Usuario(username=usuario.username, senha=gerar_hash_senha(usuario.senha))
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@app.post("/login/")
def login_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token_acesso({"sub": usuario_db.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tarefas/", response_model=Tarefa)
def criar_nova_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db), usuario: str = Depends(obter_usuario_atual)):
    return criar_tarefa(db, tarefa)

@app.get("/tarefas/", response_model=list[Tarefa])
def listar_todas_as_tarefas(db: Session = Depends(get_db), usuario: str = Depends(obter_usuario_atual)):
    return listar_tarefas(db)

@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def visualizar_tarefa(tarefa_id: int, db: Session = Depends(get_db), usuario: str = Depends(obter_usuario_atual)):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa_existente(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db), usuario: str = Depends(obter_usuario_atual)):
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
