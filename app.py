import streamlit as st
from streamlit_javascript import st_javascript

st.title('IFC File Viewer with IFC.js')

uploaded_file = st.file_uploader("Choose an IFC file", type=['ifc'])
if uploaded_file is not None:
    # Temporary save uploaded file to disk to serve it to IFC.js
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # JavaScript code to initialize IFC.js and load the uploaded model
    js_code = f"""
    const container = document.createElement("div");
    container.style = "width: 100%; height: 600px;";
    element.append(container);

    // Import IFC.js web ifc API
    import("https://unpkg.com/web-ifc/web-ifc-api.js").then((ifcAPI) => {{
        const viewer = new ifcAPI.IfcViewerAPI({{ container }});
        viewer.shadowDropper.isEnabled = false; // Adjust based on your needs
        viewer.grid.setGrid();
        viewer.axes.setAxes();

        // Load the IFC model
        viewer.IFC.loadIfcUrl("{uploaded_file.name}", false).then(() => {{
            console.log("Model loaded successfully!");
        }}).catch(err => console.error(err));
    }});
    """

    st_javascript(js_code, height=600)
else:
    st.write("Upload an IFC file to view it.")
