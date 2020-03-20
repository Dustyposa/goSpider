import os

from pathlib import Path

flv_path = r"F:\迅雷下载\ai_v"
tmp_fly = Path(flv_path)

mp4_base_p = tmp_fly.joinpath("mp4s")  # 输出文件夹
mp4_base_p.mkdir(exist_ok=True)  # 创建
cmd = "ffmpeg -i {flv_p} -c:v libx264 -crf 19 -strict experimental {mp4_p}"  # 基础转化命令
for flv_file in Path(flv_path).glob("*.flv"):
    flv_p = flv_file.absolute()
    mp4_p = mp4_base_p.joinpath(f"{flv_file.stem}.mp4").absolute()
    with os.popen(cmd.format(flv_p=flv_p.__str__(), mp4_p=mp4_p.__str__())) as pro:
        for i in pro.readlines():
            print(i)
