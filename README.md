Multi-Format Intake Agent with Intelligent Routing & Context Memory


Objective
Build a multi-agent AI system that can:

✅ Accept PDF, JSON, or Email (text) files
✅ Classify input type and purpose
✅ Route to specialized extraction agents
✅ Maintain context (sender, topic, extracted fields) in a shared memory
✅ Support downstream chaining or audits

Project Structure
```
/agents/         - Classifier, JSON, Email agents
/mcp/            - Main control plane (FastAPI entry point, router)
/memory/         - Shared memory module (SQLite or Redis)
/utils/          - Common helper functions
/data/samples/   - Sample input files (PDF, JSON, emails)
/data/output_logs/ - Sample output logs
```
Setup
1️⃣ Clone the repo:

```bash
git clone https://github.com/manoj987654/Multi_agent.git
cd Multi_agent
```

2️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```
Running the API
Start the FastAPI server:

```bash
uvicorn mcp.main:app --reload
```
Sample Usage
### Upload a `.txt` file:

```bash
curl -X POST -F "file=@C:/Users/venkey/Desktop/agent/data/samples/sample_email.txt" http://localhost:8000/process
```

### Upload a `.json` file:

```bash
curl -X POST -F "file=@data/samples/sample.json" http://localhost:8000/process?conversation_id=conv_123
```
Features
✅ Classifies input type (PDF, JSON, Email)
✅ Determines intent (Invoice, RFQ, Complaint, etc.)
✅ Routes to the correct agent
✅ Extracts structured data
✅ Stores metadata and context in shared memory
Shared Memory
The shared memory module stores:

- Source and type of input
- Extracted fields
- Conversation or thread ID
- Timestamps

Uses either SQLite (default) or Redis.    
Demo Video
A short video demo can be found at: [insert link here]
Sample Inputs & Outputs
- `data/samples/` – Contains example email, JSON, and PDF files
- `data/output_logs/` – Logs and screenshots of extracted outputs
Contributing
Open to pull requests and suggestions! Let’s make this even better together.

