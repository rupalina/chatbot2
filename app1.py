import openai
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# PostgreSQL connection
print (os.getenv('OPENAI_API_KEY'))
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )

def get_gpt3_response(prompt):
    """
    Function to get a response from GPT-3.5-turbo based on the user input.
    """
    conversation_context = (
        "You are a helpful and knowledgeable assistant. Your goal is to provide clear, accurate, and "
        "relevant responses to the user's questions or statements. If the user asks for information or advice, "
        "provide a detailed and thoughtful response. If the user makes small talk or asks casual questions, "
        "respond in a friendly and engaging manner. Here is the user's message:\n"
    )
    
    full_prompt = conversation_context + prompt
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error fetching GPT-3 response: {e}")
        return "Sorry, I couldn't get a response at the moment."

def save_message(user_input, bot_response):
    """
    Function to save the user input and bot response to the PostgreSQL database.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (user_input, bot_response) VALUES (%s, %s)",
                    (user_input, bot_response)
                )
                conn.commit()
    except Exception as e:
        print(f"Error saving message to database: {e}")

def main():
    """
    Main function to run the chatbot interaction loop.
    """
    print("Chatbot is running. Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        bot_response = get_gpt3_response(user_input)
        print(f"Bot: {bot_response}")
        save_message(user_input, bot_response)

if __name__ == "__main__":
    main()
