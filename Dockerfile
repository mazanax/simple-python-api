FROM python:3.12-slim

WORKDIR /app

RUN pip install flask

COPY app.py tag commit /app/

EXPOSE 8000

CMD ["python", "app.py"]
