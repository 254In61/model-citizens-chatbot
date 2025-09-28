# Importing FastAPI and HTTPException for building and handling the web API
from fastapi import FastAPI, HTTPException

# Importing BaseModel for defining data validation schema
from pydantic import BaseModel

# Importing requests module for sending HTTP requests
import requests

# Creating FastAPI app instance
app = FastAPI(
    # Setting API title
    title="TinyLlama Local API",

    # Describing the API purpose
    description="A simple FastAPI wrapper for the local TinyLlama running in Ollama.",

    # Defining API version
    version="1.0.0"
)

# Assigning Ollama server URL to a constant
OLLAMA_URL = "http://localhost:11434"

# Defining request body model using Pydantic
class Prompt(BaseModel):
    # Declaring a single string field to hold the input prompt
    text: str

# Creating POST endpoint for generating a response from TinyLlama
@app.post("/generate")
# Defining the generate function that takes a Prompt object as input
def generate(prompt: Prompt):
    # Creating a dictionary payload for the API request
    payload = {
        # Specifying the model to use
        "model": "tinyllama",
        # Assigning the input text to the prompt field
        "prompt": prompt.text,
        # Disabling streaming for single-shot response
        "stream": False
    }
    # Starting try block for handling potential request errors
    try:
        # Sending POST request to Ollama API with payload
        res = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        # Raising exception if response contains HTTP error
        res.raise_for_status()
        # Parsing response as JSON
        response = res.json()
        # Returning the generated response in dictionary form
        return {"reply": response["response"]}
    # Catching any exceptions during the API call
    except Exception as e:
        # Raising HTTPException with error details if failure occurs
        raise HTTPException(status_code=500, detail=str(e))