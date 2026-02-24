"""Face detection service using MediaPipe (MOCKED)"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np

# Mocks
@dataclass
class FaceLandmark:
    x: float
    y: float
    z: float
    visibility: Optional[float] = None

@dataclass
class FaceBoundingBox:
    xMin: float
    yMin: float
    xMax: float
    yMax: float
    width: float
    height: float

@dataclass
class FacePose:
    pitch: float
    yaw: float
    roll: float

@dataclass
class FaceDetectionResult:
    found: bool
    landmarks: Optional[List[FaceLandmark]] = None
    boundingBox: Optional[FaceBoundingBox] = None
    faceCenter: Optional[dict] = None
    faceSize: Optional[dict] = None
    headPose: Optional[FacePose] = None
    alignmentScore: Optional[float] = None

class FaceDetectionService:
    """Mock Service for detecting faces to bypass install issues"""
    
    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        pass
    
    def detect_face(self, image: np.ndarray) -> FaceDetectionResult:
        """
        Return a dummy face detection result.
        """
        # Mock successful detection
        return FaceDetectionResult(
            found=True,
            landmarks=[FaceLandmark(0.5, 0.5, 0.0) for _ in range(468)],
            boundingBox=FaceBoundingBox(0.2, 0.2, 0.8, 0.8, 0.6, 0.6),
            faceCenter={"x": 0.5, "y": 0.5},
            faceSize={"width": 0.6, "height": 0.6},
            headPose=FacePose(0.0, 0.0, 0.0),
            alignmentScore=0.95,
        )

    def draw_landmarks(self, image, landmarks, color=(0, 255, 0), thickness=1):
        return image

    def draw_bounding_box(self, image, bounding_box, color=(0, 255, 0), thickness=2):
        return image
