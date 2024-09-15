import json

import requests
from langchain.schema import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

model_role_map = {
    "Resume Parser": "You are a useful assistant that parses resumes in order to extract structured data using resume_text and other context.",
    "Hiring Manager": "You are a hiring manager that finds the best candidate for each job",
    "Spanish Translator": "You are a Spanish translator that translates Spanish text to English while removing random characters that may be present as a result from a poor attempt at OCR.",
    #    "GPT4": "gpt-4-turbo-preview"
}


class LLMClient:
    def _init_(self, model_name):
        self.model_name = model_name

    def query_llm(self, question, embedding):
        raise NotImplementedError("Subclasses must implement this method.")


class OpenAIModelClient(LLMClient):
    def _init_(
        self,
        model_name,
        openai_api_key,
        role="Resume Parser",
    ):
        super()._init_(model_name)
        self.openai_api_key = openai_api_key
        # Initialize the ChatOpenAI client
        self.llm_client = ChatOpenAI(
            openai_api_key=openai_api_key, model_name=model_name, temperature=0.0
        )
        self.name = model_name
        self.role = role

    def query_llm(self, question, embedding):
        """Queries the LLM with a given prompt."""
        try:
            # For simple string prompts
            # response = self.llm_client.generate(prompt)

            # If using structured prompts like in your initial method, you'd construct it inside this method:
            structured_prompt = [
                SystemMessage(content=f"{model_role_map[self.role]}"),
                HumanMessage(content=f"Question: {question}\nContext: {embedding}"),
            ]
            # Adjust based on langchain's method for structured prompts
            response = self.llm_client.invoke(structured_prompt)

            return (
                response.content
            )  # Adjust based on how responses are structured in langchain
        except Exception as e:
            print(f"Error in OpenAIModelClient.query_llm: {str(e)}")
            return None
