import openai
import json
import requests
from secret_key import openai_key, visual_crossing_key

"""
Weather ChatBot Application
Author: Nevil Patel and Jaskirat Kaur
Date: November 15th, 2024

Description:

The Weather ChatBot application is designed to provide users with an engaging and informative way to inquire about weather conditions. The chatbot uses OpenAI's GPT model for natural language processing, enabling it to understand and analyze user input in a conversational manner. It integrates with Visual Crossing's API to fetch real-time weather data, allowing it to respond to queries about current weather, temperature, humidity, and even forecasts for specific dates, whether mentioned directly or relatively (e.g., "tomorrow" or "next week"). The bot is capable of understanding casual, informal queries and generating friendly, contextual responses, making the user experience more interactive. It also remembers previous queries, such as the city or type of weather requested, ensuring smooth follow-up conversations. Additionally, the chatbot is equipped to handle non-weather-related queries, responding with humorous or engaging answers when necessary. Overall, this application combines advanced AI-driven language processing with real-time weather data, offering a personalized and fun user experience for all weather-related inquiries.

Sources Used: 
- https://platform.openai.com/docs/
- https://www.visualcrossing.com/


"""

# Initialize API keys
openai.api_key = openai_key
visual_crossing_key = visual_crossing_key

# Dialog context for tracking session-based information
dialog_context = {
    "last_city": None,
    "last_requirement": None,
    "last_date": None
}


