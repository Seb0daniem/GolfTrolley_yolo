from dataclasses import dataclass
import numpy as np
from typing import Optional

@dataclass
class Person:
    id: Optional[int]
    bbox: np.ndarray
    confidence: Optional[float] = None

@dataclass
class Hand:
    id: Optional[int]
    bbox: np.ndarray
    landmarks: Optional[np.ndarray] = None
    owner_id: Optional[int] = None

@dataclass
class Gesture:
    person_id: int
    hand_id: int
    hand_gesture: str
    confidence: float = 0.5

@dataclass
class FrameMeta:
    timestamp: float
    frame_id: int
