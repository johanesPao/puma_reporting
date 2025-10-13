FROM python:3.13-slim-bullseye AS builder

WORKDIR /puma_reporting

COPY requirements.txt .

# Install build tools untuk beberapa modul python (pandas etc)
RUN apt-get update && apt-get install -y gcc g++ unixodbc-dev unixodbc && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim-bullseye
WORKDIR /puma_reporting
COPY --from=builder /usr/local /usr/local
COPY . .
# # Install unixodbc dan msodbcsql18
# RUN apt-get update && apt-get install -y unixodbc odbcinst curl apt-transport-https gnupg && \
#     # Menambahkan kunci repo microsoft
#     curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
#     # Menambahkan repo Microsoft SQL Server
#     echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod stable main" > /etc/apt/sources.list.d/mssql-release.list && \
#     # Install msodbcsql18
#     apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
#     # Clean up
#     rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]