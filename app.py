import streamlit as st
from streamlit_javascript import st_javascript
import base64

st.title('IFC File Viewer with IFC.js')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    # Convert uploaded file to Base64 to inline it in JavaScript
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    file_url = f"data:application/octet-stream;base64,{base64_file}"

    # JavaScript code to initialize IFC.js and load the uploaded model
    js_code = f"""
    const container = document.createElement("div");
    container.style = "width: 100%; height: 600px;";
    document.body.appendChild(container); // Ensure the container is appended to the body

    
    import("https://unpkg.com/ifc/web-ifc-api.js").then((ifcAPI) => {{
        const viewer = new ifcAPI.IfcViewerAPI({{ container }});
        viewer.shadowDropper.isEnabled = false; // Adjust based on your needs
        viewer.grid.setGrid();
        viewer.axes.setAxes();


        const modelData = `{file_url}`;
        viewer.loadModel(modelData, {{}}).then(model => {{
            console.log("Model loaded successfully!", model);
        }}).catch(err => console.error("Error loading model:", err));
    }});
    """

    st_javascript(js_code, height=600)
else:
    st.write("Upload an IFC file to view it.")
