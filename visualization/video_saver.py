"""
VideoSaver: A utility class for saving video frames to a file.

This class uses OpenCV's VideoWriter to save frames to a video file. 
It supports specifying the output path, resolution, and frames per second (FPS). 
Frames are written sequentially, and the video file is finalized when the `release` method is called.

"""

import cv2
import numpy as np
from typing import Tuple, Optional

class VideoSaver:
    def __init__(
        self,
        output_path: str = "visualization/saved_videos/output.mp4",
        resolution: Tuple[int, int] = (1280, 720),
        fps: int = 30
    ) -> None:
        
        self.out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),  # Codec for MP4 format
            fps,
            resolution
        )

    def write_frame(self, frame: np.ndarray, results: Optional[dict] = None) -> None:
        # Write a single frame to the video file
        self.out.write(frame)

    def release(self) -> None:
        # Release the VideoWriter resources
        self.out.release()
