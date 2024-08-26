# Re:Memories

Re:Memories is a comprehensive platform designed to support individuals with memory-related issues. The platform allows users to journal their memories, capturing moments from their past in a safe and accessible digital space. These entries can be viewed by healthcare professionals, who can analyze them for patterns and gain a better understanding of the patient's cognitive state. In addition to journaling, Re:Memories connects users with others who have similar memories, providing an opportunity to relive and share experiences. This connection fosters a sense of community and helps combat the isolation that often accompanies memory-related conditions.

## Features

- **Memory Journaling**: Users can securely journal their memories, which are stored in a digital space.
- **Healthcare Insights**: Healthcare professionals can view journaled entries to analyze patterns and understand cognitive states.
- **AI-Powered Matching**: Users are connected with others who have similar memories, creating a community of shared experiences.
- **Privacy and Security**: The platform ensures user data is secure and private, while maintaining an intuitive interface.

## Getting Started

To get started with Re:Memories, follow the instructions below.

### Prerequisites

1. **Python**: Ensure you have Python 3.8+ installed. You can download it from [here](https://www.python.org/downloads/).
2. **Visual Studio Compiler**: This project requires certain packages that need a Visual Studio compiler. You need to install the [Microsoft Visual Studio Compiler](https://visualstudio.microsoft.com/vs/features/cplusplus/) to compile these packages.

### Installation

1. **Download the ZIP file**: 
   - Download the project ZIP file from the GitHub repository and extract it to your desired location.

2. **Navigate to the project directory**:
3. ```
   cd path/to/extracted-folder
   ```
   Create a virtual environment.
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required packages using ```pip install -r requirements.txt```
5. Run the database migrations using ```python manage.py migrate```
6. Run the project using daphne using ```daphne -p 8000 re_memories.asgi:application```
7. Open your browser and go to http://127.0.0.1:8000/ to start using Re:Memories.
   

