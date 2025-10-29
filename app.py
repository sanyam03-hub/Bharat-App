import streamlit as st
from core.query_parser import parse_query
from core.data_integrator import generate_answer

st.title("Project Samarth – Intelligent Q&A on Agri & Climate Data")
user_query = st.text_input("Ask a question about agriculture or climate:")

if st.button("Ask Samarth"):
    intent, params = parse_query(user_query)
    answer, chart, sources = generate_answer(intent, params)
    st.write(answer)
    if chart:
        st.pyplot(chart)
    st.markdown("**Data Sources:**")
    for src in sources:
        st.markdown(f"- [{src}]({src})")