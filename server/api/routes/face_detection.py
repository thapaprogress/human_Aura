"""Face detection endpoints"""

import base64
import io
from typing import List, Optional

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from services.face_detection_service import FaceDetectionService

router = APIRouter()

# Initialize face detection service
face_service = FaceDetectionService()


class FaceLandmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: Optional[float] = None


class FaceBoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    width: float
    height: float


class FacePose(BaseModel):
    pitch: float
    yaw: float
    roll: float


class FaceDetectionResult(BaseModel):
    found: bool
    landmarks: Optional[List[FaceLandmark]] = None
    bounding_box: Optional[FaceBoundingBox] = None
    face_center: Optional[dict] = None
    face_size: Optional[dict] = None
    head_pose: Optional[FacePose] = None
    alignment_score: Optional[float] = None


class FaceDetectionResponse(BaseModel):
    success: bool
    data: FaceDetectionResult


@router.post(
    "/detect",
    response_model=FaceDetectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect face in image",
)
async def detect_face(file: UploadFile = File(...)):
    """
    Detect face in uploaded image and return facial landmarks.
    
    - **file**: Image file (JPEG, PNG)
    
    Returns facial landmarks, bounding box, and alignment score.
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image",
        )
    
    try:
        # Read image bytes
        contents = await file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file",
            )
        
        # Detect face
        result = face_service.detect_face(image)
        
        return FaceDetectionResponse(
            success=True,
            data=FaceDetectionResult(
                found=result.found,
                landmarks=[
                    FaceLandmark(
                        x=lm.x,
                        y=lm.y,
                        z=lm.z,
                        visibility=lm.visibility,
                    )
                    for lm in (result.landmarks or [])
                ] if result.landmarks else None,
                bounding_box=FaceBoundingBox(
                    x_min=result.bounding_box.xMin,
                    y_min=result.bounding_box.yMin,
                    x_max=result.bounding_box.xMax,
                    y_max=result.bounding_box.yMax,
                    width=result.bounding_box.width,
                    height=result.bounding_box.height,
                ) if result.bounding_box else None,
                face_center=result.face_center,
                face_size=result.face_size,
                head_pose=FacePose(
                    pitch=result.head_pose.pitch,
                    yaw=result.head_pose.yaw,
                    roll=result.head_pose.roll,
                ) if result.head_pose else None,
                alignment_score=result.alignment_score,
            ),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face detection failed: {str(e)}",
        )


@router.post(
    "/detect-base64",
    response_model=FaceDetectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect face in base64 image",
)
async def detect_face_base64(request: dict):
    """
    Detect face in base64 encoded image.
    
    - **image**: Base64 encoded image string
    
    Returns facial landmarks, bounding box, and alignment score.
    """
    try:
        image_data = request.get("image", "")
        
        # Remove data URL prefix if present
        if "," in image_data:
            image_data = image_data.split(",")[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image data",
            )
        
        # Detect face
        result = face_service.detect_face(image)
        
        return FaceDetectionResponse(
            success=True,
            data=FaceDetectionResult(
                found=result.found,
                landmarks=[
                    FaceLandmark(
                        x=lm.x,
                        y=lm.y,
                        z=lm.z,
                        visibility=lm.visibility,
                    )
                    for lm in (result.landmarks or [])
                ] if result.landmarks else None,
                bounding_box=FaceBoundingBox(
                    x_min=result.bounding_box.xMin,
                    y_min=result.bounding_box.yMin,
                    x_max=result.bounding_box.xMax,
                    y_max=result.bounding_box.yMax,
                    width=result.bounding_box.width,
                    height=result.bounding_box.height,
                ) if result.bounding_box else None,
                face_center=result.face_center,
                face_size=result.face_size,
                head_pose=FacePose(
                    pitch=result.head_pose.pitch,
                    yaw=result.head_pose.yaw,
                    roll=result.head_pose.roll,
                ) if result.head_pose else None,
                alignment_score=result.alignment_score,
            ),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face detection failed: {str(e)}",
        )
