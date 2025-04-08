# Technical Specs

## Initialization steps
When the app first initiallizes it needs to have do the following:
- Fetch from the GEt localhost:5000/api/groups/:id/raw, this will return a collection of words in a JSON structure. It will have Spanish words and the English translation. We need to store this collection of words in memory.

## Page States
Page states describes the state the single page application should behave from, a user's perpective.

### Setup State
- When a user first start up the app they will only see a button to "Generate Sentence". Which when pressed will generate a sentence using the Sentence Generator LLM. The state will change to the Practice State.

### Practice State
- When in the Practice State the user will see an English sentence and a Spanish sentence. The will see an upload field under the English sentence. They will see a button for "Submit for Review". when they press this "Submit for Review" button an uploaded image it will be passed to the Grading System and the state will trransition into the Review State. 


## Review State
When a user is in the Review State the user will see the English sentence. The upload field will be gone. The user will now see a review oof the output from the Grading System:
- Transcription of the Image
- Translation of the Image
- Grading
    - a score using the 0 to 10 grading scale
    - a description of whether the attempt was correct or incorrect
Theere will be a button called "Next Question" which will generate a new sentence and take the user back to the Practice State.

## Sentence Generator LLM Prompt
Generate a sentence using the following word: {{word}}
The grammar should be scoped to Soanish A1 grammar
You can use the following vocabulary to construct a simple sentence:
- simple objects eg. book, car, taco, house
- simple verbs eg. to eat, to play, to sleep
- simple times eg. yesterday, tomorrow, next week

## Grading SYtem 
The Grading System will do the following:
- It will transcribe the image using MangoOCR
- It will use an LLM to produce a literal translation of the transcription
- It will use another LLM to produce a grade
- It then returns this data to the frontend app