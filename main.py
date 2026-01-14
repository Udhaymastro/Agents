import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LLM Chatbot", page_icon="🤖")
st.title("🤖 LLM Chatbot")

# Load API key securely
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Sidebar — Model Selection
st.sidebar.header("⚙️ Settings")


MODEL_OPTIONS = {
    "Xiaomi Mimo V2-flash": "xiaomi/mimo-v2-flash:free",
    "Mixtral 2512": "mistralai/devstral-2512:free",
    "LLaMA 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
    "Nvidia Nano 9b v2": "nvidia/nemotron-nano-9b-v2:free",
    "GPT-OSS 120B": "openai/gpt-oss-120b:free",
}

selected_model_label = st.sidebar.selectbox(
    "Select LLM Model",
    list(MODEL_OPTIONS.keys())
)

selected_model = MODEL_OPTIONS[selected_model_label]

st.sidebar.markdown(f"**Using model:** `{selected_model}`")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                    extra_headers={
                        "HTTP-Referer": "https://your-app-name.streamlit.app",
                        "X-Title": "OpenRouter Streamlit Chatbot"
                    }
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error(f"Error: {e}")
 