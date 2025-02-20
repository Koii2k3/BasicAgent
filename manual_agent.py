import openai
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv

from llm_config import gemini_config
from prompt import system_instruction
from tools import define_word, extract_keywords, known_actions

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=gemini_config,
    system_instruction=system_instruction
)


class Agent():
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.respond(message)
        self.messages.append({"role": "assistant", "content": result})
        return result

    def respond(self, message):
        completion = gemini_model.generate_content(message)
        return completion.text


if __name__ == "__main__":
    action_re = re.compile(r"^\*\*Action\*\*:\s*(\w+):\s*(.*)$")
    agent = Agent()
    
    MAX_TURNS = 3
    turn_counter = 0
    
    user_message = "Can you find the most important keywords in this sentence: 'Machine learning is a branch of artificial intelligence that enables computers to learn from data without explicit programming' and define the word with the most complex meaning?"
    next_prompt = user_message
    
    while turn_counter < MAX_TURNS:
        response = agent(next_prompt)
        print(f"Assistant: {response}")
        
        action_matches = [
            action_re.match(a) 
            for a in response.split('\n') 
            if action_re.match(a)
        ]
        
        if action_matches:
            action = action_matches[0].group(1)
            paras = action_matches[0].group(2)
            
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}")
            
            print(f">>>>> Call Action: {action} with paras: {paras}")
            observation = known_actions[action](paras)
            
            next_prompt = f"**Observation:** {observation}"
            print(next_prompt)     
        else:
            print("=" * 50, "End", "=" * 50)
            break
        
        turn_counter += 1
        print("-" * 50, "End Turn:", turn_counter, "-" * 50)
        
