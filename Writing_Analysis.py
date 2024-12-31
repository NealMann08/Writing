import streamlit as st
import base64
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Streamlit App
st.title("Sanskrit Translation Practice App")

# Initialize session state for the sentence
if "response_1" not in st.session_state:
    st.session_state.response_1 = None

# Step 1: Generate a simple English sentence
st.header("Step 1: Generate a Sentence")
if st.button("Generate Sentence"):
    completion_1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Sanskrit teacher."
            },
            {
                "role": "user",
                "content": """Generate a simple 5-word English sentence that can easily be translated into Sanskrit. 

                Use the following format to create the sentence:
                Pronoun + Verb + Adverb + Article + Noun"""
            }
        ],
        temperature=0.7
    )
    st.session_state.response_1 = completion_1.choices[0].message.content
    st.write(f"Generated Sentence: {st.session_state.response_1}")
else:
    if st.session_state.response_1:
        st.write(f"Previously Generated Sentence: {st.session_state.response_1}")

# Step 2: Upload Image
st.header("Step 2: Upload Your Translation")
uploaded_file = st.file_uploader("Upload an image of your Sanskrit translation:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Translation Image", use_column_width=True)

    # Encode the image for OpenAI API
    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

    # Step 3: Check the Translation
    st.header("Step 3: Check Your Translation")
    if st.button("Check Translation"):
        if st.session_state.response_1:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""Translate the Sanskrit sentence in the image to English. 
                                If the sentence is similar to '{st.session_state.response_1}', then tell the user they are correct; 
                                if it is not similar at all, then tell the user they are wrong.""",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
            )
            # Display the result
            result = response.choices[0].message.content
            st.write(f"Result: {result}")
        else:
            st.warning("Please generate a sentence first!")
