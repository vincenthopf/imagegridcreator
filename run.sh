#!/bin/bash

# Image Grid Generator Installer and Runner

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Minimum Python version
PYTHON_MIN_VERSION="3.8.0"

# Check if the script is being run with bash
if [ -z "$BASH_VERSION" ]; then
    echo -e "${RED}Error: This script must be run with bash${NC}"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    local version=$(python3 --version 2>&1 | awk '{print $2}')
    local result=$(printf '%s\n' "$PYTHON_MIN_VERSION" "$version" | sort -V | head -n1)
    
    if [ "$result" != "$PYTHON_MIN_VERSION" ]; then
        echo -e "${RED}Error: Python version $PYTHON_MIN_VERSION or newer is required. Current version: $version${NC}"
        return 1
    fi
    return 0
}

# Function to install Python (platform-specific)
install_python() {
    echo -e "${YELLOW}Installing Python...${NC}"
    
    # Detect the operating system
    case "$(uname -s)" in
        Darwin*)
            # macOS
            if ! command_exists brew; then
                echo -e "${YELLOW}Installing Homebrew...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python@3.9
            ;;
        
        Linux*)
            # Linux (Ubuntu/Debian)
            if [ -f /etc/debian_version ]; then
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential
            elif [ -f /etc/redhat-release ]; then
                # For Red Hat/CentOS/Fedora
                sudo yum install -y python3 python3-pip python3-venv python3-devel gcc
            else
                echo -e "${RED}Unsupported Linux distribution${NC}"
                exit 1
            fi
            ;;
        
        *)
            echo -e "${RED}Unsupported operating system${NC}"
            exit 1
            ;;
    esac
}

# Function to create virtual environment
create_venv() {
    # Check if venv exists
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
}

# Function to install system dependencies
install_system_deps() {
    echo -e "${YELLOW}Installing system dependencies...${NC}"
    
    case "$(uname -s)" in
        Darwin*)
            # macOS dependencies
            brew install libjpeg zlib
            ;;
        
        Linux*)
            # Linux dependencies
            if [ -f /etc/debian_version ]; then
                sudo apt-get install -y \
                    libjpeg-dev \
                    zlib1g-dev \
                    libfreetype6-dev \
                    liblcms2-dev \
                    libwebp-dev \
                    tcl-dev \
                    tk-dev
            elif [ -f /etc/redhat-release ]; then
                sudo yum install -y \
                    libjpeg-devel \
                    zlib-devel \
                    freetype-devel \
                    lcms2-devel \
                    libwebp-devel \
                    tcl-devel \
                    tk-devel
            fi
            ;;
    esac
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    
    # Install or upgrade pip and setuptools
    pip install --upgrade pip setuptools wheel
    
    # Install Pillow with extra options
    pip install --no-cache-dir "Pillow>=9.0.0"
    
    # Install required libraries
    pip install reportlab customtkinter

    # Verify Pillow installation
    python3 -c "from PIL import Image; print('Pillow installed successfully')" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install Pillow. Trying alternative method...${NC}"
        pip install --upgrade --force-reinstall "Pillow>=9.0.0"
    fi

    # Check tkinter installation
    python3 -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Installing Tkinter...${NC}"
        case "$(uname -s)" in
            Darwin*)
                brew install python-tk@3.9
                ;;
            Linux*)
                if [ -f /etc/debian_version ]; then
                    sudo apt-get install -y python3-tk
                elif [ -f /etc/redhat-release ]; then
                    sudo yum install -y python3-tk
                fi
                ;;
        esac
    fi
}

# Main script
main() {
    # Ensure script is run from its directory
    cd "$(dirname "$0")"
    
    # Check if Python is installed
    if ! command_exists python3; then
        install_python
    fi
    
    # Check Python version
    if ! check_python_version; then
        install_python
    fi
    
    # Install system dependencies
    install_system_deps
    
    # Create virtual environment
    create_venv
    
    # Install dependencies
    install_dependencies
    
    # Run the application
    echo -e "${GREEN}Starting Image Grid Generator...${NC}"
    python3 image_grid_app.py
    
    # Deactivate virtual environment
    deactivate
}

# Error handling
set -e
trap 'echo -e "${RED}An error occurred. Please check the output above.${NC}"' ERR

# Run the main function
main
