import os
import subprocess
import shutil
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ffmpeg_command = request.form['ffmpeg_command']
        save_ffmpeg_command(ffmpeg_command)
        return 'FFmpeg command updated successfully!'
    else:
        ffmpeg_command = get_ffmpeg_command()
        return render_template('index.html', ffmpeg_command=ffmpeg_command)

def process_file(file_path, converted_files, ffmpeg_command):
    file_dir, file_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_name)

    if file_ext.lower() in ['.mkv', '.mp4'] and not file_name.endswith(' - 720p'):
        output_file_name = f"{file_name} - 720p{file_ext}"
        output_path = os.path.join(file_dir, output_file_name)

        if not os.path.exists(output_path):
            command = ['ffmpeg', '-i', file_path] + ffmpeg_command.split() + ['-map', '0', '-c:a', 'copy', '-c:s', 'copy', '-preset', 'medium', '-tune', 'fastdecode', output_path]
            subprocess.call(command)
            copy_file(file_path, output_file_name, '.srt')
            copy_file(file_path, output_file_name, '.nfo')
        
        converted_files.add(file_name)

def copy_file(file_path, output_file_name, file_extension):
    file_dir, file_name = os.path.split(file_path)
    file_name, _ = os.path.splitext(file_name)
    source_file_path = os.path.join(file_dir, file_name + file_extension)

    if os.path.exists(source_file_path):
        dest_file_path = os.path.join(file_dir, f"{output_file_name}{file_extension}")
        shutil.copy2(source_file_path, dest_file_path)

def process_directory(directory):
    converted_files = set()
    record_file = os.path.join(directory, 'converted_files.txt')

    if os.path.exists(record_file):
        with open(record_file, 'r') as file:
            converted_files = set(file.read().splitlines())

    ffmpeg_command = get_ffmpeg_command()

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path, converted_files, ffmpeg_command)

    with open(record_file, 'w') as file:
        file.write('\n'.join(converted_files))

def save_ffmpeg_command(ffmpeg_command):
    with open('ffmpeg_command.txt', 'w') as file:
        file.write(ffmpeg_command)

def get_ffmpeg_command():
    if os.path.exists('ffmpeg_command.txt'):
        with open('ffmpeg_command.txt', 'r') as file:
            return file.read()
    else:
        return ''

if __name__ == '__main__':
    target_directory = '/home/rodhfr/Videos/Rodolfo/filme/root/'
    process_directory(target_directory)
    app.run(host='0.0.0.0', port=5000)

