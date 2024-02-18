import streamlit as st
from streamlit_javascript import st_javascript
import base64
import tempfile

st.title('IFC File Viewer with Streamlit JavaScript')

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

    # Prepare JavaScript code for execution
    js_code = f"""
        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.height = '600px';
        document.body.appendChild(container);

        import('https://unpkg.com/ifc/web-ifc-viewer@0.0.29/dist/ifc-viewer-api.js').then((module) => {{
            const IfcViewerAPI = module.default;
            const viewer = new IfcViewerAPI({{
                container: container,
                backgroundColor: [255, 255, 255]
            }});
            viewer.IFC.setWasmPath('https://unpkg.com/ifc/');
            viewer.shadowDropper.isEnabled = false;
            viewer.grid.setGrid();
            viewer.axes.setAxes();

            (async () => {{
                const response = await fetch('data:;base64,{base64_file}');
                const buffer = await response.arrayBuffer();
                await viewer.IFC.loadIfc(buffer, false);
                console.log('Model loaded successfully');
            }})().catch(console.error);
        }}).catch(console.error);
    """

    # Execute JavaScript code
    result = st_javascript(js_code)
else:
    st.write("Upload an IFC file to view it.")
