from typing import Dict, List, Optional
from dataclasses import dataclass
import os

@dataclass
class DialogueSegment:
    introduction: str
    conversation: List[str]
    question: str

class TranscriptStructurer:
    def __init__(self):
        """Initialize structurer"""
        pass  # No AWS client needed for now

    def structure_transcript(self, transcript: List[Dict]) -> List[DialogueSegment]:
        """Structure the transcript into dialogue segments"""
        segments = []
        current_intro = []
        current_conversation = []
        current_question = ""
        
        # States to track where we are in the transcript
        IN_INTRO = "intro"
        IN_CONVO = "conversation"
        IN_QUESTION = "question"
        current_state = IN_INTRO
        
        for entry in transcript:
            text = entry['text'].strip()
            
            # Check for section markers
            if text.lower().startswith('conversation:') or text.lower().startswith('dialogue:'):
                current_state = IN_CONVO
                continue
            elif text.lower().startswith('question:'):
                # Save current conversation and start new segment
                if current_conversation:
                    segment = DialogueSegment(
                        introduction='\n'.join(current_intro),
                        conversation=current_conversation.copy(),
                        question=text
                    )
                    segments.append(segment)
                    # Reset for next segment
                    current_intro = []
                    current_conversation = []
                current_state = IN_QUESTION
                continue
            elif text.lower().startswith('introduction:') or text.lower().startswith('context:'):
                current_state = IN_INTRO
                continue
                
            # Add text to appropriate section
            if current_state == IN_INTRO:
                current_intro.append(text)
            elif current_state == IN_CONVO:
                if text.strip():  # Only add non-empty lines
                    current_conversation.append(text)
            elif current_state == IN_QUESTION:
                current_question = text
        
        # Add final segment if there's remaining content
        if current_conversation or current_intro or current_question:
            segments.append(DialogueSegment(
                introduction='\n'.join(current_intro),
                conversation=current_conversation,
                question=current_question
            ))
            
        return segments

    def save_structured_data(self, segments: List[DialogueSegment], filename: str) -> bool:
        """Save structured data to file"""
        try:
            # Create structured directory if it doesn't exist
            os.makedirs("./structured", exist_ok=True)
            
            output = []
            for i, segment in enumerate(segments, 1):
                output.append(f"\n=== Segment {i} ===\n")
                
                if segment.introduction:
                    output.append("=== Introduction ===")
                    output.append(segment.introduction)
                    output.append("")
                
                output.append("=== Conversation ===")
                output.extend(segment.conversation)
                output.append("")
                
                if segment.question:
                    output.append("=== Question ===")
                    output.append(segment.question)
                
                output.append("\n" + "="*30 + "\n")
                
            with open(f"./structured/{filename}.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
            return True
            
        except Exception as e:
            print(f"Error saving structured data: {str(e)}")
            return False

    def load_transcript(self, filepath: str) -> List[DialogueSegment]:
        """Load transcript from file and structure it"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                transcript = [{'text': line.strip()} for line in f if line.strip()]
            return self.structure_transcript(transcript)
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return []

def main():
    # Simple test using direct file path
    structurer = TranscriptStructurer()
    structured_text = structurer.load_transcript("transcripts/sY7L5cfCWno.txt")
    
    # Print raw structured text
    print("Raw structured text:")
    print(structured_text)
    print("\n---\n")
    
    if structured_text:
        print("Successfully structured transcript:")
        for i, segment in enumerate(structured_text, 1):
            print(f"\nSegment {i}:")
            print(f"Introduction: {segment.introduction}")
            print("Conversation:")
            for line in segment.conversation:
                print(f"  {line}")
            print(f"Question: {segment.question}")
    else:
        print("Failed to structure transcript")

if __name__ == "__main__":
    main()
