"""
Environment Optimization Service - Recommendation Engine
Environmental Psychology-based productivity system
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum
import json


class TaskType(Enum):
    """Task categories based on environmental psychology research"""
    DEEP_FOCUS = "deep_focus"  # Coding, writing, analysis
    CREATIVE = "creative"      # Brainstorm, design, ideation
    ANALYTICAL = "analytical"  # Math, data, research
    COLLABORATIVE = "collaborative"  # Meetings, teamwork
    LEARNING = "learning"      # Reading, training, studying


class Sensitivity(Enum):
    """User environmental sensitivity profiles"""
    LOW = "low"              # Tolerates wide ranges
    MODERATE = "moderate"    # Balanced preferences
    HIGH = "high"            # Requires optimal ranges


@dataclass
class EnvironmentalInputs:
    """Environmental sensor/manual data"""
    # Lighting
    illuminance_lux: float  # 0-2000
    color_temperature_k: float  # 2700-6500
    cri_index: float  # 70-100
    natural_light_percentage: float  # 0-100
    glare_level: str  # "none", "slight", "moderate", "severe"
    
    # Acoustics
    ambient_db: float  # dB sound pressure level
    sound_type: str  # "silence", "ambient", "speech", "noise", "music"
    
    # Layout
    desk_height_inches: float
    monitor_distance_inches: float
    monitor_angle_degrees: float
    clutter_level: int  # 0-100 (% of visible items)
    plants_count: int
    window_access: bool
    ceiling_height_feet: float
    
    # Climate
    temperature_f: float
    humidity_percentage: float
    co2_ppm: float
    
    # Personal
    user_sensitivity: Sensitivity
    work_schedule: str  # "morning", "afternoon", "evening", "night"


@dataclass
class RecommendationScore:
    """Scoring results for each environmental dimension"""
    lighting_score: float  # 0-100
    acoustic_score: float
    layout_score: float
    climate_score: float
    biophilic_score: float
    overall_score: float
    
    def to_dict(self) -> Dict:
        return {
            "lighting": round(self.lighting_score, 1),
            "acoustics": round(self.acoustic_score, 1),
            "layout": round(self.layout_score, 1),
            "climate": round(self.climate_score, 1),
            "biophilic": round(self.biophilic_score, 1),
            "overall": round(self.overall_score, 1),
        }


@dataclass
class Recommendation:
    """Single actionable recommendation"""
    category: str  # "lighting", "acoustics", "layout", "climate", "biophilic"
    priority: str  # "critical", "high", "medium", "low"
    action: str
    impact_score_improvement: float  # Expected % improvement
    estimated_cost: str  # "free", "$", "$$", "$$$"
    time_to_implement: str  # "immediate", "1-hour", "1-day", "1-week"
    implementation_steps: List[str]
    research_basis: str


class EnvironmentOptimizer:
    """Main recommendation engine"""
    
    # Task-specific optimal ranges
    TASK_RANGES = {
        TaskType.DEEP_FOCUS: {
            "illuminance_lux": (300, 500),
            "color_temperature_k": (4500, 6500),
            "ambient_db": (25, 40),
            "temperature_f": (68, 70),
            "clutter_level": (0, 20),
        },
        TaskType.CREATIVE: {
            "illuminance_lux": (300, 450),
            "color_temperature_k": (3000, 4000),
            "ambient_db": (40, 60),
            "temperature_f": (70, 72),
            "clutter_level": (20, 50),
        },
        TaskType.ANALYTICAL: {
            "illuminance_lux": (500, 800),
            "color_temperature_k": (4500, 6500),
            "ambient_db": (20, 35),
            "temperature_f": (68, 69),
            "clutter_level": (0, 15),
        },
        TaskType.COLLABORATIVE: {
            "illuminance_lux": (400, 500),
            "color_temperature_k": (4000, 5000),
            "ambient_db": (55, 75),
            "temperature_f": (70, 71),
            "clutter_level": (30, 60),
        },
        TaskType.LEARNING: {
            "illuminance_lux": (500, 800),
            "color_temperature_k": (4500, 6500),
            "ambient_db": (15, 30),
            "temperature_f": (69, 70),
            "clutter_level": (0, 10),
        },
    }
    
    def __init__(self, task_type: TaskType, user_sensitivity: Sensitivity):
        self.task_type = task_type
        self.user_sensitivity = user_sensitivity
        self.optimal_ranges = self.TASK_RANGES[task_type]
    
    def score_lighting(self, inputs: EnvironmentalInputs) -> float:
        """Score lighting environment (0-100)"""
        score = 100.0
        
        # Illuminance scoring
        opt_min, opt_max = self.optimal_ranges["illuminance_lux"]
        if inputs.illuminance_lux < opt_min:
            score -= (opt_min - inputs.illuminance_lux) * 0.5
        elif inputs.illuminance_lux > opt_max:
            score -= (inputs.illuminance_lux - opt_max) * 0.3
        
        # Color temperature scoring
        opt_min, opt_max = self.optimal_ranges["color_temperature_k"]
        if inputs.color_temperature_k < opt_min:
            score -= (opt_min - inputs.color_temperature_k) * 0.05
        elif inputs.color_temperature_k > opt_max:
            score -= (inputs.color_temperature_k - opt_max) * 0.05
        
        # CRI scoring
        if inputs.cri_index < 85:
            score -= (85 - inputs.cri_index) * 0.2
        
        # Natural light bonus
        score += inputs.natural_light_percentage * 0.1
        
        # Glare penalty
        glare_penalties = {"none": 0, "slight": 5, "moderate": 15, "severe": 30}
        score -= glare_penalties.get(inputs.glare_level, 0)
        
        return max(0, min(100, score))
    
    def score_acoustics(self, inputs: EnvironmentalInputs) -> float:
        """Score acoustic environment (0-100)"""
        score = 100.0
        
        # Ambient level scoring
        opt_min, opt_max = self.optimal_ranges["ambient_db"]
        
        if inputs.ambient_db < opt_min:
            # Too quiet - hyperawareness
            score -= (opt_min - inputs.ambient_db) * 2
        elif inputs.ambient_db > opt_max:
            # Too loud - distraction
            score -= (inputs.ambient_db - opt_max) * 1.5
        
        # Sound type bonus/penalty
        sound_scores = {
            "silence": 85,
            "white_noise": 90,
            "brown_noise": 92,
            "ambient": 75,
            "speech": 40,
            "music": 60,
            "industrial_noise": 20,
        }
        
        # Use provided sound type or estimate from dB
        current_sound = inputs.sound_type.lower().replace(" ", "_")
        sound_bonus = sound_scores.get(current_sound, 50)
        score = (score + sound_bonus) / 2
        
        return max(0, min(100, score))
    
    def score_layout(self, inputs: EnvironmentalInputs) -> float:
        """Score workspace layout & ergonomics (0-100)"""
        score = 100.0
        
        # Desk height (optimal: 28-30 inches)
        if inputs.desk_height_inches < 26 or inputs.desk_height_inches > 32:
            score -= abs(inputs.desk_height_inches - 29) * 2
        
        # Monitor distance (optimal: 20-30 inches)
        if inputs.monitor_distance_inches < 18 or inputs.monitor_distance_inches > 32:
            score -= abs(inputs.monitor_distance_inches - 25) * 1.5
        
        # Monitor angle (optimal: 15-20° below eye)
        if inputs.monitor_angle_degrees < 10 or inputs.monitor_angle_degrees > 25:
            score -= abs(inputs.monitor_angle_degrees - 17.5) * 1
        
        # Clutter level
        opt_min, opt_max = self.optimal_ranges["clutter_level"]
        if inputs.clutter_level > opt_max:
            score -= (inputs.clutter_level - opt_max) * 0.5
        elif inputs.clutter_level < opt_min:
            score -= (opt_min - inputs.clutter_level) * 0.3
        
        # Ceiling height bonus (creativity boost)
        if self.task_type == TaskType.CREATIVE and inputs.ceiling_height_feet >= 10:
            score += 5
        elif inputs.ceiling_height_feet < 8:
            score -= 5
        
        # Window access bonus
        if inputs.window_access:
            score += 10
        else:
            score -= 5
        
        return max(0, min(100, score))
    
    def score_climate(self, inputs: EnvironmentalInputs) -> float:
        """Score temperature, humidity, CO2 (0-100)"""
        score = 100.0
        
        # Temperature scoring
        opt_min, opt_max = self.optimal_ranges["temperature_f"]
        if inputs.temperature_f < opt_min:
            score -= (opt_min - inputs.temperature_f) * 3
        elif inputs.temperature_f > opt_max:
            score -= (inputs.temperature_f - opt_max) * 3
        
        # Humidity (optimal: 40-60%)
        if inputs.humidity_percentage < 30 or inputs.humidity_percentage > 70:
            score -= abs(inputs.humidity_percentage - 50) * 0.5
        
        # CO2 levels (optimal: <1000 ppm)
        if inputs.co2_ppm > 1000:
            score -= min((inputs.co2_ppm - 1000) * 0.01, 20)
        
        return max(0, min(100, score))
    
    def score_biophilic(self, inputs: EnvironmentalInputs) -> float:
        """Score biophilic elements (nature, plants, views)"""
        score = 50.0  # Base score
        
        # Plants
        score += min(inputs.plants_count * 15, 25)
        
        # Window access
        if inputs.window_access:
            score += 25
        
        # Natural light
        score += inputs.natural_light_percentage * 0.2
        
        return min(100, score)
    
    def calculate_scores(self, inputs: EnvironmentalInputs) -> RecommendationScore:
        """Calculate all environmental scores"""
        lighting = self.score_lighting(inputs)
        acoustic = self.score_acoustics(inputs)
        layout = self.score_layout(inputs)
        climate = self.score_climate(inputs)
        biophilic = self.score_biophilic(inputs)
        
        # Weighted overall score
        weights = {"lighting": 0.30, "acoustic": 0.25, "layout": 0.20, 
                   "climate": 0.15, "biophilic": 0.10}
        overall = (lighting * weights["lighting"] + 
                  acoustic * weights["acoustic"] +
                  layout * weights["layout"] +
                  climate * weights["climate"] +
                  biophilic * weights["biophilic"])
        
        return RecommendationScore(
            lighting_score=lighting,
            acoustic_score=acoustic,
            layout_score=layout,
            climate_score=climate,
            biophilic_score=biophilic,
            overall_score=overall
        )
    
    def generate_recommendations(self, inputs: EnvironmentalInputs, 
                                scores: RecommendationScore) -> List[Recommendation]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Lighting recommendations
        if scores.lighting_score < 70:
            if inputs.illuminance_lux < self.optimal_ranges["illuminance_lux"][0]:
                recommendations.append(Recommendation(
                    category="lighting",
                    priority="high" if scores.lighting_score < 50 else "medium",
                    action="Increase illuminance with additional LED lighting",
                    impact_score_improvement=15,
                    estimated_cost="$",
                    time_to_implement="1-hour",
                    implementation_steps=[
                        "Purchase 4000-5000K full-spectrum LED bulbs",
                        "Position lighting to eliminate glare",
                        "Aim for 400-500 lux at desk surface",
                        "Add task lighting for additional 300+ lux"
                    ],
                    research_basis="Light & Cognitive Neuroscience: adequate illumination improves focus by 25-30% (Boyce et al., 2006)"
                ))
            
            if inputs.glare_level in ["moderate", "severe"]:
                recommendations.append(Recommendation(
                    category="lighting",
                    priority="critical",
                    action="Reduce glare with positioning or anti-glare filters",
                    impact_score_improvement=20,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Reposition monitor perpendicular to windows",
                        "Add monitor anti-glare screen",
                        "Use indirect lighting instead of direct",
                        "Add desk lamp with matte finish"
                    ],
                    research_basis="Glare reduces visual acuity by 40% and increases eye strain (CIE, 2019)"
                ))
        
        # Acoustic recommendations
        if scores.acoustic_score < 70:
            if inputs.ambient_db > self.optimal_ranges["ambient_db"][1]:
                recommendations.append(Recommendation(
                    category="acoustics",
                    priority="high" if scores.acoustic_score < 50 else "medium",
                    action="Reduce ambient noise with acoustic treatment",
                    impact_score_improvement=18,
                    estimated_cost="$",
                    time_to_implement="1-day",
                    implementation_steps=[
                        "Add acoustic foam panels to walls (behind desk)",
                        "Use heavy curtains to absorb sound",
                        "Add rugs/carpeting to reduce reflections",
                        "Consider white noise machine or app (brown noise optimal)"
                    ],
                    research_basis="Noise >70dB reduces cognitive performance by 30-50% (Banbury & Berry, 2005)"
                ))
            
            if inputs.ambient_db < self.optimal_ranges["ambient_db"][0]:
                recommendations.append(Recommendation(
                    category="acoustics",
                    priority="medium",
                    action="Add ambient sound for optimal cognitive function",
                    impact_score_improvement=12,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Use brown noise app (mynoise.net, Noisli)",
                        "Try 50-60 dB ambient background",
                        "Experiment with coffee shop ambiance or rain sounds",
                        "Start with 20 mins, increase as habituation occurs"
                    ],
                    research_basis="Optimal noise masking improves focus by 15-25% (Jahncke & Hanel, 2005)"
                ))
        
        # Layout recommendations
        if scores.layout_score < 70:
            if inputs.clutter_level > self.optimal_ranges["clutter_level"][1]:
                recommendations.append(Recommendation(
                    category="layout",
                    priority="high",
                    action="Reduce visual clutter to lower cognitive load",
                    impact_score_improvement=12,
                    estimated_cost="free",
                    time_to_implement="1-hour",
                    implementation_steps=[
                        "Remove items not essential for current task",
                        "Use closed storage (drawers, cabinets)",
                        "Keep only 3-5 items visible on desk",
                        "Organize cables and wires",
                        "Use minimalist desk organizer"
                    ],
                    research_basis="Visual clutter increases cognitive load by 30% (Kellogg & Wolff, 2008)"
                ))
            
            if not inputs.window_access:
                recommendations.append(Recommendation(
                    category="layout",
                    priority="medium",
                    action="Improve space perception and mood",
                    impact_score_improvement=8,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Add large window artwork or prints",
                        "Use mirrors to increase perceived space",
                        "Add plants to simulate nature views",
                        "Consider desk near window if possible"
                    ],
                    research_basis="Nature views reduce stress by 37% and improve focus (Kaplan, 1995)"
                ))
        
        # Climate recommendations
        if scores.climate_score < 70:
            temp_issue = inputs.temperature_f < 68 or inputs.temperature_f > 72
            if temp_issue:
                recommendations.append(Recommendation(
                    category="climate",
                    priority="medium",
                    action="Maintain optimal temperature (68-72°F)",
                    impact_score_improvement=10,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Adjust thermostat to 69-70°F",
                        "Use sweater/desk heater if cold",
                        "Use fan if warm",
                        "Monitor hourly - avoid temp fluctuation"
                    ],
                    research_basis="Temperatures >72°F reduce cognition by 5-10% per degree (Seppänen et al., 2006)"
                ))
            
            if inputs.co2_ppm > 1000:
                recommendations.append(Recommendation(
                    category="climate",
                    priority="critical",
                    action="Increase ventilation to reduce CO2 levels",
                    impact_score_improvement=8,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Open window for 5-10 minutes hourly",
                        "Run exhaust fan continuously",
                        "Ensure HVAC is functioning properly",
                        "Consider indoor CO2 monitor"
                    ],
                    research_basis="CO2 >1000ppm reduces cognition by 15% (Satish et al., 2012)"
                ))
        
        # Biophilic recommendations
        if scores.biophilic_score < 70:
            if inputs.plants_count == 0:
                recommendations.append(Recommendation(
                    category="biophilic",
                    priority="medium",
                    action="Add plants for stress reduction and air quality",
                    impact_score_improvement=10,
                    estimated_cost="free",
                    time_to_implement="immediate",
                    implementation_steps=[
                        "Add 2-3 potted plants to workspace",
                        "Choose low-maintenance species (pothos, snake plant)",
                        "Position within 3 feet of desk",
                        "Water weekly, ensure indirect light"
                    ],
                    research_basis="Indoor plants reduce cortisol by 37% and improve creativity by 15% (Nieuwenhuis et al., 2014)"
                ))
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order[x.priority])
        
        return recommendations
    
    def get_productivity_tier(self, score: float) -> Tuple[str, str]:
        """Classify productivity level"""
        tiers = [
            (0, "Critical", "Immediate intervention required"),
            (40, "Major Issues", "Significant productivity loss"),
            (65, "Optimization", "Good foundation, fine-tuning needed"),
            (85, "Optimized", "Excellent environment"),
            (95, "Elite", "Peak performance conditions"),
        ]
        
        for threshold, tier_name, description in reversed(tiers):
            if score >= threshold:
                return tier_name, description
        return "Critical", "Immediate intervention required"


def generate_report(task_type: TaskType, sensitivity: Sensitivity, 
                   inputs: EnvironmentalInputs) -> Dict:
    """Generate complete optimization report"""
    
    optimizer = EnvironmentOptimizer(task_type, sensitivity)
    scores = optimizer.calculate_scores(inputs)
    recommendations = optimizer.generate_recommendations(inputs, scores)
    tier_name, tier_desc = optimizer.get_productivity_tier(scores.overall_score)
    
    return {
        "task_type": task_type.value,
        "user_sensitivity": sensitivity.value,
        "scores": scores.to_dict(),
        "productivity_tier": {
            "name": tier_name,
            "description": tier_desc,
            "score": round(scores.overall_score, 1)
        },
        "recommendations": [
            {
                "category": r.category,
                "priority": r.priority,
                "action": r.action,
                "impact_improvement": f"+{r.impact_score_improvement}%",
                "cost": r.estimated_cost,
                "time": r.time_to_implement,
                "steps": r.implementation_steps,
                "research": r.research_basis
            }
            for r in recommendations
        ]
    }
