FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/Videos

CMD ["python", "app.py"]
