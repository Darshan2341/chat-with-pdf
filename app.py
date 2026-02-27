import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

css = """
<style>
.chat-message {
    padding: 1.2rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
}
.chat-message.user { background-color: #2b313e; }
.chat-message.bot  { background-color: #475063; }
.chat-message .avatar { font-size: 1.8rem; min-width: 40px; }
.chat-message .message { color: #fff; font-size: 0.95rem; line-height: 1.5; }
</style>
"""

user_template = '<div class="chat-message user"><div class="avatar">🧑</div><div class="message">{{MSG}}</div></div>'
bot_template  = '<div class="chat-message bot"><div class="avatar">🤖</div><div class="message">{{MSG}}</div></div>'


# ---------- STEP 1: Extract text from uploaded PDFs ----------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text


# ---------- STEP 2: Split text into smaller chunks ----------
def get_text_chunks(raw_text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_text(raw_text)
    return chunks


# ---------- STEP 3: Convert chunks to embeddings and store in FAISS ----------
def get_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore


# ---------- STEP 4: Get an answer from Groq using relevant chunks ----------
def get_answer(vectorstore, question, chat_history):
    # Find the most relevant chunks from the PDF
    docs = vectorstore.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Build the LLM
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

    # Build the prompt
    system_prompt = f"""You are a helpful assistant that answers questions based on the provided PDF content.
Use the context below to answer the user's question. If the answer is not in the context, say so honestly.

Context from PDF:
{context}
"""
    messages = [HumanMessage(content=system_prompt)]

    # Add previous chat history for context
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    # Add current question
    messages.append(HumanMessage(content=question))

    response = llm.invoke(messages)
    return response.content


# ---------- STEP 5: Display chat messages ----------
def display_chat(chat_history):
    for msg in chat_history:
        if msg["role"] == "user":
            st.write(user_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)


# ---------- MAIN APP ----------
def main():
    st.set_page_config(page_title="Chat with PDF", page_icon="📄")
    st.write(css, unsafe_allow_html=True)
    st.header("📄 Chat with your PDF")

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    # Sidebar for uploading PDFs
    with st.sidebar:
        st.subheader("Your PDFs")
        pdf_docs = st.file_uploader(
            "Upload your PDF files here", 
            accept_multiple_files=True, 
            type=["pdf"]
        )

        if st.button("Process PDFs"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF first.")
            else:
                with st.spinner("Processing your PDFs..."):
                    # Step 1: Extract text
                    raw_text = get_pdf_text(pdf_docs)

                    # Step 2: Split into chunks
                    chunks = get_text_chunks(raw_text)

                    # Step 3: Create vectorstore
                    st.session_state.vectorstore = get_vectorstore(chunks)

                    st.success(f"Done! Processed {len(chunks)} text chunks.")

    # Chat input
    question = st.chat_input("Ask a question about your PDF...")

    if question:
        if st.session_state.vectorstore is None:
            st.warning("Please upload and process a PDF first using the sidebar.")
        else:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": question})

            # Get answer
            with st.spinner("Thinking..."):
                answer = get_answer(
                    st.session_state.vectorstore,
                    question,
                    st.session_state.chat_history[:-1]  # exclude current question
                )

            # Add bot response to history
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Display chat history
    display_chat(st.session_state.chat_history)


if __name__ == "__main__":
    main()




