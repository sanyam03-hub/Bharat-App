import streamlit as st
from core.query_parser import parse_query
from core.data_integrator import generate_answer
from utils.constants import INDIAN_STATES

# Set page configuration for better desktop experience
st.set_page_config(
    page_title="Project Samarth - Agri & Climate Data Q&A",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS for a modern, professional look
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1f25 100%);
        color: #e6e6e6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    header {
        background: linear-gradient(90deg, #1a1f25 0%, #262730 100%) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Main title styling */
    h1 {
        color: #4fc3f7 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1f25 0%, #262730 100%);
        border-right: 1px solid #4a4a4a;
    }
    
    .css-1d391kg h2 {
        color: #4fc3f7;
        border-bottom: 2px solid #4a4a4a;
        padding-bottom: 10px;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background-color: #2d3746;
        color: #fafafa;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4fc3f7;
        box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #262730 0%, #1a1f25 100%) !important;
        color: #4fc3f7 !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1a1f25 0%, #262730 100%) !important;
        border: 1px solid #4fc3f7 !important;
        box-shadow: 0 4px 10px rgba(79, 195, 247, 0.3);
        transform: translateY(-2px);
    }
    
    /* Info boxes */
    .css-1ei68bg {
        background: linear-gradient(135deg, #262730 0%, #1a1f25 100%);
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Example queries styling */
    .example-queries {
        background: linear-gradient(135deg, #262730 0%, #1a1f25 100%);
        border-left: 4px solid #4fc3f7;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Custom sidebar sections */
    .sidebar-section {
        background: rgba(42, 47, 59, 0.7);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .sidebar-title {
        color: #4fc3f7;
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 18px;
    }
    
    /* Response container */
    .response-container {
        background: linear-gradient(135deg, #262730 0%, #1a1f25 100%);
        border-radius: 10px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        border: 1px solid #4a4a4a;
    }
    
    /* Data sources */
    .data-sources {
        background: rgba(38, 39, 48, 0.7);
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        border-left: 4px solid #4fc3f7;
    }
    
    /* Columns */
    .css-1v0mbdj {
        gap: 2rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f25;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a4a4a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4fc3f7;
    }
</style>
""", unsafe_allow_html=True)

# Main title with icon
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🌾 Project Samarth</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #bbbbbb; margin-top: 0px; margin-bottom: 30px;'>Intelligent Q&A on Indian Agriculture & Climate Data</h3>", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 2])

# Left column for query input
with col1:
    st.markdown("<h3 style='color: #4fc3f7; margin-top: 0px; margin-bottom: 15px;'>Ask Your Question</h3>", unsafe_allow_html=True)
    
    user_query = st.text_area(
        "Enter your question about agriculture or climate data:",
        height=120,
        placeholder="e.g., What is the rainfall in Maharashtra?\nCompare rice production in Punjab and Haryana..."
    )
    
    if st.button("🔍 Ask Samarth", use_container_width=True):
        if user_query.strip():
            with st.spinner("Processing your query..."):
                intent, params = parse_query(user_query)
                answer, chart, sources = generate_answer(intent, params)
                
            # Display results in the right column
            with col2:
                st.markdown("<h3 style='color: #4fc3f7; margin-top: 0px; margin-bottom: 15px;'>Response</h3>", unsafe_allow_html=True)
                st.write(answer)
                if chart:
                    st.pyplot(chart)
                
                if sources:
                    st.markdown("<div class='data-sources'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #4fc3f7; margin-top: 0px;'>Data Sources</h4>", unsafe_allow_html=True)
                    for src in sources:
                        st.markdown(f"- [{src}]({src})")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

# Right column for results (initially empty)
with col2:
    st.markdown("<h3 style='color: #4fc3f7; margin-top: 0px; margin-bottom: 15px;'>Results</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #bbbbbb; font-style: italic;'>Enter a question and click 'Ask Samarth' to see results here.</p>", unsafe_allow_html=True)

# Add sidebar with API information and all Indian states and union territories
st.sidebar.title("Project Samarth")

# Add API information box
st.sidebar.markdown("""
<div class="sidebar-section">
    <div class="sidebar-title">API Information</div>
    <div style="font-size: 14px; line-height: 1.5;">
        <b>Data Source:</b> data.gov.in<br>
        <b>Status:</b> Using mock data for demonstration<br>
        <b>Purpose:</b> Agricultural & Climate Analytics
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-title'>States & Union Territories</div>", unsafe_allow_html=True)

# Group states and UTs for better organization
states_only = INDIAN_STATES[:28]  # First 28 are states
uts_only = INDIAN_STATES[28:]     # Remaining are union territories

st.sidebar.markdown("<b>States</b>", unsafe_allow_html=True)
# Display states without gaps
states_html = "<div style='columns: 2; column-gap: 20px; font-size: 13px;'>"
for state in states_only:
    states_html += f"<div style='padding: 1px 0;'>• {state}</div>"
states_html += "</div>"
st.sidebar.markdown(states_html, unsafe_allow_html=True)

st.sidebar.markdown("<b>Union Territories</b>", unsafe_allow_html=True)
# Display UTs without gaps
uts_html = "<div style='columns: 1; column-gap: 20px; font-size: 13px;'>"
for ut in uts_only:
    uts_html += f"<div style='padding: 1px 0;'>• {ut}</div>"
uts_html += "</div>"
st.sidebar.markdown(uts_html, unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-title'>Supported Crops</div>", unsafe_allow_html=True)
# Display supported crops
supported_crops = [
    "Rice", "Wheat", "Maize", "Sugarcane", "Cotton",
    "Jowar", "Bajra", "Ragi", "Tur", "Urad",
    "Moong", "Gram", "Groundnut", "Sunflower", "Soybean",
    "Potatoes", "Jute", "Barley", "Mustard", "Peas"
]

# Display crops without gaps
crops_html = "<div style='columns: 2; column-gap: 20px; font-size: 13px;'>"
for crop in supported_crops:
    crops_html += f"<div style='padding: 1px 0;'>• {crop}</div>"
crops_html += "</div>"
st.sidebar.markdown(crops_html, unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-title'>Quick Query Examples</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size: 13px; line-height: 1.6;">
• "What is the rainfall in Maharashtra?"<br>
• "Show me rice production in Punjab"<br>
• "Compare rainfall between Karnataka and Tamil Nadu"<br>
• "Analyze correlation between wheat production and rainfall in Uttar Pradesh"<br>
• "List the top crops of type Rice in Maharashtra and Punjab"
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)