#!/bin/bash

echo "========================================"
echo "  Portfolio Projects – Setup Script"
echo "========================================"
echo ""

# Function to set up a project
setup_project() {
    PROJECT_NAME=$1
    REQ_FILE=$2

    echo "----------------------------------------"
    echo "Setting up $PROJECT_NAME ..."
    echo "----------------------------------------"

    if [ ! -d "$PROJECT_NAME" ]; then
        echo "❌ Directory $PROJECT_NAME not found. Skipping."
        return
    fi

    cd $PROJECT_NAME

    # Create virtual environment
    echo "📦 Creating virtual environment..."
    python3 -m venv venv

    # Activate venv
    echo "🔥 Activating environment..."
    source venv/bin/activate

    # Install requirements
    if [ -f "$REQ_FILE" ]; then
        echo "📚 Installing dependencies from $REQ_FILE ..."
        pip install -r $REQ_FILE
    else
        echo "⚠️ No requirements file found. Skipping package installation."
    fi

    deactivate
    cd ..
    echo "✔ $PROJECT_NAME setup complete!"
    echo ""
}

# List of projects
setup_project "etl-aws" "requirements.txt"
setup_project "flask-api" "requirements.txt"
setup_project "data-quality" "requirements.txt"
setup_project "log-monitor" "requirements.txt"
setup_project "sdlc-toolkit" "requirements.txt"
setup_project "finance-dashboard" "requirements.txt"

echo "========================================"
echo "🎉 All project environments are ready!"
echo "Run: source <project>/venv/bin/activate"
echo "========================================"
