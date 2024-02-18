import streamlit as st
import base64
import tempfile

st.title('IFC File Viewer')

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ifc') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name  # Return the path of the saved file

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    # Save uploaded file to a temporary file and get the path
    temp_file_path = save_uploaded_file(uploaded_file)

    # Convert uploaded file to Base64 for the viewer
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    file_data = f"data:application/octet-stream;base64,{base64_file}"

    # JavaScript code to load the IFC model into the viewer
    js_code = f"""
    <div id="ifc-container" style="width: 100%; height: 600px;"></div>
    <script type="module">
        import IfcViewerAPI from "https://unpkg.com/ifc/web-ifc-viewer@0.0.29/dist/ifc-viewer-api.js";
        
        const viewer = new IfcViewerAPI({{
            container: document.getElementById('ifc-container'),
            backgroundColor: [255, 255, 255]
        }});
        viewer.IFC.setWasmPath("https://unpkg.com/ifc/");
        viewer.shadowDropper.isEnabled = false;
        viewer.grid.setGrid();
        viewer.axes.setAxes();

        async function loadModel(base64) {{
            const response = await fetch(base64);
            const buffer = await response.arrayBuffer();
            return viewer.IFC.loadIfc(buffer, false);
        }}

        loadModel("{file_data}").then(model => {{
            console.log("Model loaded", model);
        }}).catch(error => {{
            console.error("Error loading model:", error);
        }});
    </script>
    """
    # Use Streamlit's HTML component to render the custom HTML with JavaScript
    st.components.v1.html(js_code, height=600, scrolling=True)
else:
    st.write("Upload an IFC file to view it.")
