"""
Sidebar component for configuration and settings.
"""

import streamlit as st
import config
from src.utils import validate_api_key


def render_sidebar():
    """Render the sidebar with configuration options."""
    
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # API Key Section
        st.subheader("🔑 API Key")
        
        # Check if API key exists in .env
        env_key_exists = bool(config.GROQ_API_KEY)
        
        if env_key_exists:
            st.success("✅ API Key loaded from .env file")
            use_env_key = st.checkbox("Use API key from .env", value=True)
            
            if use_env_key:
                api_key = config.GROQ_API_KEY
            else:
                api_key = st.text_input(
                    "Enter Groq API Key",
                    type="password",
                    placeholder="gsk_...",
                    help="Enter your Groq API key"
                )
        else:
            st.warning("⚠️ No API key found in .env file")
            api_key = st.text_input(
                "Enter Groq API Key",
                type="password",
                placeholder="gsk_...",
                help="Get your API key from https://console.groq.com"
            )
        
        # Validate API key
        if api_key:
            if validate_api_key(api_key):
                st.session_state.api_key = api_key
            else:
                st.error("❌ Invalid API key format. Should start with 'gsk_'")
                st.session_state.api_key = None
        else:
            st.session_state.api_key = None
        
        st.divider()
        
        # Model Settings
        st.subheader("🤖 Model Settings")
        
        model_name = st.selectbox(
            "LLM Model",
            options=[
                "llama-3.3-70b-versatile",
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768"
            ],
            index=0,
            help="Select the language model to use"
        )
        st.session_state.model_name = model_name
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=config.TEMPERATURE,
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
        st.session_state.temperature = temperature
        
        top_k = st.slider(
            "Top-K Results",
            min_value=1,
            max_value=10,
            value=config.TOP_K_RESULTS,
            help="Number of documents to retrieve for context"
        )
        st.session_state.top_k = top_k
        
        st.divider()
        
        # Database Status
        st.subheader("💾 Database Status")
        
        if config.CHROMA_DB_DIR.exists():
            st.success("✅ Vector database exists")
            
            # Count files in chroma_db
            try:
                file_count = len(list(config.CHROMA_DB_DIR.rglob("*")))
                st.info(f"📊 Database files: {file_count}")
            except:
                pass
        else:
            st.warning("⚠️ No vector database found")
            st.info("👉 Upload a data file to create the database")
        
        st.divider()
        
        # Additional Info
        st.subheader("ℹ️ About")
        st.markdown("""
        **Financial RAG Chatbot**
        
        Ask questions about your transaction data using AI-powered retrieval.
        
        - 🔍 Semantic search
        - 💬 Contextual answers
        - 📊 Transaction analysis
        """)
        
        # Footer
        st.divider()
        st.caption("Built with ❤️ using Streamlit & LangChain")