from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import sys
import json

# Setup logging to both file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Mock data for testing
MOCK_VOCABULARY = {
    "1": {
        "group_name": "Basic Spanish Words",
        "words": [
            {"spanish": "casa", "english": "house"},
            {"spanish": "perro", "english": "dog"},
            {"spanish": "gato", "english": "cat"},
            {"spanish": "libro", "english": "book"},
            {"spanish": "agua", "english": "water"},
            {"spanish": "comida", "english": "food"},
            {"spanish": "coche", "english": "car"},
            {"spanish": "mesa", "english": "table"},
            {"spanish": "silla", "english": "chair"},
            {"spanish": "teléfono", "english": "phone"},
            {"spanish": "computadora", "english": "computer"},
            {"spanish": "lápiz", "english": "pencil"},
            {"spanish": "ventana", "english": "window"},
            {"spanish": "puerta", "english": "door"},
            {"spanish": "escuela", "english": "school"}
        ]
    },
    "2": {
        "group_name": "Food and Drinks",
        "words": [
            {"spanish": "manzana", "english": "apple"},
            {"spanish": "pan", "english": "bread"},
            {"spanish": "leche", "english": "milk"},
            {"spanish": "café", "english": "coffee"},
            {"spanish": "jugo", "english": "juice"},
            {"spanish": "arroz", "english": "rice"},
            {"spanish": "pollo", "english": "chicken"},
            {"spanish": "carne", "english": "meat"},
            {"spanish": "pescado", "english": "fish"},
            {"spanish": "sopa", "english": "soup"}
        ]
    },
    "3": {
        "group_name": "Animals",
        "words": [
            {"spanish": "perro", "english": "dog"},
            {"spanish": "gato", "english": "cat"},
            {"spanish": "pájaro", "english": "bird"},
            {"spanish": "pez", "english": "fish"},
            {"spanish": "conejo", "english": "rabbit"},
            {"spanish": "caballo", "english": "horse"},
            {"spanish": "vaca", "english": "cow"},
            {"spanish": "cerdo", "english": "pig"},
            {"spanish": "ratón", "english": "mouse"},
            {"spanish": "león", "english": "lion"}
        ]
    },
    "4": {
        "group_name": "Colors",
        "words": [
            {"spanish": "rojo", "english": "red"},
            {"spanish": "azul", "english": "blue"},
            {"spanish": "verde", "english": "green"},
            {"spanish": "amarillo", "english": "yellow"},
            {"spanish": "negro", "english": "black"},
            {"spanish": "blanco", "english": "white"},
            {"spanish": "gris", "english": "gray"},
            {"spanish": "marrón", "english": "brown"},
            {"spanish": "morado", "english": "purple"},
            {"spanish": "rosa", "english": "pink"}
        ]
    }
}

@app.route('/api/groups/<group_id>/words/raw')
def get_group_words(group_id):
    logger.info(f"Received request for group_id: {group_id}")
    logger.debug(f"Request headers: {dict(request.headers)}")
    
    try:
        if group_id in MOCK_VOCABULARY:
            data = MOCK_VOCABULARY[group_id]
            # Verify the data is valid JSON
            json.dumps(data)  # This will raise an error if data is not JSON serializable
            logger.info(f"Returning data for group: {data['group_name']}")
            logger.debug(f"Response data: {data}")
            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        logger.warning(f"Group ID not found: {group_id}")
        return jsonify({"error": "Group not found"}), 404
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/groups')
def list_groups():
    """Return a list of all available vocabulary groups"""
    groups = []
    for group_id, data in MOCK_VOCABULARY.items():
        groups.append({
            "id": group_id,
            "name": data["group_name"],
            "word_count": len(data["words"])
        })
    return jsonify({"groups": groups})

@app.route('/')
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    logger.info("Starting API server...")
    logger.info("Available endpoints:")
    logger.info("  - GET /api/groups/<group_id>/words/raw")
    logger.info("  - GET /api/groups")
    logger.info("  - GET / (health check)")
    app.run(host='0.0.0.0', port=5001, debug=True) 