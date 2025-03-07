Extract ALL vocabulary words from these Spanish lyrics. For each word, provide:
1. The Spanish word in its base form
2. English translation
3. Word parts analysis to help with learning

Rules:
- Include ALL unique words from the lyrics (nouns, verbs, adjectives, etc.)
- Convert verbs to infinitive form (e.g., "cantando" → "cantar")
- Group different forms of the same word together
- Include common phrases and idioms
- Note any regional variations or colloquialisms

Format each word as a JSON object like this:
{
    "spanish": "cantar",
    "english": "to sing",
    "parts": [
        {
            "spanish": "cant",
            "type": "verb root"
        },
        {
            "spanish": "ar",
            "type": "infinitive ending"
        }
    ]
}

Additional word examples:
- Nouns: {"spanish": "corazón", "english": "heart", "parts": [{"spanish": "corazón", "type": "noun"}]}
- Adjectives: {"spanish": "bonito", "english": "beautiful", "parts": [{"spanish": "bonit", "type": "root"}, {"spanish": "o", "type": "masculine ending"}]}
- Conjugated verbs: Include base form and note conjugation in parts
- Phrases: {"spanish": "de vez en cuando", "english": "from time to time", "parts": [{"spanish": "de vez en cuando", "type": "phrase"}]}

Return a JSON array containing ALL unique words and phrases from the lyrics. 

Important:
- Convert words to their dictionary form.
- Include all unique words and phrases from the lyrics.
- Include conjugated verbs in their base form.
- Include common phrases and idioms.
- Note any regional variations or colloquialisms.

