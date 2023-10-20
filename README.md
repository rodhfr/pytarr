# Hello, this software do not work well in any shape or form. Is made for study only.
 
 ## prototyping some ideas for a simple docker container project
I'm just a python script 🐍 that crawls over you media library and constantly searching for all mkv, mp4 or avi files to a copy of them using x264 8bit while appending `"- 720p"` which is useful for jellyfin identification. 
My ffmpeg command to transcode is easily modifiable inside `app.py` file.

I do preserve original video files in the same folder👌. Also, all subtitles and audio tracks are copied to the transcoded file so you don't have to search for them again 🐊. 

 ## Exclusion Mechanism
The script places a `converted_files.txt` in your media library, none of the titles inside the txt will be rendered again. If you exclude the txt, the program will render the same video files again, creating another `converted_files.txt`.

* A webapp that can customize the ffmpeg options and watch progress is planned someday in the future when my coding skills are at least decent 😸.

🆓 Source code https://github.com/rodhfr/pytarr 

📦 Docker compose: https://github.com/rodhfr/pytarr/blob/main/docker-compose.yml

## Fast spin:

```yml
version: '3.9'
services:
  my-service:
    image: pytarr:0.4
    volumes:
      - /path/to/media/file/:/app/Videos
    restart: unless-stopped
    environment:
      - TZ=America/Recife
      - PUID=1000
      - PGID=1000 
    command: bash -c "sleep 300 && python app.py"
```
