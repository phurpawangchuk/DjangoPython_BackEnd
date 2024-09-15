# main.py
import os
import openai
from dotenv import dotenv_values
from test import OpenAIModelClient

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=dotenv_values(".env")["OPENAI_API_KEY"],
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)


def test_openai_model_client(api_key):
    # Instantiate the OpenAIModelClient with test parameters
    model_client = OpenAIModelClient(
        model_name="gpt-3.5-turbo",
        openai_api_key=api_key,
        role="Resume Parser",  # You can choose any role for testing
    )

    # Define a test prompt
    test_prompt = "Explain quantum mechanics in simple terms."

    # Call the query_llm method with the test prompt
    response = model_client.query_llm(test_prompt, embedding="")

    # Check if a response is received and print it
    if response:
        print(f"Test AI Response: {response}")
    else:
        print("Test failed: No response received.")


def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a specific model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message["content"].strip()
    except openai.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    if not openai.api_key:
        print("Error: The OpenAI API key is not set.")
    else:
        test_openai_model_client(openai.api_key)
        print(generate_text("What is the meaning of life?"))
