from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import streamlit as st
from langchain_chroma import Chroma
import tempfile
from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ['OPENAI_API_KEY'] = os.environ["API_KEY"]
os.environ['OPENAI_BASE_URL'] = 'https://api.ai.it.cornell.edu'

def upload_document(file, add_source_metadata=True):
    file_extension = os.path.splitext(file.name)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name
    
    try:
        if file_extension == '.pdf':
            loader = PyPDFLoader(tmp_path)
        elif file_extension == '.txt':
            loader = TextLoader(tmp_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        docs = loader.load()
        
        if add_source_metadata:
            for doc in docs:
                if not hasattr(doc, 'metadata') or doc.metadata is None:
                    doc.metadata = {}
                doc.metadata['source_file'] = file.name
        
        return docs
    finally:
        os.unlink(tmp_path)


def upload_multiple_documents(files):
    all_docs = []
    for file in files:
        all_docs.extend(upload_document(file, add_source_metadata=True))
    return all_docs


def get_document_chunks(docs):
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        length_function=len,
        separators=["\n\n", ". ", " ", "", "\n"],
        chunk_overlap=250
    ).split_documents(docs)

def create_vectorstore(chunks):
    return Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(model="openai.text-embedding-3-large")
    )


def get_prompt_results(question, vectorstore, history=None):
    try:
        docs = vectorstore.similarity_search(question, k=5)
        
        context_parts = []
        for i, d in enumerate(docs):
            source_file = d.metadata.get('source_file', 'Unknown') if hasattr(d, 'metadata') else 'Unknown'
            context_parts.append(f"[Chunk {i+1} from {source_file}]\n{d.page_content}")
        context = "\n\n".join(context_parts)
        
        msgs = [{
            "role": "system", 
            "content": "Provide answers depending on the context of the document or documents that were presented. Use only the details from the given context. If there is insufficient background to provide a response, make this apparent. When appropriate, include clear context references and keep your writing brief. If more than one document has the same information, you can identify which document or documents the information is from. To get perspective, think about past conversation turns."
        }]
        
        if history:
            for msg in [m for m in history if m["role"] in ["user", "assistant"]][-5:]:
                msgs.append({"role": msg["role"], "content": msg["content"]})
        
        msgs.append({"role": "user", "content": f"Context from the document:\n\n{context}\n\n---\n\nQuestion: {question}"})
        
        llm = ChatOpenAI(model="openai.gpt-5", temperature=0.2)
        response = llm.invoke(msgs)
        
        return response.content, docs
    except Exception as e:
        raise RuntimeError(f"Error generating answer: {str(e)}")

st.set_page_config(page_title="Document Q&A", initial_sidebar_state="expanded")

for key, default in {"messages": [], "vectorstore": None, "processed_files": set(), "uploader_key": 0, "chunk_count": 0}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("Multi-Document Q&A System")


def show_sources(sources):
    with st.expander(f"Sources ({len(sources)} chunks)", expanded=False):
        for i, doc in enumerate(sources, 1):
            source_file = doc.metadata.get('source_file', 'Unknown') if hasattr(doc, 'metadata') else 'Unknown'
            st.markdown(f"**Source {i}** (from `{source_file}`):")
            st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
            if hasattr(doc, 'metadata') and doc.metadata:
                st.caption(f"Metadata: {doc.metadata}")
            if i < len(sources):
                st.divider()


with st.sidebar:
    st.header("Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose .txt or .pdf files", 
        type=["txt", "pdf"],
        accept_multiple_files=True,
        key=f"file_uploader_{st.session_state.uploader_key}",
        label_visibility="collapsed"
    )
    
    st.caption("Select .txt or .pdf files to upload")
    
    if uploaded_files:
        seen_files = {}
        for file in uploaded_files:
            if file.name not in seen_files:
                seen_files[file.name] = file
        
        uploaded_files = list(seen_files.values())
    
    if uploaded_files:
        current_file_names = {f.name for f in uploaded_files}
        
        removed_files = st.session_state.processed_files - current_file_names
        if removed_files:
            st.session_state.messages = []
            st.session_state.processed_files = set()
            
            if st.session_state.vectorstore:
                try:
                    st.session_state.vectorstore.delete_collection()
                except:
                    pass
                st.session_state.vectorstore = None
            
            with st.spinner(f"Rebuilding after removing {', '.join(removed_files)}..."):
                try:
                    all_docs = upload_multiple_documents(uploaded_files)
                    all_chunks = get_document_chunks(all_docs)
                    st.session_state.vectorstore = create_vectorstore(all_chunks)
                    st.session_state.processed_files = current_file_names.copy()
                    st.session_state.chunk_count = len(all_chunks)
                except Exception as e:
                    st.error(f"Error rebuilding: {str(e)}")
            
            st.rerun()
        
        new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
        if new_files:
            with st.spinner(f"Processing {len(new_files)} file(s)..."):
                try:
                    new_docs = upload_multiple_documents(new_files)
                    new_chunks = get_document_chunks(new_docs)
                    
                    if st.session_state.vectorstore:
                        st.session_state.vectorstore.add_documents(new_chunks)
                        st.session_state.messages = []
                        st.session_state.chunk_count += len(new_chunks)
                    else:
                        st.session_state.vectorstore = create_vectorstore(new_chunks)
                        st.session_state.messages = []
                        st.session_state.chunk_count = len(new_chunks)
                    
                    st.session_state.processed_files = current_file_names.copy()
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")
    
    else:
        if st.session_state.processed_files:
            st.session_state.messages = []
            st.session_state.processed_files = set()
            st.session_state.chunk_count = 0
            
            if st.session_state.vectorstore:
                try:
                    st.session_state.vectorstore.delete_collection()
                except:
                    pass
                st.session_state.vectorstore = None
            
            st.rerun()
    
    if st.session_state.processed_files:
        st.divider()
        st.markdown("### Active Documents")
        
        for filename in sorted(set(st.session_state.processed_files)):
            st.markdown(f"**{filename}**")
        
        st.success(f"{len(st.session_state.processed_files)} document(s) loaded ({st.session_state.chunk_count} chunks)")
        
        if st.button("Clear All Files", type="secondary", use_container_width=True):
            if st.session_state.vectorstore:
                try:
                    st.session_state.vectorstore.delete_collection()
                except:
                    pass
            
            new_key = st.session_state.uploader_key + 1
            
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            st.session_state.uploader_key = new_key
            
            st.rerun()
    else:
        st.divider()
        st.info("Upload files above to get started")


if not st.session_state.vectorstore:
    st.info("Upload one or more documents from the sidebar to begin.")
else:
    doc_count = len(set(st.session_state.processed_files))
    doc_text = "document" if doc_count == 1 else "documents"
    st.caption(f"Using {doc_count} {doc_text}")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                show_sources(msg["sources"])

prompt_text = "Ask about the documents..." if len(set(st.session_state.processed_files)) > 1 else "Ask about the document..."

if prompt := st.chat_input(prompt_text, disabled=not st.session_state.vectorstore):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Fetching answer..."):
            try:
                answer, sources = get_prompt_results(prompt, st.session_state.vectorstore, st.session_state.messages[:-1])
                st.write(answer)
                if sources:
                    show_sources(sources)
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
            except Exception as e:
                st.error(f"Error: {str(e)}")

