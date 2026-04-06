# Air Canvas

Air Canvas is an interactive drawing application that uses computer vision and hand tracking to allow users to draw in the air using their webcam. By detecting hand gestures, particularly the index finger, users can select colors, draw lines, and interact with a virtual canvas without touching any physical device.

## Features

- **Real-time Hand Tracking**: Utilizes MediaPipe's hand landmark detection to track the user's index finger position.
- **Color Selection**: Choose from 6 predefined colors (Red, Green, Blue, Yellow, Magenta, Cyan) by pointing to color buttons in the toolbar.
- **Drawing**: Draw smooth lines by raising the index finger and moving it across the canvas area.
- **Clear Canvas**: Clear the entire drawing with a dedicated clear button.
- **Adjustable Line Thickness**: Increase or decrease line thickness using '+' and '-' keys.
- **Save Drawing**: Save the current drawing as a PNG image by pressing 's'.
- **FPS Display**: Shows real-time frames per second for performance monitoring.
- **Cross-Platform Compatibility**: Works on systems with webcam support.

## Requirements

- Python 3.8 or higher
- Webcam
- Virtual environment (recommended)

## Dependencies

- `mediapipe` - For hand tracking (supports both legacy `mp.solutions` and new Tasks API)
- `opencv-python` - For video capture and image processing
- `numpy` - For array operations

## Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/InternetMadeCoder/air-canvas.git
   cd air-canvas
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install mediapipe opencv-python numpy
   ```

## Usage

1. Ensure your virtual environment is activated.

2. Run the application:
   ```bash
   python main.py
   ```

3. A window titled "AirSketch" will open showing your webcam feed with a toolbar at the top.

4. **Controls**:
   - **Color Selection**: Point your index finger at the color circles in the toolbar to select a color.
   - **Drawing**: Raise your index finger (tip above the middle knuckle) and move it to draw.
   - **Clear**: Point at the "CLEAR" button to erase the entire canvas.
   - **Save**: Press 's' to save the drawing as "Air_Sketch_drawing.png".
   - **Line Thickness**: Press '+' to increase or '-' to decrease line thickness.
   - **Quit**: Press 'q' to exit the application.

## MediaPipe Compatibility

This application is designed to work with different versions of MediaPipe:

- **Legacy MediaPipe (with `mp.solutions`)**: If you have an older version of MediaPipe that includes the `solutions` module, the app will use `mp.solutions.hands`.
- **Modern MediaPipe (Tasks-only)**: For newer MediaPipe packages (e.g., for Python 3.13+), the app automatically downloads and uses the `hand_landmarker.task` model bundle from Google's servers.

The application detects the available MediaPipe API at runtime and adapts accordingly.

## Troubleshooting

- **Camera not found**: Ensure your webcam is connected and not in use by another application.
- **MediaPipe import error**: Make sure MediaPipe is installed in your virtual environment.
- **Slow performance**: Try reducing the frame resolution in the code or closing other applications.
- **Model download fails**: If the automatic model download fails, you can manually download `hand_landmarker.task` from [Google's MediaPipe assets](https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task) and place it in the project directory.

## Project Structure

```
air-canvas/
├── main.py              # Main application script
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── venv/               # Virtual environment (not in repo)
├── hand_landmarker.task # Downloaded model file (ignored)
└── Air_Sketch_drawing.png # Saved drawings (ignored)
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open-source. Please check the license file for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) by Google for the hand tracking technology
- [OpenCV](https://opencv.org/) for computer vision utilities
- Inspired by various air drawing and gesture recognition projects