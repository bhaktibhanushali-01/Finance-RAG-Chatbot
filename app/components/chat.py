"""
Chat interface component.
"""

import streamlit as st
from typing import List, Dict


def add_message_to_history(role: str, content: str):
    """
    Add a message to chat history.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })


def render_chat_interface():
    """Render the chat interface with message history."""
    
    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your transactions..."):
        # Check if API key is set
        if not st.session_state.get('api_key'):
            st.error("⚠️ Please enter your Groq API key in the sidebar first!")
            return
        
        # Check if vectorstore is initialized
        if not st.session_state.get('vectorstore_ready', False):
            st.error("⚠️ Please upload a data file first to create the vector database!")
            return
        
        # Add user message to history
        add_message_to_history("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get RAG pipeline from session state
                    rag_pipeline = st.session_state.get('rag_pipeline')
                    
                    if rag_pipeline:
                        # Query the pipeline
                        response = rag_pipeline.query(prompt)
                        
                        # Display response
                        st.markdown(response)
                        
                        # Add to history
                        add_message_to_history("assistant", response)
                    else:
                        error_msg = "RAG pipeline not initialized. Please refresh the page."
                        st.error(error_msg)
                        add_message_to_history("assistant", error_msg)
                        
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    add_message_to_history("assistant", error_msg)


def clear_chat_history():
    """Clear the chat history."""
    if 'chat_history' in st.session_state:
        st.session_state.chat_history = []