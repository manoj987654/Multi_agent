from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from memory.shared_memory import SharedMemory
import os

class ClassifierAgent:
    def __init__(self, memory: SharedMemory):
        self.memory = memory
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
    
    def classify(self, content):
        # Simple format detection
        if content.strip().startswith("{") and content.strip().endswith("}"):
            format = "JSON"
        elif "From:" in content and "Subject:" in content:
            format = "Email"
        else:
            format = "Unknown"
        
        # Detect intent using LLM
        prompt = PromptTemplate.from_template("""
        Classify the intent of this message:
        {content}
        
        Possible intents: Invoice, RFQ, Complaint, Order, Other
        Intent: 
        """)
        chain = prompt | self.llm
        response = chain.invoke({"content": content[:2000]})
        intent = response.content.split()[0]
        
        return format, intent