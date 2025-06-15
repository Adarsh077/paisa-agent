FROM python:3.13.3-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002

# CMD ["mcp", "dev", "server.py"]
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]
