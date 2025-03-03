from gtts import gTTS
from typing import List, Dict, Optional
import os
from dataclasses import dataclass
from enum import Enum
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceGender(Enum):
    MALE = "male"
    FEMALE = "female"

@dataclass
class VoiceConfig:
    language: str
    tld: str  # Top Level Domain for different accents
    gender: VoiceGender

class AudioGenerator:
    def __init__(self):
        """Initialize voice configurations"""
        try:
            # Configure different voices using different TLDs for variety
            self.voice_configs = {
                "announcer": VoiceConfig(
                    language="es",
                    tld="es",  # Spain Spanish
                    gender=VoiceGender.MALE
                ),
                "tourist": VoiceConfig(
                    language="es",
                    tld="com.mx",  # Mexican Spanish
                    gender=VoiceGender.MALE
                ),
                "staff": VoiceConfig(
                    language="es",
                    tld="es",  # Spain Spanish
                    gender=VoiceGender.FEMALE
                ),
                "male_1": VoiceConfig(
                    language="es",
                    tld="com.mx",
                    gender=VoiceGender.MALE
                ),
                "female_1": VoiceConfig(
                    language="es",
                    tld="es",
                    gender=VoiceGender.FEMALE
                )
            }
            
            # Voice mapping for specific roles
            self.role_voice_mapping = {
                "Tourist": "tourist",
                "Station Staff": "staff",
                "Waiter": "male_1",
                "Customer": "female_1"
            }
            
            # Create output directory if it doesn't exist
            self.audio_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data",
                "audio"
            )
            os.makedirs(self.audio_dir, exist_ok=True)
            
        except Exception as e:
            logger.error(f"Error initializing AudioGenerator: {str(e)}")
            raise

    def get_voice_for_role(self, role: str) -> VoiceConfig:
        """Get appropriate voice configuration for a given role"""
        voice_key = self.role_voice_mapping.get(role)
        if voice_key:
            return self.voice_configs[voice_key]
        
        # Default to male/female voices based on role name
        if any(female_indicator in role.lower() for female_indicator in 
               ['woman', 'girl', 'female', 'she', 'waitress', 'mother', 'sister']):
            return self.voice_configs['female_1']
        return self.voice_configs['male_1']

    def generate_practice_audio(self, scenario_data: Dict) -> str:
        """Generate audio for a complete practice scenario"""
        try:
            # Create a complete text with pauses
            full_text = ""
            
            # Add introduction
            if scenario_data.get('introduction'):
                full_text += f"Ejercicio de práctica. {scenario_data['introduction']}\n\n"
            
            # Add conversation
            for line in scenario_data.get('conversation', []):
                full_text += f"{line['text']}\n"
            
            # Add question
            if scenario_data.get('question'):
                full_text += f"\nAhora, la pregunta: {scenario_data['question']}"
            
            # Generate audio file
            output_filename = f"practice_{hash(str(scenario_data))}.mp3"
            output_path = os.path.join(self.audio_dir, output_filename)
            
            # Generate speech using Mexican Spanish
            tts = gTTS(text=full_text, lang="es", tld="com.mx")
            tts.save(output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating practice audio: {str(e)}")
            return None 