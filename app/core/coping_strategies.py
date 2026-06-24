from typing import Dict
import random

STRATEGIES = {
    "anxious": [
        {"name": "Box Breathing (4-7-8)", "steps": "Inhale 4 sec, Hold 7 sec, Exhale 8 sec. Repeat 4 times.", "why": "Activates parasympathetic nervous system, reducing cortisol.", "time": "3-5 minutes", "type": "breathing"},
        {"name": "5-4-3-2-1 Grounding", "steps": "Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste.", "why": "Anchors you to present moment, interrupting anxiety loops.", "time": "2-3 minutes", "type": "grounding"},
    ],
    "sad": [
        {"name": "Behavioral Activation", "steps": "Do ONE small pleasurable activity right now, even 5 minutes counts.", "why": "Breaks the depression-inaction cycle (CBT-backed).", "time": "5-30 minutes", "type": "activity"},
        {"name": "Gratitude Journaling", "steps": "Write 3 specific things you're grateful for today, with detail.", "why": "Shifts neural focus from deficit to abundance.", "time": "5-10 minutes", "type": "journaling"},
    ],
    "overwhelmed": [
        {"name": "Brain Dump + Prioritize", "steps": "Write everything on your mind. Then circle only the top 2 that matter today.", "why": "Offloads cognitive load, reduces decision fatigue.", "time": "10 minutes", "type": "cognitive"},
    ],
    "angry": [
        {"name": "STOP Technique", "steps": "Stop. Take a breath. Observe your feelings. Proceed mindfully.", "why": "Creates gap between trigger and response (DBT skill).", "time": "1-2 minutes", "type": "mindfulness"},
    ],
    "lonely": [
        {"name": "Connection Prompt", "steps": "Send one person a message saying something you appreciate about them.", "why": "Micro-connections rebuild social belonging.", "time": "3 minutes", "type": "social"},
    ],
    "neutral": [
        {"name": "Mindful Check-in", "steps": "Place hand on heart. Ask: what do I need right now? Sit quietly for 60 seconds.", "why": "Builds interoceptive awareness and self-compassion.", "time": "2 minutes", "type": "mindfulness"},
    ],
}

MOTIVATIONAL_PROMPTS = [
    "You showed up today. That already takes courage.",
    "Healing isn't linear, and that's okay. You're still moving forward.",
    "You've survived every hard day so far. This one too.",
    "Your feelings are valid. All of them. No exceptions.",
    "Small steps are still steps. You're doing better than you think.",
]

MUSIC_MOODS = {
    "anxious": {"tempo": "slow", "genre": "ambient", "file": "calm_ambient.mp3"},
    "sad": {"tempo": "gentle", "genre": "soft_piano", "file": "soft_piano.mp3"},
    "angry": {"tempo": "slow", "genre": "lo-fi", "file": "lofi_chill.mp3"},
    "overwhelmed": {"tempo": "very_slow", "genre": "nature", "file": "nature_sounds.mp3"},
    "happy": {"tempo": "upbeat", "genre": "uplifting", "file": "uplifting_acoustic.mp3"},
    "lonely": {"tempo": "warm", "genre": "acoustic", "file": "warm_acoustic.mp3"},
    "neutral": {"tempo": "moderate", "genre": "lo-fi", "file": "lofi_study.mp3"},
}

def get_strategy(mood: str) -> Dict:
    strategies = STRATEGIES.get(mood, STRATEGIES["neutral"])
    return random.choice(strategies)

def get_motivational_prompt() -> str:
    return random.choice(MOTIVATIONAL_PROMPTS)
