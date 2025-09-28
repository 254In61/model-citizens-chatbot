# Summary

A Client Requirement Collection Chatbot for AKA Studio.
It works fully offline with your own TinyLlama local LLM.

This is Phase 3 of the project whose objectives are : 
1. Take Phase 2 build and deploy in testing site/environment where customer has access to it.

2. Save chatbot data to an external server for analysis.

3. Document "HOW TO" for #1.

4. Document "HOW TO" for #2

# Roadmap to Live Website

1. Containerize your chatbot (Dockerfile ready) : Docker or Podman will package the app so it runs anywhere consistently.

2. Test locally on http://localhost:5000 

3. Pick a hosting option (Azure, AWS, DigitalOcean).
   
   You have several options to host your chatbot:

   A. Cloud Hosting (Recommended)

    - Azure App Service: Push Docker image → deploy directly → get a public URL.
    - AWS Elastic Beanstalk / ECS: Similar workflow with Docker support.
    - Google Cloud Run: Serverless containers → pay per request.

   B. Virtual Machine (VM)
    - Deploy Ubuntu VM → install Docker → run the container → reverse proxy with Nginx to expose it via HTTPS.

   C. Kubernetes / OpenShift
    - Overkill for small projects, but good for enterprise scaling.

4. Deploy the Docker image to the hosting platform.

5. Add custom domain + SSL.

   - Use Nginx or your cloud provider’s built-in SSL options.
   - Point your domain (e.g., chatbot.mycompany.com) → Cloud service → Container port 5000.

6. Open access for users → Done.

# Design Overview
The tool is designed to : 
1. builds a Flask-based web chatbot application that captures client information

2. manages conversation flow

3. validates inputs (email, phone)

4. saves client data to CSV

5. uploads it to SharePoint via PowerShell

6. stores chat logs for recordkeeping.

# Python Packages/Libraries
1. Flask: For creating the web interface and handling HTTP requests.

2. ChatterBot: A chatbot library for training and responding to user input.

3. CSV, JSON, OS, Subprocess:
    - JSON: Loads predefined training data for chatbot conversations.
    - CSV: Stores client information.
    - Subprocess: Runs PowerShell scripts to upload data to SharePoint.

4. Datetime & Pytz: Track session timeout and timestamps for chat logs.

5. Regex (re): Validates email and phone number inputs.

# Chatbot Initialization

chatbot = ChatBot(
    "AKABot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=["chatterbot.logic.BestMatch", "chatterbot.logic.MathematicalEvaluation"]
)

- SQLStorageAdapter: Stores chatbot conversations in a database.
- BestMatch: Finds the best-matching response to user queries.
- MathematicalEvaluation: Allows solving simple math problems.

Training data is loaded from cb_training_data.json, then fed into ListTrainer.

# Client Data Handling
save_client_data(client_data)

- Saves user data (name, company, role, email, phone, project_description) to client_data.csv.

- Uses a fixed field order for consistency.

- Calls a PowerShell script (MgGraph.ps1) to upload this data to SharePoint.

save_chat_log(chat_log, client_data)

- Stores chat history in a timestamped text file named with the client’s name.
  Example: chat_log_John_Smith_20250923_143000.txt


# Input Validation

- Email: Must match a basic user@domain.com pattern.
- Phone: Must be 9–15 digits, optionally starting with +.

is_valid_email(email) → True/False
is_valid_phone(phone) → True/False

# How to Run 

## Locally on your machine

1. Install ollama 

   $ cd /tmp

   $ wget https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64.tgz
   
   $ sudo tar -C /usr -xzf ollama-linux-amd64.tgz

   $ ollama --version

   $ ollama serve

2. Run api 
   
   $ sudo apt install -y python3.12-venv

   $ python3 -m venv venv

   $ source venv/bin/activate

3. Clone down the repo

   $ git clone -b feature/allan-updates https://github.com/254In61/model-citizens-chatbot.git

4. Install the needed python libraries/packages

   $ pip install -r requirements.txt

5. Start FastAPI wrapper

   $ uvicorn main:app --reload --port 8000 &

6. Run Flask server

   $ python3 app.py & 

7. Start chat by going to your Web browser and accessing the address : http://127.0.0.1:5000

## Docker/Podman Image

1. Install podman on your linux machine

   $ sudo apt install -y podman

2. Pull down the container image from docker.io :

   $ podman pull docker.io/254in61/model-citizens-chatbot:latest

3. Start the backend application
   
   $ podman run -p 5000:5000 docker.io/254in61/model-citizens-chatbot

   *** If having a running application binding the same port : $ kill -9 $(lsof -t -i :5000)

4. Open the chat window on your browser : 
   
   $ http://ip_address_of_server:5000

   If this is running on your localhost : $ http://127.0.0.1:5000

   If it is running in a remote server, for example server ip is 192.168.1.98: $ http://192.168.1.98:5000

   
