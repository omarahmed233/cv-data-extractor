import requests
import streamlit as st


st.set_page_config(page_title="CV Data Extractor", page_icon="📄", layout="centered")

st.title("CV Data Extractor")
st.write("Send a PDF path to your CV extraction API and view the extracted data.")

# API settings are kept out of the visible form.
API_URL = "https://economic-smith-gurgling.ngrok-free.dev/generate"
BEARER_TOKEN = "nothing111"

with st.form("generate_form"):
    pdf_path = st.text_input(
        "CV path",
        value="/kaggle/input/datasets/omarahmed05/cvcvcv/Omar Ahmed Abd El-Kader.pdf",
        help="This path must be accessible to the machine running the FastAPI service.",
    )
    submitted = st.form_submit_button("Extract CV data", type="primary")

if submitted:
    if not pdf_path.strip():
        st.error("Enter the CV path.")
    else:
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        payload = {"pdf_path": pdf_path.strip()}

        with st.spinner("Contacting the API…"):
            try:
                response = requests.post(
                    API_URL, headers=headers, json=payload, timeout=120
                )
            except requests.RequestException as exc:
                st.error(f"Could not reach the API: {exc}")
            else:
                try:
                    result = response.json()
                except ValueError:
                    result = {"detail": response.text or "The API returned no JSON."}

                if response.ok:
                    st.success("CV data extracted successfully.")
                    st.subheader("Extracted data")
                    extracted = result.get("response", result)
                    if isinstance(extracted, (dict, list)):
                        st.json(extracted)
                    else:
                        st.write(extracted)
                else:
                    st.error(f"Request failed (HTTP {response.status_code}).")
                    detail = result.get("detail", result) if isinstance(result, dict) else result
                    if isinstance(detail, str) and (
                        "OUTPUT_PARSING_FAILURE" in detail
                        or "invalid JSON object" in detail
                    ):
                        st.warning(
                            "The API received the request, but the CV extraction model "
                            "returned text that could not be parsed as JSON. This needs "
                            "to be fixed in the FastAPI extract_cv_data function."
                        )
                        st.code(detail)
                    elif isinstance(detail, (dict, list)):
                        st.json(detail)
                    else:
                        st.code(str(detail))
