"""
Environment Optimization Service - Demo/Example Usage
Shows how to use the recommendation engine with realistic scenarios
"""

import json
from optimizer import (
    EnvironmentOptimizer, EnvironmentalInputs, TaskType, Sensitivity, generate_report
)


def print_report(report: dict, title: str) -> None:
    """Pretty print optimization report"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)
    
    # Scores section
    scores = report["scores"]
    tier = report["productivity_tier"]
    
    print(f"\n📊 PRODUCTIVITY SCORES")
    print(f"  Overall: {scores['overall']}/100 → {tier['name']} ({tier['description']})")
    print(f"  ├─ Lighting:    {scores['lighting']}/100")
    print(f"  ├─ Acoustics:   {scores['acoustics']}/100")
    print(f"  ├─ Layout:      {scores['layout']}/100")
    print(f"  ├─ Climate:     {scores['climate']}/100")
    print(f"  └─ Biophilic:   {scores['biophilic']}/100")
    
    # Recommendations
    recommendations = report["recommendations"]
    if recommendations:
        print(f"\n✨ RECOMMENDATIONS ({len(recommendations)} actions)")
        
        for i, rec in enumerate(recommendations, 1):
            priority_icons = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }
            icon = priority_icons.get(rec["priority"], "⚪")
            
            print(f"\n  {i}. {icon} {rec['action'].upper()}")
            print(f"     Priority: {rec['priority'].upper()}")
            print(f"     Impact: {rec['impact_improvement']} productivity gain")
            print(f"     Cost: {rec['cost']:<4} | Time: {rec['time']}")
            print(f"     Steps:")
            for step in rec['steps']:
                print(f"       → {step}")
            print(f"     Research: {rec['research'][:100]}...")


# ============================================================================
# SCENARIO 1: Remote Worker - Deep Focus (Coding)
# ============================================================================

print("\n\nSCENARIO 1: Remote Software Developer - Optimizing for Deep Focus")
print("-" * 70)

developer_environment = EnvironmentalInputs(
    # Lighting (needs improvement)
    illuminance_lux=250,  # Too dim for analytical work
    color_temperature_k=3500,  # Too warm (need 4500-6500K)
    cri_index=75,  # Below optimal (need 90+)
    natural_light_percentage=20,  # Very little window
    glare_level="slight",
    
    # Acoustics (poor)
    ambient_db=65,  # Too loud (household noise)
    sound_type="speech",
    
    # Layout (sub-optimal)
    desk_height_inches=31,  # Slightly high
    monitor_distance_inches=18,  # Too close
    monitor_angle_degrees=5,  # Too high (causes neck strain)
    clutter_level=45,  # Moderate clutter
    plants_count=0,
    window_access=False,
    ceiling_height_feet=9,
    
    # Climate
    temperature_f=73,  # Slightly warm
    humidity_percentage=35,  # Low
    co2_ppm=1200,  # Elevated
    
    # Personal
    user_sensitivity=Sensitivity.HIGH,
    work_schedule="morning"
)

dev_report = generate_report(
    task_type=TaskType.DEEP_FOCUS,
    sensitivity=Sensitivity.HIGH,
    inputs=developer_environment
)

print_report(dev_report, "Software Developer - Deep Focus Optimization")


# ============================================================================
# SCENARIO 2: Creative Professional - Design/Brainstorming
# ============================================================================

print("\n\nSCENARIO 2: Creative Professional - UX/UI Designer")
print("-" * 70)

designer_environment = EnvironmentalInputs(
    # Lighting (optimized)
    illuminance_lux=400,
    color_temperature_k=3800,  # Slightly warm for creativity
    cri_index=95,  # High CRI for color accuracy
    natural_light_percentage=60,  # Good window access
    glare_level="none",
    
    # Acoustics (good but variable)
    ambient_db=55,  # Background music
    sound_type="music",
    
    # Layout (good but could improve)
    desk_height_inches=29,
    monitor_distance_inches=26,
    monitor_angle_degrees=18,
    clutter_level=40,  # Creative clutter is acceptable
    plants_count=2,
    window_access=True,
    ceiling_height_feet=12,
    
    # Climate (optimal)
    temperature_f=71,
    humidity_percentage=50,
    co2_ppm=800,
    
    # Personal
    user_sensitivity=Sensitivity.MODERATE,
    work_schedule="morning"
)

designer_report = generate_report(
    task_type=TaskType.CREATIVE,
    sensitivity=Sensitivity.MODERATE,
    inputs=designer_environment
)

print_report(designer_report, "Designer - Creative Optimization")


# ============================================================================
# SCENARIO 3: Data Analyst - Analytical Work
# ============================================================================

print("\n\nSCENARIO 3: Data Analyst - Spreadsheets & Analysis")
print("-" * 70)

analyst_environment = EnvironmentalInputs(
    # Lighting (needs improvement - eyes stressed from screens)
    illuminance_lux=320,  # Low
    color_temperature_k=5200,  # Neutral
    cri_index=88,
    natural_light_percentage=0,  # Internal office
    glare_level="moderate",  # From screen reflection
    
    # Acoustics (open office - problematic)
    ambient_db=72,  # Open office noise
    sound_type="speech",
    
    # Layout (ergonomic issues)
    desk_height_inches=30,
    monitor_distance_inches=16,  # Too close
    monitor_angle_degrees=25,  # Too low
    clutter_level=60,  # Lots of papers
    plants_count=0,
    window_access=False,
    ceiling_height_feet=8,
    
    # Climate
    temperature_f=72,
    humidity_percentage=42,
    co2_ppm=1400,  # Elevated from shared office
    
    # Personal
    user_sensitivity=Sensitivity.HIGH,
    work_schedule="afternoon"
)

analyst_report = generate_report(
    task_type=TaskType.ANALYTICAL,
    sensitivity=Sensitivity.HIGH,
    inputs=analyst_environment
)

print_report(analyst_report, "Data Analyst - Analytical Work Optimization")


# ============================================================================
# SCENARIO 4: Student - Learning/Reading
# ============================================================================

print("\n\nSCENARIO 4: Student - Learning & Studying")
print("-" * 70)

student_environment = EnvironmentalInputs(
    # Lighting
    illuminance_lux=550,  # Good for reading
    color_temperature_k=5000,
    cri_index=92,
    natural_light_percentage=40,
    glare_level="none",
    
    # Acoustics (library-like)
    ambient_db=28,  # Very quiet
    sound_type="silence",
    
    # Layout
    desk_height_inches=30,
    monitor_distance_inches=24,
    monitor_angle_degrees=15,
    clutter_level=15,  # Minimal
    plants_count=1,
    window_access=True,
    ceiling_height_feet=10,
    
    # Climate
    temperature_f=69,
    humidity_percentage=45,
    co2_ppm=900,
    
    # Personal
    user_sensitivity=Sensitivity.LOW,
    work_schedule="morning"
)

student_report = generate_report(
    task_type=TaskType.LEARNING,
    sensitivity=Sensitivity.LOW,
    inputs=student_environment
)

print_report(student_report, "Student - Learning Environment Optimization")


# ============================================================================
# EXPORT RECOMMENDATIONS TO JSON
# ============================================================================

print("\n\n" + "="*70)
print("  EXPORTING RECOMMENDATIONS TO JSON")
print("="*70)

all_scenarios = {
    "developer": dev_report,
    "designer": designer_report,
    "analyst": analyst_report,
    "student": student_report
}

with open("optimization_reports.json", "w") as f:
    json.dump(all_scenarios, f, indent=2)

print("✅ Reports exported to: optimization_reports.json")
print(f"   Total scenarios: {len(all_scenarios)}")


# ============================================================================
# QUICK REFERENCE: OPTIMAL RANGES BY TASK
# ============================================================================

print("\n\n" + "="*70)
print("  QUICK REFERENCE: OPTIMAL ENVIRONMENTAL RANGES")
print("="*70)

optimizer = EnvironmentOptimizer(TaskType.DEEP_FOCUS, Sensitivity.MODERATE)

print("\nOptimal Environmental Parameters by Task Type:\n")

for task in TaskType:
    ranges = optimizer.TASK_RANGES[task]
    print(f"📌 {task.value.upper()}")
    print(f"   Light:    {ranges['illuminance_lux'][0]}-{ranges['illuminance_lux'][1]} lux")
    print(f"   Temp:     {ranges['color_temperature_k'][0]}-{ranges['color_temperature_k'][1]}K")
    print(f"   Sound:    {ranges['ambient_db'][0]}-{ranges['ambient_db'][1]} dB")
    print(f"   Temp:     {ranges['temperature_f'][0]}-{ranges['temperature_f'][1]}°F")
    print(f"   Clutter:  {ranges['clutter_level'][0]}-{ranges['clutter_level'][1]}%\n")


# ============================================================================
# MEASUREMENT GUIDE
# ============================================================================

print("\n" + "="*70)
print("  HOW TO MEASURE YOUR ENVIRONMENT")
print("="*70)

measurement_guide = {
    "Illuminance (lux)": [
        "• Use phone app: 'Light Meter' (free Android/iOS)",
        "• Hold phone horizontally at desk surface",
        "• Record midday, afternoon, and overcast readings"
    ],
    "Color Temperature (K)": [
        "• Check bulb packaging or product specs",
        "• Common: LED 3000K (warm), 4000K (neutral), 5000K+ (cool)",
        "• Smartphones: Use color temp apps (rough estimate)"
    ],
    "Sound Level (dB)": [
        "• Use phone app: 'Sound Level Meter' (free)",
        "• Measure with and without white noise",
        "• Average 3-5 readings over 2 minutes"
    ],
    "Temperature (°F)": [
        "• Use home thermostat reading",
        "• Or digital thermometer (3-minute acclimation)"
    ],
    "CO2 (ppm)": [
        "• Use CO2 monitor (CO2Meter or similar, $50-150)",
        "• Or monitor for visual indicators:",
        "  - <800ppm: Excellent",
        "  - 800-1000ppm: Good",
        "  - 1000-1400ppm: Fair",
        "  - >1400ppm: Poor (ventilate immediately)"
    ]
}

for measurement, tips in measurement_guide.items():
    print(f"\n🔧 {measurement}")
    for tip in tips:
        print(f"   {tip}")

print("\n" + "="*70)
