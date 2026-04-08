FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos de requisitos
COPY pyproject.toml .
COPY README.md .

# Copiar o código fonte
COPY src/ src/
COPY dashboard/ dashboard/
COPY config/ config/

# Instalar as dependências do python
RUN pip install --no-cache-dir .

# Expor a porta que o streamlit usa
EXPOSE 8501

# Comando para rodar o streamlit
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
