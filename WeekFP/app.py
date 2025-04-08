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
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("¡Aprende Español!")
    
    # Basic lesson selection
    lesson = st.sidebar.radio(
        "Choose a lesson:",
        ["Greetings", "Numbers", "Colors"]
    )
    
    if lesson == "Greetings":
        show_greetings()
    elif lesson == "Numbers":
        show_numbers()
    elif lesson == "Colors":
        show_colors()

def show_greetings():
    st.header("Basic Greetings")
    
    greetings = {
        "Hello": "Hola",
        "Good morning": "Buenos días",
        "Good afternoon": "Buenas tardes",
        "Good evening": "Buenas noches",
        "Goodbye": "Adiós",
        "Please": "Por favor",
        "Thank you": "Gracias"
    }
    
    for english, spanish in greetings.items():
        st.markdown(f"""
            <div class="lesson-card">
                <h3>{english}</h3>
                <p style="font-size: 24px; color: #483D8B;">{spanish}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Practice section
        user_answer = st.text_input(f"How do you say '{english}' in Spanish?", key=english)
        if user_answer.lower() == spanish.lower():
            st.success("¡Correcto! (Correct!)")
        elif user_answer:
            st.error("Try again!")

def show_numbers():
    st.header("Numbers 1-10")
    
    numbers = {
        "One": "Uno",
        "Two": "Dos",
        "Three": "Tres",
        "Four": "Cuatro",
        "Five": "Cinco",
        "Six": "Seis",
        "Seven": "Siete",
        "Eight": "Ocho",
        "Nine": "Nueve",
        "Ten": "Diez"
    }
    
    for english, spanish in numbers.items():
        st.markdown(f"""
            <div class="lesson-card">
                <h3>{english}</h3>
                <p style="font-size: 24px; color: #483D8B;">{spanish}</p>
            </div>
        """, unsafe_allow_html=True)

def show_colors():
    st.header("Basic Colors")
    
    colors = {
        "Red": "Rojo",
        "Blue": "Azul",
        "Green": "Verde",
        "Yellow": "Amarillo",
        "Black": "Negro",
        "White": "Blanco",
        "Purple": "Morado",
        "Orange": "Naranja"
    }
    
    for english, spanish in colors.items():
        st.markdown(f"""
            <div class="lesson-card">
                <h3>{english}</h3>
                <p style="font-size: 24px; color: #483D8B;">{spanish}</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 