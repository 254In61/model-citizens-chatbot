# Use a Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (Flask default)
EXPOSE 5000

# Set environment variables (if needed)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# If there's also a FastAPI / uvicorn entry in the repo (main.py)
# You may have to run both or choose one. For now, assume Flask is main.
# The command to run the app:
CMD ["flask", "run"]
