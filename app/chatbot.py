# import streamlit as st
# import os
# from groq import Groq
# import random

# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain_groq import ChatGroq
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv
# import os 

# load_dotenv()

# groq_api_key = "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"

# def main():

#     st.title("Groq Chat App")

#     # Add customization options to the sidebar
#     st.sidebar.title('Select an LLM')
#     model = st.sidebar.selectbox(
#         'Choose a model',
#         ['mixtral-8x7b-32768', 'llama2-70b-4096']
#     )
#     conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

#     memory=ConversationBufferWindowMemory(k=conversational_memory_length)

#     user_question = st.text_area("Ask a question:")

#     # session state variable
#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history=[]
#     else:
#         for message in st.session_state.chat_history:
#             memory.save_context({'input':message['human']},{'output':message['AI']})


#     # Initialize Groq Langchain chat object and conversation
#     groq_chat = ChatGroq(
#             groq_api_key=groq_api_key, 
#             model_name=model
#     )

#     conversation = ConversationChain(
#             llm=groq_chat,
#             memory=memory
#     )

#     if user_question:
#         response = conversation(user_question)
#         message = {'human':user_question,'AI':response['response']}
#         st.session_state.chat_history.append(message)
#         st.write("Chatbot:", response['response'])

# if __name__ == "__main__":
#     main()



import streamlit as st
import os
from groq import Groq
import random
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import CalendarEvent,Order,Product,Expense
from dependencies import get_db

def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CalendarEvent).offset(skip).limit(limit).all()

def get_orders(db: Session, query: str):
    return db.query(Order).filter(Order.product_name.contains(query)).all()

    
def get_products(db: Session, query: str):
    return db.query(Product).filter(Product.name.contains(query)).all()

def get_expenses(db: Session, query: str):
    return db.query(Expense).filter(Expense.description.contains(query)).all()





load_dotenv()

groq_api_key = "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"

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

        # Analyze the intent and call specific CRUD operations
        intent = response['response']
        db = next(get_db())

        if "product" in intent:
            products = get_products(db, user_question)
            response_text = f"Products: {products}"
        elif "expense" in intent:
            expenses = get_expenses(db, user_question)
            response_text = f"Expenses: {expenses}"
        elif "order" in intent:
            orders = get_orders(db, user_question)
            response_text = f"Orders: {orders}"
        elif "meeting" in intent or "event" in intent:
            events = get_events(db, user_question)
            response_text = f"Events: {events}"
        else:
            response_text = response['response']

        st.write("Chatbot:", response_text)

if __name__ == "__main__":
    main()
