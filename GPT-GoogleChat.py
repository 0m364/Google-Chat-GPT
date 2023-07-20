import os
import openai
import json
import google-chat-api

class TextGenerator:
    def __init__(self, api_key, engine='davinci-codex'):
        self.api_key = api_key
        self.engine = engine
        openai.api_key = self.api_key

    def generate_text_message(self, message, temperature=0.6, max_tokens=50):
        try:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=message,
                max_tokens=max_tokens,
                temperature=temperature
            )
            # Extract and return the generated message
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable.")
        return

    # Create TextGenerator instance
    text_generator = TextGenerator(api_key)

    # Get the current conversation ID
    chat = google-chat-api.Chat()
    conversation_id = chat.get_conversation_id()

    # Get the most recent message in the conversation
    message = chat.get_most_recent_message(conversation_id)

    # Generate a reply to the message
    generated_message = text_generator.generate_text_message(message)

    # Send the reply message
    chat.send_message(conversation_id, generated_message)

# Execute the main function
if __name__ == '__main__':
    main()
