from langchain.llms import GoogleGenerativeAI
from flask import Flask, request, jsonify

# Replace with your actual API key
API_KEY = "YOUR_GEMINI_API_KEY"

# Configure LangChain LLM
llm = GoogleGenerativeAI(api_key=API_KEY, model_name="gemini-1.5-flash")

def analyze_text(text):
    """Analyzes the provided text for gender bias using LangChain"""
    context_prompt = """
    I am an AI assistant designed to help users identify and correct gender bias in text. 
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
    """

    full_prompt = context_prompt + "\n\nAnalyze the following text for gender bias:\n\n" + text
    response = llm(full_prompt)
    return json.loads(response)

def correct_text(text):
    """Corrects the provided text for gender bias using LangChain"""
    response = llm(f"Correct the following text for gender bias: {text}")
    return response

app = Flask(__name__)

@app.route("/api/analyze", methods=["POST"])
def analyze_bias():
    try:
        data = request.get_json()
        text = data["text"]
        analysis_result = analyze_text(text)
        
        response = jsonify(analysis_result)
        response.headers()
        return response
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return jsonify({"error": "Error analyzing text"}), 500

@app.route("/api/correct", methods=["POST"])
def correct_bias():
    try:
        data = request.get_json()
        text = data["text"]
        corrected_text = correct_text(text)
        return jsonify({"corrected_text": corrected_text})
    except Exception as e:
        print(f"Error correcting text: {e}")
        return jsonify({"error": "Error correcting text"}), 500

if __name__ == "__main__":
    app.run(debug=True)