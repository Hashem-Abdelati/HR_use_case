from flask import Flask, request, render_template, jsonify
import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Gemini wrapper
from dotenv import load_dotenv
import google.generativeai as genai


# --- Load environment variables ---
load_dotenv()

# --- Load data ---
df = pd.read_csv("data/Salaries.csv", low_memory=False)
memory = ConversationBufferMemory(memory_key="chat_history")

# --- Set up Gemini LLM ---
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- Create LangChain agent ---
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True,
    prefix=(
        "You are an expert HR data analyst. You help answer budget-related questions "
        "using a dataset of employee salaries from 2011–2014. Think step-by-step and "
        "always show calculations or reasoning before giving your final answer. "
        "Use the TotalPay column for salary analysis. Do not use TotalPayBenefits unless asked about benefits. Watch for missing or inflated values."
    )
)

# --- Create Flask app ---
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    try:
        answer = agent.run(question)
    except Exception as e:
        answer = f"Error: {str(e)}"
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5051)
