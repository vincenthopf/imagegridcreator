# Image Grid Generator

A modern GUI application that allows you to create PDF grids from your images with customizable layouts.

## Features

- Drag and drop image selection
- Customizable grid layout (rows and columns)
- Live preview
- PDF output with automatic image scaling and rotation
- Support for EXIF rotation
- Modern dark theme interface

## Running with Docker

### Prerequisites

- Docker
- Docker Compose
- X11 Server (for GUI support)

### Linux Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-grid-generator
   cd image-grid-generator
   ```

2. Allow X11 forwarding:
   ```bash
   xhost +local:docker
   ```

3. Run the application:
   ```bash
   docker-compose up --build
   ```

### Windows Setup

1. Install an X11 server like VcXsrv or Xming

2. Start the X11 server

3. Set the DISPLAY environment variable:
   ```powershell
   $env:DISPLAY = "host.docker.internal:0.0"
   ```

4. Run the application:
   ```powershell
   docker-compose up --build
   ```

### macOS Setup

1. Install XQuartz:
   ```bash
   brew install --cask xquartz
   ```

2. Start XQuartz and enable "Allow connections from network clients" in Preferences

3. Allow X11 forwarding:
   ```bash
   xhost +localhost
   ```

4. Set the DISPLAY environment variable:
   ```bash
   export DISPLAY=:0
   ```

5. Run the application:
   ```bash
   docker-compose up --build
   ```

## Manual Installation

If you prefer to run the application without Docker:

1. Install Python 3.9 or later

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python image_grid_app.py
   ```

## Usage

1. Click "Select Images" to choose your input images
2. Use the sliders to adjust the grid layout
3. Preview your layout in real-time
4. Click "Select Output Path" to choose where to save your PDF
5. Click "Generate PDF" to create your image grid

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.