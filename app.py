from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_huggingface import HuggingFaceEmbeddings


if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []


def process_document(path):

    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = InMemoryVectorStore.from_documents(
        documents=docs,
        embedding=embeddings
    )

    st.session_state.vector_store = vector_db

    llm = ChatGroq(
        model="openai/gpt-oss-20b"
    )

    @tool
    def retrieve_context(query: str):
        """Retrieve documents relevant to a query from the knowledge base."""

        docs = vector_db.similarity_search(
            query=query,
            k=3
        )

        context = ""

        for doc in docs:
            context += doc.page_content + "\n\n"

        return context

    system_prompt = """
    You are a helpful assistant that answers questions using the uploaded documents.

    Your knowledge base consists only of the uploaded PDF documents.

    ALWAYS use the retrieve_context tool for questions related to the uploaded documents.

    Answer based on the retrieved context.

    If the answer cannot be found in the uploaded documents, clearly say that the information
    is not available in the uploaded documents.
    """

    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt=system_prompt,
        checkpointer=memory
    )

    st.session_state.agent = agent
    st.session_state.document_uploaded = True


st.title("📚 RAG Agent")

st.write(
    "Upload PDF documents and ask questions about their content."
)


if not st.session_state.document_uploaded:

    uploaded = st.file_uploader(
        label="Select PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded:

        with st.spinner("Processing documents..."):

            path = "./doc_files/"

            os.makedirs(path, exist_ok=True)

            for file in uploaded:

                file_path = os.path.join(
                    path,
                    file.name
                )

                with open(file_path, "wb") as f:
                    f.write(file.getvalue())

            process_document(path)

        st.success("Documents processed successfully!")

        st.rerun()


if st.session_state.document_uploaded and st.session_state.agent:

    for message in st.session_state.messages:

        role = message.get("role")
        content = message.get("content")

        st.chat_message(role).markdown(content)


    query = st.chat_input(
        "Ask anything related to uploaded documents..."
    )

    if query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        st.chat_message("user").markdown(query)

        response = st.session_state.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            },
            {
                "configurable": {
                    "thread_id": "1"
                }
            }
        )

        answer = response["messages"][-1].content

        st.chat_message("assistant").markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )