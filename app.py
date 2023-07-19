import os
import subprocess
import shutil

def process_file(file_path, converted_files):
    file_dir, file_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_name)

    if file_ext.lower() in ['.mkv', '.mp4'] and not file_name.endswith(' - 720p'):
        output_file_name = f"{file_name} - 720p{file_ext}"
        output_path = os.path.join(file_dir, output_file_name)

        if not os.path.exists(output_path):
            subprocess.call(['ffmpeg', '-i', file_path, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-s', '1280x720', '-crf', '24', '-x264-params', 'profile=main', '-map', '0', '-c:a', 'copy', '-c:s', 'copy', '-preset', 'veryfast', '-tune', 'fastdecode', output_path])
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

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path, converted_files)

    with open(record_file, 'w') as file:
        file.write('\n'.join(converted_files))

target_directory = '/app/Videos'
process_directory(target_directory)
