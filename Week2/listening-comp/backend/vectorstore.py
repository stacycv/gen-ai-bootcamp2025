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
            'introduction': "A conversation at a Japanese restaurant",
            'conversation': [
                {'speaker': 'Waiter', 'text': 'いらっしゃいませ。'},
                {'speaker': 'Customer A', 'text': 'こんにちは。4人で来ました。'},
                {'speaker': 'Waiter', 'text': 'かしこまりました。こちらのテーブルへどうぞ。'},
                {'speaker': 'Customer B', 'text': 'ありがとうございます。今日の特別メニューはありますか？'},
                {'speaker': 'Waiter', 'text': 'はい、本日は海鮮丼と天ぷら定食がおすすめです。'},
                {'speaker': 'Customer A', 'text': '私は海鮮丼をお願いします。'},
                {'speaker': 'Customer C', 'text': '天ぷら定食を2つお願いします。'},
                {'speaker': 'Customer D', 'text': '私はラーメンでお願いします。'},
                {'speaker': 'Waiter', 'text': 'かしこまりました。お飲み物はいかがですか？'},
                {'speaker': 'Customer A', 'text': 'お茶をお願いします。'},
                {'speaker': 'Customer B', 'text': '私もお茶で。'},
                {'speaker': 'Waiter', 'text': 'ご注文を確認させていただきます。'}
            ],
            'question': "Customer Aは何を注文しましたか？",
            'options': [
                "海鮮丼",
                "天ぷら定食",
                "ラーメン",
                "うどん"
            ],
            'correct_answer': "海鮮丼"
        },
        {
            'introduction': "A conversation at a Japanese school",
            'conversation': [
                {'speaker': 'Teacher', 'text': 'おはようございます。'},
                {'speaker': 'Students', 'text': 'おはようございます。'},
                {'speaker': 'Teacher', 'text': '今日は校外学習について話します。'},
                {'speaker': 'Student A', 'text': '先生、どこへ行きますか？'},
                {'speaker': 'Teacher', 'text': '来週の水曜日に京都へ行きます。'},
                {'speaker': 'Student B', 'text': '何時に学校に集まりますか？'},
                {'speaker': 'Teacher', 'text': '朝7時に学校に集まってください。'},
                {'speaker': 'Student C', 'text': 'お弁当は持って行きますか？'},
                {'speaker': 'Teacher', 'text': 'はい、お弁当と水筒を持ってきてください。'},
                {'speaker': 'Student A', 'text': 'カメラを持って行ってもいいですか？'},
                {'speaker': 'Teacher', 'text': 'はい、大丈夫です。'},
                {'speaker': 'Student D', 'text': '何時頃帰りますか？'},
                {'speaker': 'Teacher', 'text': '午後5時頃に学校に戻る予定です。'}
            ],
            'question': "校外学習はいつですか？",
            'options': [
                "来週の水曜日",
                "今日",
                "明日",
                "来週の月曜日"
            ],
            'correct_answer': "来週の水曜日"
        },
        {
            'introduction': "A conversation at a train station",
            'conversation': [
                {'speaker': 'Tourist', 'text': 'すみません。'},
                {'speaker': 'Station Staff', 'text': 'はい、いかがいたしましょうか？'},
                {'speaker': 'Tourist', 'text': '東京駅までの切符を買いたいのですが。'},
                {'speaker': 'Station Staff', 'text': '普通列車ですか、新幹線ですか？'},
                {'speaker': 'Tourist', 'text': '新幹線で行きたいです。'},
                {'speaker': 'Station Staff', 'text': '指定席と自由席がございますが、どちらにされますか？'},
                {'speaker': 'Tourist', 'text': '指定席をお願いします。'},
                {'speaker': 'Station Staff', 'text': '何時頃の電車をご希望ですか？'},
                {'speaker': 'Tourist', 'text': '10時頃の電車を探しています。'},
                {'speaker': 'Station Staff', 'text': '10時15分発がございますが、いかがでしょうか？'},
                {'speaker': 'Tourist', 'text': 'はい、それでお願いします。'},
                {'speaker': 'Station Staff', 'text': 'かしこまりました。窓側と通路側、どちらがよろしいですか？'}
            ],
            'question': "お客様はどの種類の席を選びましたか？",
            'options': [
                "指定席",
                "自由席",
                "グリーン車",
                "立ち席"
            ],
            'correct_answer': "指定席"
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