<template>
  <div class="container">
    <h1>Inclusify</h1>
    <textarea 
      v-model="inputText" 
      placeholder="Enter your text here..." 
      rows="10"
    ></textarea>

    <button @click="analyzeText">Analyze</button>

    <div v-if="analyzedText">
      <h2>Analyzed Text:</h2>
      <div v-html="highlightedText"></div> 
    </div>

    <div v-if="correctedText">
      <h2>Corrected Text:</h2>
      <textarea 
        v-model="correctedText" 
        rows="10"
        readonly
      ></textarea>
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
    };
  },
  methods: {
    async analyzeText() {
      try {
        // 1. Send the text to Gemini API for analysis
        const response = await axios.post('/api/analyze', { text: this.inputText }); 
        const analyzedResult = response.data; 

        // 2. Highlight problematic areas in the original text
        this.analyzedText = this.highlightBias(this.inputText, analyzedResult.bias_locations);

        // 3. Get the corrected text from Gemini API
        const correctResponse = await axios.post('/api/correct', { text: this.inputText });
        this.correctedText = correctResponse.data.corrected_text;

      } catch (error) {
        console.error('Error analyzing text:', error);
        this.analyzedText = 'Error analyzing text.';
      }
    },
    highlightBias(text, biasLocations) {
      let highlightedText = '';
      let lastIndex = 0;

      biasLocations.forEach((location) => {
        highlightedText += text.substring(lastIndex, location.start);
        highlightedText += `<span style="color:red;">${text.substring(location.start, location.end)}</span>`;
        lastIndex = location.end;
      });

      highlightedText += text.substring(lastIndex);
      return highlightedText;
    },
  },
};
</script>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>