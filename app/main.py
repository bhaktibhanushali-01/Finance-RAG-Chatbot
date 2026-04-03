"""
Main Streamlit application for the Financial RAG Chatbot.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from src.vectorstore import VectorStoreManager
from src.llm import LLMManager
from src.rag_pipeline import RAGPipeline
from app.components.sidebar import render_sidebar
from app.components.chat import render_chat_interface, clear_chat_history
from app.components.file_upload import render_file_upload


# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = config.STYLES_DIR / "custom.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'vectorstore_ready' not in st.session_state:
        st.session_state.vectorstore_ready = False
    
    if 'api_key' not in st.session_state:
        st.session_state.api_key = config.GROQ_API_KEY if config.GROQ_API_KEY else None
    
    if 'model_name' not in st.session_state:
        st.session_state.model_name = config.LLM_MODEL
    
    if 'temperature' not in st.session_state:
        st.session_state.temperature = config.TEMPERATURE
    
    if 'top_k' not in st.session_state:
        st.session_state.top_k = config.TOP_K_RESULTS


@st.cache_resource
def load_vectorstore():
    """Load or create vector store (cached)."""
    vectorstore_manager = VectorStoreManager()
    
    # Try to load existing vectorstore
    vectorstore = vectorstore_manager.load_vectorstore()
    
    if vectorstore is None:
        st.warning("⚠️ No existing vector database found. Please upload a data file.")
        return None, None
    
    retriever = vectorstore_manager.get_retriever(
        k=st.session_state.get('top_k', config.TOP_K_RESULTS)
    )
    
    return vectorstore_manager, retriever


def initialize_rag_pipeline():
    """Initialize the RAG pipeline."""
    if not st.session_state.get('api_key'):
        return None
    
    if not st.session_state.get('vectorstore_ready', False):
        # Try to load existing vectorstore
        vectorstore_manager, retriever = load_vectorstore()
        
        if retriever is None:
            return None
        
        st.session_state.vectorstore_manager = vectorstore_manager
        st.session_state.vectorstore_ready = True
    else:
        retriever = st.session_state.vectorstore_manager.get_retriever(
            k=st.session_state.get('top_k', config.TOP_K_RESULTS)
        )
    
    # Initialize LLM
    llm = LLMManager.get_llm(
        api_key=st.session_state.api_key,
        model=st.session_state.get('model_name', config.LLM_MODEL),
        temperature=st.session_state.get('temperature', config.TEMPERATURE)
    )
    
    # Create RAG pipeline
    rag_pipeline = RAGPipeline(llm, retriever)
    
    return rag_pipeline


def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.title("💰 Financial Transaction RAG Chatbot")
    st.markdown("Ask questions about your financial transactions using AI-powered search and analysis.")
    
    # Create tabs
    tab1, tab2 = st.tabs(["💬 Chat", "📁 Data Management"])
    
    with tab1:
        # Initialize RAG pipeline if not already done
        if 'rag_pipeline' not in st.session_state or st.session_state.rag_pipeline is None:
            if st.session_state.get('api_key') and st.session_state.get('vectorstore_ready', False):
                with st.spinner("Initializing RAG pipeline..."):
                    try:
                        st.session_state.rag_pipeline = initialize_rag_pipeline()
                        if st.session_state.rag_pipeline:
                            st.success("✅ RAG pipeline initialized!")
                    except Exception as e:
                        st.error(f"❌ Error initializing RAG pipeline: {str(e)}")
        
        # Chat controls
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                clear_chat_history()
                st.rerun()
        
        # Render chat interface
        render_chat_interface()
        
        # Sample questions
        with st.expander("💡 Sample Questions"):
            st.markdown("""
            - What are the major expense categories?
            - Tell me about investment related transactions
            - What EMI payments are there?
            - Summarize the travel expenses
            - What is the average transaction amount?
            - How much did I spend on food?
            """)
    
    with tab2:
        # File upload and management
        render_file_upload()


if __name__ == "__main__":
    main()