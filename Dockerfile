FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

ENV PUID=1000
ENV PGID=1000

# Set user and group with specified UID and GID from the environment variables
RUN groupadd -g $PGID appgroup && useradd -u $PUID -g $PGID -m appuser
# Set group permissions for the /app directory and its contents using the appuser user and appgroup group
RUN chown -R appuser:appgroup /app && chmod -R g=u /app

USER appuser

VOLUME /app/Videos



CMD ["python", "app.py"]
