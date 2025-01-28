from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from flask import Flask, request, jsonify, make_response
import json

# Replace with your actual Anthropic API key
CLAUDE_API_KEY = ""
BACKEND_API_KEY = "1236"

# Configure LangChain LLM (Claude)
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=CLAUDE_API_KEY) 

mockResponseData = {'biased_parts': ['assertive', 'strong negotiator', 'competitive drive'], 'corrected_text': 'We are seeking a highly motivated and results-oriented Sales Manager to lead our team. The ideal candidate will possess excellent negotiation skills and a drive to achieve targets.'}

def analyze_text(text):
#    """Analyzes the provided text for gender bias using LangChain and HumanMessage"""
    context_prompt = """I am an AI assistant designed to help users identify and correct gender bias in text. 
    I will analyze the provided text and:

    1. **Identify any words, phrases, or stereotypes that may unfairly favor one gender over another.** 
       - This includes but is not limited to:
         - **Stereotypical language:** Words or phrases that reinforce harmful stereotypes about men or women (e.g., "aggressive," "decisive" for men; "nurturing," "collaborative" for women).
         - **Unnecessary gendered language:** Using "he/him" or "she/her" when referring to a person of unspecified gender. 
         - **Job requirements that may disproportionately exclude one gender:** For example, requiring extensive travel or long working hours, which may disproportionately impact women with caregiving responsibilities.

    2. **Mark the potentially biased parts of the text.**

    3. **Suggest a corrected version of the text that is free from gender bias, while maintaining the original intent and meaning.**

    I will provide the following in my response:
    * **biased_parts:** A list of the identified biased parts of the text.
    * **corrected_text:** The corrected version of the text.

    **Example:**

    **Biased Text:** 
    We are seeking a highly motivated and assertive Sales Manager to lead our team. The ideal candidate will be a strong negotiator with a competitive drive.

    **Corrected Text:**
    We are seeking a highly motivated and results-oriented Sales Manager to lead our team. The ideal candidate will possess strong communication, negotiation, and interpersonal skills. They will be a collaborative team player with a focus on achieving sales targets. 
    
    I will strive to be objective, unbiased, and inclusive in my analysis and suggestions.
    Please answer in a JSON format only and dont add any words.
    """

    human_message = HumanMessage(content=context_prompt + "Analyze the following text for gender bias:" + text)
    response = llm.invoke([human_message])
    #print(response.content)
    return json.loads(response.content)

def validate_api_key(api_key):
    """
    Validates the provided API key.

    Args:
        api_key (str): The API key to validate.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    # Replace with your actual API key validation logic
    valid_api_keys = [BACKEND_API_KEY] 
    return api_key in valid_api_keys

def create_http_response(data):
    response = data
    response.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
    response.headers['Access-Control-Allow-Methods'] = "POST, OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, x-api-key"

    return response


app = Flask(__name__)

@app.route("/claude/analyze", methods=["POST", "OPTIONS"])
def analyze_bias():
    

    if request.method == 'OPTIONS':
        print('request.method == OPTIONS')
        # Handle CORS preflight request
        response = create_http_response(jsonify({'message': 'CORS preflight successful'}))
         
        return response, 200
    
    """
    Endpoint that requires a valid API key.
    """
    api_key = request.headers.get('x-api-key')
    if not api_key or not validate_api_key(api_key):
        return create_http_response(jsonify({'error': 'Invalid API key'})), 401
    

    try:
        print(request.get_json())
        data = request.get_json()
        text = data["prompt"]
       # text = "We are seeking a highly motivated and assertive Sales Manager to lead our team. The ideal candidate will be a strong negotiator with a competitive drive."
        analysis_result = analyze_text(text)
  #      print(analysis_result)

     #   response = create_http_response(jsonify(mockResponseData))
        response = create_http_response(jsonify(analysis_result))

        return response, 200
    
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return jsonify({"error": "Error analyzing text"}), 500

if __name__ == "__main__":
    app.run(debug=True)