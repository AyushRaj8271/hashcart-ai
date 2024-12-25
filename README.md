# HashCart AI

## **Overview**

This project aims to build a **Smart Personal Assistant Chatbot** using Generative AI models and API integration. The chatbot handles user queries, interfaces with multiple APIs, and provides results intuitively. Designed for seamless interactions across various domains like e-commerce, calendars, and expense management, the chatbot leverages intelligent context management to enhance user productivity.

---

## **Features**

### **1. Core Chatbot Functionalities**

- **Natural Language Processing**:
  - Handles user queries intelligently using a Generative AI model (Llama3).
  - Provides context-aware responses for coherent interactions.
- **Ambiguity Resolution**:
  - Handles ambiguous queries and gracefully manages unanswerable ones.

### **2. API Endpoints**

#### **General Endpoints**

- `/chat`: Process user queries and return appropriate responses.
- `/create-user`: Create users and assign roles with specific app permissions.
- `/create-session`: Start a new chat session and get a session ID.
- `/fetch-sessions`: Retrieve all sessions for a user.
- `/get-session-history`: Fetch chat history for a specific session.

#### **Application-Specific Endpoints**

**HashCart (E-Commerce):**

- `/api/products/upload`: Upload product data and save it to the database (Admin-only).
- `/api/products/search`: Search and filter products based on multilingual names and descriptions.
- `/api/orders`: Place an order using natural language.

**Calendar:**

- `/api/calendar/manage/events [POST]`: Schedule meetings with optional reminders.
- `/api/calendar/manage/events [GET]`: Retrieve scheduled meetings and show reminders.

**Expense Tracker:**

- `/api/expense/add-expense`: Log expenses or auto-log orders.
- `/api/expenses/report`: Generate and download expense reports.
- `/api/expenses/analyze`: Suggest saving strategies based on spending patterns.

### **3. Generative AI Features**

- **Mixture of Agents**:
  - Distributes queries to appropriate APIs (e.g., e-commerce, calendar, expense tracker).
- **Advanced Search**:
  - Implements Retrieval-Augmented Generation (RAG) for multilingual product searches.
- **Financial Insights**:
  - Recommends cost-saving strategies based on data analysis.
- **Google Search Integration**:
  - Fetches and synthesizes information from public APIs for enhanced responses.

### **4. Streamlit Web Interface**

- User-friendly UI for interacting with the chatbot.
- Showcases features like order placement, meeting scheduling, and expense reporting.

### **5. Additional Features**

- **Authentication & Authorization**:
  - Role-Based Access Control (RBAC) ensures users access only authorized APIs.
- **Batch Processing**:
  - Parallel indexing of product documents using multi-threading (asyncio).
- **Data Visualization**:
  - Expense analysis with charts generated using Matplotlib and Seaborn.
- **Error Handling**:
  - Graceful management of exceptions, rate limits, and API token limits.

---

## **Tech Stack**

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL with PG Vector for embeddings
- **AI Models**: Llama3 (70B), Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: Streamlit
- **Libraries**: asyncio, Matplotlib, Seaborn

---

## **Setup Instructions**

### **Prerequisites**

- Python 3.9+
- PostgreSQL
- pip

### **Installation Steps**

1. Clone the repository:

   ```bash
   git clone hashcart-ai
   cd hashcart-ai
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables:

   - Create a `.env` file in the project root.
   - Add the following:
     ```env
     DATABASE_URL=postgresql+psycopg2://<user>:<password>@localhost/<dbname>
     LLM_MODEL=llama3-groq-70b-8192-tool-use-preview
     EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
     ```

5. Set up the database:

   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

7. (Optional) Run the Streamlit UI:
   ```bash
   streamlit run main1/app.py
   ```

### **Testing**

- Run the test suite using `pytest`:
  ```bash
  pytest
  ```

---

## **Usage**

- Access the FastAPI docs at `http://127.0.0.1:8000/docs`.
- Interact with the chatbot via Streamlit at `http://localhost:8501`.

---

## **Future Improvements**

- Add support for additional apps and services.
- Implement fine-tuning for AI models based on user feedback.
- Introduce multilingual capabilities for enhanced user experience.

---

## **License**

This project is licensed under the MIT License. See `LICENSE` for details.
