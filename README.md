# 🌤️ Pipeline ETL de Dados Meteorológicos (SP)

Este projeto é um pipeline de dados ponta a ponta que extrai, transforma e carrega dados climáticos da cidade de São Paulo em tempo real. Ele utiliza uma arquitetura moderna de engenharia de dados, totalmente conteinerizada com Docker.

## 🏗️ Arquitetura e Tecnologias

- **Extração**: Python (Requests) consumindo a API do OpenWeatherMap.
- **Transformação**: Pandas para limpeza, normalização e tratamento de fuso horário.
- **Carga**: PostgreSQL para armazenamento persistente via SQLAlchemy.
- **Orquestração**: Apache Airflow para agendamento das tarefas (uma vez por hora).
- **Visualização**: Streamlit para um dashboard interativo com insights em tempo real.
- **Infraestrutura**: Docker e Docker Compose para isolamento e facilidade de execução.

## 📂 Estrutura do Projeto

- `dags/`: Contém o arquivo `weather_dag.py` que define o fluxo do Airflow.
- `src/`: Scripts principais de extração, transformação e carga dos dados.
- `dashboard/`: Código da aplicação Streamlit e seu Dockerfile específico.
- `config/`: Localização do arquivo `.env` (credenciais e configurações).
- `data/`: Armazenamento temporário de arquivos brutos (JSON/Parquet).

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados.
- Uma `API_KEY` válida do OpenWeatherMap no arquivo `config/.env`.

### Passo a Passo
1. Clone o repositório.
2. Certifique-se de que o arquivo `config/.env` está configurado corretamente.
3. Na raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```

## 🔗 Acessos

- **Airflow UI**: [http://localhost:8080](http://localhost:8080) (Login padrão: `airflow` / `airflow`)
- **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
- **PostgreSQL**: Porta `5433` (externa) para conexão via DBeaver/outras ferramentas.

## 🔄 Fluxo de Dados (ETL)

1. **Extract**: Obtém o JSON da API do OpenWeatherMap para São Paulo.
2. **Transform**: Normaliza as colunas aninhadas, converte temperaturas e ajusta os timestamps para o fuso horário `America/Sao_Paulo`.
3. **Load**: Verifica se o registro já existe no banco (pelo horário) e insere apenas dados novos na tabela `sp_weather`.
