# Use uma imagem oficial do Python
FROM python:3.10

# Configuração para evitar buffer no log
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie apenas os arquivos necessários para evitar cache excessivo
COPY requirements.txt /app/requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . /app

# Exponha a porta onde o FastAPI será executado
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8011"]