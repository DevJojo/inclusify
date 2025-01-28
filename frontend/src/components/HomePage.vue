<template>
  <div class="container">
    

    <h1>Challenge your prompt</h1>
    
    <textarea 
      v-model="inputText" 
      placeholder="Enter your text here..." 
      rows="10" 
      class="input-field"
    ></textarea>

    <button class="analyze-button" @click="analyzeMyText">Analyze</button>

    <div v-if="loading" class="overlay">
      <div class="spinner"></div> 
    </div>
    <div v-else>
      <div v-if="analyzedText" class="result-container">
        <h2>Analyzed Text:</h2>
        <div v-html="highlightedText" class="highlighted-text"></div> 
      </div>

      <div v-if="correctedText" class="result-container">
        <h2>Corrected Text:</h2>
        <div v-html="correctedText" class="corrected-text"></div> 
      </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputText: '',
      analyzedText: '',
      correctedText: '',
      loading: false,
    };
  },
  methods: {
    async analyzeMyText() {
      this.loading = true;
      try {
       
        // 1. Construct the prompt for the Gemini API
        const API_KEY = '1236'
        const prompt = this.inputText
        this.analyzeText = this.inputText

        // 2. Send the prompt to the Gemini API
        const response = await axios.post('http://127.0.0.1:5000/claude/analyze', { prompt: prompt }, {
          headers: { 
            'Content-Type': 'application/json',
            'x-api-key': API_KEY }
        })

        console.log(response.data)
        const analyzedResult = response.data; 

        // 3. Highlight problematic areas in the original text
        this.highlightBias(this.inputText, analyzedResult.biased_parts);
        // 4. Get the corrected text from the response
        this.correctedText = analyzedResult.corrected_text;

      } catch (error) {
        this.loading = false
        console.error('Error analyzing text:', error);
        this.analyzedText = 'Error analyzing text.';
      } finally {
        this.loading = false; 
      }
    },
    highlightBias(text, keywords) {
      let highlightedText = text;

      keywords.forEach(keyword => {
        const regex = new RegExp(`(${keyword})`, 'gi'); 
        highlightedText = highlightedText.replace(regex, `<span style="color: red;">$1</span>`);
      });

      this.highlightedText = highlightedText;
      this.analyzedText = highlightedText;
    },
  },
};
</script>

<style>
.container {
  max-width: 80%;
  margin: 0 auto;
  padding: 20px;
}

.input-field {
  font-size: 10pt;
  width: 80%; 
  margin-bottom: 10px; 
  padding: 10px;
}

.analyze-button {
  width: 80%; 
  padding: 10px;
}

.result-container {
  background-color: #f0f0f0; 
  margin: auto 10%;
  padding: 20px;
  margin-top: 20px;
}

.highlighted-text {
  white-space: pre-wrap; 
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent gray */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure it's on top */
}

.spinner {
  border: 4px solid #f3f3f3; 
  border-top: 4px solid #3498db; 
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>