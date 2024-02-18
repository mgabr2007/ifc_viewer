import streamlit as st
from streamlit_javascript import st_javascript

st.title('IFC File Viewer with IFC.js')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    # Convert uploaded file to Base64 to inline it directly in the HTML
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    file_data = f"data:application/octet-stream;base64,{base64_file}"

    # JavaScript code to initialize IFC.js viewer and load the IFC model
    js_code = f"""
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '600px';
    document.body.appendChild(container);

    import('https://unpkg.com/ifc/web-ifc-viewer.js').then((module) => {{
        const IfcViewerAPI = module.default;
        const viewer = new IfcViewerAPI({{ container }});
        viewer.shadowDropper.isEnabled = false;
        viewer.grid.setGrid();
        viewer.axes.setAxes();

        // Load the model from the Base64 string
        viewer.IFC.loadFromString("{file_data}", true).then((model) => {{
            console.log('Model loaded', model);
        }}).catch((error) => {{
            console.error('Error loading model:', error);
        }});
    }});

    return "IFC model is being loaded...";
    """

    # Use st_javascript to execute the JavaScript code
    result = st_javascript(js_code)
    if result:
        st.success("IFC model loaded successfully.")
else:
    st.write("Upload an IFC file to view it.")
