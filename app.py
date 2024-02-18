import streamlit as st
import base64
import ifcopenshell
import json

st.title('IFC File Viewer with Enhanced Data Processing')

# Function to process IFC file with ifcopenshell and extract relevant data
def process_ifc_file(ifc_file):
    ifc_model = ifcopenshell.open(ifc_file.name)
    # Example: Extract some basic data from the IFC file
    # This part can be customized to extract the data you're interested in
    projects = ifc_model.by_type("IfcProject")
    data = [{"name": project.Name, "description": project.Description} for project in projects]
    return json.dumps(data)  # Return data as JSON for simplicity

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    # Process the IFC file with ifcopenshell
    processed_data = process_ifc_file(uploaded_file)
    
    # Present structured IFC data in the UI
    st.json(processed_data)  # Example of presenting JSON data; customize as needed

    # Convert uploaded file to Base64 for the viewer
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    file_data = f"data:application/octet-stream;base64,{base64_file}"

    # JavaScript code remains the same to load the IFC model into the viewer
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
    # Using Streamlit's HTML component to render the custom HTML with JavaScript
    st.components.v1.html(js_code, height=600, scrolling=True)
else:
    st.write("Upload an IFC file to view it.")
