# AURLA-Like Aura Camera App - Complete Technical Specification

## Executive Summary

This document provides a comprehensive technical blueprint for building an AURLA-like aura camera application using modern web technologies. The app will be built with a React/Next.js frontend and Python backend, featuring computer vision for face detection, biofeedback simulation, and AI-powered aura generation.

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Technology Stack](#2-technology-stack)
3. [Core Features & Requirements](#3-core-features--requirements)
4. [Computer Vision Components](#4-computer-vision-components)
5. [Biofeedback Simulation System](#5-biofeedback-simulation-system)
6. [Aura Generation Engine](#6-aura-generation-engine)
7. [Database Schema](#7-database-schema)
8. [API Specification](#8-api-specification)
9. [Frontend Components](#9-frontend-components)
10. [Project Structure](#10-project-structure)
11. [Installation & Setup](#11-installation--setup)
12. [Deployment Guide](#12-deployment-guide)

---

## 1. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Web App    │  │  Mobile App  │  │   PWA        │  │   Desktop    │   │
│  │  (Next.js)   │  │ (React Nat.) │  │  (Next.js)   │  │  (Electron)  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY LAYER                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI / Node.js API Gateway                     │   │
│  │  - Authentication  │  - Rate Limiting  │  - Request Validation      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MICROSERVICES LAYER                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Auth     │  │   Aura     │  │   Photo    │  │  Reading   │           │
│  │  Service   │  │  Engine    │  │  Service   │  │  Service   │           │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Payment   │  │  User      │  │ Analytics  │  │  Notification│          │
│  │  Service   │  │  Service   │  │  Service   │  │  Service   │           │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI/ML PROCESSING LAYER                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Face Detection │  │ Biofeedback Sim │  │  Aura Generator │             │
│  │  (MediaPipe)    │  │  (Python/TF)    │  │   (PyTorch)     │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  Color Analysis │  │  Reading NLP    │  │  Image Overlay  │             │
│  │   (OpenCV)      │  │   (OpenAI API)  │  │   (PIL/Pillow)  │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  PostgreSQL  │  │    Redis     │  │  Cloudinary  │  │    S3        │   │
│  │  (Primary DB)│  │   (Cache)    │  │   (Images)   │  │  (Storage)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Opens App
      │
      ▼
┌─────────────────┐
│ Camera Access   │◄────── Request camera permission
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Face Detection  │◄────── MediaPipe Face Mesh
│ & Alignment     │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Biofeedback     │◄────── Simulate sensor data
│ Data Capture    │        (mouse/touch position, 
└─────────────────┘         time held, etc.)
      │
      ▼
┌─────────────────┐
│ Aura Generation │◄────── AI model processes data
│ Algorithm       │        → generates color profile
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Image Overlay   │◄────── Apply aura effect to photo
│ & Rendering     │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Reading         │◄────── NLP generates interpretation
│ Generation      │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Display Result  │◄────── Show photo + reading
└─────────────────┘
```

---

## 2. Technology Stack

### Frontend Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | Next.js 15 | React framework with SSR/SSG |
| Language | TypeScript | Type-safe development |
| Styling | Tailwind CSS 4 | Utility-first CSS |
| UI Components | shadcn/ui | Pre-built accessible components |
| State Management | Zustand | Global state management |
| Animation | Framer Motion | Smooth UI animations |
| Camera Access | react-webcam | Browser camera integration |
| Canvas | HTML5 Canvas API | Image processing & overlay |

### Backend Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| API Framework | FastAPI (Python) | High-performance API |
| Alternative | Node.js + Express | JavaScript backend option |
| Authentication | JWT + bcrypt | Secure user auth |
| Validation | Pydantic / Zod | Data validation |
| Documentation | OpenAPI/Swagger | API documentation |

### AI/ML Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Face Detection | MediaPipe Face Mesh | 468-point facial landmarks |
| Computer Vision | OpenCV | Image processing |
| Deep Learning | PyTorch / TensorFlow | Aura generation models |
| NLP | OpenAI API / Local LLM | Reading generation |
| Image Generation | Stable Diffusion / Custom | Aura effect generation |

### Database & Storage

| Component | Technology | Purpose |
|-----------|------------|---------|
| Primary DB | PostgreSQL | User data, readings, sessions |
| Cache | Redis | Session cache, rate limiting |
| Image Storage | Cloudinary / AWS S3 | Photo storage & CDN |
| File Storage | Local / S3 | Temporary processing files |

### DevOps & Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Consistent environments |
| Orchestration | Docker Compose | Local development |
| CI/CD | GitHub Actions | Automated deployment |
| Monitoring | Prometheus + Grafana | Performance monitoring |
| Logging | Winston / Loguru | Application logging |

---

## 3. Core Features & Requirements

### Feature Matrix

| Feature | Priority | Complexity | Status |
|---------|----------|------------|--------|
| Camera Capture | P0 | Medium | Required |
| Face Detection | P0 | Medium | Required |
| Biofeedback Simulation | P0 | High | Required |
| Aura Generation | P0 | High | Required |
| Reading Generation | P0 | Medium | Required |
| Photo Gallery | P1 | Low | Required |
| User Authentication | P1 | Medium | Required |
| Subscription System | P1 | High | Required |
| Social Sharing | P2 | Low | Optional |
| History/Tracking | P2 | Medium | Optional |
| Analytics Dashboard | P3 | Medium | Optional |

### Functional Requirements

#### FR-001: Camera Capture
- Access device camera (front/back)
- Real-time preview with face detection overlay
- Capture high-resolution photo (minimum 1080p)
- Support for both selfie and friend photography

#### FR-002: Face Detection & Alignment
- Detect face position and orientation
- Guide user to center face in frame
- Validate face is properly positioned before capture
- Support multiple faces (for friend mode)

#### FR-003: Biofeedback Data Collection
- Simulate biofeedback sensors using:
  - Touch/mouse position tracking
  - Time spent in alignment
  - Device movement/accelerometer (mobile)
  - Optional: heart rate from camera (photoplethysmography)
- Collect data for 3-5 seconds during alignment
- Store raw biofeedback data for processing

#### FR-004: Aura Generation
- Process biofeedback data through ML model
- Generate color profile with:
  - Dominant color (majority)
  - Secondary colors (moderate)
  - Accent colors (minority)
- Calculate color intensity (0-100%)
- Determine aura positioning (ascendant, descendant, etc.)

#### FR-005: Image Processing & Overlay
- Apply aura effect to captured photo
- Use gaussian blur and gradient overlays
- Support multiple aura styles (soft, vibrant, ethereal)
- Generate high-quality output image (PNG/JPEG)

#### FR-006: Reading Generation
- Generate personalized interpretation based on:
  - Detected colors and their positions
  - Color combinations and relationships
  - Intensity levels
- Provide 3-part reading:
  - Color analysis
  - Alignment interpretation
  - General guidance

#### FR-007: User Management
- User registration and login
- Profile management
- Session history
- Subscription management

#### FR-008: Session Management
- Free first session for new users
- Daily session limits for subscribers
- Single session purchases
- Session history tracking

### Non-Functional Requirements

#### NFR-001: Performance
- Camera preview: < 50ms latency
- Face detection: < 100ms processing
- Aura generation: < 2 seconds total
- Image generation: < 3 seconds
- API response time: < 200ms (p95)

#### NFR-002: Scalability
- Support 10,000 concurrent users
- Handle 1,000 sessions per minute
- Auto-scaling based on demand

#### NFR-003: Security
- End-to-end encryption for sensitive data
- GDPR compliance
- No photo data retention on servers
- Secure payment processing

#### NFR-004: Reliability
- 99.9% uptime SLA
- Graceful degradation for ML services
- Automatic failover

---

## 4. Computer Vision Components

### 4.1 Face Detection Pipeline

```python
# Face Detection Service
class FaceDetectionService:
    """
    Uses MediaPipe Face Mesh for 468-point facial landmark detection
    """
    
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detect_face(self, image: np.ndarray) -> FaceDetectionResult:
        """
        Detect face and return landmarks, bounding box, and pose
        """
        results = self.face_mesh.process(image)
        
        if not results.multi_face_landmarks:
            return FaceDetectionResult(found=False)
        
        landmarks = results.multi_face_landmarks[0]
        
        # Extract key points
        face_data = {
            'landmarks': self._extract_landmarks(landmarks),
            'bounding_box': self._calculate_bounding_box(landmarks),
            'face_center': self._calculate_face_center(landmarks),
            'face_size': self._calculate_face_size(landmarks),
            'head_pose': self._estimate_head_pose(landmarks),
            'alignment_score': self._calculate_alignment(landmarks)
        }
        
        return FaceDetectionResult(found=True, data=face_data)
    
    def _calculate_alignment(self, landmarks) -> float:
        """
        Calculate how well-centered the face is (0-1 score)
        """
        # Check if face is centered in frame
        # Check if face is facing forward (not tilted)
        # Return composite alignment score
        pass
```

### 4.2 Face Alignment Guide

```typescript
// React Component for Face Alignment Overlay
interface FaceAlignmentGuideProps {
  faceData: FaceDetectionResult | null;
  targetFrame: Rect;
}

const FaceAlignmentGuide: React.FC<FaceAlignmentGuideProps> = ({
  faceData,
  targetFrame
}) => {
  const getAlignmentStatus = () => {
    if (!faceData?.found) return 'no-face';
    if (faceData.data.alignment_score > 0.9) return 'perfect';
    if (faceData.data.alignment_score > 0.7) return 'good';
    return 'adjusting';
  };

  return (
    <div className="relative">
      {/* Camera preview */}
      <Webcam ref={webcamRef} />
      
      {/* Face frame overlay */}
      <FaceFrameOverlay 
        targetFrame={targetFrame}
        faceBoundingBox={faceData?.data?.bounding_box}
        status={getAlignmentStatus()}
      />
      
      {/* Alignment guides */}
      <AlignmentGuides status={getAlignmentStatus()} />
      
      {/* Instructions */}
      <AlignmentInstructions status={getAlignmentStatus()} />
    </div>
  );
};
```

### 4.3 Key Facial Landmarks for Aura Positioning

```
Face Mesh Landmarks (468 points total)

Key Points for Aura Analysis:
├── Forehead Center (10)
├── Left Eye Center (468)
├── Right Eye Center (473)
├── Nose Tip (1)
├── Chin (152)
├── Left Cheek (234)
├── Right Cheek (454)
└── Face Contour (all boundary points)

Aura Zones:
┌─────────────────────────────────┐
│         Coronation              │  ← Top (crown/head)
│    (Top of head energy)         │
├─────────────────────────────────┤
│  Descendant │   Ascendant       │
│   (Giving)  │   (Receiving)     │
│             │                   │
│    [FACE]   │                   │
│             │                   │
├─────────────────────────────────┤
│          Cathedra               │  ← Bottom (base/root)
│     (Lower body energy)         │
└─────────────────────────────────┘

Etherea: Surrounding all sides
```

---

## 5. Biofeedback Simulation System

### 5.1 Biofeedback Data Model

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import numpy as np

@dataclass
class BiofeedbackReading:
    """Single biofeedback measurement"""
    timestamp: datetime
    touch_x: float  # 0-1 normalized position
    touch_y: float  # 0-1 normalized position
    pressure: float  # 0-1 simulated pressure
    stability: float  # 0-1 movement stability score
    
@dataclass
class BiofeedbackSession:
    """Complete biofeedback session data"""
    session_id: str
    user_id: Optional[str]
    start_time: datetime
    end_time: datetime
    duration_ms: int
    readings: List[BiofeedbackReading]
    
    # Aggregated metrics
    average_stability: float
    stability_variance: float
    touch_pattern: str  # 'steady', 'erratic', 'focused'
    
    # Derived signals
    simulated_gsr: float  # Galvanic skin response (0-1)
    simulated_hrv: float  # Heart rate variability (0-1)
    stress_indicator: float  # 0-1 stress level
    calmness_score: float  # 0-1 calmness level
```

### 5.2 Biofeedback Collection Service

```typescript
// Biofeedback Collection Hook
interface UseBiofeedbackOptions {
  sampleRate: number; // Hz (e.g., 30 samples/second)
  minDuration: number; // milliseconds
  onComplete: (data: BiofeedbackSession) => void;
}

const useBiofeedback = (options: UseBiofeedbackOptions) => {
  const [isCollecting, setIsCollecting] = useState(false);
  const [readings, setReadings] = useState<BiofeedbackReading[]>([]);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  
  const startCollection = useCallback(() => {
    setIsCollecting(true);
    setReadings([]);
    startTimeRef.current = Date.now();
    
    intervalRef.current = setInterval(() => {
      const reading = collectReading();
      setReadings(prev => [...prev, reading]);
    }, 1000 / options.sampleRate);
  }, []);
  
  const stopCollection = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    setIsCollecting(false);
    
    const session = processSession(readings, startTimeRef.current);
    options.onComplete(session);
  }, [readings]);
  
  const collectReading = (): BiofeedbackReading => {
    // For web: track mouse/touch position
    // For mobile: use touch + accelerometer
    
    return {
      timestamp: new Date(),
      touch_x: getCurrentTouchX(),
      touch_y: getCurrentTouchY(),
      pressure: simulatePressure(),
      stability: calculateStability(readings)
    };
  };
  
  return { isCollecting, startCollection, stopCollection, readings };
};
```

### 5.3 Biofeedback to Aura Mapping

```python
class BiofeedbackToAuraMapper:
    """
    Maps biofeedback signals to aura color characteristics
    """
    
    def __init__(self):
        self.color_mappings = {
            # Color: (stress_range, calmness_range, stability_range)
            'red': ((0.7, 1.0), (0.0, 0.3), (0.0, 0.5)),
            'orange': ((0.5, 0.8), (0.2, 0.5), (0.3, 0.6)),
            'yellow': ((0.3, 0.6), (0.4, 0.7), (0.5, 0.8)),
            'green': ((0.2, 0.5), (0.5, 0.8), (0.6, 0.9)),
            'blue': ((0.1, 0.4), (0.6, 0.9), (0.7, 1.0)),
            'indigo': ((0.0, 0.3), (0.7, 1.0), (0.8, 1.0)),
            'violet': ((0.0, 0.2), (0.8, 1.0), (0.9, 1.0)),
            'pink': ((0.2, 0.5), (0.6, 0.9), (0.5, 0.8)),
            'white': ((0.0, 0.3), (0.9, 1.0), (0.9, 1.0)),
            'gold': ((0.1, 0.4), (0.7, 0.95), (0.8, 1.0)),
            'silver': ((0.2, 0.5), (0.6, 0.9), (0.7, 1.0)),
            'turquoise': ((0.1, 0.4), (0.7, 0.95), (0.6, 0.9)),
            'magenta': ((0.4, 0.7), (0.4, 0.7), (0.4, 0.7)),
            'emerald': ((0.1, 0.4), (0.6, 0.9), (0.7, 1.0)),
            'citrine': ((0.3, 0.6), (0.5, 0.8), (0.5, 0.8)),
            'amethyst': ((0.0, 0.3), (0.75, 1.0), (0.8, 1.0)),
            'quartz': ((0.0, 0.3), (0.85, 1.0), (0.9, 1.0)),
            'sapphire': ((0.0, 0.25), (0.7, 0.95), (0.85, 1.0)),
            'ruby': ((0.6, 0.9), (0.1, 0.4), (0.2, 0.5)),
            'garnet': ((0.5, 0.8), (0.15, 0.45), (0.25, 0.55)),
            'opal': ((0.2, 0.5), (0.55, 0.85), (0.6, 0.9)),
            'peridot': ((0.15, 0.45), (0.55, 0.85), (0.65, 0.95)),
            'topaz': ((0.25, 0.55), (0.5, 0.8), (0.55, 0.85)),
            'aquamarine': ((0.05, 0.35), (0.65, 0.95), (0.75, 1.0)),
            'lapis': ((0.0, 0.3), (0.7, 1.0), (0.8, 1.0)),
            'carnelian': ((0.55, 0.85), (0.2, 0.5), (0.3, 0.6)),
            'rose_quartz': ((0.1, 0.4), (0.75, 1.0), (0.7, 1.0)),
            'smoky_quartz': ((0.4, 0.7), (0.3, 0.6), (0.4, 0.7)),
            'tigers_eye': ((0.3, 0.6), (0.45, 0.75), (0.5, 0.8)),
            'moonstone': ((0.05, 0.35), (0.7, 1.0), (0.75, 1.0)),
            'sunstone': ((0.25, 0.55), (0.55, 0.85), (0.6, 0.9)),
            'labradorite': ((0.1, 0.4), (0.6, 0.9), (0.7, 1.0)),
            'malachite': ((0.15, 0.45), (0.5, 0.8), (0.65, 0.95)),
            'aventurine': ((0.1, 0.4), (0.6, 0.9), (0.7, 1.0)),
            'obsidian': ((0.5, 0.8), (0.2, 0.5), (0.3, 0.6)),
            'jade': ((0.05, 0.35), (0.65, 0.95), (0.75, 1.0)),
            'amber': ((0.3, 0.6), (0.5, 0.8), (0.55, 0.85)),
            'copper': ((0.4, 0.7), (0.35, 0.65), (0.45, 0.75)),
        }
    
    def map_to_aura(self, biofeedback: BiofeedbackSession) -> AuraProfile:
        """
        Convert biofeedback session to aura color profile
        """
        # Calculate composite scores
        stress = biofeedback.stress_indicator
        calmness = biofeedback.calmness_score
        stability = biofeedback.average_stability
        
        # Find matching colors
        color_scores = {}
        for color, (stress_range, calm_range, stab_range) in self.color_mappings.items():
            score = self._calculate_match_score(
                stress, calmness, stability,
                stress_range, calm_range, stab_range
            )
            color_scores[color] = score
        
        # Sort by score and select top colors
        sorted_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create aura profile
        return AuraProfile(
            majority_color=sorted_colors[0][0],
            majority_percentage=sorted_colors[0][1],
            moderate_colors=[c[0] for c in sorted_colors[1:3]],
            moderate_percentages=[c[1] for c in sorted_colors[1:3]],
            minority_colors=[c[0] for c in sorted_colors[3:6]],
            minority_percentages=[c[1] for c in sorted_colors[3:6]],
            intensity=self._calculate_intensity(biofeedback),
            positioning=self._calculate_positioning(biofeedback)
        )
    
    def _calculate_match_score(self, stress, calmness, stability, 
                                stress_range, calm_range, stab_range) -> float:
        """Calculate how well current biofeedback matches color profile"""
        stress_match = 1 - abs(stress - (stress_range[0] + stress_range[1]) / 2)
        calm_match = 1 - abs(calmness - (calm_range[0] + calm_range[1]) / 2)
        stab_match = 1 - abs(stability - (stab_range[0] + stab_range[1]) / 2)
        
        return (stress_match + calm_match + stab_match) / 3
```

---

## 6. Aura Generation Engine

### 6.1 Aura Profile Data Model

```python
@dataclass
class AuraPositioning:
    """Aura positioning around the subject"""
    ascendant: List[str]  # Colors on right side (receiving)
    descendant: List[str]  # Colors on left side (giving)
    cathedra: List[str]  # Colors on bottom (root)
    coronation: List[str]  # Colors on top (crown)
    etherea: List[str]  # Colors surrounding all sides

@dataclass
class AuraProfile:
    """Complete aura color profile"""
    # Primary colors
    majority_color: str
    majority_percentage: float  # 0-100
    
    # Secondary colors
    moderate_colors: List[str]
    moderate_percentages: List[float]
    
    # Accent colors
    minority_colors: List[str]
    minority_percentages: List[float]
    
    # Visual properties
    intensity: float  # 0-100
    brightness: float  # 0-100
    saturation: float  # 0-100
    
    # Positioning
    positioning: AuraPositioning
    
    # Metadata
    generated_at: datetime
    session_id: str

@dataclass
class AuraImage:
    """Generated aura image with metadata"""
    image_data: bytes  # PNG/JPEG data
    width: int
    height: int
    format: str  # 'png' or 'jpeg'
    aura_profile: AuraProfile
    original_photo_id: str
```

### 6.2 Aura Image Generation Service

```python
class AuraImageGenerator:
    """
    Generates aura overlay images using PIL/Pillow and OpenCV
    """
    
    def __init__(self):
        self.color_definitions = self._load_color_definitions()
        self.blur_kernels = {
            'soft': (51, 51),
            'medium': (71, 71),
            'strong': (101, 101)
        }
    
    def generate_aura_image(
        self,
        base_photo: np.ndarray,
        aura_profile: AuraProfile,
        style: str = 'soft'
    ) -> AuraImage:
        """
        Generate aura overlay on base photo
        """
        # Create aura layers
        aura_layers = self._create_aura_layers(
            base_photo.shape[:2],
            aura_profile,
            style
        )
        
        # Composite layers onto base photo
        composite = self._composite_aura(base_photo, aura_layers)
        
        # Add decorative elements
        composite = self._add_decorations(composite, aura_profile)
        
        # Convert to bytes
        image_bytes = self._encode_image(composite)
        
        return AuraImage(
            image_data=image_bytes,
            width=composite.shape[1],
            height=composite.shape[0],
            format='png',
            aura_profile=aura_profile,
            original_photo_id=''
        )
    
    def _create_aura_layers(
        self,
        image_size: Tuple[int, int],
        aura_profile: AuraProfile,
        style: str
    ) -> List[np.ndarray]:
        """
        Create individual aura color layers
        """
        layers = []
        height, width = image_size
        
        # Create gradient masks for each position
        center_x, center_y = width // 2, height // 2
        
        # Majority color layer (dominant)
        majority_layer = self._create_color_layer(
            image_size,
            self.color_definitions[aura_profile.majority_color],
            intensity=aura_profile.intensity / 100,
            position='center',
            spread=0.8
        )
        layers.append(majority_layer)
        
        # Moderate color layers
        for i, (color, pct) in enumerate(
            zip(aura_profile.moderate_colors, aura_profile.moderate_percentages)
        ):
            position = ['ascendant', 'descendant', 'cathedra', 'coronation'][i % 4]
            layer = self._create_color_layer(
                image_size,
                self.color_definitions[color],
                intensity=pct / 100 * 0.7,
                position=position,
                spread=0.5
            )
            layers.append(layer)
        
        # Minority color layers (subtle accents)
        for color, pct in zip(
            aura_profile.minority_colors, 
            aura_profile.minority_percentages
        ):
            layer = self._create_color_layer(
                image_size,
                self.color_definitions[color],
                intensity=pct / 100 * 0.4,
                position='etherea',
                spread=0.3
            )
            layers.append(layer)
        
        return layers
    
    def _create_color_layer(
        self,
        image_size: Tuple[int, int],
        color: Tuple[int, int, int],
        intensity: float,
        position: str,
        spread: float
    ) -> np.ndarray:
        """
        Create a single color aura layer with gradient
        """
        height, width = image_size
        
        # Create base layer
        layer = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Create gradient based on position
        if position == 'center':
            gradient = self._create_radial_gradient(
                (height, width),
                center=(width//2, height//2),
                radius=int(min(height, width) * spread)
            )
        elif position == 'ascendant':
            gradient = self._create_directional_gradient(
                (height, width),
                direction='right',
                spread=spread
            )
        elif position == 'descendant':
            gradient = self._create_directional_gradient(
                (height, width),
                direction='left',
                spread=spread
            )
        elif position == 'coronation':
            gradient = self._create_directional_gradient(
                (height, width),
                direction='up',
                spread=spread
            )
        elif position == 'cathedra':
            gradient = self._create_directional_gradient(
                (height, width),
                direction='down',
                spread=spread
            )
        else:  # etherea
            gradient = self._create_noise_gradient(
                (height, width),
                spread=spread
            )
        
        # Apply color and intensity
        layer[:, :, 0] = int(color[0] * intensity)  # R
        layer[:, :, 1] = int(color[1] * intensity)  # G
        layer[:, :, 2] = int(color[2] * intensity)  # B
        layer[:, :, 3] = (gradient * 255 * intensity).astype(np.uint8)  # Alpha
        
        # Apply blur for soft edges
        layer = cv2.GaussianBlur(layer, self.blur_kernels['soft'], 0)
        
        return layer
    
    def _composite_aura(
        self,
        base_photo: np.ndarray,
        aura_layers: List[np.ndarray]
    ) -> np.ndarray:
        """
        Composite aura layers onto base photo using alpha blending
        """
        result = base_photo.copy().astype(float)
        
        for layer in aura_layers:
            # Normalize alpha to 0-1
            alpha = layer[:, :, 3:4] / 255.0
            
            # Alpha blend
            result = result * (1 - alpha) + layer[:, :, :3] * alpha
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _load_color_definitions(self) -> Dict[str, Tuple[int, int, int]]:
        """Load RGB color definitions for all aura colors"""
        return {
            'red': (255, 50, 50),
            'orange': (255, 140, 0),
            'yellow': (255, 220, 0),
            'green': (50, 200, 50),
            'blue': (50, 100, 255),
            'indigo': (75, 0, 130),
            'violet': (148, 0, 211),
            'pink': (255, 105, 180),
            'white': (255, 255, 255),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192),
            'turquoise': (64, 224, 208),
            'magenta': (255, 0, 255),
            'emerald': (80, 200, 120),
            'citrine': (228, 208, 10),
            'amethyst': (153, 102, 204),
            'quartz': (255, 250, 250),
            'sapphire': (15, 82, 186),
            'ruby': (224, 17, 95),
            'garnet': (115, 54, 53),
            'opal': (169, 198, 213),
            'peridot': (142, 182, 80),
            'topaz': (255, 200, 124),
            'aquamarine': (127, 255, 212),
            'lapis': (38, 97, 156),
            'carnelian': (179, 27, 27),
            'rose_quartz': (251, 195, 195),
            'smoky_quartz': (96, 96, 96),
            'tigers_eye': (181, 137, 62),
            'moonstone': (210, 210, 230),
            'sunstone': (255, 165, 79),
            'labradorite': (128, 128, 160),
            'malachite': (11, 218, 81),
            'aventurine': (80, 180, 80),
            'obsidian': (20, 20, 20),
            'jade': (0, 168, 107),
            'amber': (255, 191, 0),
            'copper': (184, 115, 51),
        }
```

### 6.3 Color Definitions Reference

```python
# Complete color meanings for reading generation
COLOR_MEANINGS = {
    'red': {
        'name': 'Red',
        'keywords': ['energy', 'passion', 'strength', 'action', 'vitality'],
        'description': 'Red represents physical energy, passion, and vitality. It indicates a person who is action-oriented and full of life force.',
        'positive': ['Energetic', 'Passionate', 'Strong-willed', 'Courageous'],
        'challenges': ['May be impulsive', 'Can be aggressive', 'Might be restless'],
        'chakras': ['Root Chakra - Grounding and survival'],
        'elements': ['Fire'],
    },
    'orange': {
        'name': 'Orange',
        'keywords': ['creativity', 'joy', 'confidence', 'social', 'enthusiasm'],
        'description': 'Orange reflects creativity, emotional warmth, and social connection. It suggests an outgoing and optimistic personality.',
        'positive': ['Creative', 'Sociable', 'Optimistic', 'Adventurous'],
        'challenges': ['May seek attention', 'Can be restless', 'Might overindulge'],
        'chakras': ['Sacral Chakra - Creativity and emotions'],
        'elements': ['Fire', 'Water'],
    },
    'yellow': {
        'name': 'Yellow',
        'keywords': ['intellect', 'optimism', 'clarity', 'confidence', 'logic'],
        'description': 'Yellow indicates mental clarity, optimism, and intellectual energy. It shows a person who thinks clearly and radiates positivity.',
        'positive': ['Intelligent', 'Optimistic', 'Clear-thinking', 'Confident'],
        'challenges': ['May overthink', 'Can be critical', 'Might be anxious'],
        'chakras': ['Solar Plexus - Personal power and will'],
        'elements': ['Fire', 'Air'],
    },
    'green': {
        'name': 'Green',
        'keywords': ['growth', 'healing', 'balance', 'love', 'harmony'],
        'description': 'Green represents growth, healing energy, and balance. It indicates a nurturing person who brings harmony to others.',
        'positive': ['Healing', 'Balanced', 'Nurturing', 'Growth-oriented'],
        'challenges': ['May be overly accommodating', 'Can be jealous', 'Might resist change'],
        'chakras': ['Heart Chakra - Love and compassion'],
        'elements': ['Earth', 'Water'],
    },
    'blue': {
        'name': 'Blue',
        'keywords': ['communication', 'truth', 'calm', 'intuition', 'peace'],
        'description': 'Blue reflects communication, truth, and inner peace. It shows someone who values honesty and seeks harmony.',
        'positive': ['Truthful', 'Peaceful', 'Communicative', 'Intuitive'],
        'challenges': ['May suppress emotions', 'Can be distant', 'Might over-analyze'],
        'chakras': ['Throat Chakra - Communication and expression'],
        'elements': ['Water', 'Air'],
    },
    'indigo': {
        'name': 'Indigo',
        'keywords': ['intuition', 'wisdom', 'spirituality', 'perception', 'depth'],
        'description': 'Indigo indicates deep intuition, spiritual awareness, and inner wisdom. It suggests a person with strong psychic abilities.',
        'positive': ['Intuitive', 'Wise', 'Spiritual', 'Perceptive'],
        'challenges': ['May be withdrawn', 'Can be overly sensitive', 'Might escape reality'],
        'chakras': ['Third Eye Chakra - Intuition and insight'],
        'elements': ['Light', 'Ether'],
    },
    'violet': {
        'name': 'Violet',
        'keywords': ['spirituality', 'transformation', 'magic', 'vision', 'unity'],
        'description': 'Violet represents spiritual transformation, visionary thinking, and connection to higher consciousness.',
        'positive': ['Spiritual', 'Visionary', 'Transformative', 'Inspiring'],
        'challenges': ['May be impractical', 'Can be escapist', 'Might be aloof'],
        'chakras': ['Crown Chakra - Spiritual connection'],
        'elements': ['Ether', 'Cosmic'],
    },
    'pink': {
        'name': 'Pink',
        'keywords': ['love', 'compassion', 'gentleness', 'nurturing', 'sensitivity'],
        'description': 'Pink reflects unconditional love, compassion, and gentle energy. It indicates a caring and sensitive soul.',
        'positive': ['Loving', 'Compassionate', 'Gentle', 'Sensitive'],
        'challenges': ['May be overly emotional', 'Can be naive', 'Might avoid conflict'],
        'chakras': ['Heart Chakra - Love and healing'],
        'elements': ['Water', 'Earth'],
    },
    'white': {
        'name': 'White',
        'keywords': ['purity', 'protection', 'clarity', 'transcendence', 'truth'],
        'description': 'White represents purity, spiritual protection, and transcendence. It indicates a highly evolved spiritual state.',
        'positive': ['Pure', 'Protected', 'Clear', 'Transcendent'],
        'challenges': ['May be detached', 'Can be perfectionist', 'Might be isolated'],
        'chakras': ['All Chakras - Universal connection'],
        'elements': ['All Elements', 'Divine'],
    },
    'gold': {
        'name': 'Gold',
        'keywords': ['wisdom', 'enlightenment', 'abundance', 'divine', 'mastery'],
        'description': 'Gold indicates divine wisdom, spiritual mastery, and enlightened consciousness. It suggests a highly evolved soul.',
        'positive': ['Wise', 'Enlightened', 'Abundant', 'Masterful'],
        'challenges': ['May have ego issues', 'Can be materialistic', 'Might be prideful'],
        'chakras': ['Crown and Solar Plexus - Divine will'],
        'elements': ['Sun', 'Divine Fire'],
    },
    'silver': {
        'name': 'Silver',
        'keywords': ['intuition', 'feminine', 'mystery', 'reflection', 'adaptability'],
        'description': 'Silver reflects intuitive abilities, feminine energy, and the mysterious aspects of life.',
        'positive': ['Intuitive', 'Adaptable', 'Mysterious', 'Reflective'],
        'challenges': ['May be moody', 'Can be secretive', 'Might be indecisive'],
        'chakras': ['Third Eye and Crown - Lunar connection'],
        'elements': ['Moon', 'Water'],
    },
    'turquoise': {
        'name': 'Turquoise',
        'keywords': ['healing', 'communication', 'balance', 'protection', 'wholeness'],
        'description': 'Turquoise represents healing communication and protective energy. It bridges heart and throat chakra energies.',
        'positive': ['Healing', 'Communicative', 'Balanced', 'Protected'],
        'challenges': ['May be scattered', 'Can be unpredictable', 'Might be restless'],
        'chakras': ['Heart and Throat - Healing communication'],
        'elements': ['Water', 'Air'],
    },
    'magenta': {
        'name': 'Magenta',
        'keywords': ['transformation', 'universal love', 'harmony', 'change', 'integration'],
        'description': 'Magenta indicates transformative energy and universal love. It bridges the physical and spiritual realms.',
        'positive': ['Transformative', 'Loving', 'Harmonious', 'Integrative'],
        'challenges': ['May be intense', 'Can be overwhelming', 'Might be unstable'],
        'chakras': ['Transpersonal - Above the crown'],
        'elements': ['Cosmic', 'Universal'],
    },
    'emerald': {
        'name': 'Emerald',
        'keywords': ['healing', 'abundance', 'growth', 'love', 'vitality'],
        'description': 'Emerald represents deep healing, abundant growth, and heart-centered love.',
        'positive': ['Healing', 'Abundant', 'Growing', 'Loving'],
        'challenges': ['May be possessive', 'Can be jealous', 'Might be materialistic'],
        'chakras': ['Heart Chakra - Deep healing'],
        'elements': ['Earth'],
    },
    'citrine': {
        'name': 'Citrine',
        'keywords': ['abundance', 'joy', 'manifestation', 'confidence', 'clarity'],
        'description': 'Citrine indicates manifesting energy, joy, and personal power. It attracts abundance and positivity.',
        'positive': ['Abundant', 'Joyful', 'Manifesting', 'Confident'],
        'challenges': ['May be scattered', 'Can be impatient', 'Might be greedy'],
        'chakras': ['Solar Plexus - Manifestation'],
        'elements': ['Fire', 'Sun'],
    },
    'amethyst': {
        'name': 'Amethyst',
        'keywords': ['spirituality', 'protection', 'clarity', 'transformation', 'peace'],
        'description': 'Amethyst represents spiritual protection, mental clarity, and transformative peace.',
        'positive': ['Spiritual', 'Protected', 'Clear', 'Peaceful'],
        'challenges': ['May be escapist', 'Can be detached', 'Might be spacey'],
        'chakras': ['Third Eye and Crown - Spiritual protection'],
        'elements': ['Air', 'Water'],
    },
    'quartz': {
        'name': 'Quartz',
        'keywords': ['clarity', 'amplification', 'healing', 'energy', 'programmability'],
        'description': 'Quartz indicates clarity, energy amplification, and programmable intention.',
        'positive': ['Clear', 'Amplified', 'Healing', 'Focused'],
        'challenges': ['May be too sensitive', 'Can absorb negativity', 'Might need cleansing'],
        'chakras': ['All Chakras - Universal amplifier'],
        'elements': ['All Elements'],
    },
    'sapphire': {
        'name': 'Sapphire',
        'keywords': ['wisdom', 'royalty', 'truth', 'focus', 'discipline'],
        'description': 'Sapphire represents royal wisdom, truth, and focused discipline.',
        'positive': ['Wise', 'Truthful', 'Focused', 'Disciplined'],
        'challenges': ['May be rigid', 'Can be cold', 'Might be judgmental'],
        'chakras': ['Throat and Third Eye - Royal wisdom'],
        'elements': ['Water', 'Air'],
    },
    'ruby': {
        'name': 'Ruby',
        'keywords': ['passion', 'vitality', 'courage', 'love', 'power'],
        'description': 'Ruby indicates passionate vitality, courageous love, and personal power.',
        'positive': ['Passionate', 'Vital', 'Courageous', 'Powerful'],
        'challenges': ['May be impulsive', 'Can be aggressive', 'Might be controlling'],
        'chakras': ['Root and Heart - Passionate love'],
        'elements': ['Fire'],
    },
    'garnet': {
        'name': 'Garnet',
        'keywords': ['commitment', 'passion', 'energy', 'regeneration', 'devotion'],
        'description': 'Garnet represents committed passion, regenerative energy, and devoted love.',
        'positive': ['Committed', 'Passionate', 'Energetic', 'Devoted'],
        'challenges': ['May be possessive', 'Can be obsessive', 'Might be stubborn'],
        'chakras': ['Root and Heart - Committed love'],
        'elements': ['Fire', 'Earth'],
    },
    'opal': {
        'name': 'Opal',
        'keywords': ['inspiration', 'creativity', 'transformation', 'mystery', 'emotion'],
        'description': 'Opal indicates inspired creativity, emotional transformation, and mysterious depths.',
        'positive': ['Inspired', 'Creative', 'Transformative', 'Emotional'],
        'challenges': ['May be moody', 'Can be unpredictable', 'Might be sensitive'],
        'chakras': ['All Chakras - Color play'],
        'elements': ['Water', 'Fire'],
    },
    'peridot': {
        'name': 'Peridot',
        'keywords': ['healing', 'renewal', 'growth', 'compassion', 'abundance'],
        'description': 'Peridot represents healing renewal, growth, and compassionate abundance.',
        'positive': ['Healing', 'Renewing', 'Growing', 'Compassionate'],
        'challenges': ['May be naive', 'Can be overly trusting', 'Might be gullible'],
        'chakras': ['Heart and Solar Plexus - Healing growth'],
        'elements': ['Earth', 'Fire'],
    },
    'topaz': {
        'name': 'Topaz',
        'keywords': ['clarity', 'strength', 'wisdom', 'confidence', 'truth'],
        'description': 'Topaz indicates mental clarity, inner strength, and confident wisdom.',
        'positive': ['Clear', 'Strong', 'Wise', 'Confident'],
        'challenges': ['May be prideful', 'Can be stubborn', 'Might be inflexible'],
        'chakras': ['Solar Plexus and Throat - Confident truth'],
        'elements': ['Fire', 'Air'],
    },
    'aquamarine': {
        'name': 'Aquamarine',
        'keywords': ['calm', 'courage', 'communication', 'clarity', 'soothing'],
        'description': 'Aquamarine represents calm courage, clear communication, and soothing energy.',
        'positive': ['Calm', 'Courageous', 'Communicative', 'Clear'],
        'challenges': ['May be passive', 'Can be avoidant', 'Might be detached'],
        'chakras': ['Throat - Calm communication'],
        'elements': ['Water'],
    },
    'lapis': {
        'name': 'Lapis Lazuli',
        'keywords': ['wisdom', 'truth', 'inner vision', 'royalty', 'communication'],
        'description': 'Lapis indicates deep wisdom, truth, and inner vision. It connects to royal consciousness.',
        'positive': ['Wise', 'Truthful', 'Visionary', 'Royal'],
        'challenges': ['May be elitist', 'Can be dogmatic', 'Might be controlling'],
        'chakras': ['Third Eye and Throat - Royal wisdom'],
        'elements': ['Air', 'Water'],
    },
    'carnelian': {
        'name': 'Carnelian',
        'keywords': ['motivation', 'courage', 'creativity', 'vitality', 'action'],
        'description': 'Carnelian represents motivated action, creative courage, and vital energy.',
        'positive': ['Motivated', 'Courageous', 'Creative', 'Vital'],
        'challenges': ['May be impulsive', 'Can be aggressive', 'Might be reckless'],
        'chakras': ['Sacral - Creative action'],
        'elements': ['Fire'],
    },
    'rose_quartz': {
        'name': 'Rose Quartz',
        'keywords': ['love', 'compassion', 'healing', 'peace', 'self-love'],
        'description': 'Rose Quartz indicates unconditional love, compassionate healing, and peaceful self-acceptance.',
        'positive': ['Loving', 'Compassionate', 'Healing', 'Peaceful'],
        'challenges': ['May be overly emotional', 'Can be naive', 'Might be dependent'],
        'chakras': ['Heart - Unconditional love'],
        'elements': ['Water', 'Earth'],
    },
    'smoky_quartz': {
        'name': 'Smoky Quartz',
        'keywords': ['grounding', 'protection', 'transformation', 'release', 'stability'],
        'description': 'Smoky Quartz represents grounding protection, transformative release, and stable energy.',
        'positive': ['Grounded', 'Protected', 'Transformative', 'Stable'],
        'challenges': ['May be pessimistic', 'Can be stuck', 'Might be resistant'],
        'chakras': ['Root - Grounding protection'],
        'elements': ['Earth'],
    },
    'tigers_eye': {
        'name': "Tiger's Eye",
        'keywords': ['protection', 'confidence', 'clarity', 'grounding', 'willpower'],
        'description': "Tiger's Eye indicates protective confidence, clear willpower, and grounded determination.",
        'positive': ['Protected', 'Confident', 'Clear', 'Determined'],
        'challenges': ['May be stubborn', 'Can be aggressive', 'Might be controlling'],
        'chakras': ['Solar Plexus - Confident will'],
        'elements': ['Earth', 'Fire'],
    },
    'moonstone': {
        'name': 'Moonstone',
        'keywords': ['intuition', 'feminine', 'cycles', 'new beginnings', 'emotional balance'],
        'description': 'Moonstone represents intuitive feminine energy, cyclical new beginnings, and emotional balance.',
        'positive': ['Intuitive', 'Balanced', 'Cyclical', 'Renewing'],
        'challenges': ['May be moody', 'Can be irrational', 'Might be unstable'],
        'chakras': ['Crown and Third Eye - Lunar intuition'],
        'elements': ['Water', 'Moon'],
    },
    'sunstone': {
        'name': 'Sunstone',
        'keywords': ['joy', 'abundance', 'leadership', 'personal power', 'optimism'],
        'description': 'Sunstone indicates joyful abundance, leadership power, and optimistic energy.',
        'positive': ['Joyful', 'Abundant', 'Leader', 'Optimistic'],
        'challenges': ['May be arrogant', 'Can be dominating', 'Might be prideful'],
        'chakras': ['Solar Plexus and Sacral - Solar power'],
        'elements': ['Fire', 'Sun'],
    },
    'labradorite': {
        'name': 'Labradorite',
        'keywords': ['transformation', 'protection', 'magic', 'intuition', 'strength'],
        'description': 'Labradorite represents transformative protection, magical intuition, and inner strength.',
        'positive': ['Transformative', 'Protected', 'Magical', 'Strong'],
        'challenges': ['May be secretive', 'Can be mysterious', 'Might be elusive'],
        'chakras': ['Third Eye and Crown - Magical transformation'],
        'elements': ['Air', 'Water'],
    },
    'malachite': {
        'name': 'Malachite',
        'keywords': ['transformation', 'protection', 'healing', 'abundance', 'change'],
        'description': 'Malachite indicates transformative healing, protective abundance, and powerful change.',
        'positive': ['Transformative', 'Protected', 'Healing', 'Abundant'],
        'challenges': ['May be intense', 'Can be overwhelming', 'Might be chaotic'],
        'chakras': ['Heart and Solar Plexus - Transformative healing'],
        'elements': ['Earth'],
    },
    'aventurine': {
        'name': 'Aventurine',
        'keywords': ['luck', 'prosperity', 'confidence', 'leadership', 'opportunity'],
        'description': 'Aventurine represents lucky prosperity, confident leadership, and new opportunities.',
        'positive': ['Lucky', 'Prosperous', 'Confident', 'Opportunistic'],
        'challenges': ['May be reckless', 'Can be greedy', 'Might be opportunistic'],
        'chakras': ['Heart - Lucky love'],
        'elements': ['Earth'],
    },
    'obsidian': {
        'name': 'Obsidian',
        'keywords': ['protection', 'grounding', 'truth', 'transformation', 'release'],
        'description': 'Obsidian indicates protective grounding, harsh truth, and transformative release.',
        'positive': ['Protected', 'Grounded', 'Truthful', 'Transformative'],
        'challenges': ['May be harsh', 'Can be negative', 'Might be destructive'],
        'chakras': ['Root - Protective grounding'],
        'elements': ['Earth', 'Fire'],
    },
    'jade': {
        'name': 'Jade',
        'keywords': ['harmony', 'balance', 'good fortune', 'wisdom', 'longevity'],
        'description': 'Jade represents harmonious balance, good fortune, and ancient wisdom.',
        'positive': ['Harmonious', 'Balanced', 'Fortunate', 'Wise'],
        'challenges': ['May be materialistic', 'Can be status-conscious', 'Might be possessive'],
        'chakras': ['Heart - Harmonious love'],
        'elements': ['Earth'],
    },
    'amber': {
        'name': 'Amber',
        'keywords': ['healing', 'warmth', 'vitality', 'protection', 'cleansing'],
        'description': 'Amber indicates warm healing, vital protection, and cleansing energy.',
        'positive': ['Healing', 'Warm', 'Vital', 'Protected'],
        'challenges': ['May be stuck', 'Can be stagnant', 'Might be inflexible'],
        'chakras': ['Solar Plexus - Warm healing'],
        'elements': ['Earth', 'Fire'],
    },
    'copper': {
        'name': 'Copper',
        'keywords': ['conductivity', 'healing', 'balance', 'energy flow', 'vitality'],
        'description': 'Copper represents conductive healing, balanced energy flow, and vital conductivity.',
        'positive': ['Conductive', 'Healing', 'Balanced', 'Vital'],
        'challenges': ['May be restless', 'Can be scattered', 'Might be unfocused'],
        'chakras': ['All Chakras - Energy conductor'],
        'elements': ['Earth', 'Metal'],
    },
}
```

---

## 7. Database Schema

### 7.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE SCHEMA                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    users     │       │   sessions   │       │    auras     │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │◄──────│ user_id (FK) │       │ id (PK)      │
│ email        │       │ id (PK)      │◄──────│ session_id   │
│ password_hash│       │ started_at   │       │ user_id (FK) │
│ created_at   │       │ completed_at │       │ profile_json │
│ updated_at   │       │ status       │       │ image_url    │
│ is_active    │       │ biofeedback  │       │ reading_text │
│ subscription │       │ metadata     │       │ created_at   │
└──────────────┘       └──────────────┘       └──────────────┘
        │                      │                      │
        │              ┌───────┴───────┐              │
        │              │               │              │
        ▼              ▼               ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│subscriptions │  │biofeedback_  │  │   photos     │  │   readings   │
├──────────────┤  │   readings   │  ├──────────────┤  ├──────────────┤
│ id (PK)      │  ├──────────────┤  │ id (PK)      │  │ id (PK)      │
│ user_id (FK) │  │ id (PK)      │  │ session_id   │  │ aura_id (FK) │
│ plan_type    │  │ session_id   │  │ user_id (FK) │  │ section      │
│ status       │  │ timestamp    │  │ original_url │  │ content      │
│ started_at   │  │ touch_x      │  │ processed_url│  │ color_refs   │
│ expires_at   │  │ touch_y      │  │ created_at   │  │ created_at   │
│ payment_id   │  │ pressure     │  └──────────────┘  └──────────────┘
└──────────────┘  │ stability    │
                  │ derived_data │
                  └──────────────┘
```

### 7.2 SQL Schema Definition

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    subscription_status VARCHAR(50) DEFAULT 'inactive',
    daily_sessions_used INTEGER DEFAULT 0,
    daily_sessions_reset_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions Table (Photo Sessions)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'started', -- started, capturing, processing, completed, failed
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    face_detected BOOLEAN DEFAULT false,
    alignment_score DECIMAL(3,2),
    biofeedback_duration_ms INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Biofeedback Readings Table
CREATE TABLE biofeedback_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    touch_x DECIMAL(5,4), -- 0-1 normalized
    touch_y DECIMAL(5,4), -- 0-1 normalized
    pressure DECIMAL(5,4), -- 0-1 simulated
    stability DECIMAL(5,4), -- 0-1 movement stability
    simulated_gsr DECIMAL(5,4), -- derived
    simulated_hrv DECIMAL(5,4), -- derived
    stress_indicator DECIMAL(5,4), -- derived
    calmness_score DECIMAL(5,4), -- derived
    raw_data JSONB -- any additional sensor data
);

-- Photos Table
CREATE TABLE photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    original_url VARCHAR(500) NOT NULL,
    processed_url VARCHAR(500),
    width INTEGER,
    height INTEGER,
    format VARCHAR(10),
    file_size_bytes INTEGER,
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Aura Profiles Table
CREATE TABLE aura_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    majority_color VARCHAR(50) NOT NULL,
    majority_percentage DECIMAL(5,2),
    moderate_colors JSONB, -- array of colors
    moderate_percentages JSONB, -- array of percentages
    minority_colors JSONB, -- array of colors
    minority_percentages JSONB, -- array of percentages
    intensity DECIMAL(5,2),
    brightness DECIMAL(5,2),
    saturation DECIMAL(5,2),
    positioning JSONB, -- ascendant, descendant, etc.
    profile_data JSONB, -- complete profile object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Aura Images Table
CREATE TABLE aura_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aura_profile_id UUID REFERENCES aura_profiles(id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    width INTEGER,
    height INTEGER,
    format VARCHAR(10),
    style VARCHAR(50), -- soft, medium, strong
    file_size_bytes INTEGER,
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Readings Table
CREATE TABLE readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aura_profile_id UUID REFERENCES aura_profiles(id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    section VARCHAR(50) NOT NULL, -- color_analysis, alignment, guidance
    title VARCHAR(200),
    content TEXT NOT NULL,
    color_references JSONB, -- colors mentioned in this section
    generated_by VARCHAR(50) DEFAULT 'ai', -- ai, template, hybrid
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subscriptions Table
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan_type VARCHAR(50) NOT NULL, -- free, weekly, monthly, yearly
    status VARCHAR(50) DEFAULT 'active', -- active, cancelled, expired, paused
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    payment_provider VARCHAR(50), -- stripe, paypal, etc.
    payment_provider_subscription_id VARCHAR(255),
    price_cents INTEGER,
    currency VARCHAR(3) DEFAULT 'USD',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments Table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE SET NULL,
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50) DEFAULT 'pending', -- pending, completed, failed, refunded
    payment_provider VARCHAR(50),
    payment_provider_charge_id VARCHAR(255),
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Sessions (Auth) Table
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_valid BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50), -- user, session, photo, etc.
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier, subscription_status);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
CREATE INDEX idx_biofeedback_session_id ON biofeedback_readings(session_id);
CREATE INDEX idx_photos_user_id ON photos(user_id);
CREATE INDEX idx_photos_session_id ON photos(session_id);
CREATE INDEX idx_aura_profiles_user_id ON aura_profiles(user_id);
CREATE INDEX idx_readings_user_id ON readings(user_id);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 8. API Specification

### 8.1 API Endpoints Overview

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/register | Register new user | No |
| POST | /api/auth/login | User login | No |
| POST | /api/auth/logout | User logout | Yes |
| POST | /api/auth/refresh | Refresh token | Yes |
| GET | /api/users/me | Get current user | Yes |
| PUT | /api/users/me | Update user profile | Yes |
| POST | /api/sessions | Create new session | Yes |
| GET | /api/sessions | List user sessions | Yes |
| GET | /api/sessions/:id | Get session details | Yes |
| POST | /api/sessions/:id/capture | Capture photo | Yes |
| POST | /api/sessions/:id/biofeedback | Submit biofeedback | Yes |
| POST | /api/sessions/:id/generate | Generate aura | Yes |
| GET | /api/auras | List user auras | Yes |
| GET | /api/auras/:id | Get aura details | Yes |
| GET | /api/auras/:id/image | Get aura image | Yes |
| GET | /api/auras/:id/reading | Get aura reading | Yes |
| GET | /api/subscriptions/plans | List subscription plans | No |
| POST | /api/subscriptions | Create subscription | Yes |
| GET | /api/subscriptions/me | Get current subscription | Yes |
| POST | /api/subscriptions/cancel | Cancel subscription | Yes |
| POST | /api/payments/intent | Create payment intent | Yes |
| POST | /api/webhooks/stripe | Stripe webhook | No |

### 8.2 Detailed API Specifications

#### Authentication Endpoints

```yaml
# POST /api/auth/register
Register:
  request:
    body:
      email: string (required, email format)
      password: string (required, min 8 chars)
      first_name: string (optional)
      last_name: string (optional)
  response:
    201:
      user:
        id: uuid
        email: string
        first_name: string
        last_name: string
        created_at: datetime
      token: string (JWT)
      refresh_token: string
    400: Validation error
    409: Email already exists

# POST /api/auth/login
Login:
  request:
    body:
      email: string (required)
      password: string (required)
  response:
    200:
      user:
        id: uuid
        email: string
        first_name: string
        last_name: string
        subscription_tier: string
      token: string (JWT)
      refresh_token: string
      expires_in: number (seconds)
    401: Invalid credentials
```

#### Session Endpoints

```yaml
# POST /api/sessions
Create Session:
  request:
    headers:
      Authorization: Bearer {token}
    body:
      mode: string (optional, default: 'selfie') # selfie, friend
  response:
    201:
      session:
        id: uuid
        user_id: uuid
        status: string
        started_at: datetime
        mode: string
      upload_url: string (for photo upload)
      
# POST /api/sessions/:id/capture
Capture Photo:
  request:
    headers:
      Authorization: Bearer {token}
      Content-Type: multipart/form-data
    body:
      photo: file (required, image/jpeg or image/png)
      face_data: json (optional, client-side face detection)
  response:
    200:
      session:
        id: uuid
        status: string
      photo:
        id: uuid
        url: string
        width: number
        height: number
      face_detection:
        found: boolean
        landmarks: array
        alignment_score: number
        bounding_box: object
      next_step: string # 'biofeedback' or 'retry'

# POST /api/sessions/:id/biofeedback
Submit Biofeedback:
  request:
    headers:
      Authorization: Bearer {token}
    body:
      readings: array
        - timestamp: datetime
          touch_x: number (0-1)
          touch_y: number (0-1)
          pressure: number (0-1)
          stability: number (0-1)
      duration_ms: number
  response:
    200:
      session:
        id: uuid
        status: string
      biofeedback:
        average_stability: number
        stability_variance: number
        touch_pattern: string
        simulated_gsr: number
        simulated_hrv: number
        stress_indicator: number
        calmness_score: number
      next_step: string # 'generate'

# POST /api/sessions/:id/generate
Generate Aura:
  request:
    headers:
      Authorization: Bearer {token}
    body:
      style: string (optional, default: 'soft') # soft, medium, strong
  response:
    200:
      session:
        id: uuid
        status: 'completed'
        completed_at: datetime
      aura:
        id: uuid
        profile:
          majority_color: string
          majority_percentage: number
          moderate_colors: array
          moderate_percentages: array
          minority_colors: array
          minority_percentages: array
          intensity: number
          brightness: number
          saturation: number
          positioning: object
        image_url: string
        thumbnail_url: string
      reading:
        sections: array
          - section: string
            title: string
            content: string
```

#### Aura Endpoints

```yaml
# GET /api/auras
List Auras:
  request:
    headers:
      Authorization: Bearer {token}
    query:
      limit: number (default: 20)
      offset: number (default: 0)
      order_by: string (default: 'created_at')
      order: string (default: 'desc')
  response:
    200:
      auras: array
        - id: uuid
          image_url: string
          thumbnail_url: string
          majority_color: string
          created_at: datetime
      pagination:
        total: number
        limit: number
        offset: number
        has_more: boolean

# GET /api/auras/:id
Get Aura Details:
  request:
    headers:
      Authorization: Bearer {token}
  response:
    200:
      aura:
        id: uuid
        session_id: uuid
        profile: object (complete aura profile)
        image_url: string
        thumbnail_url: string
        created_at: datetime
      reading:
        sections: array
      photo:
        original_url: string
```

#### Subscription Endpoints

```yaml
# GET /api/subscriptions/plans
List Plans:
  response:
    200:
      plans: array
        - id: string
          name: string
          description: string
          price_cents: number
          currency: string
          interval: string # weekly, monthly, yearly
          features: array
          sessions_per_day: number

# POST /api/subscriptions
Create Subscription:
  request:
    headers:
      Authorization: Bearer {token}
    body:
      plan_id: string (required)
      payment_method_id: string (required)
  response:
    201:
      subscription:
        id: uuid
        plan_type: string
        status: string
        started_at: datetime
        expires_at: datetime
      client_secret: string (for Stripe confirmation)
```

---

## 9. Frontend Components

### 9.1 Component Architecture

```
src/
├── app/                          # Next.js App Router
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── layout.tsx
│   ├── (main)/
│   │   ├── dashboard/
│   │   ├── history/
│   │   ├── profile/
│   │   └── layout.tsx
│   ├── api/                      # API Routes
│   ├── session/
│   │   └── [id]/
│   │       ├── capture/
│   │       ├── biofeedback/
│   │       └── result/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── camera/
│   │   ├── CameraPreview.tsx
│   │   ├── FaceDetectionOverlay.tsx
│   │   ├── AlignmentGuide.tsx
│   │   └── CaptureButton.tsx
│   ├── biofeedback/
│   │   ├── BiofeedbackCollector.tsx
│   │   ├── TouchIndicator.tsx
│   │   ├── ProgressBar.tsx
│   │   └── StabilityMeter.tsx
│   ├── aura/
│   │   ├── AuraDisplay.tsx
│   │   ├── AuraImage.tsx
│   │   ├── ColorLegend.tsx
│   │   └── ReadingCard.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Navigation.tsx
│   │   └── Sidebar.tsx
│   └── common/
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       └── Toast.tsx
├── hooks/
│   ├── useCamera.ts
│   ├── useFaceDetection.ts
│   ├── useBiofeedback.ts
│   ├── useSession.ts
│   └── useAuth.ts
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   ├── utils.ts
│   └── constants.ts
├── store/
│   ├── authStore.ts
│   ├── sessionStore.ts
│   └── uiStore.ts
├── types/
│   ├── auth.ts
│   ├── session.ts
│   ├── aura.ts
│   └── index.ts
└── styles/
    └── globals.css
```

### 9.2 Key React Components

#### Camera Component

```typescript
// components/camera/CameraCapture.tsx
'use client';

import { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { FaceDetectionOverlay } from './FaceDetectionOverlay';
import { AlignmentGuide } from './AlignmentGuide';
import { useFaceDetection } from '@/hooks/useFaceDetection';
import { Button } from '@/components/ui/button';

interface CameraCaptureProps {
  onCapture: (imageData: string, faceData: FaceDetectionResult) => void;
  mode?: 'selfie' | 'friend';
}

export const CameraCapture: React.FC<CameraCaptureProps> = ({
  onCapture,
  mode = 'selfie'
}) => {
  const webcamRef = useRef<Webcam>(null);
  const [isReady, setIsReady] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  
  const {
    faceData,
    isDetecting,
    alignmentScore,
    startDetection,
    stopDetection
  } = useFaceDetection({
    minDetectionConfidence: 0.5,
    onFaceDetected: (data) => {
      console.log('Face detected:', data);
    }
  });

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: mode === 'selfie' ? 'user' : 'environment'
  };

  const handleCapture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc && faceData) {
      setCapturedImage(imageSrc);
      onCapture(imageSrc, faceData);
    }
  }, [faceData, onCapture]);

  const isAligned = alignmentScore >= 0.8;

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      {/* Camera Preview */}
      <div className="relative aspect-video bg-black rounded-2xl overflow-hidden">
        {!capturedImage ? (
          <>
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              screenshotQuality={0.95}
              videoConstraints={videoConstraints}
              onUserMedia={() => {
                setIsReady(true);
                startDetection();
              }}
              className="w-full h-full object-cover"
            />
            
            {/* Face Detection Overlay */}
            {isReady && (
              <FaceDetectionOverlay
                faceData={faceData}
                isDetecting={isDetecting}
              />
            )}
            
            {/* Alignment Guide */}
            <AlignmentGuide
              alignmentScore={alignmentScore}
              isAligned={isAligned}
            />
          </>
        ) : (
          <img
            src={capturedImage}
            alt="Captured"
            className="w-full h-full object-cover"
          />
        )}
      </div>

      {/* Controls */}
      <div className="mt-6 flex justify-center gap-4">
        {!capturedImage ? (
          <Button
            size="lg"
            onClick={handleCapture}
            disabled={!isAligned}
            className="rounded-full px-8"
          >
            {isAligned ? 'Capture' : 'Align Your Face'}
          </Button>
        ) : (
          <>
            <Button
              variant="outline"
              onClick={() => {
                setCapturedImage(null);
                startDetection();
              }}
            >
              Retake
            </Button>
            <Button onClick={() => onCapture(capturedImage, faceData!)}>
              Continue
            </Button>
          </>
        )}
      </div>
    </div>
  );
};
```

#### Biofeedback Collector Component

```typescript
// components/biofeedback/BiofeedbackCollector.tsx
'use client';

import { useEffect, useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Progress } from '@/components/ui/progress';
import { useBiofeedback } from '@/hooks/useBiofeedback';

interface BiofeedbackCollectorProps {
  sessionId: string;
  onComplete: (data: BiofeedbackSession) => void;
  durationMs?: number;
}

export const BiofeedbackCollector: React.FC<BiofeedbackCollectorProps> = ({
  sessionId,
  onComplete,
  durationMs = 5000
}) => {
  const [progress, setProgress] = useState(0);
  const [touchPosition, setTouchPosition] = useState({ x: 0.5, y: 0.5 });
  
  const { 
    isCollecting, 
    readings, 
    startCollection, 
    stopCollection,
    stability 
  } = useBiofeedback({
    sampleRate: 30,
    onComplete
  });

  useEffect(() => {
    startCollection();
    
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + (100 / (durationMs / 100));
        if (newProgress >= 100) {
          stopCollection();
          clearInterval(interval);
          return 100;
        }
        return newProgress;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [durationMs, startCollection, stopCollection]);

  const handleTouchMove = useCallback((e: React.TouchEvent | React.MouseEvent) => {
    const container = e.currentTarget as HTMLElement;
    const rect = container.getBoundingClientRect();
    
    let clientX, clientY;
    if ('touches' in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = (e as React.MouseEvent).clientX;
      clientY = (e as React.MouseEvent).clientY;
    }
    
    setTouchPosition({
      x: (clientX - rect.left) / rect.width,
      y: (clientY - rect.top) / rect.height
    });
  }, []);

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="text-center">
        <h2 className="text-2xl font-semibold mb-2">
          Hold Your Position
        </h2>
        <p className="text-muted-foreground">
          Keep your thumbs on the sensors while we read your energy
        </p>
      </div>

      {/* Touch Area */}
      <div
        className="relative w-64 h-64 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 border-2 border-primary/30 touch-none"
        onTouchMove={handleTouchMove}
        onMouseMove={handleTouchMove}
      >
        {/* Touch Indicator */}
        <motion.div
          className="absolute w-16 h-16 rounded-full bg-primary/50 blur-xl"
          animate={{
            x: touchPosition.x * 256 - 32,
            y: touchPosition.y * 256 - 32,
          }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        />
        
        {/* Stability Ring */}
        <svg className="absolute inset-0 w-full h-full">
          <circle
            cx="50%"
            cy="50%"
            r="45%"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="text-primary/30"
            strokeDasharray={`${stability * 283} 283`}
            transform="rotate(-90 128 128)"
          />
        </svg>
        
        {/* Center Icon */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center">
            <span className="text-4xl">✨</span>
          </div>
        </div>
      </div>

      {/* Progress */}
      <div className="w-full max-w-md space-y-2">
        <div className="flex justify-between text-sm">
          <span>Collecting Energy...</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Stability Indicator */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>Stability:</span>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className={`w-2 h-2 rounded-full ${
                i <= Math.round(stability * 5)
                  ? 'bg-green-500'
                  : 'bg-gray-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
```

#### Aura Display Component

```typescript
// components/aura/AuraDisplay.tsx
'use client';

import { motion } from 'framer-motion';
import { AuraImage } from './AuraImage';
import { ColorLegend } from './ColorLegend';
import { ReadingCard } from './ReadingCard';
import { Button } from '@/components/ui/button';
import { Download, Share2 } from 'lucide-react';

interface AuraDisplayProps {
  aura: AuraWithReading;
  onDownload: () => void;
  onShare: () => void;
}

export const AuraDisplay: React.FC<AuraDisplayProps> = ({
  aura,
  onDownload,
  onShare
}) => {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Aura Image */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative aspect-square max-w-lg mx-auto"
      >
        <AuraImage
          src={aura.image_url}
          alt="Your Aura"
          className="rounded-2xl shadow-2xl"
        />
        
        {/* Glow Effect */}
        <div 
          className="absolute inset-0 rounded-2xl opacity-50 blur-3xl -z-10"
          style={{
            background: `radial-gradient(circle, ${aura.profile.majority_color}40, transparent 70%)`
          }}
        />
      </motion.div>

      {/* Color Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <ColorLegend profile={aura.profile} />
      </motion.div>

      {/* Reading */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="space-y-4"
      >
        <h3 className="text-xl font-semibold text-center">
          Your Aura Reading
        </h3>
        {aura.reading.sections.map((section, index) => (
          <ReadingCard
            key={section.section}
            section={section}
            delay={index * 0.1}
          />
        ))}
      </motion.div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="flex justify-center gap-4"
      >
        <Button variant="outline" onClick={onDownload}>
          <Download className="w-4 h-4 mr-2" />
          Download
        </Button>
        <Button onClick={onShare}>
          <Share2 className="w-4 h-4 mr-2" />
          Share
        </Button>
      </motion.div>
    </div>
  );
};
```

---

## 10. Project Structure

### 10.1 Complete File Tree

```
aura-camera-app/
├── README.md
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
├── postcss.config.js
├── .env.example
├── .env.local
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Makefile
│
├── prisma/                          # Database schema & migrations
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
│
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── (main)/
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── history/
│   │   │   │   └── page.tsx
│   │   │   ├── profile/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── session/
│   │   │   └── [id]/
│   │   │       ├── capture/
│   │   │       │   └── page.tsx
│   │   │       ├── biofeedback/
│   │   │       │   └── page.tsx
│   │   │       └── result/
│   │   │           └── page.tsx
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── [...nextauth]/
│   │   │   │   │   └── route.ts
│   │   │   │   ├── register/
│   │   │   │   │   └── route.ts
│   │   │   │   └── refresh/
│   │   │   │       └── route.ts
│   │   │   ├── sessions/
│   │   │   │   ├── route.ts
│   │   │   │   └── [id]/
│   │   │   │       ├── route.ts
│   │   │   │       ├── capture/
│   │   │   │       │   └── route.ts
│   │   │   │       ├── biofeedback/
│   │   │   │       │   └── route.ts
│   │   │   │       └── generate/
│   │   │   │           └── route.ts
│   │   │   ├── auras/
│   │   │   │   ├── route.ts
│   │   │   │   └── [id]/
│   │   │   │       ├── route.ts
│   │   │   │       ├── image/
│   │   │   │       │   └── route.ts
│   │   │   │       └── reading/
│   │   │   │           └── route.ts
│   │   │   ├── subscriptions/
│   │   │   │   ├── route.ts
│   │   │   │   ├── plans/
│   │   │   │   │   └── route.ts
│   │   │   │   └── me/
│   │   │   │       └── route.ts
│   │   │   └── webhooks/
│   │   │       └── stripe/
│   │   │           └── route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── select.tsx
│   │   │   ├── toast.tsx
│   │   │   └── toaster.tsx
│   │   ├── camera/
│   │   │   ├── CameraCapture.tsx
│   │   │   ├── CameraPreview.tsx
│   │   │   ├── FaceDetectionOverlay.tsx
│   │   │   ├── AlignmentGuide.tsx
│   │   │   └── CaptureButton.tsx
│   │   ├── biofeedback/
│   │   │   ├── BiofeedbackCollector.tsx
│   │   │   ├── TouchIndicator.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   └── StabilityMeter.tsx
│   │   ├── aura/
│   │   │   ├── AuraDisplay.tsx
│   │   │   ├── AuraImage.tsx
│   │   │   ├── ColorLegend.tsx
│   │   │   ├── ColorBar.tsx
│   │   │   ├── PositioningChart.tsx
│   │   │   └── ReadingCard.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── MobileMenu.tsx
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       ├── EmptyState.tsx
│   │       └── Toast.tsx
│   │
│   ├── hooks/
│   │   ├── useCamera.ts
│   │   ├── useFaceDetection.ts
│   │   ├── useBiofeedback.ts
│   │   ├── useSession.ts
│   │   ├── useAuth.ts
│   │   ├── useToast.ts
│   │   └── useSubscription.ts
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── prisma.ts
│   │   ├── stripe.ts
│   │   ├── cloudinary.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   │
│   ├── store/
│   │   ├── authStore.ts
│   │   ├── sessionStore.ts
│   │   └── uiStore.ts
│   │
│   ├── types/
│   │   ├── auth.ts
│   │   ├── session.ts
│   │   ├── aura.ts
│   │   ├── biofeedback.ts
│   │   ├── subscription.ts
│   │   └── index.ts
│   │
│   └── styles/
│       └── globals.css
│
├── server/                          # Python ML Services
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── face_detection.py
│   │   │   ├── biofeedback.py
│   │   │   ├── aura_generation.py
│   │   │   └── reading_generation.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── rate_limit.py
│   │       └── error_handler.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── face_detection_service.py
│   │   ├── biofeedback_service.py
│   │   ├── aura_generation_service.py
│   │   ├── reading_generation_service.py
│   │   └── image_processing_service.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── face_detection.py
│   │   ├── biofeedback.py
│   │   ├── aura.py
│   │   └── reading.py
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── face_mesh/
│   │   │   └── face_mesh_landmark.tflite
│   │   ├── aura_generator/
│   │   │   └── aura_generator.pkl
│   │   └── reading_generator/
│   │       └── reading_generator.pkl
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py
│   │   ├── color_utils.py
│   │   └── text_utils.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_face_detection.py
│       ├── test_biofeedback.py
│       ├── test_aura_generation.py
│       └── test_reading_generation.py
│
├── scripts/
│   ├── setup.sh
│   ├── dev.sh
│   ├── build.sh
│   └── deploy.sh
│
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    └── CONTRIBUTING.md
```

---

## 11. Installation & Setup

### 11.1 Prerequisites

- Node.js 18+ 
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Cloudinary account (for image storage)
- Stripe account (for payments)

### 11.2 Environment Variables

```bash
# .env.local (Frontend)
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_PYTHON_API_URL=http://localhost:8000
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your_cloud_name
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# .env (Backend)
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aura_camera

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# OpenAI (for reading generation)
OPENAI_API_KEY=sk-...

# Server
PORT=8000
HOST=0.0.0.0
DEBUG=true
```

### 11.3 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/aura-camera-app.git
cd aura-camera-app

# 2. Install frontend dependencies
npm install

# 3. Setup database
npx prisma migrate dev
npx prisma generate
npx prisma db seed

# 4. Install Python dependencies
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 5. Download ML models
python scripts/download_models.py

# 6. Start development servers
# Terminal 1 - Frontend
cd ..
npm run dev

# Terminal 2 - Python API
cd server
python main.py

# 7. Open http://localhost:3000
```

### 11.4 Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/aura_camera
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
      - ml-api

  ml-api:
    build:
      context: ./server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/aura_camera
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=aura_camera
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## 12. Deployment Guide

### 12.1 Production Checklist

- [ ] Set up production database (Supabase, Railway, AWS RDS)
- [ ] Configure Redis (Upstash, Redis Cloud)
- [ ] Set up image storage (Cloudinary, AWS S3)
- [ ] Configure Stripe for payments
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Configure CDN (Cloudflare, Vercel Edge)
- [ ] Set up CI/CD (GitHub Actions, Vercel)
- [ ] Configure SSL certificates
- [ ] Set up backups
- [ ] Load testing

### 12.2 Vercel Deployment

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel --prod

# 4. Set environment variables in Vercel dashboard
```

### 12.3 Python API Deployment (Railway/Render)

```bash
# 1. Push code to GitHub

# 2. Connect Railway/Render to GitHub repo

# 3. Configure environment variables

# 4. Deploy
```

---

## Summary

This comprehensive specification provides everything needed to build an AURLA-like aura camera application. The architecture includes:

1. **Modern Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and shadcn/ui
2. **Python ML Backend**: FastAPI with MediaPipe, OpenCV, and PyTorch
3. **Complete Database Schema**: PostgreSQL with Prisma ORM
4. **Full API Specification**: RESTful endpoints with authentication
5. **AI/ML Components**: Face detection, biofeedback simulation, aura generation
6. **Production-Ready**: Docker, CI/CD, monitoring, and deployment guides

The next step is to implement the core components starting with the camera capture and face detection features.
