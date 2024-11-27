import os
import streamlit as st
from groq import Groq
import pandas as pd
import numpy as np
import plotly.express as px
from langchain_groq import ChatGroq
from PIL import Image
import io
import base64
from dotenv import load_dotenv
# Load environment variables
# load_dotenv()
api_key = st.secrets["GROQ_API_KEY"]

from src.components.navigation import page_config, custom_style, footer


# Secrets and API Configuration
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)


def encode_image_to_base64(image):
    """Convert PIL Image to base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')



def analyze_image_with_groq(image):
    """
    Analyze satellite image using Groq's vision model.
    
    Args:
        image (PIL.Image): Uploaded image to analyze
    
    Returns:
        str: Detailed image analysis result
    """
    try:
        # Encode image to base64
        base64_image = encode_image_to_base64(image)
        
        # Modify message structure to remove system message
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text", 
                            "text": "You are an expert satellite imagery and geospatial analysis professional. Perform a comprehensive analysis of this satellite image. Focus on land use, vegetation cover, geological features, potential environmental changes, and any significant observations."
                        }
                    ]
                }
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Image analysis error: {e}")
        return "Unable to analyze image. Please try again."



def generate_climate_change_visualization(data):
    """
    Create interactive climate change visualization.
    
    Args:
        data (dict): Climate-related data points
    
    Returns:
        plotly figure for climate trends
    """
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Value'])
    df.index.name = 'Year'
    df.reset_index(inplace=True)
    
    fig = px.line(
        df, 
        x='Year', 
        y='Value', 
        title='Climate Change Indicators Over Time',
        labels={'Value': 'Change Magnitude'},
        template='plotly_white'
    )
    return fig

def main():
    """Main application workflow"""
    st.title("🛰️ GeoInsight Pro: Satellite AI Analysis")
    custom_style()
    # Sidebar navigation
    page = st.sidebar.radio(
        "Choose Analysis Module",
        ["Image Classification", "Climate Change", "Environmental Impact"]
    )
   
    if page == "Image Classification":
        image_classification_module()
   
    elif page == "Climate Change":
        climate_change_module()
    
    elif page == "Environmental Impact":
        environmental_impact_module()
        
        
    footer()

def image_classification_module():
    """Satellite Image Classification and Analysis Module"""
    st.header("🖼️ Satellite Image Classification")
    
    uploaded_file = st.file_uploader(
        "Upload Satellite Image", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a satellite or aerial image for AI analysis"
    )
   
    if uploaded_file is not None:
        # Open image with PIL
        image = Image.open(uploaded_file)
        
        # Display uploaded image
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Satellite Image", use_column_width=True)
        
        with col2:
            with st.spinner('Analyzing image with AI...'):
                analysis_result = analyze_image_with_groq(image)
            
            st.subheader("AI Analysis Results")
            st.write(analysis_result)

def climate_change_module():
    """
    Comprehensive Climate Change Analysis Module
    Provides multi-dimensional insights into global climate trends
    """
    st.header("🌍 Climate Change & Land Transformation Analysis")
    
    # Tabs for different analysis perspectives
    tab1, tab2, tab3 = st.tabs([
        "Global Temperature Trends", 
        "Sea Level Rise", 
        "Carbon Emissions"
    ])
    
    with tab1:
        # Global Temperature Trend Visualization
        temp_data = {
            'Year': [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023],
            'Temperature Anomaly (°C)': [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.4, 1.6]
        }
        df_temp = pd.DataFrame(temp_data)
        
        fig_temp = px.line(
            df_temp, 
            x='Year', 
            y='Temperature Anomaly (°C)', 
            title='Global Temperature Anomalies (1950-2023)',
            labels={'Temperature Anomaly (°C)': 'Temperature Difference from Baseline'},
            template='plotly_white'
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        st.markdown("""
        ### Key Observations
        - Significant temperature increase since 1950
        - Accelerating warming trend in recent decades
        - 2023 shows highest recorded temperature anomaly
        """)
    
    with tab2:
        # Sea Level Rise Visualization
        sea_level_data = {
            'Year': [1900, 1950, 1980, 2000, 2010, 2020, 2023],
            'Sea Level Rise (mm)': [0, 50, 100, 150, 200, 250, 280]
        }
        df_sea = pd.DataFrame(sea_level_data)
        
        fig_sea = px.area(
            df_sea, 
            x='Year', 
            y='Sea Level Rise (mm)', 
            title='Cumulative Sea Level Rise',
            labels={'Sea Level Rise (mm)': 'Cumulative Rise in Millimeters'},
            template='plotly_white'
        )
        st.plotly_chart(fig_sea, use_container_width=True)
        
        st.warning("Projected sea level rise poses significant risks to coastal communities")
    
    with tab3:
        # Carbon Emissions Visualization
        emissions_data = {
            'Sector': ['Energy', 'Transportation', 'Industry', 'Agriculture', 'Waste'],
            'Emissions (Gt CO2)': [25, 8, 12, 6, 3]
        }
        df_emissions = pd.DataFrame(emissions_data)
        
        fig_emissions = px.pie(
            df_emissions, 
            values='Emissions (Gt CO2)', 
            names='Sector', 
            title='Global Carbon Emissions by Sector',
            hole=0.3
        )
        st.plotly_chart(fig_emissions, use_container_width=True)

def environmental_impact_module():
    """
    Comprehensive Environmental Impact Assessment Module
    Provides insights into ecological changes and environmental indicators
    """
    st.header("🌱 Environmental Impact & Ecosystem Health")
    st.markdown('''
        <style>
            div.block-container{padding-top:0px;}
            font-family: 'Roboto', sans-serif; /* Add Roboto font */
            color: #00008B; /* Make the text blue */
        </style>
            ''',
        unsafe_allow_html=True)
    
    # Analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Biodiversity Indicators")
        biodiversity_data = {
            'Region': ['Amazon', 'Congo Basin', 'Southeast Asia'],
            'Species Diversity Loss (%)': [15, 10, 12]
        }
        df_biodiversity = pd.DataFrame(biodiversity_data)
        
        fig_biodiversity = px.bar(
            df_biodiversity, 
            x='Region', 
            y='Species Diversity Loss (%)', 
            title='Regional Biodiversity Loss',
            color='Region'
        )
        st.plotly_chart(fig_biodiversity, use_container_width=True)
    
    with col2:
        st.subheader("Forest Cover Changes")
        forest_data = {
            'Year': [2000, 2005, 2010, 2015, 2020],
            'Forest Cover (Million km²)': [40, 39, 38, 36, 34]
        }
        df_forest = pd.DataFrame(forest_data)
        
        fig_forest = px.area(
            df_forest, 
            x='Year', 
            y='Forest Cover (Million km²)', 
            title='Global Forest Cover Decline',
            template='plotly_white'
        )
        st.plotly_chart(fig_forest, use_container_width=True)
    
    # Interactive Impact Assessment
    st.subheader("Environmental Scenario Simulator")
    
    # Sliders for interactive exploration
    conservation_effort = st.slider(
        "Conservation Effort Intensity", 
        min_value=0, 
        max_value=100, 
        value=50,
        help="Adjust the level of environmental conservation efforts"
    )
    
    emission_reduction = st.slider(
        "Carbon Emission Reduction (%)", 
        min_value=0, 
        max_value=50, 
        value=25,
        help="Simulate potential carbon emission reduction scenarios"
    )
    
    # Simulated Impact Calculation
    simulated_recovery = (conservation_effort * 0.5) + (emission_reduction * 0.75)
    
    st.metric(
        "Projected Ecosystem Recovery Potential", 
        f"{simulated_recovery:.2f}%",
        delta=f"{simulated_recovery - 50:.2f}% from baseline"
    )
    
    # Detailed Insights
    st.markdown("""
    ### Key Environmental Insights
    - Global forest cover continues to decline
    - Biodiversity loss varies by region
    - Conservation efforts can mitigate environmental degradation
    """)


if __name__ == "__main__":
    main()