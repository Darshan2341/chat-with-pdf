# 📄 Chat with PDF

A conversational AI app that lets you upload PDF files and ask questions about their content — powered by LangChain,GROQ, and Streamlit.

---

## 🚀 Features

- Upload one or more PDF files
- Automatically extracts and indexes content
- Ask natural language questions about your documents
- Remembers conversation context (multi-turn chat)
- Clean, user-friendly chat interface

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web UI |
| LangChain | AI orchestration |
| GROQ| Language model |LLaMA3
| FAISS | Vector similarity search |
| HuggingFace | Free text embeddings |
| PyPDF2 | PDF text extraction |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Darshan2341/chat-with-pdf.git
cd chat-with-pdf
```

### 2. Create a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
cp .env.example .env
```
Open `.env` and replace `your_openai_api_key_here` with your actual [OpenAI API key](https://platform.openai.com/api-keys).

### 5. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📸 How to Use

1. Open the app in your browser
2. Use the **sidebar** to upload one or more PDF files
3. Click **⚙️ Process** and wait for indexing to complete
4. Type your question in the text box and press Enter
5. The AI will answer based on the document content

---

## 📁 Project Structure

```
chat-with-pdf/
├── app.py              # Main application logic
├── htmlTemplates.py    # Chat bubble styling
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── .env                # Your actual keys (not committed)
├── .gitignore
└── README.md
```

---

## 💡 How It Works

1. **Text Extraction** — PyPDF2 reads the raw text from each page
2. **Chunking** — LangChain splits text into overlapping 1000-character chunks
3. **Embedding** — Each chunk is converted to a vector using HuggingFace's free MiniLM model
4. **Indexing** — FAISS stores all vectors for fast similarity search
5. **Retrieval** — When you ask a question, the most relevant chunks are retrieved
6. **Generation** — GPT-3.5 reads those chunks and generates a grounded, accurate answer
7. **Memory** — ConversationBufferMemory keeps track of chat history for follow-up questions

---

## 🔐 Security Notes

- Never commit your `.env` file — it's in `.gitignore` for this reason
- Keep your OpenAI API key private
- For production, consider adding authentication

---

## 🙋 Author

**Your Name**  
[LinkedIn](www.linkedin.com/in/darshan-pokale-b1834334b)
 | [GitHub](https://github.com/Darshan2341)

---

## 📄 License

MIT License — free to use and modify.
