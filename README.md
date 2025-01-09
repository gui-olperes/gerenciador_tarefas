# gerenciador_tarefas

## Requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados em sua máquina:

- Docker

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

   A documentação da API estará disponível no seguinte endereço:

   ```
   http://localhost:8000/docs
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

## Autenticação da API

Para utilizar os endpoints de tarefa, siga os passos abaixo para realizar a autenticação:

1. **Registrar um Usuário**
   - Acesse o endpoint `/usuarios` para registrar um novo usuário.

2. **Realizar Login**
   - Utilize o endpoint `/login` para autenticar o usuário registrado.
   - O endpoint retornará um token.

3. **Adicionar o Token à Requisição**
   - **Via Interface `/docs`**:
     - Clique no botão "Authorize" e insira o token no formato `Bearer token`.
   - **Via Requisição Externa**:
     - Inclua o token no cabeçalho da requisição com a seguinte estrutura:
       ```json
       {
         "Authorization": "Bearer token"
       }
       ```

Após realizar a autenticação, você terá acesso a todos os endpoints disponíveis na API.



