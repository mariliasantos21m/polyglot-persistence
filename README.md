# Polyglot Persistence Application

## Visão Geral

Este projeto demonstra o conceito de **Persistência Poliglota**, integrando múltiplos bancos de dados para diferentes necessidades de armazenamento e consulta. A aplicação permite o cadastro, consulta e visualização de pontos geográficos, além de cálculos de distância e operações espaciais.

---

## Estrutura de Pastas

```
├── app.py                # Interface Streamlit para visualização e interação
├── api.py                # API FastAPI para integração dos bancos
├── api_client.py         # Cliente para consumir a API
├── locations.db          # Banco SQLite local
├── dtos/                 # Data Transfer Objects (modelos de dados)
│   ├── geometry.py
│   └── location.py
├── mongo/                # Integração e consultas MongoDB
│   ├── db_mongo.py
│   └── query.py
├── sqlite/               # Integração e consultas SQLite
│   ├── db_sqlite.py
│   ├── query.py
│   └── tables.py
└── README.md
```

---

## Funcionalidades

- **Persistência Poliglota:** Utiliza SQLite para dados estruturados e MongoDB para dados semiestruturados.
- **Cadastro de Pontos:** Interface para cadastrar novos locais com propriedades geográficas e metadados.
- **Consulta Integrada:** Busca e visualização de pontos, independente do banco de origem.
- **Geoprocessamento:** Visualização espacial dos pontos e cálculo de distâncias geodésicas entre locais.
- **API REST:** Endpoints para manipulação dos dados e integração entre bancos.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Frameworks:**
	- [Streamlit](https://streamlit.io/) (interface web)
	- [FastAPI](https://fastapi.tiangolo.com/) (API REST)
- **Banco de Dados:**
	- SQLite (local, relacional)
	- MongoDB (NoSQL, flexível)
- **Bibliotecas:**
	- pydeck, geopy, pymongo, sqlite3

---

## Como Executar

1. **Instale as dependências:**
	 ```bash
	 pip install -r requirements.txt
	 ```
2. **Inicie o servidor FastAPI:**
	 ```bash
	 uvicorn api:app --reload
	 ```
3. **Execute a interface Streamlit:**
	 ```bash
	 streamlit run app.py
	 ```

---

## Observações

- Certifique-se de que o MongoDB está em execução e acessível.
- O banco SQLite será criado automaticamente na raiz do projeto.
- Os arquivos em `dtos/` definem os modelos de dados utilizados na integração.
- As pastas `mongo/` e `sqlite/` concentram a lógica de persistência e consulta para cada banco.

---

## Licença

Projeto acadêmico para fins de estudo e demonstração. Sinta-se livre para adaptar e evoluir conforme sua necessidade.
