from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app  
from app.models import Usuario
from app.database import SessionLocal, Base
from app.auth import criar_token_acesso
import pytest

user_test = "test_usuario"
senha_test = "test_senha"
 

# Fixture para o cliente de testes 
@pytest.fixture
def client():
    return TestClient(app)

# Testa o registro de um novo usuário
def test_registrar_usuario(client):
    usuario_data = {
        "username": user_test,
        "senha": senha_test
    }

    response = client.post("/usuarios/", json=usuario_data)
    if response.status_code == 200:
        assert "id" in response.json()
    else:
        assert response.status_code == 400
        assert response.json().get("detail") == "Usuário já existe" 

# Fixture para obter o token de autenticação
@pytest.fixture
def token(client):
    usuario_data = {
        "username": user_test,
        "senha": senha_test
    }

    response = client.post("/login/", json=usuario_data)
    
    assert response.status_code == 200
    assert "access_token" in response.json()

    return response.json()["access_token"]

# Testa a criação de uma tarefa 
def test_criar_tarefa(client, token):
    tarefa_data = {
        "titulo": "Test",
        "descricao": "Test",
        "estado": "em andamento"
    }

    response = client.post(
        "/tarefas/", 
        json=tarefa_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["titulo"] == tarefa_data["titulo"]

# Testa a listagem de tarefas
def test_listar_tarefas(client, token):
    response = client.get(
        "/tarefas/", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json()["tarefas"], list) 

# Testa a listagem de tarefas sem estar autenticado
def test_listar_tarefas_sem_autenticacao(client, token):
    response = client.get("/tarefas/")
    
    assert response.status_code == 403

# Testa o filtro de estado de tarefas
def test_listar_tarefas_com_estado(client, token):
    tarefa_data = {
        "titulo": "Tarefa Pendente",
        "descricao": "Descrição da tarefa",
        "estado": "pendente"
    }
    
    # Cria a tarefa
    client.post(
        "/tarefas/", 
        json=tarefa_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = client.get(
        "/tarefas/?estado=pendente", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert len(response.json()["tarefas"]) > 0

# Testa editar uma tarefa
def test_editar_tarefas_com_estado(client, token):
    tarefa_data_criar = {
        "titulo": "Tarefa para Editar",
        "descricao": "Descrição da tarefa para editar",
        "estado": "em andamento"
    }

    # Criação da tarefa
    response_criar = client.post(
        "/tarefas/", 
        json=tarefa_data_criar, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response_criar.status_code == 200
    tarefa_id = response_criar.json()["id"]

    tarefa_data_editar = {
        "titulo": "Tarefa Editada",
        "descricao": "Tarefa Editada",
        "estado": "concluida"
    }
    
    # Editando a tarefa
    response_editar = client.put(
        f"/tarefas/{tarefa_id}", 
        json=tarefa_data_editar,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response_editar.status_code == 200

    # Recuperando a tarefa editada
    response_get = client.get(
        "/tarefas/?estado=concluida", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response_get.status_code == 200
    tarefas = response_get.json()["tarefas"]
    assert len(tarefas) > 0  
    assert tarefas[0]["estado"] == "concluida"  

def test_deletar_tarefas_com_estado(client, token):
    tarefa_data = {
        "titulo": "Tarefa para deletar",
        "descricao": "Descrição da tarefa para deletar",
        "estado": "em andamento"
    }
    
    # Criação da tarefa
    response = client.post(
        "/tarefas/", 
        json=tarefa_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    tarefa_id = response.json()["id"]

    # Deletando a tarefa
    response_delete = client.delete(
        f"/tarefas/{tarefa_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response_delete.status_code == 200
    
    # Verificando se a tarefa foi realmente deletada
    response_get = client.get(
        f"/tarefas/{tarefa_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response_get.status_code == 404
    assert "detail" in response_get.json() 
