# OtooHelpAI — AI Student Learning Assistant
## Overview
An AI-powered educational application designed to help students understand complex concepts, generate study materials, and test their knowledge through interactive quizzes.

The application uses a locally hosted large language model to provide personalized learning experiences without requiring a paid API.

## Features
- AI-generated explanations
- Simplified explanations for beginners
- Automatic study note generation
- Interactive multiple-choice quizzes
- Automated grading and answer explanations
- Customizable difficulty levels
- Downloadable study materials
- Persistent learning history
- Learning analytics dashboard

## Technologies Used
- Python
- Streamlit
- Ollama
- Llama 3.2
- JSON

## Installation

1. Install Python and Ollama.
2. Download the AI model:

   `ollama pull llama3.2`

3. Install the required Python libraries:

   `pip install -r requirements.txt`

4. Start Ollama and launch the application:

   `streamlit run app.py`

## Skills Demonstrated
- Large language model integration
- Prompt engineering
- Structured AI output processing
- Data persistence
- Input validation
- Automated assessment
- User interface development
- Data visualization

## Responsible AI
AI-generated responses may contain inaccuracies. Users are encouraged to verify important information with reliable educational sources.

Learning history is stored locally in an unencrypted JSON file. Quiz results are not permanently tracked.

## Future Improvements
- PDF document uploads
- Personalized study recommendations
- Quiz performance tracking
- AI response accuracy evaluation
