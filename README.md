It's just a python script 🐍 that crawls over you media library and constantly searches for all mkv, mp4 or avi files, then converts a copy of them using x264 8bit while appending `"- 720p"` which is useful for jellyfin identification. 
The ffmpeg command is easily modifiable inside `app.py` file.

Original video file is preserved in the same folder. All subtitles and audio tracks are preserved to the rendered file. 

 ## Exclusion Mechanism
The script places a `converted_files.txt` in your media library, none of the titles inside of the txt will be rendered again. If you exclude the txt the script, the program will render the same video files again, creating another `converted_files.txt`.

A webapp that can customize the ffmpeg options is planned someday in the future when my coding skills are at least decent.

Source code https://github.com/rodhfr/pytarr 

Docker compose: https://github.com/rodhfr/pytarr/blob/main/docker-compose.yml

Fast spin:

```yml
version: '3.9'
services:
  my-service:
    image: pytarr:0.3
    volumes:
      - /path/to/media/file/:/app/Videos
    restart: unless-stopped
    environment:
      - TZ=America/Recife
      - PUID=1000
      - PGID=1000 
    command: bash -c "sleep 300 && python app.py"
```
