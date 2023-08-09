FROM python:latest

WORKDIR /app

RUN pip install --upgrade pip

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["python", "app.py"]