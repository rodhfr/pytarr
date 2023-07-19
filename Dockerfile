FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

VOLUME /app/Videos

CMD ["python", "app.py"]
