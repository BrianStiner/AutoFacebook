import os
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the Agent class
class Agent:
    def __init__(self, name, initial_prompt_file, model="gpt-3.5-turbo", temperature=0.8):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.memory = []

        with open(initial_prompt_file, 'r') as file:
            initial_prompt = file.read()
            self.memory.append({"role": "system", "content": initial_prompt})

    def generate_message(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content.strip()

# Initialize agents
agent1 = Agent("Agent1", "agent1_initial_prompt.txt")
agent2 = Agent("Agent2", "agent2_initial_prompt.txt")

# load the code
with open("code.txt", "r") as file:
    code = file.read()

# Start the conversation
agent2.memory.append({"role": "user", "content": code})
conversation = agent1.memory + agent2.memory
iterations = 3

for i in range(iterations):
    conversation.append({
        "role": "user",
        "name": agent1.name,
        "content": agent1.generate_message(conversation)
    })
    conversation.append({
        "role": "user",
        "name": agent2.name,
        "content": agent2.generate_message(conversation)
    })

# Save the conversation to a file
with open("chat_output.txt", "w") as output_file:
    for message in conversation:
        role = message["role"]
        content = message["content"]
        if "name" in message:
            name = message["name"]
            output_file.write(f"{name}: {content}\n")
        else:
            output_file.write(f"{role}: {content}\n")
