from typing import Dict, List, Optional
from dataclasses import dataclass
import os
import re

@dataclass
class Question:
    number: int
    context: str
    question_text: str
    answer_options: List[str] = None

@dataclass
class DialogueSegment:
    introduction: str
    conversation: List[str]
    question: str
    answer_options: List[str] = None

@dataclass
class Section:
    number: int
    description: str
    example: Optional[DialogueSegment]
    segments: List[DialogueSegment]

class TranscriptStructurer:
    def __init__(self):
        """Initialize structurer"""
        pass

    def structure_transcript(self, transcript: List[Dict]) -> List[Section]:
        """Structure the transcript into sections with dialogue segments"""
        sections = []
        current_section = None
        current_intro = []
        current_conversation = []
        current_question = ""
        current_options = []
        current_segments = []  # Add this to store DialogueSegment objects
        in_example = False
        
        for entry in transcript:
            text = entry['text'].strip()
            
            # Skip empty lines and music markers
            if not text or '[音楽]' in text:
                continue
                
            # Check for section markers
            if '問題' in text:
                try:
                    section_num = re.search(r'問題(\d+)', text)
                    if section_num:
                        if current_section is not None:
                            sections.append(Section(
                                number=current_section,
                                description=''.join(current_intro),
                                example=None,
                                segments=current_segments.copy()  # Use segments instead of conversation
                            ))
                        
                        current_section = int(section_num.group(1))
                        current_intro = []
                        current_conversation = []
                        current_question = ""
                        current_options = []
                        current_segments = []  # Reset segments
                        in_example = False
                        continue
                except ValueError:
                    current_intro.append(text)
                    continue
            
            # Check for example marker
            if '例' in text:
                in_example = True
                continue
            
            # Check for answer options (1-4 or multiple choice indicators)
            if re.match(r'^[1-4]\.', text) or '選んでください' in text:
                current_options.append(text)
                continue
            
            # Check for new dialogue segment
            if text.endswith('ます') or text.endswith('ください'):
                if current_conversation:
                    segment = DialogueSegment(
                        introduction='\n'.join(current_intro),
                        conversation=current_conversation.copy(),
                        question=current_question,
                        answer_options=current_options.copy()
                    )
                    if in_example:
                        if current_section is not None and sections:
                            sections[-1].example = segment
                        in_example = False
                    else:
                        current_segments.append(segment)  # Append to segments instead of conversation
                    current_intro = []
                    current_conversation = []
                    current_question = ""
                    current_options = []
                continue
            
            # Add to appropriate section
            if text.endswith('か'):
                current_question = text
            else:
                current_conversation.append(text)
        
        # Add final section
        if current_section is not None:
            sections.append(Section(
                number=current_section,
                description=''.join(current_intro),
                example=None,
                segments=current_segments.copy()
            ))
        
        return sections

    def save_structured_data(self, sections: List[Section], filename: str) -> bool:
        """Save structured data to file"""
        try:
            os.makedirs("./structured", exist_ok=True)
            
            output = []
            for section in sections:
                output.append(f"\n{'='*50}")
                output.append(f"問題 {section.number}")
                output.append('='*50)
                
                output.append("\n=== Description ===")
                output.append(section.description)
                
                if section.example:
                    output.append("\n=== Example ===")
                    output.append(f"Context: {section.example.context}")
                    output.append(f"Question: {section.example.question_text}")
                
                output.append("\n=== Questions ===")
                for q in section.segments:
                    output.append(f"\nQuestion {q.number}:")
                    output.append(f"Context: {q.context}")
                    output.append(f"Question: {q.question_text}")
                
                output.append("\n" + "="*50 + "\n")
                
            with open(f"./structured/{filename}.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
            return True
            
        except Exception as e:
            print(f"Error saving structured data: {str(e)}")
            return False

    def load_transcript(self, filepath: str) -> List[Section]:
        """Load transcript from file and structure it"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                transcript = [{'text': line.strip()} for line in f if line.strip()]
            return self.structure_transcript(transcript)
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return []

    def save_to_questions(self, section: Section, filename: str) -> bool:
        """Save individual section output to questions folder"""
        try:
            os.makedirs("../data/questions", exist_ok=True)
            
            output = []
            output.append(f"{'='*50}")
            output.append(f"問題 {section.number}")
            output.append('='*50)
            
            output.append("\n=== Description ===")
            output.append(section.description)
            
            if section.example:
                output.append("\n=== Example ===")
                output.append("Introduction:")
                output.append(section.example.introduction)
                output.append("\nConversation:")
                for line in section.example.conversation:
                    output.append(line)
                output.append("\nQuestion:")
                output.append(section.example.question)
                if section.example.answer_options:
                    output.append("\nPossible Answers:")
                    for option in section.example.answer_options:
                        output.append(option)
            
            output.append("\n=== Dialogues ===")
            for segment in section.segments:
                output.append("\nIntroduction:")
                output.append(segment.introduction)
                output.append("\nConversation:")
                for line in segment.conversation:
                    output.append(line)
                output.append("\nQuestion:")
                output.append(segment.question)
                if segment.answer_options:
                    output.append("\nPossible Answers:")
                    for option in segment.answer_options:
                        output.append(option)
                output.append("\n" + "-"*30)
            
            with open(f"../data/questions/section_{section.number}_{filename}.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
            return True
            
        except Exception as e:
            print(f"Error saving to questions folder: {str(e)}")
            return False

def format_question(similar_questions):
    """
    Format similar questions for RAG context
    
    Args:
        similar_questions (list): List of similar questions
        
    Returns:
        str: Formatted context for RAG
    """
    return "\n".join(similar_questions)

def main():
    structurer = TranscriptStructurer()
    structured_text = structurer.load_transcript("../data/transcripts/sY7L5cfCWno.txt")
    
    if structured_text:
        print("Successfully structured transcript")
        for section in structured_text:
            if structurer.save_to_questions(section, "sY7L5cfCWno"):
                print(f"Saved section {section.number} to questions folder")
            else:
                print(f"Failed to save section {section.number}")
    else:
        print("Failed to structure transcript")

if __name__ == "__main__":
    main()
