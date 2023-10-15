from pathlib import Path
from typing import Union
import moviepy.editor as mp
import random
import os



class VideoPreprocessing:
    @staticmethod
    def trim_video(video_path: Union[str, Path], output_path: Union[str, Path], video_name: str) -> None:
        video = mp.VideoFileClip(video_path)
        duration = video.duration
        trimmed_video = video.subclip(duration * 0.1, duration * 0.9)
        for i in range(1):
            random_time = random.uniform(0.0, trimmed_video.duration)
            trimmed_video.save_frame(os.path.join(output_path, f"thumbnail_{video_name[:-4]}_{i}.jpg"), t=random_time)
        video.reader.close()


# VideoPreprocessing.trim_video("57.mp4", "qw")
