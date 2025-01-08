from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
        
class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    estado: str

class TarefaCreate(TarefaBase):
    pass

class TarefaUpdate(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    estado: Optional[str]

class Tarefa(TarefaBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True