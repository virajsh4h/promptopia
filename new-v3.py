import streamlit as st
from google import genai
from google.genai import types

# Set page config and apply custom dark theme styling.
st.set_page_config(
    page_title="Promptopia",
    layout="centered",
)
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stTextInput, .stTextArea {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #333333;
    }
    .stButton>button {
        background-color: #6200ee;
        color: #ffffff;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Promptopia")
st.subheader("Test your prompt engineering skills!")

# Get the Gemini API Key from the user.
user_api_key: str = st.text_input(
    "Enter your Gemini API Key:",
    placeholder="You cannot proceed without a valid API key",
    type="password"
)

if user_api_key:
    try:
        client = genai.Client(api_key=user_api_key)
        
        # Prompt input with a token limit of 70 tokens.
        user_prompt: str = st.text_area(
            "Enter your prompt:",
            "",
            placeholder="Enter your prompt (max 70 tokens)"
        )
        
        # Approximate token count using whitespace splitting.
        token_count = len(user_prompt.split())
        st.write(f"Token count: {token_count}")
        
        # Button to update the token count.
        if st.button("Update Token Count"):
            token_count = len(user_prompt.split())
            st.write(f"Updated token count: {token_count}")
        
        if token_count > 10:
            st.error("Your prompt exceeds the 70 token limit. Please shorten your prompt.")
        else:
            if st.button("Generate Response"):
                st.subheader("LLM Output")
                stream = st.empty()
                stream.write("Generating response... 🚀")
                full_response = ""
                
                if user_prompt.strip():
                    # Generate response with fixed temperature (0.01) and without an output token limit.
                    response = client.models.generate_content_stream(
                        model="gemini-2.0-flash",
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.01,
                            top_k=100,    # You can adjust these as needed.
                            top_p=0.95
                            # Notice: max_output_tokens is omitted, removing any output token limit.
                        )
                    )
                    for chunk in response:
                        if chunk.text: 
                            full_response += chunk.text
                            stream.write(full_response)
                        else:
                            stream.write("No response generated. Please try again.")
                else:
                    st.warning("Please enter a prompt!")
    except Exception as e:
        st.error("Invalid API Key. Please try again.")
else:
    st.warning("Please contact your co-ordinator for support.")

st.markdown("---")
st.markdown("❤️ Made at DESPU for PROMPTOPIA.")
