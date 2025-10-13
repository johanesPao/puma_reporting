FROM python:3.13-slim

WORKDIR /puma_reporting

COPY . .

# Install git sebelum pip install untuk install mssql-python dari github
RUN apt-get update && apt-get install -y \
    # Install build dependencies yang dibutuhkan beberapa modul python
    gcc \
    g++ \
    make \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    curl \
    apt-transport-https \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    # Clean up
    && rm -rf /var/libs/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]