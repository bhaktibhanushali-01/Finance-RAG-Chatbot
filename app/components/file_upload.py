"""
File upload component for data ingestion.
"""

import streamlit as st
from pathlib import Path
import shutil
import config
from src.vectorstore import VectorStoreManager
from src.embeddings import EmbeddingsManager
from src.llm import LLMManager
from src.rag_pipeline import RAGPipeline


def render_file_upload():
    """Render file upload interface."""
    
    st.subheader("📁 Upload Transaction Data")
    
    uploaded_file = st.file_uploader(
        "Choose a text file",
        type=['txt'],
        help="Upload a .txt file containing transaction data"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Save file button
        if st.button("💾 Process File", type="primary"):
            with st.spinner("Processing file..."):
                try:
                    # Save uploaded file to data directory
                    file_path = config.DATA_DIR / uploaded_file.name
                    
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success(f"✅ File saved to {file_path}")
                    
                    # Rebuild vector store
                    with st.spinner("Building vector database..."):
                        vectorstore_manager = VectorStoreManager()
                        vectorstore = vectorstore_manager.rebuild_vectorstore()
                        retriever = vectorstore_manager.get_retriever(
                            k=st.session_state.get('top_k', config.TOP_K_RESULTS)
                        )
                        
                        st.session_state.vectorstore_manager = vectorstore_manager
                        st.session_state.vectorstore_ready = True
                        
                        st.success("✅ Vector database created!")
                    
                    # Initialize RAG pipeline if API key is available
                    if st.session_state.get('api_key'):
                        with st.spinner("Initializing RAG pipeline..."):
                            llm = LLMManager.get_llm(
                                api_key=st.session_state.api_key,
                                model=st.session_state.get('model_name', config.LLM_MODEL),
                                temperature=st.session_state.get('temperature', config.TEMPERATURE)
                            )
                            
                            rag_pipeline = RAGPipeline(llm, retriever)
                            st.session_state.rag_pipeline = rag_pipeline
                            
                            st.success("✅ RAG pipeline ready!")
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
    
    # Show existing files
    st.divider()
    st.subheader("📂 Existing Data Files")
    
    if config.DATA_DIR.exists():
        txt_files = list(config.DATA_DIR.glob("*.txt"))
        
        if txt_files:
            for file in txt_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"📄 {file.name}")
                with col2:
                    if st.button("🗑️", key=f"delete_{file.name}"):
                        file.unlink()
                        st.rerun()
        else:
            st.info("No data files found. Upload a file to get started!")
    
    # Rebuild database button
    st.divider()
    if st.button("🔄 Rebuild Vector Database"):
        with st.spinner("Rebuilding vector database..."):
            try:
                vectorstore_manager = VectorStoreManager()
                vectorstore = vectorstore_manager.rebuild_vectorstore()
                retriever = vectorstore_manager.get_retriever(
                    k=st.session_state.get('top_k', config.TOP_K_RESULTS)
                )
                
                st.session_state.vectorstore_manager = vectorstore_manager
                st.session_state.vectorstore_ready = True
                
                # Reinitialize RAG pipeline
                if st.session_state.get('api_key'):
                    llm = LLMManager.get_llm(
                        api_key=st.session_state.api_key,
                        model=st.session_state.get('model_name', config.LLM_MODEL),
                        temperature=st.session_state.get('temperature', config.TEMPERATURE)
                    )
                    
                    rag_pipeline = RAGPipeline(llm, retriever)
                    st.session_state.rag_pipeline = rag_pipeline
                
                st.success("✅ Vector database rebuilt successfully!")
                
            except Exception as e:
                st.error(f"❌ Error rebuilding database: {str(e)}")