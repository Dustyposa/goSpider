from path import Path

from moviepy.editor import VideoFileClip

for file in Path("videos_files").files():
    video = VideoFileClip(file.abspath())

    audio = video.audio
    audio.write_audiofile(f"./audio_files/{file.stem}.mp3")
    print(f"写入文件{file.stem}.mp3")
