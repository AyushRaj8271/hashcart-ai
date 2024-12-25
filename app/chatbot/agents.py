from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Define tool functions for each API

def get_products(query):
    """Fetch products from the E-commerce API."""
    response = requests.get(f"http://localhost:8000/api/products/search?query={query}")
    return response.json()

def get_expenses(query):
    """Fetch expenses from the Expense Tracker API."""
    response = requests.get(f"http://localhost:8000/api/expenses/report?query={query}")
    return response.json()

def get_orders(query):
    """Fetch orders from the E-commerce API."""
    response = requests.get(f"http://localhost:8000/api/orders/search?query={query}")
    return response.json()

def get_events(query):
    """Fetch events from the Calendar API."""
    response = requests.get(f"http://localhost:8000/api/events/search?query={query}")
    return response.json()

# List of tools available to the agents
tools = [
    Tool(
        name="Products",
        func=get_products,
        description="Useful for fetching products from the E-commerce API",
    ),
    Tool(
        name="Expenses",
        func=get_expenses,
        description="Useful for fetching expenses from the Expense Tracker API",
    ),
    Tool(
        name="Orders",
        func=get_orders,
        description="Useful for fetching orders from the E-commerce API",
    ),
    Tool(
        name="Events",
        func=get_events,
        description="Useful for fetching events from the Calendar API",
    ),
]

# Pull the prompt template from the hub
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
prompt = hub.pull("hwchase17/react")

# Initialize a ChatOpenAI model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Create the ReAct agents using the create_react_agent function
product_agent = create_react_agent(llm=llm, tools=[tools[0], tools[2]], prompt=prompt, stop_sequence=True)
expense_agent = create_react_agent(llm=llm, tools=[tools[1]], prompt=prompt, stop_sequence=True)
calendar_agent = create_react_agent(llm=llm, tools=[tools[3]], prompt=prompt, stop_sequence=True)

# Create agent executors from the agents and tools
product_agent_executor = AgentExecutor.from_agent_and_tools(agent=product_agent, tools=[tools[0], tools[2]], verbose=True)
expense_agent_executor = AgentExecutor.from_agent_and_tools(agent=expense_agent, tools=[tools[1]], verbose=True)
calendar_agent_executor = AgentExecutor.from_agent_and_tools(agent=calendar_agent, tools=[tools[3]], verbose=True)

def determine_agent(query):
    """Determine which agent should handle the query based on keywords."""
    if "product" in query or "order" in query:
        return product_agent_executor
    elif "expense" in query:
        return expense_agent_executor
    elif "event" in query or "meeting" in query:
        return calendar_agent_executor
    else:
        return None

def handle_query(query):
    """Handle the query by routing it to the appropriate agent."""
    agent_executor = determine_agent(query)
    if agent_executor:
        response = agent_executor.invoke({"input": query})
        return response
    else:
        return "I can't handle this query."