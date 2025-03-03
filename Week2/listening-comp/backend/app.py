vector_store = QuestionVectorStore()

# Load questions from your text files
questions = load_questions_from_files()  # You'll need to implement this
vector_store.create_vector_store(questions)

# When you need to find similar questions
similar_questions = vector_store.find_similar_questions("Where is the restroom?") 