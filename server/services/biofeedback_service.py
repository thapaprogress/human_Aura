"""Biofeedback processing service"""

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal, Optional

import numpy as np


@dataclass
class BiofeedbackReading:
    timestamp: str
    touch_x: Optional[float] = None
    touch_y: Optional[float] = None
    pressure: Optional[float] = None
    stability: Optional[float] = None
    simulated_gsr: Optional[float] = None
    simulated_hrv: Optional[float] = None
    stress_indicator: Optional[float] = None
    calmness_score: Optional[float] = None


@dataclass
class BiofeedbackSession:
    session_id: str
    start_time: datetime
    end_time: datetime
    duration_ms: int
    readings: List[BiofeedbackReading] = field(default_factory=list)
    average_stability: float = 0.0
    stability_variance: float = 0.0
    touch_pattern: Literal["steady", "erratic", "focused", "scattered"] = "focused"
    simulated_gsr: float = 0.0
    simulated_hrv: float = 0.0
    stress_indicator: float = 0.0
    calmness_score: float = 0.0


class BiofeedbackService:
    """Service for processing biofeedback data"""
    
    def __init__(self, sample_rate: int = 30):
        self.sample_rate = sample_rate
    
    def process_readings(
        self,
        readings: List[Dict],
        duration_ms: int,
    ) -> BiofeedbackSession:
        """
        Process biofeedback readings and return session summary.
        
        Args:
            readings: List of biofeedback reading dictionaries
            duration_ms: Duration of biofeedback collection
        
        Returns:
            BiofeedbackSession with aggregated metrics
        """
        # Convert dict readings to objects
        reading_objects = [
            BiofeedbackReading(
                timestamp=r.get("timestamp", ""),
                touch_x=r.get("touch_x"),
                touch_y=r.get("touch_y"),
                pressure=r.get("pressure"),
                stability=r.get("stability"),
                simulated_gsr=r.get("simulated_gsr"),
                simulated_hrv=r.get("simulated_hrv"),
                stress_indicator=r.get("stress_indicator"),
                calmness_score=r.get("calmness_score"),
            )
            for r in readings
        ]
        
        # Calculate aggregated metrics
        stabilities = [r.stability for r in reading_objects if r.stability is not None]
        gsrs = [r.simulated_gsr for r in reading_objects if r.simulated_gsr is not None]
        hrvs = [r.simulated_hrv for r in reading_objects if r.simulated_hrv is not None]
        stresses = [r.stress_indicator for r in reading_objects if r.stress_indicator is not None]
        calmnesses = [r.calmness_score for r in reading_objects if r.calmness_score is not None]
        
        average_stability = np.mean(stabilities) if stabilities else 0.5
        stability_variance = np.var(stabilities) if stabilities else 0.1
        
        simulated_gsr = np.mean(gsrs) if gsrs else 0.5
        simulated_hrv = np.mean(hrvs) if hrvs else 0.5
        stress_indicator = np.mean(stresses) if stresses else 0.5
        calmness_score = np.mean(calmnesses) if calmnesses else 0.5
        
        # Determine touch pattern
        touch_pattern = self._determine_touch_pattern(reading_objects)
        
        return BiofeedbackSession(
            session_id=self._generate_session_id(),
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_ms=duration_ms,
            readings=reading_objects,
            average_stability=round(average_stability, 4),
            stability_variance=round(stability_variance, 4),
            touch_pattern=touch_pattern,
            simulated_gsr=round(simulated_gsr, 4),
            simulated_hrv=round(simulated_hrv, 4),
            stress_indicator=round(stress_indicator, 4),
            calmness_score=round(calmness_score, 4),
        )
    
    def simulate_readings(
        self,
        duration_ms: int = 5000,
    ) -> BiofeedbackSession:
        """
        Generate simulated biofeedback readings for testing.
        
        Args:
            duration_ms: Duration to simulate
        
        Returns:
            BiofeedbackSession with simulated data
        """
        # Calculate number of readings
        num_readings = int((duration_ms / 1000) * self.sample_rate)
        
        # Generate base personality traits (consistent throughout session)
        base_stability = random.uniform(0.4, 0.9)
        base_calmness = random.uniform(0.3, 0.9)
        base_stress = 1 - base_calmness
        
        readings = []
        current_x, current_y = 0.5, 0.5
        
        for i in range(num_readings):
            # Simulate touch position with some movement
            movement = random.gauss(0, 0.02)
            current_x = max(0, min(1, current_x + movement))
            current_y = max(0, min(1, current_y + movement))
            
            # Simulate stability with some variation
            stability = base_stability + random.gauss(0, 0.05)
            stability = max(0, min(1, stability))
            
            # Simulate pressure based on stability
            pressure = 0.3 + stability * 0.7
            
            # Simulate GSR (galvanic skin response)
            simulated_gsr = 0.2 + pressure * 0.6 + random.uniform(0, 0.2)
            
            # Simulate HRV (heart rate variability)
            simulated_hrv = 0.3 + stability * 0.5 + random.uniform(0, 0.2)
            
            # Calculate derived signals
            stress_indicator = 1 - stability
            calmness_score = stability
            
            readings.append(BiofeedbackReading(
                timestamp=datetime.now().isoformat(),
                touch_x=round(current_x, 4),
                touch_y=round(current_y, 4),
                pressure=round(pressure, 4),
                stability=round(stability, 4),
                simulated_gsr=round(simulated_gsr, 4),
                simulated_hrv=round(simulated_hrv, 4),
                stress_indicator=round(stress_indicator, 4),
                calmness_score=round(calmness_score, 4),
            ))
        
        # Process the simulated readings
        return self.process_readings(
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
                for r in readings
            ],
            duration_ms=duration_ms,
        )
    
    def _determine_touch_pattern(
        self,
        readings: List[BiofeedbackReading],
    ) -> Literal["steady", "erratic", "focused", "scattered"]:
        """Determine touch pattern from readings"""
        if len(readings) < 10:
            return "focused"
        
        stabilities = [r.stability for r in readings if r.stability is not None]
        if not stabilities:
            return "focused"
        
        avg_stability = np.mean(stabilities)
        variance = np.var(stabilities)
        
        if avg_stability > 0.8:
            return "steady"
        elif variance > 0.1:
            return "erratic"
        elif avg_stability > 0.5:
            return "focused"
        else:
            return "scattered"
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())
