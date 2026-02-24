"""Aura generation service"""

import io
import random
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Tuple

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

from services.biofeedback_service import BiofeedbackSession


@dataclass
class AuraPositioning:
    ascendant: List[str] = field(default_factory=list)    # Right side - receiving
    descendant: List[str] = field(default_factory=list)   # Left side - giving
    cathedra: List[str] = field(default_factory=list)     # Bottom - root
    coronation: List[str] = field(default_factory=list)   # Top - crown
    etherea: List[str] = field(default_factory=list)      # All sides


@dataclass
class AuraProfile:
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
    chakra: str = "Unknown"


class AuraGenerationService:
    """Service for generating aura images and profiles"""
    
    # Color definitions with RGB values
    COLOR_DEFINITIONS: Dict[str, Tuple[int, int, int]] = {
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
    
    # Color mappings based on biofeedback signals
    COLOR_MAPPINGS: Dict[str, Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]] = {
        # color: (stress_range, calmness_range, stability_range)
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
    
    def __init__(self):
        self.blur_kernels = {
            'soft': (51, 51),
            'medium': (71, 71),
            'strong': (101, 101),
        }
    
    def generate_aura_profile(
        self,
        biofeedback: BiofeedbackSession,
    ) -> AuraProfile:
        """
        Generate aura profile from biofeedback session.
        
        Args:
            biofeedback: Processed biofeedback session
        
        Returns:
            AuraProfile with color distribution
        """
        # Get biofeedback metrics
        stress = biofeedback.stress_indicator
        calmness = biofeedback.calmness_score
        stability = biofeedback.average_stability
        
        # Calculate color scores
        color_scores = {}
        for color, (stress_range, calm_range, stab_range) in self.COLOR_MAPPINGS.items():
            score = self._calculate_match_score(
                stress, calmness, stability,
                stress_range, calm_range, stab_range
            )
            # Add a slight random jitter to prevent "Copper" or any single color 
            # from dominating due to tied scores or central values (0.5)
            jitter = random.uniform(-0.02, 0.02)
            color_scores[color] = score + jitter
        
        # Sort by score
        sorted_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create aura profile
        majority_color = sorted_colors[0][0]
        majority_percentage = round(sorted_colors[0][1] * 100, 1)
        
        moderate_colors = [c[0] for c in sorted_colors[1:3]]
        moderate_percentages = [round(c[1] * 100, 1) for c in sorted_colors[1:3]]
        
        minority_colors = [c[0] for c in sorted_colors[3:6]]
        minority_percentages = [round(c[1] * 100, 1) for c in sorted_colors[3:6]]
        
        # Calculate visual properties - reduced intensity for better visual transparency
        intensity = round(15 + calmness * 15, 1)  # 15% to 30% max alpha
        
        # Further reduce intensity for very bright colors that wash out faces
        if majority_color in ['white', 'silver', 'gold', 'quartz']:
            intensity *= 0.8
            
        brightness = round(40 + stability * 60, 1)
        saturation = round(40 + (1 - stress) * 60, 1)
        
        # Determine Chakra
        chakra_map = {
            'red': 'Root Chakra',
            'orange': 'Sacral Chakra',
            'yellow': 'Solar Plexus Chakra',
            'green': 'Heart Chakra',
            'blue': 'Throat Chakra',
            'indigo': 'Third Eye Chakra',
            'violet': 'Crown Chakra',
            'pink': 'Heart Chakra',
            'white': 'Soul Star',
            'gold': 'Higher Heart',
            'silver': 'Moon Center',
            'turquoise': 'Higher Heart',
            'magenta': 'Zeal Point',
            'emerald': 'Heart Chakra',
            'citrine': 'Solar Plexus',
            'amethyst': 'Third Eye',
            'lapis': 'Throat Chakra',
            'copper': 'Earth Star',
            'garnet': 'Root Chakra',
            'ruby': 'Root Chakra',
        }
        active_chakra = chakra_map.get(majority_color, "Universal Energy")

        # Generate positioning
        positioning = self._generate_positioning(
            majority_color,
            moderate_colors,
            minority_colors,
        )
        
        return AuraProfile(
            majority_color=majority_color,
            majority_percentage=majority_percentage,
            moderate_colors=moderate_colors,
            moderate_percentages=moderate_percentages,
            minority_colors=minority_colors,
            minority_percentages=minority_percentages,
            intensity=intensity,
            brightness=brightness,
            saturation=saturation,
            positioning=positioning,
            chakra=active_chakra
        )
    
    def generate_aura_image(
        self,
        image_bytes: bytes,
        aura_profile: AuraProfile,
        style: Literal['soft', 'medium', 'strong'] = 'soft',
    ) -> bytes:
        """
        Generate aura overlay image.
        
        Args:
            image_bytes: Original photo bytes
            aura_profile: Aura color profile
            style: Aura style (soft, medium, strong)
        
        Returns:
            Aura image as bytes
        """
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create aura layers
        aura_layers = self._create_aura_layers(
            image.size,
            aura_profile,
            style,
        )
        
        # Enhance the base image for clarity before overlaying aura
        # Boost contrast and sharpness to make the face "pop" through the aura
        enhancer_contrast = ImageEnhance.Contrast(image)
        image = enhancer_contrast.enhance(1.1)
        enhancer_sharpness = ImageEnhance.Sharpness(image)
        image = enhancer_sharpness.enhance(1.2)
        enhancer_brightness = ImageEnhance.Brightness(image)
        image = enhancer_brightness.enhance(1.05)
        
        # Composite layers onto image
        composite = self._composite_aura(image, aura_layers)
        
        # Save to bytes
        output = io.BytesIO()
        composite.save(output, format='PNG')
        output.seek(0)
        
        return output.getvalue()
    
    def _calculate_match_score(
        self,
        stress: float,
        calmness: float,
        stability: float,
        stress_range: Tuple[float, float],
        calm_range: Tuple[float, float],
        stab_range: Tuple[float, float],
    ) -> float:
        """Calculate how well biofeedback matches color profile"""
        stress_mid = (stress_range[0] + stress_range[1]) / 2
        calm_mid = (calm_range[0] + calm_range[1]) / 2
        stab_mid = (stab_range[0] + stab_range[1]) / 2
        
        stress_match = 1 - abs(stress - stress_mid)
        calm_match = 1 - abs(calmness - calm_mid)
        stab_match = 1 - abs(stability - stab_mid)
        
        return (stress_match + calm_match + stab_match) / 3
    
    def _generate_positioning(
        self,
        majority_color: str,
        moderate_colors: List[str],
        minority_colors: List[str],
    ) -> AuraPositioning:
        """Generate aura positioning based on colors"""
        return AuraPositioning(
            ascendant=[moderate_colors[0] if moderate_colors else majority_color],
            descendant=[moderate_colors[1] if len(moderate_colors) > 1 else majority_color],
            cathedra=[majority_color],
            coronation=[minority_colors[0] if minority_colors else majority_color],
            etherea=[majority_color] + moderate_colors[:2],
        )
    
    def _create_aura_layers(
        self,
        image_size: Tuple[int, int],
        aura_profile: AuraProfile,
        style: str,
    ) -> List[Image.Image]:
        """Create aura color layers"""
        layers = []
        width, height = image_size
        
        # Majority color layer (dominant, moved up to head/crown area)
        majority_layer = self._create_color_layer(
            image_size,
            aura_profile.majority_color,
            intensity=aura_profile.intensity / 100,
            position='upper_center',
            spread=1.0, # Wider spread for soft falloff
            style=style,
        )
        layers.append(majority_layer)
        
        # Moderate color layers
        for i, (color, pct) in enumerate(
            zip(aura_profile.moderate_colors, aura_profile.moderate_percentages)
        ):
            position = ['ascendant', 'descendant', 'cathedra', 'coronation'][i % 4]
            layer = self._create_color_layer(
                image_size,
                color,
                intensity=pct / 100 * 0.7,
                position=position,
                spread=0.5,
                style=style,
            )
            layers.append(layer)
        
        # Minority color layers (subtle accents)
        for color, pct in zip(aura_profile.minority_colors, aura_profile.minority_percentages):
            layer = self._create_color_layer(
                image_size,
                color,
                intensity=pct / 100 * 0.4,
                position='etherea',
                spread=0.3,
                style=style,
            )
            layers.append(layer)
        
        return layers
    
    def _create_color_layer(
        self,
        image_size: Tuple[int, int],
        color: str,
        intensity: float,
        position: str,
        spread: float,
        style: str,
    ) -> Image.Image:
        """Create a single color aura layer with gradient"""
        width, height = image_size
        
        # Create transparent layer
        layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Get color RGB
        rgb = self.COLOR_DEFINITIONS.get(color, (128, 128, 128))
        
        # Create gradient based on position
        if position == 'center':
            gradient = self._create_radial_gradient(
                (width, height),
                center=(width // 2, height // 2),
                radius=int(min(width, height) * spread),
                inner_clearance=0.6  # More aggressive clearance
            )
        elif position == 'upper_center':
            # Position above the face (typical Third Eye/Crown area)
            gradient = self._create_radial_gradient(
                (width, height),
                center=(width // 2, height // 3), # 1/3 from the top
                radius=int(min(width, height) * spread),
                inner_clearance=0.4
            )
        elif position == 'ascendant':
            gradient = self._create_directional_gradient(
                (width, height),
                direction='right',
                spread=spread,
            )
        elif position == 'descendant':
            gradient = self._create_directional_gradient(
                (width, height),
                direction='left',
                spread=spread,
            )
        elif position == 'coronation':
            gradient = self._create_directional_gradient(
                (width, height),
                direction='up',
                spread=spread,
            )
        elif position == 'cathedra':
            gradient = self._create_directional_gradient(
                (width, height),
                direction='down',
                spread=spread,
            )
        else:  # etherea
            gradient = self._create_radial_gradient(
                (width, height),
                center=(width // 2, height // 2),
                radius=int(min(width, height) * spread),
                inner_clearance=0.5
            )
        
        # Apply color and intensity to gradient
        for y in range(height):
            for x in range(width):
                alpha = int(gradient[y, x] * 255 * intensity)
                layer.putpixel((x, y), (*rgb, alpha))
        
        # Apply blur
        blur_radius = self.blur_kernels[style][0] // 10
        layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        return layer
    
    def _create_radial_gradient(
        self,
        size: Tuple[int, int],
        center: Tuple[int, int],
        radius: int,
        inner_clearance: float = 0.0,
    ) -> np.ndarray:
        """Create radial gradient mask with optional inner clearance"""
        width, height = size
        cx, cy = center
        
        y, x = np.ogrid[:height, :width]
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        
        # Outer fade out
        gradient = np.clip(1 - (distance / radius), 0, 1)
        
        # Power for soft outer falloff
        gradient = np.power(gradient, 1.2)
        
        # If inner clearance is requested, fade the gradient out in the center
        if inner_clearance > 0:
            # Create a larger "clear" core with a sharper edge
            inner_mask = np.clip(distance / (radius * inner_clearance), 0, 1)
            # Smoothly but quickly transition from 0 to 1
            inner_mask = np.power(inner_mask, 0.5) 
            gradient = gradient * inner_mask
            
        return gradient
    
    def _create_directional_gradient(
        self,
        size: Tuple[int, int],
        direction: str,
        spread: float,
    ) -> np.ndarray:
        """Create directional gradient mask"""
        width, height = size
        
        if direction == 'right':
            gradient = np.linspace(0, 1, width)
            gradient = np.tile(gradient, (height, 1))
        elif direction == 'left':
            gradient = np.linspace(1, 0, width)
            gradient = np.tile(gradient, (height, 1))
        elif direction == 'up':
            gradient = np.linspace(1, 0, height)
            gradient = np.tile(gradient[:, np.newaxis], (1, width))
        else:  # down
            gradient = np.linspace(0, 1, height)
            gradient = np.tile(gradient[:, np.newaxis], (1, width))
        
        # Apply spread
        gradient = np.clip(gradient * (1 / spread), 0, 1)
        
        return gradient
    
    def _composite_aura(
        self,
        base_image: Image.Image,
        aura_layers: List[Image.Image],
    ) -> Image.Image:
        """Composite aura layers onto base image"""
        result = base_image.convert('RGBA')
        
        for layer in aura_layers:
            result = Image.alpha_composite(result, layer)
        
        return result.convert('RGB')
