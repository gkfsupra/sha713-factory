
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000 1883
CMD ["python","bridge/mqtt_bridge.py"]
