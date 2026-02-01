# ERP de Gerenciamento de Clientes

## Visão Geral
Este projeto é um MVP (Produto Mínimo Viável) de um sistema ERP focado no gerenciamento de clientes, desenvolvido com FastAPI (back-end), SQLite (banco de dados) e Streamlit (front-end web). O objetivo é fornecer uma solução simples, eficiente e extensível para pequenas empresas ou equipes que precisam organizar, consultar e manter informações de clientes de forma centralizada.

## Problemas que o sistema resolve
- **Centralização de dados de clientes:** Evita informações dispersas em planilhas, e-mails ou papéis, facilitando o acesso e atualização.
- **Facilidade de cadastro e consulta:** Permite cadastrar, editar, visualizar e excluir clientes de forma rápida e intuitiva.
- **Acesso web:** Interface amigável via navegador, sem necessidade de instalar aplicativos pesados.
- **API RESTful pronta para integrações:** Possibilita integração com outros sistemas, automações ou relatórios.
- **Controle de status:** Permite marcar clientes como ativos/inativos, facilitando o acompanhamento de relacionamento.

## Funcionalidades
- Cadastro de clientes (nome, e-mail, telefone, endereço, status)
- Listagem e busca de clientes
- Edição e exclusão de registros
- Visualização de detalhes do cliente
- Interface web (Streamlit) para uso prático
- API REST (FastAPI) para integrações

## Tecnologias Utilizadas
- **FastAPI:** Framework moderno para criação de APIs rápidas e seguras.
- **SQLite:** Banco de dados leve, ideal para MVPs e fácil de migrar para outros bancos.
- **SQLAlchemy:** ORM para manipulação de dados de forma segura e produtiva.
- **Streamlit:** Framework para criação de interfaces web interativas em Python.
- **Pydantic:** Validação de dados e schemas para a API.
- **Uvicorn:** Servidor ASGI para rodar o FastAPI.

## Estrutura do Projeto
```
backend/
  main.py         # API FastAPI
  models.py       # Modelos ORM
  database.py     # Conexão e setup do banco
  crud.py         # Operações CRUD
frontend/
  app.py          # Interface Streamlit
requirements.txt  # Dependências do projeto
```

## Como Executar
1. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```
2. **Inicie o back-end (API):**
   ```
   uvicorn backend.main:app --reload
   ```
3. **Inicie o front-end (Streamlit):**
   ```
   streamlit run frontend/app.py
   ```
4. **Acesse a interface web:**
   - Normalmente em http://localhost:8501

## Possibilidades de Expansão
- Cadastro de produtos, vendas, ordens de serviço, etc.
- Relatórios gerenciais
- Controle de permissões de usuários
- Integração com sistemas de faturamento, e-mail, WhatsApp
- Deploy em nuvem

## Público-Alvo
- Pequenas empresas
- Prestadores de serviço
- Equipes comerciais
- Startups que precisam de um CRM/ERP simples e rápido

## Observações
- O sistema é um MVP e pode ser facilmente expandido.
- O uso de SQLite facilita testes e implantação inicial.
- O código é todo em Python, facilitando manutenção e customização.

---
Desenvolvido para ser simples, didático e pronto para evoluir conforme as necessidades do negócio.