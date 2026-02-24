"""Aura generation endpoints"""

import base64
import io
from typing import List, Optional

import numpy as np
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.aura_generation_service import AuraGenerationService
from services.biofeedback_service import BiofeedbackService

router = APIRouter()

# Initialize services
aura_service = AuraGenerationService()
biofeedback_service = BiofeedbackService()


class BiofeedbackReading(BaseModel):
    timestamp: str
    touch_x: Optional[float] = None
    touch_y: Optional[float] = None
    pressure: Optional[float] = None
    stability: Optional[float] = None
    simulated_gsr: Optional[float] = None
    simulated_hrv: Optional[float] = None
    stress_indicator: Optional[float] = None
    calmness_score: Optional[float] = None


class AuraPositioning(BaseModel):
    ascendant: List[str]
    descendant: List[str]
    cathedra: List[str]
    coronation: List[str]
    etherea: List[str]


class AuraProfile(BaseModel):
    majority_color: str
    majority_percentage: float
    moderate_colors: List[str]
    moderate_percentages: List[float]
    minority_colors: List[str]
    minority_percentages: List[float]
    intensity: float
    brightness: float
    saturation: float
    positioning: AuraPositioning


class GenerateAuraRequest(BaseModel):
    image: str  # Base64 encoded image
    biofeedback_readings: List[BiofeedbackReading]
    duration_ms: int
    style: str = "soft"  # soft, medium, strong


class GenerateAuraResponse(BaseModel):
    success: bool
    data: dict


@router.post(
    "/generate",
    response_model=GenerateAuraResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate aura from photo and biofeedback",
)
async def generate_aura(request: GenerateAuraRequest):
    """
    Generate aura image from photo and biofeedback data.
    
    - **image**: Base64 encoded photo
    - **biofeedback_readings**: Array of biofeedback readings
    - **duration_ms**: Duration of biofeedback collection in milliseconds
    - **style**: Aura style (soft, medium, strong)
    
    Returns aura profile and generated image.
    """
    try:
        # Process biofeedback data
        biofeedback_session = biofeedback_service.process_readings(
            readings=[
                {
                    "timestamp": r.timestamp,
                    "touch_x": r.touch_x,
                    "touch_y": r.touch_y,
                    "pressure": r.pressure,
                    "stability": r.stability,
                    "simulated_gsr": r.simulated_gsr,
                    "simulated_hrv": r.simulated_hrv,
                    "stress_indicator": r.stress_indicator,
                    "calmness_score": r.calmness_score,
                }
                for r in request.biofeedback_readings
            ],
            duration_ms=request.duration_ms,
        )
        
        # Generate aura profile from biofeedback
        aura_profile = aura_service.generate_aura_profile(biofeedback_session)
        
        # Decode base64 image
        image_data = request.image
        if "," in image_data:
            image_data = image_data.split(",")[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Generate aura image
        aura_image = aura_service.generate_aura_image(
            image_bytes=image_bytes,
            aura_profile=aura_profile,
            style=request.style,
        )
        
        # Encode aura image to base64
        aura_image_base64 = base64.b64encode(aura_image).decode('utf-8')
        
        return GenerateAuraResponse(
            success=True,
            data={
                "profile": {
                    "majority_color": aura_profile.majority_color,
                    "majority_percentage": aura_profile.majority_percentage,
                    "moderate_colors": aura_profile.moderate_colors,
                    "moderate_percentages": aura_profile.moderate_percentages,
                    "minority_colors": aura_profile.minority_colors,
                    "minority_percentages": aura_profile.minority_percentages,
                    "intensity": aura_profile.intensity,
                    "brightness": aura_profile.brightness,
                    "saturation": aura_profile.saturation,
                    "chakra": aura_profile.chakra,
                    "positioning": {
                        "ascendant": aura_profile.positioning.ascendant,
                        "descendant": aura_profile.positioning.descendant,
                        "cathedra": aura_profile.positioning.cathedra,
                        "coronation": aura_profile.positioning.coronation,
                        "etherea": aura_profile.positioning.etherea,
                    },
                },
                "image": f"data:image/png;base64,{aura_image_base64}",
                "biofeedback_summary": {
                    "average_stability": biofeedback_session.average_stability,
                    "calmness_score": biofeedback_session.calmness_score,
                    "stress_indicator": biofeedback_session.stress_indicator,
                    "touch_pattern": biofeedback_session.touch_pattern,
                },
            },
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Aura generation failed: {str(e)}",
        )


@router.post(
    "/profile-only",
    response_model=GenerateAuraResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate aura profile only (no image)",
)
async def generate_aura_profile_only(request: GenerateAuraRequest):
    """
    Generate aura profile from biofeedback data without generating image.
    
    - **biofeedback_readings**: Array of biofeedback readings
    - **duration_ms**: Duration of biofeedback collection in milliseconds
    
    Returns aura profile only.
    """
    try:
        # Process biofeedback data
        biofeedback_session = biofeedback_service.process_readings(
            readings=[
                {
                    "timestamp": r.timestamp,
                    "touch_x": r.touch_x,
                    "touch_y": r.touch_y,
                    "pressure": r.pressure,
                    "stability": r.stability,
                    "simulated_gsr": r.simulated_gsr,
                    "simulated_hrv": r.simulated_hrv,
                    "stress_indicator": r.stress_indicator,
                    "calmness_score": r.calmness_score,
                }
                for r in request.biofeedback_readings
            ],
            duration_ms=request.duration_ms,
        )
        
        # Generate aura profile
        aura_profile = aura_service.generate_aura_profile(biofeedback_session)
        
        return GenerateAuraResponse(
            success=True,
            data={
                "profile": {
                    "majority_color": aura_profile.majority_color,
                    "majority_percentage": aura_profile.majority_percentage,
                    "moderate_colors": aura_profile.moderate_colors,
                    "moderate_percentages": aura_profile.moderate_percentages,
                    "minority_colors": aura_profile.minority_colors,
                    "minority_percentages": aura_profile.minority_percentages,
                    "intensity": aura_profile.intensity,
                    "brightness": aura_profile.brightness,
                    "saturation": aura_profile.saturation,
                    "chakra": aura_profile.chakra,
                    "positioning": {
                        "ascendant": aura_profile.positioning.ascendant,
                        "descendant": aura_profile.positioning.descendant,
                        "cathedra": aura_profile.positioning.cathedra,
                        "coronation": aura_profile.positioning.coronation,
                        "etherea": aura_profile.positioning.etherea,
                    },
                },
                "biofeedback_summary": {
                    "average_stability": biofeedback_session.average_stability,
                    "calmness_score": biofeedback_session.calmness_score,
                    "stress_indicator": biofeedback_session.stress_indicator,
                    "touch_pattern": biofeedback_session.touch_pattern,
                },
            },
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Aura profile generation failed: {str(e)}",
        )
