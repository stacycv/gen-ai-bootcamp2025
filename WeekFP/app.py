import streamlit as st

# Basic page setup
st.set_page_config(
    page_title="Learn Spanish",
    layout="wide"
)

# Custom CSS with purple and sky blue colors
st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp {
        background-color: #E6E6FA;  /* Light purple background */
    }
    
    .main {
        background-color: #E6E6FA;
    }
    
    /* Lesson cards */
    .lesson-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid #87CEEB;  /* Sky blue accent */
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #483D8B;  /* Dark purple */
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #87CEEB;  /* Sky blue */
        color: #483D8B;  /* Dark purple text */
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #E6E6FA;  /* Light purple */
    }
    
    .level-section {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #87CEEB;
    }
    </style>
""", unsafe_allow_html=True)

# Lesson content organized by levels
lessons = {
    "Beginner": {
        "Basic Greetings": {
            "Hello": "Hola",
            "Goodbye": "Adiós",
            "Good morning": "Buenos días",
            "Good afternoon": "Buenas tardes",
            "Thank you": "Gracias"
        },
        "Numbers 1-10": {
            "One": "Uno",
            "Two": "Dos",
            "Three": "Tres",
            "Four": "Cuatro",
            "Five": "Cinco"
        },
        "Basic Colors": {
            "Red": "Rojo",
            "Blue": "Azul",
            "Green": "Verde",
            "Yellow": "Amarillo"
        }
    },
    "Intermediate": {
        "Daily Activities": {
            "I eat breakfast": "Desayuno",
            "I go to work": "Voy al trabajo",
            "I study Spanish": "Estudio español",
            "I watch TV": "Veo la televisión"
        },
        "Weather": {
            "It's sunny": "Hace sol",
            "It's raining": "Está lloviendo",
            "It's cold": "Hace frío",
            "It's hot": "Hace calor"
        },
        "Shopping": {
            "How much is it?": "¿Cuánto cuesta?",
            "It's expensive": "Es caro",
            "It's cheap": "Es barato",
            "I want to buy": "Quiero comprar"
        }
    },
    "Advanced": {
        "Business Spanish": {
            "Meeting": "Reunión",
            "Project": "Proyecto",
            "Deadline": "Fecha límite",
            "Budget": "Presupuesto"
        },
        "Medical Terms": {
            "Hospital": "Hospital",
            "Doctor": "Médico",
            "Emergency": "Emergencia",
            "Prescription": "Receta"
        },
        "Academic Language": {
            "Research": "Investigación",
            "Thesis": "Tesis",
            "Analysis": "Análisis",
            "Theory": "Teoría"
        }
    }
}

def main():
    st.title("¡Aprende Español!")
    
    # Level selection in sidebar
    level = st.sidebar.radio(
        "Choose your level:",
        ["Beginner", "Intermediate", "Advanced"]
    )
    
    # Show level description
    level_descriptions = {
        "Beginner": "Start your Spanish journey with basic vocabulary and phrases",
        "Intermediate": "Expand your knowledge with everyday conversations and grammar",
        "Advanced": "Master complex topics and specialized vocabulary"
    }
    
    st.markdown(f"""
        <div class="level-section">
            <h2>{level}</h2>
            <p>{level_descriptions[level]}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Lesson selection for the chosen level
    lesson_name = st.selectbox(
        "Choose a lesson:",
        list(lessons[level].keys())
    )
    
    # Show selected lesson
    show_lesson(level, lesson_name)

def show_lesson(level, lesson_name):
    st.header(lesson_name)
    
    # Get vocabulary for the selected lesson
    vocabulary = lessons[level][lesson_name]
    
    # Show vocabulary cards
    for english, spanish in vocabulary.items():
        st.markdown(f"""
            <div class="lesson-card">
                <h3>{english}</h3>
                <p style="font-size: 24px; color: #483D8B;">{spanish}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Practice section
        user_answer = st.text_input(f"How do you say '{english}' in Spanish?", key=f"{level}_{lesson_name}_{english}")
        if user_answer.lower() == spanish.lower():
            st.success("¡Correcto! (Correct!)")
        elif user_answer:
            st.error("Try again!")

if __name__ == "__main__":
    main() 