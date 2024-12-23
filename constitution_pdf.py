import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates2 import css, bot_template, user_template
# from htmltemplate3 import css, bot_template, user_template
from langchain.prompts import PromptTemplate
import speech_recognition as sr
from streamlit_mic_recorder import speech_to_text
from gtts.lang import tts_langs
import streamlit as st
from gtts import gTTS
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
import pickle




# Custom question prompt
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""


CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

def format_chat_for_download(chat_history):
    formatted_text = ""
    for i, message in enumerate(chat_history):
        if message ["role"] == "user":
            formatted_text += f"User: {i+1}: {message['content']}\n"
        elif message["role"] == "bot":
            formatted_text += f"Bot {i+1}: {message['content']}\n"
    return formatted_text

def load_vectorstore(embedding_file):
    """Load precomputed embeddings from file."""
    with open(embedding_file, "rb") as f:
        vectorstore = pickle.load(f)
    return vectorstore



def get_conversationchain(vectorstore):
    os.environ['GROQ_API_KEY2'] = os.getenv("GROQ_API_KEY2")
    groq_api_key = os.getenv("GROQ_API_KEY2")
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        condense_question_prompt=CUSTOM_QUESTION_PROMPT,
        memory=memory
    )
    return conversation_chain


def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Could not request results; check your network connection")
    return ""



def handle_userinput(user_question):
    # Check if the conversation chain has been set up
    if st.session_state.conversation is None:
        st.error("Please upload and process documents before asking questions.")
        return

    response_container = st.container()    
    response = st.session_state.conversation({'question': user_question})

    # Update the chat history in session state
    st.session_state.chat_history = response['chat_history']
     # Add button to listen to the response
    bot_response = response['answer']

    st.markdown(bot_template.replace("{{MSG}}", bot_response), unsafe_allow_html=True)

    tts = gTTS(bot_response, lang='en')  # You can change the language code if necessary
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)
    audio_file = os.path.join(temp_audio_dir,f"responseaudio{len(st.session_state.chat_history) // 2 + 1}.mp3")

        # Save the TTS audio to a file in memory
    tts.save(audio_file)

        # Play the audio
    st.audio(audio_file)


    st.markdown('<div class="subheading">Chat History</div>', unsafe_allow_html=True)

    # Display each message in the chat history in reverse order
    for i, message in enumerate((st.session_state.chat_history)):
        cleaned_message = message.content.replace("According to the provided context, ", "")
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", cleaned_message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", cleaned_message), unsafe_allow_html=True)



def main():
    load_dotenv()
    st.set_page_config(page_title="SamvidhanSevak", page_icon=":scroll:", layout="wide")
    

    st.write(css, unsafe_allow_html=True)

    st.markdown('''
<div class="top-heading-container">
    <div class="top-heading">SamvidhanSevak</div>
    <div class="top-subheading">Your AI companion for exploring the Constitution of India</div>
</div>
''', unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    if "hold_active" not in st.session_state:
        st.session_state.hold_active = False
    
     # Load precomputed embeddings
    embedding_file = "constitution_embeddings.pkl"
    if "vectorstore" not in st.session_state:
        try:
            st.session_state.vectorstore = load_vectorstore(embedding_file)
            st.session_state.conversation = get_conversationchain(st.session_state.vectorstore)
            # st.write("Embeddings loaded successfully.") 
            #  # Debugging message
            st.success('Embeddings loaded successfully.', icon="✅")
        except Exception as e:
            st.error(f"Error loading embeddings: {e}")
            return


    if st.sidebar.button("New Chat"):
        st.session_state.conversation = None
        st.session_state.chat_history = None
        if st.session_state.vectorstore:
            # Recreate conversation chain with existing vector store
            st.session_state.conversation = get_conversationchain(st.session_state.vectorstore)
        st.success("Chat history cleared!")

    

    # Add a toggle for selecting input mode
    input_mode = st.radio("Select Input Mode", ("Text", "Audio"))


    # input_mode = st.radio("Select Input Mode", ("Text", "Audio"), horizontal=True)

    # user_question = None

    # if input_mode == "Text":
    #     user_question = st.text_input("Enter your question here:")
    # elif input_mode == "Audio":
    #     st.write("Click the button below to record your audio.")
    #     # Dummy audio placeholder
    #     user_question = st.text_input("Your transcribed audio will appear here after recording.")

    # if user_question:
    #     st.write(f"**You asked:** {user_question}")
    #     # Placeholder for chatbot response
    #     st.write("**Response:** This is a dummy response while the backend processes your query.")

    # Sidebar for additional information
    with st.sidebar:
        st.header("About SamvidhanSevak")
        st.write(
            """
            **SamvidhanSevak** is designed to help you understand the Constitution of India. 
            Ask about specific articles, clauses, or general legal principles.
            """
        )
        st.markdown("---")
        st.write("### Features:")
        st.write("- Explore articles of the Constitution")
        st.write("- Understand legal principles in plain language")
        st.write("- Switch between text and audio input modes")
        st.markdown("---")
        st.write("### Contact Us:")
        st.write("[Visit Our Website](#)")
        st.write("support@samvidhansevak.ai")


    # Placeholder for user input or feedback
    spoken_text_placeholder = st.empty()
    user_question = None
    
    if input_mode == "Text":
        user_question = st.text_input("Ask a question to SamvidhanSevak:")
    elif input_mode == "Audio":
        st.write("Click the button below to record your audio.")
        user_question = speech_to_text(language="en")

        if user_question:
            spoken_text_placeholder.text_area("You said:", user_question, height=70)
    if user_question:
        handle_userinput(user_question)
    


if __name__ == '__main__':
    main()



