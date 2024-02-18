import streamlit as st
import base64

st.title('IFC File Viewer with IFC.js')

uploaded_file = st.file_uploader("Choose an IFC file Ya Mostafa Please", type=['ifc'])
if uploaded_file is not None:
    # Convert uploaded file to Base64 to inline it directly in the HTML
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    file_data = f"data:application/octet-stream;base64,{base64_file}"

    # Embedding IFC.js and initializing it within an HTML template
    html_code = f"""
<div id="ifc-container" style="width: 100%; height: 600px;"></div>
<script type="module">
    import IfcViewerAPI from "https://unpkg.com/ifc/web-ifc-viewer.js";
    
    const viewer = new IfcViewerAPI({{ container: document.getElementById('ifc-container'), pick: true }});
    viewer.IFC.loader.ifcManager.applyWebIfcConfig({ COORDINATE_TO_ORIGIN: true, USE_FAST_BOOLS: false });
    viewer.shadowDropper.isEnabled = false;
    viewer.grid.setGrid();
    viewer.axes.setAxes();

    async function loadModel(base64) {
        const response = await fetch(base64);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        viewer.IFC.loadIfcUrl(url);
    }

    const modelData = "data:application/octet-stream;base64,{base64_file}";
    loadModel(modelData);
</script>
"""


    # Using Streamlit's components to render the custom HTML with JavaScript
    st.components.v1.html(html_code, height=600)
else:
    st.write("Upload an IFC file to view it.")
