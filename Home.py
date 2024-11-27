import streamlit as st
from groq import Groq
import pandas as pd
import numpy as np
import plotly.express as px
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
# Load environment variables
# load_dotenv()
api_key = st.secrets["GROQ_API_KEY"]

from src.components.navigation import page_config, custom_style, footer


# Set up Groq LLM client
groq_llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"], #or os.getenv("GROQ_API_KEY")
    model="llama-3.1-8b-instant",  # Specify the model you want to use
    temperature=0.1,
    max_tokens=None,
    timeout=3,
    max_retries=2,
)


client = Groq(api_key=api_key)

def analyze_image_with_groq(image_path):
    response = client.chat.completions.create(
        model="llama2-70b-4096",
        messages=[
            {"role": "system", "content": "You are a satellite imagery expert"},
            {"role": "user", "content": f"Analyze this satellite image: {image_path}"}
        ]
    )
    return response.choices[0].message.content



def main():
    st.title("GeoInsight Pro: Satellite AI Analysis")
    custom_style()
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Image Classification", "Climate Change", "Environmental Impact"]
    )
    
    if page == "Image Classification":
        image_classification_module()
    
    elif page == "Climate Change":
        climate_change_module()
        
    footer()

def image_classification_module():
    st.header("Satellite Image Classification")
    uploaded_file = st.file_uploader("Upload Satellite Image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # AI processing logic here
        pass

def climate_change_module():
    st.header("Land Transformation Analysis")
    # Comparative visualization
    pass

if __name__ == "__main__":
    main()