# 🌍 Ultimate AI Travel Planner using CrewAI Agents

## Overview
The Ultimate AI Travel Planner is a Streamlit-based app designed to help users plan their trips efficiently. The app integrates a large language model (LLM) from Gemini (ChatGoogleGenerativeAI) to assist with travel research, itinerary planning, budgeting, and more. The app also utilizes multiple agents from CrewAI, each with a specific role, to handle different aspects of the travel planning process. This provides users with comprehensive and detailed travel plans tailored to their destination.

## Features
- **Destination Research**: Research the top attractions, weather, and activities for a chosen destination using web tools.
- **Itinerary Planning**: Generate a day-by-day itinerary based on the user's selected dates and destination.
- **Budget Advisor**: Get cost estimates and budget-friendly recommendations for the trip.
- **Local Expertise**: Learn about local cuisine, hidden gems, and cultural insights specific to the destination.
- **Comprehensive Travel Guide**: The app compiles all the information into a final travel plan, which can be downloaded as a text file.

## Tech Stack
- **Streamlit**: Used for the frontend interface.
- **LangChain**: Provides the necessary tools and integrations for managing the LLM (Google's Gemini model).
- **CrewAI**: Implements agents that specialize in different tasks (research, itinerary, budgeting, local expertise, etc.).
- **DuckDuckGoSearchResults**: Custom search tool to provide relevant web results.
- **gTTS and SpeechRecognition (optional)**: For future enhancements, voice input/output can be added.
- **Python 3.9+**: Programming language for the app backend.
- **Environment Variables**: Sensitive keys and configurations are managed using the `.env` file.

## Setup Instructions
### Prerequisites
1. Install Python 3.9 or above.
2. Create a `.env` file in the root directory of your project with your Gemini API key:
    ```
    gemini_api_key=<your_gemini_api_key>
    ```

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ultimate-travel-planner.git
    cd ultimate-travel-planner
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Run the Application
1. Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2. Open your browser and go to `http://localhost:8501` to see the app in action.

## Usage
- Input your source city, destination, budget, and travel dates.
- Click 'Plan My Trip' to generate a comprehensive travel plan.
- Download the travel plan as a text file.

## Future Enhancements
- Add voice input/output for enhanced interactivity.
- Integrate real-time currency conversion using external APIs.
- Implement weather forecasts for better planning.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Contact
For any inquiries or support, please contact [suryaramansurya538@gmail.com].
