import re
from langchain.chat_models import ChatOpenAI
import os

class EmailAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
    
    def parse(self, content):
        # Extract basic fields
        sender = self._extract_field(content, "From:")
        subject = self._extract_field(content, "Subject:")
        
        # Extract body
        body = content.split("\n\n", 1)[-1]
        
        # Detect urgency
        urgency = "High" if "urgent" in subject.lower() else "Medium"
        
        # Extract intent with LLM
        intent_response = self.llm.invoke(f"What is the primary intent of this email?\n\n{body[:1000]}")
        intent = intent_response.content
        
        return {
            "sender": sender,
            "subject": subject,
            "urgency": urgency,
            "intent": intent,
            "body": body[:500]  # Store first 500 characters
        }
    
    def _extract_field(self, content, field_name):
        match = re.search(f"{field_name}(.*)", content)
        return match.group(1).strip() if match else "Unknown"