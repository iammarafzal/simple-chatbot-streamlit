from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import operator
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

class ChatbotState(TypedDict):
    message: str
    chat_history: Annotated[list, operator.add]

def chat(state: ChatbotState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's questions correctly. And also try to consider context if given."),
        ("human", "User's Context: {context}\n\nUser's question: {question}.")
    ])

    chat_history = state['chat_history']

    if len(state['chat_history']) > 5:
        chat_history = state['chat_history'][-5:]

    chain = prompt | model 
    response = chain.invoke({'question': state['message'], 'context': chat_history}).content[0]['text']

    return {'chat_history': [{
                'human': state['message'],
                'assistant': response
            }]
        }

# -------------------------------- Graph --------------------------------
graph = StateGraph(ChatbotState)

graph.add_node('chat_node', chat)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# -------------------------------- Checkpointer --------------------------------
conn = sqlite3.connect(database="db/chatbot.db", check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

workflow = graph.compile(checkpointer=checkpointer)

# -------------------------------- Threads --------------------------------
def get_all_thread_ids():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)