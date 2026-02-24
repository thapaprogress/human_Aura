"""Reading generation service"""

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ReadingSection:
    section: str
    title: str
    content: str


@dataclass
class AuraReading:
    sections: List[ReadingSection]
    color_references: List[str]
    generated_at: datetime = field(default_factory=datetime.now)


class ReadingGenerationService:
    """Service for generating aura readings"""
    
    # Color meanings database
    COLOR_MEANINGS: Dict[str, Dict] = {
        'red': {
            'name': 'Red',
            'keywords': ['energy', 'passion', 'strength', 'action', 'vitality'],
            'description': 'Red represents physical energy, passion, and vitality.',
            'positive': ['Energetic', 'Passionate', 'Strong-willed', 'Courageous'],
            'challenges': ['May be impulsive', 'Can be aggressive', 'Might be restless'],
            'chakras': ['Root Chakra'],
            'guidance': 'Channel your energy into positive action. Take time to ground yourself when feeling overwhelmed.',
        },
        'orange': {
            'name': 'Orange',
            'keywords': ['creativity', 'joy', 'confidence', 'social', 'enthusiasm'],
            'description': 'Orange reflects creativity, emotional warmth, and social connection.',
            'positive': ['Creative', 'Sociable', 'Optimistic', 'Adventurous'],
            'challenges': ['May seek attention', 'Can be restless', 'Might overindulge'],
            'chakras': ['Sacral Chakra'],
            'guidance': 'Express your creativity freely. Share your joy with others while maintaining healthy boundaries.',
        },
        'yellow': {
            'name': 'Yellow',
            'keywords': ['intellect', 'optimism', 'clarity', 'confidence', 'logic'],
            'description': 'Yellow indicates mental clarity, optimism, and intellectual energy.',
            'positive': ['Intelligent', 'Optimistic', 'Clear-thinking', 'Confident'],
            'challenges': ['May overthink', 'Can be critical', 'Might be anxious'],
            'chakras': ['Solar Plexus'],
            'guidance': 'Trust your intellect and maintain your optimistic outlook. Balance thinking with feeling.',
        },
        'green': {
            'name': 'Green',
            'keywords': ['growth', 'healing', 'balance', 'love', 'harmony'],
            'description': 'Green represents growth, healing energy, and balance.',
            'positive': ['Healing', 'Balanced', 'Nurturing', 'Growth-oriented'],
            'challenges': ['May be overly accommodating', 'Can be jealous', 'Might resist change'],
            'chakras': ['Heart Chakra'],
            'guidance': 'Embrace growth and healing. Your nurturing energy brings harmony to those around you.',
        },
        'blue': {
            'name': 'Blue',
            'keywords': ['communication', 'truth', 'calm', 'intuition', 'peace'],
            'description': 'Blue reflects communication, truth, and inner peace.',
            'positive': ['Truthful', 'Peaceful', 'Communicative', 'Intuitive'],
            'challenges': ['May suppress emotions', 'Can be distant', 'Might over-analyze'],
            'chakras': ['Throat Chakra'],
            'guidance': 'Speak your truth with compassion. Trust your intuition and maintain your inner peace.',
        },
        'indigo': {
            'name': 'Indigo',
            'keywords': ['intuition', 'wisdom', 'spirituality', 'perception', 'depth'],
            'description': 'Indigo indicates deep intuition, spiritual awareness, and inner wisdom.',
            'positive': ['Intuitive', 'Wise', 'Spiritual', 'Perceptive'],
            'challenges': ['May be withdrawn', 'Can be overly sensitive', 'Might escape reality'],
            'chakras': ['Third Eye Chakra'],
            'guidance': 'Trust your inner vision. Your spiritual awareness is a gift - use it wisely.',
        },
        'violet': {
            'name': 'Violet',
            'keywords': ['spirituality', 'transformation', 'magic', 'vision', 'unity'],
            'description': 'Violet represents spiritual transformation and connection to higher consciousness.',
            'positive': ['Spiritual', 'Visionary', 'Transformative', 'Inspiring'],
            'challenges': ['May be impractical', 'Can be escapist', 'Might be aloof'],
            'chakras': ['Crown Chakra'],
            'guidance': 'Embrace your spiritual journey. Your connection to higher realms brings wisdom and inspiration.',
        },
        'pink': {
            'name': 'Pink',
            'keywords': ['love', 'compassion', 'gentleness', 'nurturing', 'sensitivity'],
            'description': 'Pink reflects unconditional love, compassion, and gentle energy.',
            'positive': ['Loving', 'Compassionate', 'Gentle', 'Sensitive'],
            'challenges': ['May be overly emotional', 'Can be naive', 'Might avoid conflict'],
            'chakras': ['Heart Chakra'],
            'guidance': 'Your loving nature heals others. Remember to show the same compassion to yourself.',
        },
        'white': {
            'name': 'White',
            'keywords': ['purity', 'protection', 'clarity', 'transcendence', 'truth'],
            'description': 'White represents purity, spiritual protection, and transcendence.',
            'positive': ['Pure', 'Protected', 'Clear', 'Transcendent'],
            'challenges': ['May be detached', 'Can be perfectionist', 'Might be isolated'],
            'chakras': ['All Chakras'],
            'guidance': 'Your pure energy is protected. Maintain clarity while staying connected to the physical world.',
        },
        'gold': {
            'name': 'Gold',
            'keywords': ['wisdom', 'enlightenment', 'abundance', 'divine', 'mastery'],
            'description': 'Gold indicates divine wisdom, spiritual mastery, and enlightened consciousness.',
            'positive': ['Wise', 'Enlightened', 'Abundant', 'Masterful'],
            'challenges': ['May have ego issues', 'Can be materialistic', 'Might be prideful'],
            'chakras': ['Crown and Solar Plexus'],
            'guidance': 'Your enlightened presence inspires others. Share your wisdom with humility and grace.',
        },
        'silver': {
            'name': 'Silver',
            'keywords': ['intuition', 'feminine', 'mystery', 'reflection', 'adaptability'],
            'description': 'Silver reflects intuitive abilities, feminine energy, and the mysterious aspects of life.',
            'positive': ['Intuitive', 'Adaptable', 'Mysterious', 'Reflective'],
            'challenges': ['May be moody', 'Can be secretive', 'Might be indecisive'],
            'chakras': ['Third Eye and Crown'],
            'guidance': 'Trust your intuitive flashes. Your reflective nature helps you navigate life\'s mysteries.',
        },
        'turquoise': {
            'name': 'Turquoise',
            'keywords': ['healing', 'communication', 'balance', 'protection', 'wholeness'],
            'description': 'Turquoise represents healing communication and protective energy.',
            'positive': ['Healing', 'Communicative', 'Balanced', 'Protected'],
            'challenges': ['May be scattered', 'Can be unpredictable', 'Might be restless'],
            'chakras': ['Heart and Throat'],
            'guidance': 'Your healing words have power. Communicate with compassion and maintain your balance.',
        },
    }
    
    # Default meaning for colors not in database
    DEFAULT_MEANING = {
        'name': 'Crystal',
        'keywords': ['energy', 'clarity', 'balance'],
        'description': 'This color indicates a unique energy signature.',
        'positive': ['Unique', 'Balanced', 'Clear'],
        'challenges': ['May be misunderstood', 'Can be complex'],
        'chakras': ['Multiple Chakras'],
        'guidance': 'Trust your unique energy. Your individual path brings special gifts.',
    }
    
    def __init__(self, use_openai: bool = False):
        self.use_openai = use_openai
        if use_openai:
            try:
                import openai
                self.openai_client = openai.OpenAI()
            except ImportError:
                self.use_openai = False
    
    def generate_reading(
        self,
        aura_profile: Dict,
        biofeedback_summary: Dict,
    ) -> AuraReading:
        """
        Generate aura reading from profile.
        
        Args:
            aura_profile: Aura color profile
            biofeedback_summary: Summary of biofeedback data
        
        Returns:
            AuraReading with sections
        """
        if self.use_openai:
            return self._generate_with_openai(aura_profile, biofeedback_summary)
        else:
            return self.generate_reading_template(aura_profile, biofeedback_summary)
    
    def generate_reading_template(
        self,
        aura_profile: Dict,
        biofeedback_summary: Dict,
    ) -> AuraReading:
        """
        Generate aura reading using templates (no AI).
        
        Args:
            aura_profile: Aura color profile
            biofeedback_summary: Summary of biofeedback data
        
        Returns:
            AuraReading with template-based sections
        """
        sections = []
        color_refs = []
        
        # Color Analysis Section
        color_analysis = self._generate_color_analysis(aura_profile)
        sections.append(color_analysis)
        color_refs.extend(self._extract_colors(color_analysis.content))
        
        # Alignment Section
        alignment = self._generate_alignment_section(aura_profile)
        sections.append(alignment)
        color_refs.extend(self._extract_colors(alignment.content))
        
        # Guidance Section
        guidance = self._generate_guidance_section(aura_profile, biofeedback_summary)
        sections.append(guidance)
        color_refs.extend(self._extract_colors(guidance.content))
        
        return AuraReading(
            sections=sections,
            color_references=list(set(color_refs)),
        )
    
    def _generate_color_analysis(self, aura_profile: Dict) -> ReadingSection:
        """Generate color analysis section"""
        majority_color = aura_profile['majority_color']
        majority_pct = aura_profile['majority_percentage']
        moderate_colors = aura_profile.get('moderate_colors', [])
        minority_colors = aura_profile.get('minority_colors', [])
        
        majority_meaning = self.COLOR_MEANINGS.get(majority_color, self.DEFAULT_MEANING)
        
        content = f"""Your aura reveals a beautiful {majority_meaning['name']} dominant energy at {majority_pct}%, indicating {majority_meaning['description'].lower()}

Your dominant {majority_color} energy suggests you are """
        
        # Add positive traits
        content += ', '.join(majority_meaning['positive'][:3])
        content += '. '
        
        # Add supporting colors
        if moderate_colors:
            content += f"The supporting {', '.join(moderate_colors[:2])} energies enhance your natural abilities, creating a harmonious blend of energies. "
        
        # Add intensity note
        intensity = aura_profile.get('intensity', 50)
        if intensity > 70:
            content += "Your aura shows strong, vibrant energy that radiates outward powerfully."
        elif intensity > 40:
            content += "Your aura displays balanced energy that flows steadily and consistently."
        else:
            content += "Your aura shows gentle, subtle energy that flows softly around you."
        
        return ReadingSection(
            section='color_analysis',
            title='Your Color Analysis',
            content=content,
        )
    
    def _generate_alignment_section(self, aura_profile: Dict) -> ReadingSection:
        """Generate alignment section"""
        positioning = aura_profile.get('positioning', {})
        
        content = "Your aura flows around you in a unique pattern that reveals how energy moves through your being:\n\n"
        
        # Ascendant (receiving)
        ascendant = positioning.get('ascendant', [])
        if ascendant:
            content += f"**Ascendant (Right Side)** - What you are receiving:\n"
            content += f"Your right side shows {', '.join(ascendant[:2])}, indicating you are currently receptive to "
            asc_meanings = [self.COLOR_MEANINGS.get(c, self.DEFAULT_MEANING) for c in ascendant[:2]]
            content += f"{asc_meanings[0]['keywords'][0]} and {asc_meanings[-1]['keywords'][0]} in your environment.\n\n"
        
        # Descendant (giving)
        descendant = positioning.get('descendant', [])
        if descendant:
            content += f"**Descendant (Left Side)** - What you are expressing:\n"
            content += f"Your left side displays {', '.join(descendant[:2])}, showing you are expressing "
            desc_meanings = [self.COLOR_MEANINGS.get(c, self.DEFAULT_MEANING) for c in descendant[:2]]
            content += f"{desc_meanings[0]['keywords'][0]} and {desc_meanings[-1]['keywords'][0]} to others.\n\n"
        
        # Coronation (top)
        coronation = positioning.get('coronation', [])
        if coronation:
            content += f"**Coronation (Top)** - Your highest aspirations:\n"
            content += f"The crown of your aura reveals {', '.join(coronation[:1])}, suggesting "
            cor_meaning = self.COLOR_MEANINGS.get(coronation[0], self.DEFAULT_MEANING)
            content += f"{cor_meaning['keywords'][0]} and {cor_meaning['keywords'][1]} in your thoughts and aspirations.\n\n"
        
        # Cathedra (bottom)
        cathedra = positioning.get('cathedra', [])
        if cathedra:
            content += f"**Cathedra (Bottom)** - Your foundation:\n"
            content += f"Your base shows {', '.join(cathedra[:1])}, indicating "
            cat_meaning = self.COLOR_MEANINGS.get(cathedra[0], self.DEFAULT_MEANING)
            content += f"{cat_meaning['keywords'][0]} as your grounding energy."
        
        return ReadingSection(
            section='alignment',
            title='Your Energy Alignment',
            content=content,
        )
    
    def _generate_guidance_section(
        self,
        aura_profile: Dict,
        biofeedback_summary: Dict,
    ) -> ReadingSection:
        """Generate guidance section"""
        majority_color = aura_profile['majority_color']
        calmness = biofeedback_summary.get('calmness_score', 0.5)
        stress = biofeedback_summary.get('stress_indicator', 0.5)
        
        majority_meaning = self.COLOR_MEANINGS.get(majority_color, self.DEFAULT_MEANING)
        
        content = f"""Your aura suggests you are in a phase of significant energetic development. The strong {majority_color} presence indicates your {majority_meaning['chakras'][0]} is highly active.

**Personal Guidance:**

"""
        
        # Add color-specific guidance
        content += majority_meaning['guidance'] + "\n\n"
        
        # Add biofeedback-based guidance
        if calmness > 0.7:
            content += "Your calm and centered energy supports deep spiritual work. This is an excellent time for meditation and introspection.\n\n"
        elif calmness > 0.4:
            content += "Your balanced energy allows for both action and reflection. Find moments of stillness throughout your day.\n\n"
        else:
            content += "Your active energy seeks expression. Channel this into creative or physical activities before settling into meditation.\n\n"
        
        if stress > 0.6:
            content += "You may be experiencing some tension. Focus on grounding practices and connect with nature to restore balance."
        elif stress > 0.3:
            content += "Maintain your current practices to keep your energy flowing smoothly."
        else:
            content += "Your peaceful state is a gift. Share this calm energy with those around you."
        
        return ReadingSection(
            section='guidance',
            title='Your Spiritual Guidance',
            content=content,
        )
    
    def _extract_colors(self, text: str) -> List[str]:
        """Extract color names from text"""
        colors = []
        for color in self.COLOR_MEANINGS.keys():
            if color.replace('_', ' ') in text.lower() or color in text.lower():
                colors.append(color)
        return colors
    
    def _generate_with_openai(
        self,
        aura_profile: Dict,
        biofeedback_summary: Dict,
    ) -> AuraReading:
        """Generate reading using OpenAI API"""
        # This would use OpenAI API for more sophisticated readings
        # For now, fall back to template
        return self.generate_reading_template(aura_profile, biofeedback_summary)
