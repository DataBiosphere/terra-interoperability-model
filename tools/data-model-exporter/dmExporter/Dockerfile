# syntax=docker/dockerfile:1
FROM python:3.10.0-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "data_model_exporter/dmExporter.py"]