import discord
from chatbot import get_user_weather_response

"""
Weather Chatot for Discord
Author: Jaskirat Kaur and Neil Patel
Date: November 15th,2024
Description:
This weather discord chatbot provides the weather updates based on the user input. The bot responds to greetings,farewells ,and queries about the weather in various cities. It interacts with user through messages and fetches weather information using the chatbot module.If the user asks any question out of weather information scope, it will responds accordingly.


"""



class MyClient(discord.Client):
    """A Discord bot client for providing weather information."""

    def __init__(self):
        """Constructor: Sets up the bot's intents."""
        intents = discord.Intents.default()
        intents.message_content = True  # Enable the bot to read message content
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot successfully logs in."""
        print(f'Logged in as {self.user}')
        print('Ready to provide weather updates!')

    async def on_message(self, message):
        """
        Called when the bot receives a message.
        The message object contains the message's details.
        """
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Check if the bot is tagged (mentioned)
        if self.user.mentioned_in(message):
            # Predefined responses for greetings and farewells
            greetings = ['hello', 'hi', 'hey']
            goodbyes = ['goodbye', 'bye']

            # Preprocess the incoming message
            user_input = message.content.strip().lower()

            # Handle greetings
            if any(greet in user_input for greet in greetings):
                await message.channel.send("Hello, Welcome to the Weather Bot! I'm your Weather Bot. Ask me about the weather in any city!")
                return

            # Handle goodbyes
            if any(bye in user_input for bye in goodbyes):
                await message.channel.send("Goodbye! Stay safe and take care!")
                return

            # Handle weather queries
            try:
                # Pass the user's input to the weather bot function
                response = get_user_weather_response(user_input)
                await message.channel.send(response)

            except Exception as e:
                # Handle unexpected errors gracefully
                print(f"Error: {e}")
                await message.channel.send("Sorry, I couldn't process your request. Please try again later.")

        else:
            # If the bot is not tagged, do not respond
            return

# Initialize and run the bot
if __name__ == "__main__":
    # Load the bot token from a file
    try:
        with open("token.txt") as file:
            token = file.read().strip()  # Ensure no extra whitespace
    except FileNotFoundError:
        print("Token file not found. Please ensure 'token.txt' contains your bot token.")
        exit()

    # Create an instance of the bot and run it
    client = MyClient()
    client.run(token)

