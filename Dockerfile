FROM python:3.14-slim

WORKDIR /puma_reporting

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]