from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from crewai import Agent, Crew, Task, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if API key is available
api_key = os.getenv("gemini_api_key")
if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

# Initialize the ChatGoogleGenerativeAI model with API key
llm = LLM(
    api_key=api_key,
    model="gemini/gemini-2.0-flash"
)

# Custom search tool using DuckDuckGoSearchResults
@tool
def search_web_tool(query: str):
    """
    Searches the web and returns results.
    """
    search_tool = DuckDuckGoSearchResults(num_results=5, verbose=True)
    return search_tool.run(query)

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    # Example conversion rates (you can use an API like Open Exchange Rates for real-time data)
    conversion_rates = {
        "USD": {"INR": 83, "EUR": 0.92},
        "INR": {"USD": 0.012, "EUR": 0.011},
        "EUR": {"USD": 1.09, "INR": 90}
    }
    try:
        return amount * conversion_rates[from_currency][to_currency]
    except KeyError:
        st.error(f"Currency conversion not available for {from_currency} to {to_currency}.")
        return None

# Streamlit App
st.title("🌍 Ultimate Travel Planner")

# User inputs
source = st.text_input("Enter your source city (e.g., Mumbai):")
destination = st.text_input("Enter your destination city (e.g., Australia):")  # Strong focus on destination
currency_type = st.selectbox("Select your currency type:", ["INR", "USD", "EUR"])
budget = st.number_input(f"Enter your budget (in {currency_type}):", min_value=0)
start_date = st.date_input("Select your travel start date:")
end_date = st.date_input("Select your travel end date:")

# Button to generate the plan
if st.button("Plan My Trip"):
    st.write(f"🚀 Generating your travel plan for {destination}...")

    # Step 1: Convert budget to INR for calculations (optional)
    budget_inr = convert_currency(budget, currency_type, "INR") if currency_type != "INR" else budget

    # Step 2: Define CrewAI Agents
    researcher = Agent(
        role="Destination Researcher",
        goal=f"Research the best attractions, weather, and activities in {destination}. Focus on providing relevant details for {destination}, not any other country.",
        backstory="You are an expert in travel research and know how to find exciting places in a specific destination.",
        tools=[search_web_tool],  # Use the custom search tool
        llm=llm,  # Use ChatGoogleGenerativeAI as the LLM
        allow_delegation=False  # Keep delegation disabled for focus on single-task
    )

    planner = Agent(
        role="Itinerary Planner",
        goal=f"Create a detailed itinerary specifically for {destination} from {start_date} to {end_date}. Only include activities and attractions from {destination}.",
        backstory="You are skilled in organizing daily schedules for efficient travel.",
        llm=llm,  # Use ChatGoogleGenerativeAI as the LLM
        allow_delegation=False  # Planner will focus only on itinerary for the specified destination
    )

    budget_advisor = Agent(
        role="Budget Advisor",
        goal=f"Provide cost estimates and budget-friendly recommendations for {destination} within a budget of {currency_type} {budget:,.2f}.",
        backstory="You are a financial expert ensuring the trip stays within budget.",
        llm=llm,  # Use ChatGoogleGenerativeAI as the LLM
        allow_delegation=False  # Budget agent focuses solely on budget
    )

    local_expert = Agent(
        role="Local Expert",
        goal=f"Suggest local cuisine, hidden gems, and cultural insights for {destination}. Make sure everything is specifically related to {destination}.",
        backstory=f"You have deep local knowledge of {destination}'s culture.",
        llm=llm,  # Use ChatGoogleGenerativeAI as the LLM
        allow_delegation=False
    )

    travel_writer = Agent(
        role="Travel Writer",
        goal=f"Compile the final travel plan for {destination}, including attractions, itinerary, budget tips, and local insights.",
        backstory="You specialize in creating comprehensive travel guides.",
        llm=llm,  # Use ChatGoogleGenerativeAI as the LLM
        allow_delegation=False  # Focus only on writing
    )

    # Step 3: Define Tasks for Each Agent
    research_task = Task(
        description=f"Research top attractions and activities in {destination}. Focus only on {destination}.",
        expected_output="A list of top attractions and activities in the destination.",
        agent=researcher
    )

    plan_task = Task(
        description=f"Create a detailed itinerary for {destination} from {start_date} to {end_date}, including attractions, activities, and transportation. Make sure all the details are specific to {destination}.",
        expected_output="A day-by-day itinerary for the trip.",
        agent=planner
    )

    budget_task = Task(
        description=f"Provide budget-friendly tips and cost estimates for {destination} with a budget of {currency_type} {budget:,.2f}.",
        expected_output="Budget-friendly recommendations and cost estimates.",
        agent=budget_advisor
    )

    local_task = Task(
        description=f"Suggest local cuisine, hidden gems, and cultural tips for {destination}. Focus only on {destination}.",
        expected_output="A list of local cuisine, hidden gems, and cultural tips.",
        agent=local_expert
    )

    write_task = Task(
        description=f"Compile the final travel plan for {destination}, including attractions, itinerary, budget tips, and local insights.",
        expected_output="A comprehensive travel plan.",
        agent=travel_writer
    )

    # Step 4: Create the Crew
    crew = Crew(
        agents=[researcher, planner, budget_advisor, local_expert, travel_writer],
        tasks=[research_task, plan_task, budget_task, local_task, write_task],
        verbose=True  # Ensure this is correct for detailed logging
    )

    # Step 5: Execute the Crew
    result = crew.kickoff()

    # Step 6: Display the Results
    st.subheader(f"Final Travel Plan for {destination}")
    if hasattr(result, 'raw'):
        st.write(result.raw)  # Display raw output if available
    else:
        st.error("Unable to fetch the travel plan. Please try again.")

    #Download the plan as a text file
    if hasattr(result, 'raw'):
        st.download_button(
            label="Download Travel Plan",
            data=result.raw,  # Use the raw output for the download
            file_name=f"{destination}_travel_plan.txt",
            mime="text/plain"
        )

# Footer
st.write("---")
st.write("Your Perfect Travel Plan")
