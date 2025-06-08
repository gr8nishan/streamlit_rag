FROM python:3.12-slim

RUN apt-get update && apt-get install -y libgl1
RUN apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8888"]
EXPOSE 8888