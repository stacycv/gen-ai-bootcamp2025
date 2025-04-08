import streamlit as st

# Basic page setup
st.set_page_config(
    page_title="¡Hola Español!",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Reset and main styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background-color: #1a2b4e;  /* Navy background */
    }
    
    /* Header styles */
    .landing-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        background-color: white;
        width: 100%;
        margin-bottom: 100px;  /* Add space between header and hero section */
    }
    
    .logo {
        color: #1a2b4e;
        font-size: 32px;
        font-weight: bold;
    }
    
    .logo span {
        color: #e94747;
    }
    
    .nav-links {
        display: flex;
        gap: 40px;
        margin-left: auto;
        margin-right: 40px;
    }
    
    .nav-link {
        color: #1a2b4e;
        text-decoration: none;
        font-size: 18px;
        font-weight: 500;
    }
    
    .signup-btn {
        background-color: #e94747;
        color: white;
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 500;
        font-size: 18px;
    }
    
    /* Hero section styles */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 72px;
        font-weight: bold;
        color: white;
        margin-bottom: 40px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 24px;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 60px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }
    
    .cta-buttons {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 40px;
    }
    
    .cta-primary {
        background-color: #e94747;
        color: white;
        padding: 16px 40px;
        border-radius: 50px;
        text-decoration: none;
        font-size: 20px;
        font-weight: 500;
        transition: background-color 0.3s;
    }
    
    .cta-secondary {
        background-color: transparent;
        color: white;
        padding: 16px 40px;
        border-radius: 50px;
        border: 2px solid white;
        text-decoration: none;
        font-size: 20px;
        font-weight: 500;
    }

    /* Hide Streamlit elements */
    .stButton, footer, header {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

# Landing page
if st.session_state.show_welcome:
    # Header
    st.markdown("""
        <div class="landing-header">
            <div class="logo">¡Hola <span>Español!</span></div>
            <div class="nav-links">
                <a href="#" class="nav-link">Home</a>
                <a href="#" class="nav-link">Beginner</a>
                <a href="#" class="nav-link">Intermediate</a>
                <a href="#" class="nav-link">Expert</a>
            </div>
            <a href="#" class="signup-btn">Sign Up</a>
        </div>
        
        <div class="hero-section">
            <h1 class="hero-title">Learn Spanish the Natural Way</h1>
            <p class="hero-subtitle">¡Hola Español! makes learning Spanish fun, interactive, and effective with lessons tailored to your skill level.</p>
            <div class="cta-buttons">
                <a href="#" class="cta-primary" onclick="handleStart()">Start as Beginner</a>
                <a href="#" class="cta-secondary" onclick="handleTest()">Take Placement Test</a>
            </div>
        </div>
        
        <script>
            function handleStart() {
                window.location.href = '#start';
            }
            
            function handleTest() {
                window.location.href = '#test';
            }
        </script>
    """, unsafe_allow_html=True)
    
    # Hidden buttons to handle navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start as Beginner", key="start_btn"):
            st.session_state.show_welcome = False
            st.session_state.level = "Beginner"
            st.experimental_rerun()
    with col2:
        if st.button("Take Placement Test", key="test_btn"):
            st.session_state.show_welcome = False
            st.session_state.show_test = True
            st.experimental_rerun()

# Rest of your app code goes here (when show_welcome is False)
else:
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