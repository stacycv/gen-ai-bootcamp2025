from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
import boto3
import os
import json
import random

def load_questions_from_files():
    """Load questions from the data/questions directory"""
    questions = []
    questions_dir = "../data/questions"
    
    for filename in os.listdir(questions_dir):
        if filename.startswith("section_") and filename.endswith(".txt"):
            with open(os.path.join(questions_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse the content to extract dialogues and questions
                sections = parse_question_file(content)
                questions.extend(sections)
    
    return questions

def parse_question_file(content):
    """Parse a question file to extract structured data"""
    sections = []
    current_section = None
    current_dialogue = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("Context:"):
            if current_section:
                if current_section.get('conversation') and current_section.get('question'):
                    sections.append(current_section)
            current_section = {
                'introduction': "A Japanese conversation practice",
                'conversation': [],
                'question': "",
                'options': [],
                'correct_answer': None
            }
            continue
            
        if current_section:
            # If line contains Japanese text, add it to conversation
            if any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in line):
                # Split into speaker-text if possible
                if 'か' in line and len(current_section['conversation']) > 1:
                    # This is likely a question
                    current_section['question'] = line.replace('か', '?')
                else:
                    # This is conversation
                    if ':' in line:
                        speaker, text = line.split(':', 1)
                    else:
                        speaker = f'Speaker {len(current_section["conversation"]) % 2 + 1}'
                        text = line
                    current_section['conversation'].append({
                        'speaker': speaker.strip(),
                        'text': text.strip()
                    })
            
            # If line starts with a number, it's probably an option
            elif line[0].isdigit():
                option = line[1:].strip()
                if option:
                    current_section['options'].append(option)
                    if not current_section.get('correct_answer'):
                        current_section['correct_answer'] = option
    
    # Add the last section if it exists
    if current_section and current_section.get('conversation'):
        if not current_section.get('options'):
            current_section['options'] = [
                "はい、そうです。",
                "いいえ、違います。",
                "わかりません。",
                "もう一度お願いします。"
            ]
            current_section['correct_answer'] = "はい、そうです。"
        sections.append(current_section)
    
    # If no valid sections were created, return a default question
    if not sections:
        return [{
            'introduction': "A conversation at a Japanese restaurant",
            'conversation': [
                {'speaker': 'Waiter', 'text': 'いらっしゃいませ。'},
                {'speaker': 'Customer', 'text': 'すみません、メニューをお願いします。'},
                {'speaker': 'Waiter', 'text': 'はい、少々お待ちください。'},
                {'speaker': 'Customer', 'text': 'ありがとうございます。ラーメンを一つお願いします。'},
                {'speaker': 'Waiter', 'text': 'かしこまりました。お飲み物はいかがですか？'},
                {'speaker': 'Customer', 'text': 'お水をお願いします。'},
                {'speaker': 'Waiter', 'text': 'はい、承知いたしました。'}
            ],
            'question': "お客様は何を注文しましたか？",
            'options': [
                "ラーメンとお水",
                "うどんとお茶",
                "カレーとコーヒー",
                "寿司とビール"
            ],
            'correct_answer': "ラーメンとお水"
        }]
    
    return sections

def get_similar_questions(practice_type, topic=None):
    """Get questions based on practice type and topic"""
    
    # Define conversation templates for different scenarios
    conversation_templates = [
        {
            'introduction': "Una conversación en un restaurante español",
            'conversation': [
                {'speaker': 'Camarero', 'text': '¡Bienvenidos!'},
                {'speaker': 'Cliente A', 'text': 'Hola, somos cuatro personas.'},
                {'speaker': 'Camarero', 'text': 'Por aquí, por favor. Esta es su mesa.'},
                {'speaker': 'Cliente B', 'text': 'Gracias. ¿Tienen menú del día?'},
                {'speaker': 'Camarero', 'text': 'Sí, hoy tenemos paella y pescado fresco.'},
                {'speaker': 'Cliente A', 'text': 'Para mí la paella, por favor.'},
                {'speaker': 'Cliente C', 'text': 'Dos pescados, por favor.'},
                {'speaker': 'Cliente D', 'text': 'Yo quiero la sopa.'},
                {'speaker': 'Camarero', 'text': '¿Y para beber?'},
                {'speaker': 'Cliente A', 'text': 'Agua mineral, por favor.'},
                {'speaker': 'Cliente B', 'text': 'Lo mismo para mí.'},
                {'speaker': 'Camarero', 'text': 'Muy bien, repito el pedido...'}
            ],
            'question': "¿Qué pidió el Cliente A?",
            'options': [
                "Paella",
                "Pescado",
                "Sopa",
                "Ensalada"
            ],
            'correct_answer': "Paella"
        },
        {
            'introduction': "Una conversación en una escuela española",
            'conversation': [
                {'speaker': 'Profesor', 'text': 'Buenos días.'},
                {'speaker': 'Estudiantes', 'text': 'Buenos días, profesor.'},
                {'speaker': 'Profesor', 'text': 'Hoy vamos a hablar sobre la excursión.'},
                {'speaker': 'Estudiante A', 'text': '¿A dónde vamos?'},
                {'speaker': 'Profesor', 'text': 'El miércoles que viene iremos a Madrid.'},
                {'speaker': 'Estudiante B', 'text': '¿A qué hora nos encontramos?'},
                {'speaker': 'Profesor', 'text': 'A las 7 de la mañana en la escuela.'},
                {'speaker': 'Estudiante C', 'text': '¿Llevamos comida?'},
                {'speaker': 'Profesor', 'text': 'Sí, traigan almuerzo y agua.'},
                {'speaker': 'Estudiante A', 'text': '¿Podemos llevar cámara?'},
                {'speaker': 'Profesor', 'text': 'Sí, está permitido.'}
            ],
            'question': "¿Cuándo es la excursión?",
            'options': [
                "El miércoles que viene",
                "Hoy",
                "Mañana",
                "El lunes que viene"
            ],
            'correct_answer': "El miércoles que viene"
        },
        {
            'introduction': "Una conversación en una estación de tren",
            'conversation': [
                {'speaker': 'Turista', 'text': 'Disculpe.'},
                {'speaker': 'Empleado', 'text': '¿En qué puedo ayudarle?'},
                {'speaker': 'Turista', 'text': 'Quiero comprar un billete para Barcelona.'},
                {'speaker': 'Empleado', 'text': '¿Tren normal o AVE?'},
                {'speaker': 'Turista', 'text': 'AVE, por favor.'},
                {'speaker': 'Empleado', 'text': '¿Asiento de ventana o pasillo?'},
                {'speaker': 'Turista', 'text': 'Ventana, por favor.'},
                {'speaker': 'Empleado', 'text': '¿Para qué hora?'},
                {'speaker': 'Turista', 'text': 'Para las 10 si es posible.'},
                {'speaker': 'Empleado', 'text': 'Hay uno a las 10:15.'},
                {'speaker': 'Turista', 'text': 'Perfecto, ese mismo.'}
            ],
            'question': "¿Qué tipo de asiento eligió el turista?",
            'options': [
                "Ventana",
                "Pasillo",
                "Primera clase",
                "No especificado"
            ],
            'correct_answer': "Ventana"
        }
    ]
    
    try:
        # Return a random conversation template
        return [random.choice(conversation_templates)]
    except Exception as e:
        print(f"Error in get_similar_questions: {str(e)}")
        return [{
            'introduction': "A basic conversation",
            'conversation': [
                {'speaker': 'A', 'text': 'こんにちは。'},
                {'speaker': 'B', 'text': 'こんにちは。'},
            ],
            'question': "What greeting is used?",
            'options': [
                "こんにちは",
                "さようなら",
                "おはよう",
                "こんばんは"
            ],
            'correct_answer': "こんにちは"
        }]

class QuestionVectorStore:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.embeddings = BedrockEmbeddings(
            client=self.bedrock_client,
            model_id="amazon.titan-embed-text-v1"  # or your preferred embedding model
        )
        self.vector_store = None

    def create_vector_store(self, questions):
        """Create vector store from list of questions"""
        texts = [q["text"] for q in questions]
        metadata = [{"section": q["section"], "type": q["type"]} for q in questions]
        
        self.vector_store = FAISS.from_texts(
            texts,
            self.embeddings,
            metadatas=metadata
        )
        
    def find_similar_questions(self, query: str, k: int = 3):
        """Find k most similar questions to the query"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        return self.vector_store.similarity_search(query, k=k) 