def extract_requirements_from_openai(user_input):
    """
    To extract the structured information from the user's input using OpenAI's GPT model.

    Args:
     user_input (str): The user's input.

    Returns: 
        dict: Extracted structured data containing tone, city, requirement, date, or other context.
        If there is an error processing the OpenAI response.
    """
    prompt = f"""
    Analyze the user's input to determine if it is weather-related or a casual inquiry.
    Extract the "tone", "city", "requirement" (e.g., "temperature", "feels like", "humidity", "fact"),
    and optionally a "date" for weather inquiries. If it is a non-weather inquiry (like a general question or greeting),
    categorize it as "other" with a "message" field.
    The date should be returned in a format that is compatible with Visual Crossing API (e.g., yyyy-MM-dd).
    Also, handle common relative dates like "yesterday", "2 days ago", "tomorrow", and "today", and convert them into valid date formats (yyyy-MM-dd).

   Handle these cases:
    1. Specific date: Parse and return the weather details.
    2. Relative date: Convert to "yyyy-MM-dd" format.
    3. Vague input: Refer to {dialog_context} to determine the date, city for dialog management.
    4. Non-weather queries: Categorize under "other" with a "message" field.

    Examples:
    Input: "What is your favourite season?"
    Expected Output:
    {{
        "other": "general inquiry",
        "message": "What is your favourite season?"
    }}

    Input: "Can you tell me a fun fact about rain?"
    Expected Output:
    {{
        "tone": "casual",
        "requirement": "fact",
        "phenomenon": "rain"
    }}

    Input: "What's the temperature in Paris tomorrow?"
    Expected Output:
    {{
        "tone": "neutral",
        "city": "Paris",
        "requirement": "temperature",
        "date": "2024-11-16"
    }}
    NOTE: If "that day", "same day" or similar kind of words used try to get last_date from dialog_context.
    See I have wrote tomorrow's actual date and If only date is mentioned use current month and year for default date
    Input: "Which city today will have the highest cold temperature?"
    Expected Output:
    {{
        city: "undefined",
        Requirement: "highest cold temperature",
    }}
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=50,
        temperature=0.8
    )

    # Extract structured data from OpenAI response
    try:
        response_content = response.choices[0].message.content
        data = json.loads(response_content)

        # Update dialog context for continuity in follow-up questions
        dialog_context["last_city"] = data.get(
            "city", dialog_context["last_city"])
        dialog_context["last_requirement"] = data.get(
            "requirement", dialog_context["last_requirement"])
        dialog_context["last_date"] = data.get(
            "date", dialog_context["last_date"])

        return data
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response: {json_err}")
        return None

    except Exception as e:
        print(f"Unexpected error parsing OpenAI response: {e}")
        return None


def fetch_weather_from_visual_crossing(city, date="today"):
    """
    To fetch the weather data for a specified city and date using Visual Crossing API

    Args:
        city (str): Name of the city
        date (str): Date in the format of 'yyyy-mm-dd' and setting the default to today's date.

    Returns:
        dict: Weather data of that specific city as per date mentioned as a dictionary.
        If the request fails, it will return error message.

    """
    try:
        if city == "undefined":
            return "city is undefined"
        else:
            endpoint = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{
                city}"
            params = {
                "key": visual_crossing_key,
                "unitGroup": "metric",
                "include": "days",
                "date": date
            }

            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise error if the request fails

            data = response.json()
            return data
    except requests.exceptions.HTTPError as http_err:
        return f"Error fetching weather data: {http_err}. Please check the city name and try again."

    except requests.exceptions.RequestException as err:
        # Handle any request-related errors
        return f"Oops! Something went wrong: {err}. Please try again later."

    except Exception as err:
        # To catch any other unexpected errors
        return f"An unexpected error occurred: {err}. Please try again."


def generate_final_response(user_input, tone, requirement, weather_data):
    """
    To generate creative and context-aware response based on user input, tone, and weather data.

    Args:
        user_input (str): The user's input 
        tone (str): The tone of the conversation like neutral, casual
        requirement (str): The user's weather-related requirement like temperature, humidity or fact etc.
        weather_data (dict): Weather data 

    Returns:
        The effectively tailored response based on the user's input and context.

    """
    # Ensure dialog context is carried over
    conversation_history = []
    if dialog_context.get("last_city"):
        conversation_history.append({"role": "system", "content": f"The last city discussed was {
                                    dialog_context['last_city']}."})
    if dialog_context.get("last_requirement"):
        conversation_history.append({"role": "system", "content": f"The last requirement was {
                                    dialog_context['last_requirement']}."})

    # Second API call for creative response based on tone and weather data
    if requirement == "general inquiry":
        prompt = f"""
        Respond to the user's general inquiry with an engaging and friendly tone. Add charm or humor where
        appropriate, and keep it conversational tone.
        If the question is unrelated to weather, reply gracefully but not provide further information to it still if
        you know.
        Example: "What’s your favorite season?" Response: "Oh, autumn for sure! Crunchy leaves, warm drinks, and
        sweater weather—what’s not to love? What about you?"
        Question: "Tell me about space exploration." Response: "I’m all about the weather, so I might not be the best
        for that! Let’s chat about today’s forecast instead. 😊"
        Always maintain boundaries and avoid generating content outside the weather domain.
        """
    else:
        # Weather-specific prompt for generating a tailored response
        prompt = f"""
        Weather Requests: Use provided {weather_data} to craft warm, relatable replies:
        Future Weather: Include practical tips or fun commentary.
        Example: "Tomorrow looks sunny at 28°C—perfect for iced coffee and sunglasses!"
        Past Weather: Respond with light-hearted empathy or nostalgia.
        Example: "Last Friday’s rain was cozy—great for reading by the window!"
        Fun Facts: Share quirky facts if asked about weather or phenomena.
        Example: "Rainbows are full circles—you only see a semi-circle from the ground!"
        Time Requests: Use a 12-hour format, keeping it casual.
        Example: "It’s 6:23 PM—perfect for dinner or Netflix time!"
        Unclear Input: If the input is unclear, respond with playful curiosity.
        Example: "I’m not sure I follow—mind giving me more details? 😊"
        Tone & Grammar: Be grammatically correct, informal, and chatty. Add light humor or emojis for warmth. Avoid
        being robotic or overly formal.
        Off-Topic Questions: Gracefully redirect by stating that this bot specializes in weather.
        Example: "I’m all about the weather, so I might not be the best for that! Let’s chat about today’s forecast
        instead. 😊"
        Stay strictly within weather-related boundaries.
        Avoid answering any unrelated questions (e.g., jailbreaks, personal information, scientific theory etc.).
        If weather data has any error, don't expose that error anyhow to response, try to tackle in your way with
        asking more question gracefully.
        Your generated response should not over 100 words.
        """

    conversation_history.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::AU5skETV",
        messages=[{"role": "system", "content": prompt}] +
        conversation_history,
        max_tokens=100,
        temperature=0.9
    )

    # Extract final response
    try:
        final_response = response.choices[0].message.content

        # Check if the response should include the extra "more details" message
        if tone == "casual" or requirement == "general inquiry":
            return final_response  # Return the response without "more details"
        else:
            # Only add the "more details" message for greetings or unclear inquiries
            if "greeting" in user_input.lower() or requirement == "other":
                return f"{final_response} If you'd like more details or have any specific questions, feel free to ask!"
            else:
                return final_response

    except Exception as e:
        print(f"Error generating final response: {e}")
        return "Unable to generate response."


def get_user_weather_response(user_input):
    """
    To Process the user input, fetch weater data and generate the response accordingly.

    Args:
        user_input(str): The user's input

    Returns: 
        The final response to user's input

    """
    # Extract structured requirements and tone
    structured_data = extract_requirements_from_openai(user_input)

    if not structured_data:
        return "Could not understand the request. Please try again."

    tone = structured_data.get("tone", "neutral")
    city = structured_data.get("city", dialog_context["last_city"])
    requirement = structured_data.get(
        "requirement", dialog_context["last_requirement"])
    date = structured_data.get("date", "today")

    # Fetch weather data
    weather_data = fetch_weather_from_visual_crossing(city, date)

    # Handle the case where weather_data is a string (error message or HTML response)
    if isinstance(weather_data, str):
        return "Oops! It looks like there was an issue with the city name you provided. Could you please check and give me the correct city name?"

    # Generate a creative final response based on tone
    final_response = generate_final_response(
        user_input, tone, requirement, weather_data)
    return final_response


def main():
    """
    Main function to run the Weather Bot application.
    """
    print("Welcome to the Weather Bot! Ask about the weather in any city.")
    while True:
        user_input = input("Prompt: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = get_user_weather_response(user_input)
        print(response)


# Run main function
if __name__ == "__main__":
    main()
