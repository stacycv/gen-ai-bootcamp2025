from .vectorstore import get_similar_questions
from .structured_data import format_question

def generate_question(similar_questions, practice_type):
    """
    Generate a question using RAG based on similar questions and practice type
    
    Args:
        similar_questions (list): List of similar questions from vector store
        practice_type (str): Type of practice (Listening, Vocabulary, Dialogue)
        
    Returns:
        dict: Question data containing question, options, correct answer, and dialogue
    """
    # Take the first question from similar questions
    question_data = similar_questions[0] if similar_questions else {
        'dialogue': [],
        'question': "No questions available for this topic",
        'options': ["Option 1", "Option 2", "Option 3", "Option 4"],
        'correct_answer': "Option 1"
    }
    
    # Format dialogue if it exists
    if 'dialogue' in question_data:
        formatted_dialogue = []
        for i, line in enumerate(question_data['dialogue']):
            if isinstance(line, dict):
                formatted_dialogue.append(line)
            else:
                # Alternate between speakers if not specified
                speaker = 'Person A' if i % 2 == 0 else 'Person B'
                formatted_dialogue.append({
                    'speaker': speaker,
                    'text': line.strip()
                })
        question_data['dialogue'] = formatted_dialogue
    
    return question_data 