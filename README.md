# gerenciador_tarefas

## Requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados em sua máquina:

- Docker
- Docker Compose

## Passo a Passo para Executar o Projeto

### Clonar o Repositório

1. Abra o terminal.
2. Clone o repositório do projeto com o seguinte comando:

   ```bash
   git clone https://github.com/gui-olperes/gerenciador_tarefas.git
   ```

3. Entre no diretório do projeto:

   ```bash
   cd gerenciador_tarefas
   ```

### Construir e Iniciar os Contêineres

1. **Construir os Contêineres**

   Na raiz do projeto, execute o seguinte comando para construir os contêineres definidos no `docker-compose.yml`:

   ```bash
   docker-compose build
   ```

2. **Iniciar a API**

   Execute o comando abaixo para iniciar o serviço da API:

   ```bash
   docker-compose up api
   ```

3. **Acessar a API**

   A API estará disponível no seguinte endereço:

   ```
   http://localhost:8000
   ```

4. **Parar a API**

   Para parar o serviço da API, pressione `Ctrl+C` no terminal onde ela está sendo executada ou use o comando:

   ```bash
   docker-compose down
   ```

### Executar os Testes

1. **Rodar os Testes**

   Para executar os testes do projeto, utilize o seguinte comando:

   ```bash
   docker-compose run test
   ```

2. **Resultados dos Testes**

   O resultado dos testes será exibido diretamente no terminal após a execução do comando.

## Estrutura do Projeto

O projeto possui a seguinte estrutura básica:

```
/app
├── pyproject.toml
├── poetry.lock
├── app/
│   ├── main.py
│   └── ...
├── tests/
│   ├── test_example.py
│   └── ...
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Variáveis de Ambiente

No arquivo `docker-compose.yml`, a seguinte variável de ambiente está configurada:

- `POETRY_VIRTUALENVS_CREATE=false`: Desativa a criação de ambientes virtuais pelo Poetry, permitindo que as dependências sejam instaladas diretamente no sistema do contêiner.

Se necessário, você pode adicionar outras variáveis de ambiente na seção `environment` do `docker-compose.yml`.


