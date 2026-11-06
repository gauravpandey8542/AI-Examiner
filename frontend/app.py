import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Q&A Project", page_icon="📄")
st.title("Chat with your PDF")

if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar: upload a document
with st.sidebar:
    st.header("Upload a PDF")
    uploaded = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded and st.button("Ingest document"):
        with st.spinner("Reading and indexing the document..."):
            resp = requests.post(
                f"{API_URL}/documents",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                timeout=300,
            )
        if resp.ok:
            info = resp.json()
            st.session_state.doc_id = info["doc_id"]
            st.session_state.history = []
            st.success(f"Indexed {info['pages']} pages, {info['chunks']} chunks")
        else:
            st.error(resp.text)

# Handle a new question
question = st.chat_input("Ask a question about the document")
if question:
    if not st.session_state.doc_id:
        st.warning("Upload and ingest a document first.")
    else:
        with st.spinner("Thinking..."):
            resp = requests.post(
                f"{API_URL}/ask",
                json={"question": question, "doc_id": st.session_state.doc_id},
                timeout=120,
            )
        if resp.ok:
            st.session_state.history.append({"question": question, **resp.json()})
        else:
            st.error(resp.text)

# Show the conversation
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.write(turn["answer"])
        with st.expander("Sources"):
            for s in turn["sources"]:
                st.markdown(f"**[{s['id']}] page {s['page']}**")
                st.caption(s["text"])