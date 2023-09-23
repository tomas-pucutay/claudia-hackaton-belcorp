import openai
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics
import os
from dotenv import load_dotenv
from prompts import get_assistant_prompt_tips
from search import search

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

_ = load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

persist_directory = "db"
embedding = OpenAIEmbeddings()
if not os.path.exists('db'):
    print("No database found")
    raise Exception("No database found")
print("Loading existing db..")
vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding)

with st.sidebar:
    st.image('https://i.ibb.co/YB2xw4T/Claudia.png')
    

st.title("ClaudIA - Tu amiga y consejera")

"""
Estoy aqui para ayudarte a ganar más 
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Pregúntame de cualquier producto Belcorp y lo venderemos!"}
    ]

if "response" not in st.session_state:
    st.session_state["response"] = None

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])
if prompt := st.chat_input(placeholder="Preguntame sobre productos y marcas. Te daré tips de venta"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    result = search(vectordb, prompt)
    response = result.get('answer')
    st.session_state["response"] = response
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])
if st.session_state["response"]:
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Opcional] Me ayudaría mucho si me das mas detalles",
        key=f"feedback_{len(messages)}",
    )
    # This app is logging feedback to Trubrics backend, but you can send it anywhere.
    # The return value of streamlit_feedback() is just a dict.
    # Configure your own account at https://trubrics.streamlit.app/
    if feedback and "TRUBRICS_EMAIL" in st.secrets:
        config = trubrics.init(
            email=st.secrets.TRUBRICS_EMAIL,
            password=st.secrets.TRUBRICS_PASSWORD,
        )
        collection = trubrics.collect(
            component_name="default",
            model="gpt",
            response=feedback,
            metadata={"chat": messages},
        )
        trubrics.save(config, collection)
        st.toast("Feedback recorded!", icon="📝")