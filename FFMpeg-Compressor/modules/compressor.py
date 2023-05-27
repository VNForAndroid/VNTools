from modules import printer
import configparser
import os

audio_exts = ['.aac', '.flac', '.m4a', '.mp3', '.ogg', '.opus', '.raw', '.wav', '.wma']
image_exts = ['.apng', '.avif', '.jfif', '.pjpeg', '.pjp', '.svg', '.webp', '.jpg', '.jpeg', '.png', '.raw']
video_exts = ['.3gp' '.amv', '.avi', '.gif', '.m4v', '.mkv', '.mov', '.mp4', '.m4v', '.mpeg', '.mpv', '.webm', '.ogv']

config = configparser.ConfigParser()
config.read("config.ini")

ffmpeg_params = config['FFMPEG']['FFmpegParams']
req_audio_ext = config['FFMPEG']['AudioExt']
req_image_ext = config['FFMPEG']['ImageExt']
req_video_ext = config['FFMPEG']['VideoExt']


def compress(folder):
    files = len(os.listdir(path=folder))
    progress = 0
    for file in os.listdir(path=folder):
        if os.path.splitext(file)[1] in audio_exts:
            bitrate = config['FFMPEG']['AudioBitRate']
            printer.files(int((progress / files) * 100), file, os.path.splitext(file)[0], req_audio_ext, f"{bitrate}bit/s")
            os.system(f"ffmpeg -i '{folder}/{file}' {ffmpeg_params} '{folder}_compressed/{os.path.splitext(file)[0]}.{req_audio_ext}'")

        elif os.path.splitext(file)[1] in image_exts:
            if req_image_ext == "jpg" or os.path.splitext(file)[1] == "jpeg":
                jpg_comp = config['FFMPEG']['JpegComp']
                printer.files(int((progress / files) * 100), file, os.path.splitext(file)[0], req_image_ext,f"{jpg_comp}%")
                os.system(f"ffmpeg -i '{folder}/{file}' {ffmpeg_params} -q {jpg_comp} '{folder}_compressed/{os.path.splitext(file)[0]}.{req_image_ext}'")
            else:
                comp_level = config['FFMPEG']['CompLevel']
                printer.files(int((progress / files) * 100), file, os.path.splitext(file)[0], req_image_ext, f"{comp_level}%")
                os.system(f"ffmpeg -i '{folder}/{file}' {ffmpeg_params} -compression_level {comp_level} '{folder}_compressed/{os.path.splitext(file)[0]}.{req_image_ext}'")

        elif os.path.splitext(file)[1] in video_exts:
            codec = config['FFMPEG']['VideoCodec']
            printer.files(int((progress / files) * 100), file, os.path.splitext(file)[0], req_video_ext, codec)
            os.system(f"ffmpeg -i '{folder}/{file}' {ffmpeg_params} -vcodec {codec} '{folder}_compressed/{os.path.splitext(file)[0]}.{req_video_ext}'")

        else:
            printer.warning("File extension not recognized. This may affect the quality of the compression.")
            print(f"\r[{int((progress/files) * 100)}%] \033[0;33m{file}\033[0m")
            os.system(f"ffmpeg -i '{folder}/{file}' {ffmpeg_params} '{folder}_compressed/{file}'")

        progress += 1