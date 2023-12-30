FROM python:3.12

WORKDIR /app

RUN groupadd -r myuser && useradd -r -g myuser myuser
RUN chown -R myuser:myuser /app

RUN pip install --upgrade pip

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:8000/ || exit 1

USER myuser

CMD ["python", "app.py"]
