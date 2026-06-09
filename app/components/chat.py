"""
Chat interface component.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def add_message_to_history(role, content, chart_data=None):
    """
    Add a message to chat history.

    Args:
        role: 'user' or 'assistant'
        content: Message content
        chart_data: Optional chart data for visualizations
    """

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "chart_data": chart_data
    })


def render_chat_interface():
    """Render the chat interface with message history."""

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chat messages
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Display chart if available
            if message.get("chart_data"):

                df = pd.DataFrame(message["chart_data"])

                fig = px.pie(
                    df,
                    names="name",
                    values="value",
                    title="Expense Breakdown"
                )

                st.plotly_chart(fig, use_container_width=True)

    # User input
    if prompt := st.chat_input("Ask a question about your transactions..."):

        # Check API key
        if not st.session_state.get('api_key'):
            st.error("⚠️ Please enter your Groq API key in the sidebar first!")
            return

        # Check vector database
        if not st.session_state.get('vectorstore_ready', False):
            st.error("⚠️ Please upload a data file first to create the vector database!")
            return

        # Save user message
        add_message_to_history("user", prompt)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    rag_pipeline = st.session_state.get('rag_pipeline')

                    if rag_pipeline:

                        response = rag_pipeline.query(prompt)

                        # If backend returns JSON dictionary
                        if isinstance(response, dict):

                            answer = response.get("answer", "")
                            chart_data = response.get("chart_data")

                        else:
                            # Fallback for plain text responses
                            answer = str(response)
                            chart_data = None

                        # Display answer
                        st.markdown(answer)

                        # Display pie chart if chart data exists
                        if chart_data:

                            df = pd.DataFrame(chart_data)

                            fig = px.pie(
                                df,
                                names="name",
                                values="value",
                                title="Expense Breakdown"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                        # Save assistant response
                        add_message_to_history(
                            "assistant",
                            answer,
                            chart_data
                        )

                    else:

                        error_msg = (
                            "RAG pipeline not initialized. "
                            "Please refresh the page."
                        )

                        st.error(error_msg)

                        add_message_to_history(
                            "assistant",
                            error_msg
                        )

                except Exception as e:

                    error_msg = (
                        f"Error generating response: {str(e)}"
                    )

                    st.error(error_msg)

                    add_message_to_history(
                        "assistant",
                        error_msg
                    )


def clear_chat_history():
    """Clear the chat history."""

    if 'chat_history' in st.session_state:
        st.session_state.chat_history = []