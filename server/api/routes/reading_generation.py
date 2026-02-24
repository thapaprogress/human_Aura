"""Reading generation endpoints"""

from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.reading_generation_service import ReadingGenerationService

router = APIRouter()

# Initialize reading generation service
reading_service = ReadingGenerationService()


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


class GenerateReadingRequest(BaseModel):
    aura_profile: AuraProfile
    biofeedback_summary: dict


class ReadingSection(BaseModel):
    section: str
    title: str
    content: str


class GenerateReadingResponse(BaseModel):
    success: bool
    data: dict


@router.post(
    "/generate",
    response_model=GenerateReadingResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate aura reading",
)
async def generate_reading(request: GenerateReadingRequest):
    """
    Generate personalized aura reading from aura profile.
    
    - **aura_profile**: Aura color profile
    - **biofeedback_summary**: Summary of biofeedback data
    
    Returns reading with color analysis, alignment, and guidance sections.
    """
    try:
        # Convert Pydantic model to dict for service
        aura_profile_dict = request.aura_profile.model_dump()
        
        # Generate reading
        reading = reading_service.generate_reading(
            aura_profile=aura_profile_dict,
            biofeedback_summary=request.biofeedback_summary,
        )
        
        return GenerateReadingResponse(
            success=True,
            data={
                "sections": [
                    {
                        "section": section.section,
                        "title": section.title,
                        "content": section.content,
                    }
                    for section in reading.sections
                ],
                "color_references": reading.color_references,
                "generated_at": reading.generated_at,
            },
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reading generation failed: {str(e)}",
        )


@router.post(
    "/generate-template",
    response_model=GenerateReadingResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate aura reading using templates (no AI)",
)
async def generate_reading_template(request: GenerateReadingRequest):
    """
    Generate aura reading using template-based approach (no AI required).
    
    - **aura_profile**: Aura color profile
    - **biofeedback_summary**: Summary of biofeedback data
    
    Returns reading with color analysis, alignment, and guidance sections.
    """
    try:
        # Convert Pydantic model to dict for service
        aura_profile_dict = request.aura_profile.model_dump()
        
        # Generate reading using templates
        reading = reading_service.generate_reading_template(
            aura_profile=aura_profile_dict,
            biofeedback_summary=request.biofeedback_summary,
        )
        
        return GenerateReadingResponse(
            success=True,
            data={
                "sections": [
                    {
                        "section": section.section,
                        "title": section.title,
                        "content": section.content,
                    }
                    for section in reading.sections
                ],
                "color_references": reading.color_references,
                "generated_at": reading.generated_at,
            },
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reading generation failed: {str(e)}",
        )
