## install
ffmpeg
> python -m pip install ffmpeg moviepy

### use way 
> `convert_fly_to_mp4.py`  
> 指定 `flv` 文件的目录，之后会自动创建 `mp4s` 目录，在里面存入 转化后的格式  
> `flv`文件目录指定方式 ·flv_path = “XXX”·
>  
>  
>`video_clipping.py`  
> 剪切 `mp4`格式视频，剪切后会生成`outputs`目录，里面会存剪切后的视频。  
> 默认为 10 分钟剪切一次，不足20分钟不剪
