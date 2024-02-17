import streamlit as st
from ifc_viewer import ifc_viewer

st.title('IFC File Viewer')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    ifc_viewer(uploaded_file)
