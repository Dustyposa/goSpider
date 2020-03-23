import subprocess
from pathlib import Path

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def get_length(filename) -> float:
    # 获取视频总长度
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


mp4_path = "."
outputs_dir_name = "outputs"


def main() -> None:
    Path(mp4_path / outputs_dir_name).mkdir(exist_ok=True)  # 创建输出文件夹
    for file in Path(mp4_path).glob("*.mp4"):
        cut_video(file.absolute().__str__())


def cut_video(file_name: str):
    video_path = file_name
    tmp = Path(file_name)
    output_path = (tmp.parent / outputs_dir_name).joinpath(tmp.stem + "{}").with_suffix(".mp4").absolute().__str__()
    cut_time = 12  # unit s
    total_duration = get_length(file_name) - 20
    splice_time = 10 * 60  # 分割时间
    index = 1
    while (total_duration - cut_time) / splice_time > 2:
        ffmpeg_extract_subclip(video_path.format(""), cut_time, cut_time + splice_time,
                               targetname=output_path.format(index))
        cut_time += splice_time
        index += 1
    ffmpeg_extract_subclip(video_path.format(""), cut_time, total_duration, targetname=output_path.format(index))
    print(f"{output_path.format(index)}文件生成成功。")


if __name__ == '__main__':
    main()
