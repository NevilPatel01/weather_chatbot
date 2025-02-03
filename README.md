# Weather ChatBot Application 🌦️

---

## 📜 **Description**
The Weather ChatBot is an engaging and intelligent assistant designed to provide real-time weather updates and fun interactions. Powered by OpenAI's GPT and Visual Crossing's Weather API, this chatbot handles weather-related queries with ease and adds a conversational charm to your interactions. From casual queries like "What's the weather tomorrow in Paris?" to fun facts about rain, the bot is equipped to deliver!

### Features
- 🌡️ Real-time weather updates for cities worldwide.
- 📅 Handles specific and relative date queries (e.g., "tomorrow," "next week").
- 🎭 Casual tone with friendly and engaging responses.
- 🔗 Contextual memory to track conversations and maintain continuity.
- 🤓 Fun facts and playful interactions.
- 🚫 Graceful handling of off-topic queries.
- 🛠️ API integration with Visual Crossing for reliable weather data.

---

## 🛠️ **Tech Stack**
- **Language:** Python  
- **APIs:**  
  - OpenAI GPT for natural language processing.  
  - Visual Crossing Weather API for real-time and forecast data.

---

## ⚙️ **Setup & Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/NevilPatel01/weather_chatbot.git
   ```
2. Install required dependencies:
    ```bash
    ```
3.  Configure your API keys:
- Create a `secret_key.py` file and add your OpenAI and Visual Crossing API keys:
    ```bash
    openai_key = "YOUR_OPENAI_API_KEY"
    visual_crossing_key = "YOUR_VISUAL_CROSSING_API_KEY"
    ```
4. Run the bot:
    ```bash
    python weather_chatbot.py
    ```

## 🗺️ API Usage

### OpenAI GPT
- Utilized to process user input, extract context, and generate a natural language response.

### Visual Crossing
Used to fetch:
- Current weather conditions.
- Weather forecasts for specific or relative dates.
- Additional metrics like temperature, humidity, and more.

## 🛡️ Error Handling
- Gracefully handles invalid city names and API errors.
- Ensures follow-up interactions are managed smoothly with contextual memory.
- Redirects off-topic queries to keep the conversation relevant to weather.

## 📢 Acknowledgments
- Feel free to contribute and make this chatbot even more awesome! 💡
