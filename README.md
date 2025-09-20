# Polyglot Persistence Application

## Descrição do Projeto

Este projeto tem como objetivo desenvolver uma aplicação prática utilizando **Persistência Poliglota**, combinando diferentes bancos de dados para atender a contextos variados:  

- **SQLite**: para armazenamento local, rápido e leve de dados estruturados.  
- **MongoDB**: para dados semiestruturados, permitindo maior flexibilidade e escalabilidade.  

Além disso, a aplicação incorpora **recursos de geoprocessamento**, manipulando objetos JSON para armazenar, consultar e visualizar dados espaciais (latitude e longitude).

---

## Funcionalidades

- Armazenamento de dados em múltiplos bancos de dados (SQLite e MongoDB).  
- Consulta de dados de forma integrada, independente do banco de origem.  
- Manipulação de informações geográficas usando JSON, incluindo latitude e longitude.  
- Visualização de dados espaciais para análises geográficas e geoprocessamento.

---

## Tecnologias Utilizadas

- **Banco de dados:** SQLite, MongoDB  
- **Linguagem de programação:** [especificar linguagem usada, ex: Python, Java, C#]  
- **Manipulação de JSON:** Para geoprocessamento e integração com bancos NoSQL  
- **Bibliotecas de apoio:** [listar bibliotecas relevantes, ex: PyMongo, GeoJSON, SQLite3]

---

## Execução

1. Executar servidor http: `uvicorn api:app --reload`
2. Excutar streamlit: `streamlit run app.py`
