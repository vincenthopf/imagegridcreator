#!/bin/bash

# Image Grid Generator Setup Script

# Check Python version
python_version=$(python3 --version 2>&1)
required_version="Python 3.8"

# Function to check Python version
check_python_version() {
    if [[ "$python_version" < "$required_version" ]]; then
        echo "Error: Python 3.8 or newer is required. Current version: $python_version"
        exit 1
    fi
}

# Function to create virtual environment
setup_virtual_env() {
    echo "Creating virtual environment..."
    python3 -m venv image_grid_env
    source image_grid_env/bin/activate
}

# Function to install dependencies
install_dependencies() {
    echo "Installing required dependencies..."
    pip install pillow reportlab customtkinter
    
    # Check if tkinter is installed
    python3 -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Tkinter is not installed. Attempting to install..."
        
        # Detect OS and install tkinter
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install python-tk@3.9
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux (assumes Ubuntu/Debian)
            sudo apt-get update
            sudo apt-get install -y python3-tk
        else
            echo "Unsupported operating system. Please install tkinter manually."
            exit 1
        fi
    fi
}

# Main script
main() {
    check_python_version
    setup_virtual_env
    install_dependencies
    
    echo "Setup complete! Run the application with:"
    echo "source image_grid_env/bin/activate"
    echo "python3 image_grid_generator.py"
}

# Run the main function
main
