import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession


# Initialize Vertex AI with your project
project="Gemini Explorer"

vertexai.init(project="gemini-explorer-433821")  # CORRECT PROJECT NAME AS PER GOOGLE CLOUD ENVIRONMENR

config=generative_models.GenerationConfig(
    temperature=0.4
)

#Load model with config

model=GenerativeModel(
    "gemini-pro",
    generation_config=config
)

chat=model.start_chat()

#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):

    response=chat.send_message(query)
    output=response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role":"model",
            "content":output
        }
    )

st.title("Gemini Explorer")

#initialize the char history

if "messages" not in st.session_state:
    st.session_state.messages=[]

#Display and load the char history

for index, message in enumerate(st.session_state.messages):
    content=Content(
        role=message["role"],
        parts=[part.from_text(message["content"])]
    )

    if index !=0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)

# For initial message startup
if len(st.session_state.messages)==0:
    #Capture the user's name
    user_name=st.text_input("Please enter your name")
    # Define Don's response with personalized geeting
    if(user_name):
        initial_prompt=f"Introduce yourself to {user_name} as 'Don Explorer'(an Ai assistant powered by Google Gemini)"
        llm_function(chat, initial_prompt)


# For capture user input
query=st.chat_input("Ask ReX anything!")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)

