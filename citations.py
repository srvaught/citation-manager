import asyncio
import nest_asyncio
import streamlit as st
import requests
import spacy
import re
import docx
from sentence_transformers import SentenceTransformer
import pdfplumber
from fuzzywuzzy import fuzz

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file while handling multi-column layouts.
    """
    text = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text.append(extracted_text)
    return "\n".join(text)

# Function to extract text from DOCX (Word files)
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_citations(text):
    """
    Extracts legal citations from text using regex and NLP.
    """

    regex_patterns = [
        # 🔹 U.S. Supreme Court Cases (e.g., Brown v. Board of Education, 347 U.S. 483 (1954))
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?),?\s*(\d{1,4}\sU\.S\.\s\d{1,5})\s*\((\d{4})\)",

        # 🔹 Federal Reporter (e.g., Doe v. United States, 419 F.3d 1058 (9th Cir. 2005))
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?),?\s*(\d{1,4}\sF\.3d\s\d{1,5})\s*\((\d{4})\)",

        # 🔹 Federal Reporter (Older cases, F.2d format)
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?),?\s*(\d{1,4}\sF\.2d\s\d{1,5})\s*\((\d{4})\)",

        # 🔹 State Court Citations (e.g., People v. Anderson, 6 Cal.3d 628 (1972))
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?),?\s*(\d{1,4}\sCal\.\d+\s\d+)\s*\((\d{4})\)",

        # 🔹 Other State Court Citations (e.g., People v. Goetz, 68 N.Y.2d 96 (1986))
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?),?\s*(\d+\sN\.Y\.2d\s\d+)\s*\((\d{4})\)",

        # 🔹 General Case Name Pattern (e.g., Citizens United v. FEC)
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?\s+v\.\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*(?:\s(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.))?)",
    ]

    matches = []
    for pattern in regex_patterns:
        matches.extend(re.findall(pattern, text))

    citations = set()
    for match in matches:
        citation = "".join([m for m in match if m]).strip()
        citations.add(citation)

    return sorted(citations)



def format_case_query(case_name):
    """
    Formats a case name to extract only the last word of the first name and 
    the first word of the second name.
    
    Example:
    - "Tinker v. Des Moines Independent Community School District" → "Tinker v. Des"
    - "Brown v. Board of Education" → "Brown v. Board"
    - "Citizens United v. FEC" → "Citizens United v. FEC" (does not remove "FEC")
    - "New York Times Co. v. Sullivan" → "New York Times v. Sullivan" (removes "Co.")
    """
    words = case_name.split()

    # Remove abbreviations like "Co." or "Inc."
    words = [w for w in words if w.lower() not in ["co.", "inc.", "llc", "ltd", "corp."]]

    if "v." in words:  
        v_index = words.index("v.")
        if v_index > 0 and v_index < len(words) - 1:
            first_part = words[v_index - 1]  # Last word before "v."
            second_part = words[v_index + 1]  # First word after "v."
            return f"{first_part} v. {second_part}"  

    return case_name  

def clean_case_name(case_name):
    """
    Removes corporate suffixes (Inc., Co., Corp., Ltd.) for better API search.
    """
    return re.sub(r"\b(?:Inc\.|Co\.|Corp\.|LLC\.|Ltd\.)\b", "", case_name).strip()

def fetch_cases_using_api(citation):
    """
    Fetches multiple relevant case details from CourtListener and ranks them by relevance.
    """
    case_match = re.match(r"([A-Z][a-zA-Z]+ v\. [A-Z][a-zA-Z]+)", citation)
    if case_match:
        query = clean_case_name(case_match.group(1))
    else:
        query = clean_case_name(citation)

    search_url = "https://www.courtlistener.com/api/rest/v4/search/"
    params = {"q": query, "page_size": 5}  # Retrieve up to 5 relevant cases

    try:
        response = requests.get(search_url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return []

        # Rank results by fuzzy matching score
        ranked_cases = sorted(
            data["results"],
            key=lambda case: fuzz.ratio(query, case.get("caseName", "Unknown Case")),
            reverse=True
        )

        # Format case details into a list
        cases = [
            {
                "Case Name": case.get("caseName", "Unknown Case"),
                "Citation": case["citation"][0] if isinstance(case.get("citation"), list) and case.get("citation") else "Unknown Citation",
                "Court": case.get("court", "Unknown Court"),
                "Decision Date": case.get("dateFiled", "Unknown Date"),
                "Docket Number": case.get("docketNumber", "Unknown Docket"),
                "URL": f"https://www.courtlistener.com{case.get('absolute_url', '')}",
            }
            for case in ranked_cases
        ]

        return cases

    except requests.exceptions.RequestException as e:
        return [{"Error": f"API request failed: {str(e)}"}]






nest_asyncio.apply()

try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Load NLP model
nlp = spacy.load("en_core_web_sm")
embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Load Sentence-Transformer for semantic search

# Set up API Key
API_KEY = "3f2f4836a121d7081383cb0b48b3b36532c5f67d"
HEADERS = {"Authorization": f"Token {API_KEY}", "Accept": "application/json"}
COURTS_API = "https://www.courtlistener.com/api/rest/v4/courts/"


# Streamlit UI
st.title("📄 Legal Citation Lookup Tool (NLP Enhanced)")
st.write("Upload a PDF or DOCX document or enter a citation manually.")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    with st.spinner(f"Extracting text from {file_type.upper()}..."):
        extracted_text = extract_text_from_pdf(uploaded_file) if file_type == "pdf" else extract_text_from_docx(uploaded_file)

    if extracted_text:
        st.text_area("Extracted Text", extracted_text[:2000], height=300)
        citations = extract_citations(extracted_text)

        if citations:
            st.write("### 📌 Detected Citations:")
            selected_citation = st.selectbox("Select a citation to look up:", citations)

            if st.button("Fetch Cases"):
                cases = fetch_cases_using_api(selected_citation)
                if not cases:
                    st.warning("No matching cases found.")
                else:
                    st.session_state["cases"] = cases  # Store cases in session state

            # Check if cases exist in session state before allowing selection
            if "cases" in st.session_state and st.session_state["cases"]:
                cases = st.session_state["cases"]
                case_options = [f"{case['Case Name']} ({case['Citation']})" for case in cases]

                selected_case_index = st.selectbox(
                    "Select the most relevant case:", 
                    range(len(case_options)), 
                    format_func=lambda i: case_options[i],
                    key="selectbox_upload"  # For file upload flow
                )


                # Store selected case index in session state
                st.session_state["selected_case_index"] = selected_case_index

                if st.button("Show Selected Case Details", key="show_selected_from_upload"):
                    selected_case = cases[st.session_state["selected_case_index"]]

                    st.write("### 📌 Selected Case Details")
                    for key, value in selected_case.items():
                        if key != "URL":
                            st.write(f"**{key}**: {value}")
                    st.markdown(f"[🔗 View Full Case]({selected_case['URL']})")

        else:
            st.warning("No legal citations found in the document.")
    else:
        st.error("Failed to extract text from the document.")

# Manual citation input
citation_input = st.text_input("Or enter a citation manually (e.g., 384 U.S. 436)")

if st.button("Search Cases"):
    if citation_input:
        cases = fetch_cases_using_api(citation_input)
        if not cases:
            st.warning("No matching cases found.")
        else:
            st.session_state["cases"] = cases  # Store cases in session state

    if "cases" in st.session_state and st.session_state["cases"]:
        cases = st.session_state["cases"]
        case_options = [f"{case['Case Name']} ({case['Citation']})" for case in cases]

        selected_case_index = st.selectbox(
            "Select the most relevant case:", 
            range(len(case_options)), 
            format_func=lambda i: case_options[i],
            key="selectbox_manual"  # For manual citation flow
        )


        # Store selected case index in session state
        st.session_state["selected_case_index"] = selected_case_index

        if st.button("Show Selected Case Details", key="show_selected_from_manual"):
            selected_case = cases[st.session_state["selected_case_index"]]

            st.write("### 📌 Selected Case Details")
            for key, value in selected_case.items():
                if key != "URL":
                    st.write(f"**{key}**: {value}")
            st.markdown(f"[🔗 View Full Case]({selected_case['URL']})")
    else:
        st.warning("Please enter a citation.")
