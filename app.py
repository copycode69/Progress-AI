from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
import logging
from dotenv import load_dotenv  


load_dotenv()

app = Flask(__name__)
CORS(app)  
logging.basicConfig(level=logging.DEBUG)


API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    logging.debug(f'Received input: {user_input}')
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": user_input})
        response.raise_for_status()  

      
        api_response = response.json()
        logging.debug(f'API Response: {api_response}')

        
        reply = api_response[0].get('generated_text', 'Sorry, something went wrong.')
        
        
        if reply == 'Sorry, something went wrong.':
            logging.error('Generated text not found in response')
        
    except requests.exceptions.RequestException as e:
        logging.error(f'Error: {e}')
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
