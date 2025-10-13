FROM python:3.14-slim

WORKDIR /puma_reporting

COPY . .

# Install git sebelum pip install untuk install mssql-python dari github
RUN apt-get update && apt-get install -y \
    # Install build dependencies yang dibutuhkan beberapa modul python
    gcc \
    g++ \
    make \
    libtool \
    libkrb5-3 \
    libgssapi-krb5-2 \
    libltdl7 \
    krb5-user \
    git \
    # Clean up
    && rm -rf /var/libs/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]