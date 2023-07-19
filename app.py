import os
import re
import subprocess
import shutil
import tempfile

def extract_resolution(filename):
    # Use regular expression to extract the resolution from the filename
    match = re.search(r'-(\d+p)', filename)
    return match.group(1) if match else ""

def process_file(file_path, converted_files):
    file_dir, file_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_name)

    if file_ext.lower() in ['.mkv', '.mp4'] and not file_name.endswith(' - 720p'):
        original_resolution = extract_resolution(file_name)
        output_file_name = file_name.replace(original_resolution, ' 720p') + file_ext
        output_path = os.path.join(file_dir, output_file_name)

        if not os.path.exists(output_path):
            # Create a temporary cache file with the .part extension inside the .cache folder
            cache_dir = os.path.join(file_dir, '.cache')
            os.makedirs(cache_dir, exist_ok=True)
            temp_output_path = os.path.join(cache_dir, f"{output_file_name}.part")

            subprocess.call(['ffmpeg', '-i', file_path, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-s', '1280x720', '-crf', '24', '-x264-params', 'profile=main', '-map', '0', '-c:a', 'copy', '-c:s', 'copy', '-preset', 'veryfast', '-tune', 'fastdecode', temp_output_path])

            # Move the temporary cache file to the final output path
            os.rename(temp_output_path, output_path)

            # Copy .srt files
            copy_file(file_path, file_name, '.srt')
            copy_file(file_path, file_name, '.nfo')

            # Copy .en.srt files
            srt_file_path = os.path.join(file_dir, f"{file_name}.en.srt")
            if os.path.exists(srt_file_path):
                dest_srt_file_path = os.path.join(file_dir, f"{output_file_name}.en.srt")
                shutil.copy2(srt_file_path, dest_srt_file_path)

        converted_files.add(file_name)

def copy_file(file_path, output_file_name, file_extension):
    file_dir, _ = os.path.split(file_path)
    source_file_path = os.path.join(file_dir, f"{output_file_name}{file_extension}")

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

    # Clear the .cache folder after processing
    cache_dir = os.path.join(directory, '.cache')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    with open(record_file, 'w') as file:
        file.write('\n'.join(converted_files))

target_directory = '/app/Videos'
process_directory(target_directory)
