import streamlit as st
import os
import requests
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
auth_token = os.getenv("AUTH_TOKEN")

headers = {
    "Authorization": f"Bearer {auth_token}"
}

def get_orders(query: str):
    response = requests.post(f"http://localhost:8000/api/orders/search", json={"query": query}, headers=headers)
    return response.json()

def get_products(query: str):
    response = requests.post(f"http://localhost:8000/search/?query={query}", headers=headers)
    return response.json()

def get_expenses(query: str):
    response = requests.get(f"http://localhost:8000/expenses/?user_id=5&skip=0&limit=10", headers=headers)
    return response.json()

def get_events(query: str):
    response = requests.get(f"http://localhost:8000/events/?skip=1&limit=10", headers=headers)
    return response.json()

def main():
    st.title("Groq Chat App")

    # Add customization options to the sidebar
    st.sidebar.title('Select an LLM')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    if user_question:
        response = conversation(user_question)
        message = {'human': user_question, 'AI': response['response']}
        st.session_state.chat_history.append(message)

        # Analyze the intent and call specific API endpoints
        intent = response['response']
        print("Intent:", intent)

        if "product" in intent:
            products = get_products(user_question)
            response_text = f"Products: {products}"
        elif "expense" in intent:
            expenses = get_expenses(user_question)
            response_text = f"Expenses: {expenses}"
        elif "order" in intent:
            orders = get_orders(user_question)
            response_text = f"Orders: {orders}"
        elif "meeting" in intent or "event" in intent:
            events = get_events(user_question)
            response_text = f"Events: {events}"
        else:
            response_text = response['response']

        st.write("Chatbot:", response_text)

if __name__ == "__main__":
    main()