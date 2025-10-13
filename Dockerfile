FROM python:3.14-slim

WORKDIR /puma_reporting

COPY . .

# Install git sebelum pip install untuk install mssql-python dari github
RUN apt-get update && apt-get install -y git && rm -rf /var/libs/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]