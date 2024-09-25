import openai
import os
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')

def test_openai_api(prompt):
    """
    Function to test OpenAI API call with a given prompt.
    """
    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        
        
        bot_response = response.choices[0].message['content'].strip()
        print(f"Bot Response: {bot_response}")
    except Exception as e:
        print(f"Error fetching GPT-3 response: {e}")

if __name__ == "__main__":
    
    test_prompt = "Hello, how are you today?"
    
  
    test_openai_api(test_prompt)
