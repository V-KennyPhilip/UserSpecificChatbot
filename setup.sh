#!/bin/bash

# Create a Python virtual environment
python -m venv ./venv

# Activate the virtual environment
source ./venv/bin/activate

# Install required packages
pip install rasa
pip install rasa-sdk
pip install requests

# Initialize the project directories
mkdir -p data
mkdir -p actions

# Train the model
rasa train

echo "Setup complete! Run the following commands to start your chatbot:"
echo "1. In one terminal: rasa run actions"
echo "2. In another terminal: rasa shell or rasa run"