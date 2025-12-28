import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Lazy import to avoid loading heavy models on startup
from app.rag_pipeline import DhabiRAG
from app.ingestion import DhabiIngester
from app.analytics import analyze_feedback
import config

st.set_page_config(page_title="DhabiFeedback AI", layout="wide", page_icon="🇦🇪")

# Initialize session state for RAG to avoid reloading model
if 'rag' not in st.session_state:
    st.session_state.rag = DhabiRAG()

st.title("🇦🇪 DhabiFeedback AI")
st.markdown("**Smart City Citizen Resolution Engine** | Dubai/Abu Dhabi Government")

tab1, tab2, tab3 = st.tabs(["🔍 Query Feedback", "📊 Analytics", "⚙️ System Control"])

with tab1:
    st.header("Citizen Feedback Resolution")
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Enter citizen feedback (Arabic/English):", 
                             placeholder="e.g., Heavy traffic near Burj Khalifa or فاتورة كهرباء مرتفعة")
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🚀 Analyze & Resolve", type="primary")
    
    if analyze_btn and query:
        with st.spinner("🔍 Retrieving policies and generating action plan..."):
            try:
                # Retrieve
                docs = st.session_state.rag.retrieve(query)
                if not docs:
                    st.warning("Index is empty or no relevant documents found. Please rebuild index in System Control.")
                else:
                    # Generate
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    st.markdown("### 🏛️ Government Response")
                    
                    # Stream the response
                    for chunk in st.session_state.rag.generate_response(query, docs):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    
                    response_placeholder.markdown(full_response)
                    
                    # st.success(response) - Removed as we are streaming markdown now
                    
                    with st.expander("📄 Retrieved Policy Context (Evidence)"):
                        for i, (text, meta, score) in enumerate(docs[:3]):
                            source = meta.get('source', 'Unknown')
                            st.markdown(f"**[{i+1}] Source:** `{os.path.basename(source)}` (Relevance: {1/(1+score):.2f})")
                            st.info(text[:300] + "...")
            except Exception as e:
                st.error(f"An error occurred: {e}")

with tab2:
    st.header("City-Wide Feedback Analytics")
    if st.button("Load Analytics Data"):
        with st.spinner("Analyzing sentiment..."):
            df = analyze_feedback()
            if not df.empty and 'sentiment' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Complaints by Category")
                    fig_cat = px.pie(df, names='category', title='Feedback Distribution')
                    st.plotly_chart(fig_cat, use_container_width=True)
                
                with col2:
                    st.subheader("Sentiment Analysis")
                    fig_sent = px.bar(df, x='category', color='sentiment', title='Sentiment by Category')
                    st.plotly_chart(fig_sent, use_container_width=True)
                    
                st.dataframe(df.head(10))
            else:
                st.warning("No data available or analytics failed.")

with tab3:
    st.header("System Management")
    st.write("Manage the knowledge base and embedding index.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Rebuild Knowledge Base (Index)"):
            with st.spinner("Ingesting documents and building FAISS index..."):
                ingester = DhabiIngester()
                ingester.create_index()
                st.success("✅ Index rebuilt successfully!")
                
    with col2:
        st.info(f"**Configuration:**\n\n- Model: `{config.OLLAMA_MODEL}`\n- Index Path: `{config.FAISS_INDEX_PATH}`")

