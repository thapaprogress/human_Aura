"""Biofeedback processing endpoints"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.biofeedback_service import BiofeedbackService

router = APIRouter()

# Initialize biofeedback service
biofeedback_service = BiofeedbackService()


class BiofeedbackReadingInput(BaseModel):
    timestamp: str
    touch_x: Optional[float] = None
    touch_y: Optional[float] = None
    pressure: Optional[float] = None
    stability: Optional[float] = None
    simulated_gsr: Optional[float] = None
    simulated_hrv: Optional[float] = None
    stress_indicator: Optional[float] = None
    calmness_score: Optional[float] = None


class ProcessBiofeedbackRequest(BaseModel):
    readings: List[BiofeedbackReadingInput]
    duration_ms: int


class BiofeedbackSummary(BaseModel):
    average_stability: float
    stability_variance: float
    touch_pattern: str
    simulated_gsr: float
    simulated_hrv: float
    stress_indicator: float
    calmness_score: float
    duration_ms: int
    reading_count: int


class ProcessBiofeedbackResponse(BaseModel):
    success: bool
    data: BiofeedbackSummary


@router.post(
    "/process",
    response_model=ProcessBiofeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Process biofeedback readings",
)
async def process_biofeedback(request: ProcessBiofeedbackRequest):
    """
    Process biofeedback readings and return summary metrics.
    
    - **readings**: Array of biofeedback readings
    - **duration_ms**: Duration of biofeedback collection in milliseconds
    
    Returns processed biofeedback summary.
    """
    try:
        # Convert readings to dict format
        readings_dict = [
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
            for r in request.readings
        ]
        
        # Process readings
        session = biofeedback_service.process_readings(
            readings=readings_dict,
            duration_ms=request.duration_ms,
        )
        
        return ProcessBiofeedbackResponse(
            success=True,
            data=BiofeedbackSummary(
                average_stability=session.average_stability,
                stability_variance=session.stability_variance,
                touch_pattern=session.touch_pattern,
                simulated_gsr=session.simulated_gsr,
                simulated_hrv=session.simulated_hrv,
                stress_indicator=session.stress_indicator,
                calmness_score=session.calmness_score,
                duration_ms=session.duration_ms,
                reading_count=len(session.readings),
            ),
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Biofeedback processing failed: {str(e)}",
        )


@router.post(
    "/simulate",
    response_model=ProcessBiofeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate simulated biofeedback data",
)
async def simulate_biofeedback(duration_ms: int = 5000):
    """
    Generate simulated biofeedback data for testing.
    
    - **duration_ms**: Duration to simulate (default: 5000ms)
    
    Returns simulated biofeedback summary.
    """
    try:
        # Generate simulated readings
        session = biofeedback_service.simulate_readings(duration_ms=duration_ms)
        
        return ProcessBiofeedbackResponse(
            success=True,
            data=BiofeedbackSummary(
                average_stability=session.average_stability,
                stability_variance=session.stability_variance,
                touch_pattern=session.touch_pattern,
                simulated_gsr=session.simulated_gsr,
                simulated_hrv=session.simulated_hrv,
                stress_indicator=session.stress_indicator,
                calmness_score=session.calmness_score,
                duration_ms=session.duration_ms,
                reading_count=len(session.readings),
            ),
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Biofeedback simulation failed: {str(e)}",
        )
