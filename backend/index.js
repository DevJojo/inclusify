const express = require('express');
//const { functionsFramework, CloudFunctions } = require('@google-cloud/functions-framework');
const app = express();
const { Gemini } = require('gemini-ai'); 
//import Gemini from "gemini-ai";


const gemini = new Gemini({
  apiKey: 'YOUR_GEMINI_API_KEY', 
});

const contextPrompt = `
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
`;

app.use(express.json());

app.post('/api/analyze', async (req, res) => {

    try {
        // Mock Response in JSON format
        const mockResponse = {
          biased_parts: [
            { start: 15, end: 24 }, // Example: "assertive Sales"
            { start: 50, end: 62 }  // Example: "competitive drive"
          ],
          corrected_text: "We are seeking a highly motivated and results-oriented Sales Manager to lead our team. The ideal candidate will be a strong negotiator with excellent interpersonal and communication skills."
        }
        
        res.json(mockResponse);

    }catch (error) {
        console.error('Error analyzing text:', error);
        res.status(500).send('Error analyzing text.');
    };
    
  /**  
  try {
    const { text } = req.body; 
    const fullPrompt = contextPrompt + `\n\nAnalyze the following text for gender bias:\n\n${text}`;
    const response = await gemini.generateText(fullPrompt); 
    const analyzedResult = JSON.parse(response.text); 
    res.json(analyzedResult);
  } catch (error) {
    console.error('Error analyzing text:', error);
    res.status(500).send('Error analyzing text.');
  }
     */
});


app.post('/api/correct', async (req, res) => {
  try {
    const { text } = req.body;
    const correctedText = await Gemini.correctText(text); 
    res.json({ corrected_text: correctedText });
  } catch (error) {
    console.error('Error correcting text:', error);
    res.status(500).send('Error correcting text.');
  }
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});