import os
import sys
import logging
from audio_generator import AudioGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_practice_scenario():
    """Test audio generation with a practice scenario"""
    
    # Sample practice scenario
    scenario_data = {
        'introduction': '駅での会話です。',
        'conversation': [
            {
                'speaker': 'Tourist',
                'text': 'すみません。'
            },
            {
                'speaker': 'Station Staff',
                'text': 'はい、いかがいたしましょうか？'
            },
            {
                'speaker': 'Tourist',
                'text': '東京駅までの切符を買いたいのですが。'
            },
            {
                'speaker': 'Station Staff',
                'text': '普通列車ですか、新幹線ですか？'
            },
            {
                'speaker': 'Tourist',
                'text': '新幹線で行きたいです。'
            },
            {
                'speaker': 'Station Staff',
                'text': '指定席と自由席がございますが、どちらにされますか？'
            },
            {
                'speaker': 'Tourist',
                'text': '指定席をお願いします。'
            }
        ],
        'question': 'お客様はどの種類の席を選びましたか？'
    }

    try:
        # Initialize audio generator
        generator = AudioGenerator()
        
        # Generate audio
        logger.info("Generating practice scenario audio...")
        audio_path = generator.generate_practice_audio(scenario_data)
        
        if audio_path and os.path.exists(audio_path):
            logger.info(f"\nAudio generated successfully!")
            logger.info(f"Audio file location: {audio_path}")
            
            # If on macOS, try to play the audio
            if sys.platform == 'darwin':
                os.system(f'afplay "{audio_path}"')
                logger.info("\nPlaying audio... (macOS only)")
            else:
                logger.info("\nTo play the audio, open the file at the location shown above.")
        else:
            logger.error("Failed to generate audio")
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")

if __name__ == "__main__":
    test_practice_scenario() 