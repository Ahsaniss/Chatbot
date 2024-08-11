import streamlit as st
import google.generativeai as genai

# Directly set your API key here (for testing purposes)
api_key = "AIzaSyBCEhToUI4aWoyeM0tdSOU4OllSOS5cJNU"

# Configure the Gemini AI model
genai.configure(api_key=api_key)

# Set a default model
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-1.5-flash"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit app layout
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("Hey, I am AI created by Ahsani")
st.subheader("Talk to me and I'll do my best to assist you!")

# Add custom CSS for message styling
st.markdown("""
<style>
    .user-message {
        background-color: #f0f0f0;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: inline-block;
    }
    .assistant-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="{role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate assistant response
    model = genai.GenerativeModel(
        model_name=st.session_state["gemini_model"],
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
    )
    
    # Convert messages to the format expected by the Gemini API
    formatted_history = []
    for message in st.session_state.messages:
        if message["role"] == "user":
            formatted_history.append({
                "parts": [{"text": message["content"]}],
                "role": "user"
            })
        elif message["role"] == "assistant":
            formatted_history.append({
                "parts": [{"text": message["content"]}],
                "role": "model"
            })
    
    try:
        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(prompt)
        
        # Display assistant response in chat message container
        st.markdown(f'<div class="assistant-message">{response.text}</div>', unsafe_allow_html=True)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"An error occurred: {e}")
