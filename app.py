import streamlit as st
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.prompts import PromptTemplate



def PDF_traitement():
    loader=PyPDFDirectoryLoader("PDFs_Scrapping_Directory")
    documents=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    Documents_chunks=text_splitter.split_documents(documents)
    return Documents_chunks



def get_vectorstore(Documents_chunks):
    huggingface_embeddings=HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",    
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True}
    )
    vectorstore=FAISS.from_documents(Documents_chunks,huggingface_embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    # Custom prompt template
    prompt_template = """
You are a helpful and concise assistant, skilled at providing clear and precise answers.
Use the provided context to answer the user's question without losing clarity. The  Context: {context}

Now, based on the context, answer the following Question: {question}

Your response should Be brief, clear, and relevant and Focus on key points, avoiding unnecessary details or repetition, Provide insights rather than copying large parts of the context.

IMPORTANT: "Please ensure the answer is complete and addresses the question fully."

If the context lacks enough information, explain that clearly.

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    # Initialize the HuggingFace LLM
    llm = HuggingFaceHub(
        repo_id="mistralai/Mistral-Small-Instruct-2409",
        model_kwargs={"temperature": 0.1, "max_length": 500},
        # Specify the task as "text-generation"
        task="text-generation" 
    )
    
    # Set up the memory to keep conversation history  
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True
    )
    # Create a RetrievalQA using the custom prompt
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    return conversation_chain



def handle_userinput(user_question):
    # Get the response from the conversation
    response = st.session_state.conversation({'question': user_question})
    # Save the updated chat history
    st.session_state.chat_history = response['chat_history']


    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            # User message
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            # Bot message (only the extracted part)
            sentance = "If the context lacks enough information, explain that clearly.\n\nAnswer:"
            st.write(bot_template.replace("{{MSG}}", message.content.split(sentance)[-1].strip()), unsafe_allow_html=True)

            


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with ESSAI")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
        
    st.image("https://i.ibb.co/ggvLcSv/ESSAI-UC.png")
    st.header("Chat with ESSAI")
    
    if st.session_state.conversation is None:
        with st.spinner("Processing..."):
            # Process PDFs and create vectorstore and conversation chain
            Documents_chunks = PDF_traitement()
            vectorstore = get_vectorstore(Documents_chunks)
            st.session_state.conversation = get_conversation_chain(vectorstore)
            #st.write(Documents_chunks)
    # Display input only after processing
    user_question = st.chat_input("Ask a question about OUSSAI:")
    if user_question:
        handle_userinput(user_question)
    
    with st.sidebar:
        if st.button("Clear Chat history"):
            st.session_state.conversation = None
            st.session_state.chat_history = None
            with st.spinner("Processing..."):
            # Process PDFs and create vectorstore and conversation chain
                Documents_chunks = PDF_traitement()
                vectorstore = get_vectorstore(Documents_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
            st.success("Chat history cleared!")
        


if __name__ == '__main__':
    main()