from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
import operator
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

class ChatbotState(TypedDict):
    message: str
    response: str
    chat_history: Annotated[list, operator.add]

def chat(state: ChatbotState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's questions correctly. And also try to consider context if given."),
        ("human", "User's Context: {context}\n\nUser's question: {question}.")
    ])

    chat_history = state['chat_history']

    if len(state['chat_history']) > 2:
        chat_history = state['chat_history'][-2:]

    chain = prompt | model 
    response = chain.invoke({'question': state['message'], 'context': chat_history}).content[0]['text']

    return {'response': response,
            'chat_history': [{
                'human': state['message'],
                'assistant': response
            }]
            }

graph = StateGraph(ChatbotState)

graph.add_node('chat_node', chat)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

memory = MemorySaver()

workflow = graph.compile(checkpointer=memory)
