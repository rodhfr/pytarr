FROM python:3.9

COPY . /app
WORKDIR /app
RUN groupadd -g $GROUP_ID appgroup && useradd -u $USER_ID -g $GROUP_ID -m appuser
RUN chown -R appuser:appgroup /app && chmod -R g=u /app
USER appuser
VOLUME /app/Videos
RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y



CMD ["python", "app.py"]
