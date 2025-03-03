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
        # Create output directory first
        self.audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "audio"
        )
        os.makedirs(self.audio_dir, exist_ok=True)

        try:
            # Configure different voices using different TLDs for variety
            self.voice_configs = {
                "announcer": VoiceConfig(
                    language="es",
                    tld="com.mx",  # Mexican Spanish
                    gender=VoiceGender.MALE
                ),
                "male": VoiceConfig(
                    language="es",
                    tld="com.mx",  # Mexican Spanish
                    gender=VoiceGender.MALE
                ),
                "female": VoiceConfig(
                    language="es",
                    tld="com.mx",  # Mexican Spanish
                    gender=VoiceGender.FEMALE
                )
            }
            
            # Simplified voice mapping - just alternate male/female
            self.last_voice = "male"  # Track last used voice to alternate
            
        except Exception as e:
            logger.error(f"Error initializing AudioGenerator: {str(e)}")
            raise

    def get_voice_for_role(self, role: str) -> VoiceConfig:
        """Get appropriate voice configuration for a given role"""
        # Alternate between male and female voices
        self.last_voice = "female" if self.last_voice == "male" else "male"
        return self.voice_configs[self.last_voice]

    def generate_practice_audio(self, scenario_data: Dict) -> str:
        """Generate audio for a complete practice scenario"""
        try:
            # Create temporary directory for voice segments
            temp_dir = os.path.join(self.audio_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            audio_segments = []

            # Generate introduction with announcer voice
            if scenario_data.get('introduction'):
                intro_text = f"Ejercicio de práctica. {scenario_data['introduction']}"
                intro_path = os.path.join(temp_dir, "intro.mp3")
                tts = gTTS(text=intro_text, lang="es", tld="com.mx", slow=False)
                tts.save(intro_path)
                audio_segments.append(intro_path)

            # Generate conversation with different voices
            if scenario_data.get('conversation'):
                for i, line in enumerate(scenario_data['conversation']):
                    # Get voice config for this speaker
                    voice_config = self.get_voice_for_role(line['speaker'])
                    
                    # Generate audio for this line
                    line_path = os.path.join(temp_dir, f"line_{i}.mp3")
                    tts = gTTS(
                        text=f"{line['text']}", 
                        lang="es",
                        tld=voice_config.tld,
                        slow=False
                    )
                    tts.save(line_path)
                    audio_segments.append(line_path)

            # Generate question with announcer voice
            if scenario_data.get('question'):
                question_text = f"\nAhora, la pregunta: {scenario_data['question']}"
                question_path = os.path.join(temp_dir, "question.mp3")
                tts = gTTS(text=question_text, lang="es", tld="com.mx", slow=False)
                tts.save(question_path)
                audio_segments.append(question_path)

            # Combine all audio segments
            output_filename = f"practice_{hash(str(scenario_data))}.mp3"
            output_path = os.path.join(self.audio_dir, output_filename)

            # Combine audio files using system command
            with open(output_path, 'wb') as outfile:
                for segment in audio_segments:
                    with open(segment, 'rb') as infile:
                        outfile.write(infile.read())

            # Cleanup temp files
            for segment in audio_segments:
                if os.path.exists(segment):
                    os.remove(segment)

            return output_path
            
        except Exception as e:
            logger.error(f"Error generating practice audio: {str(e)}")
            return None 