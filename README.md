## 🔹 Step 1: Install Prerequisites
Before setting up the project, ensure you have the following installed on your system:

### Required Software:
- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)
- **Git** → [Download Git](https://git-scm.com/downloads)
- **pip** (comes with Python)

To verify installations, run the following in **Command Prompt (Windows)** or **Terminal (Mac/Linux)**:
```bash
python --version  # Should return Python 3.8+
git --version     # Should return Git version
```

---

## Step 2: Clone the GitHub Repository
To download the project, run the following command in **Command Prompt (Windows)** or **Terminal (Mac/Linux)**:

```bash
git clone https://github.com/YOUR-USERNAME/legal-citation-manager.git
```

Then, navigate into the project directory:
```bash
cd legal-citation-manager
```

---

## 🔹 Step 3: Create a Virtual Environment
It is recommended to create a **virtual environment** to manage dependencies.

```bash
python -m venv citation_env  # Creates a virtual environment
```

Activate the virtual environment:
- **Windows:**
  ```bash
  citation_env\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source citation_env/bin/activate
  ```

You should now see `(citation_env)` at the beginning of your terminal prompt.

---

## 🔹 Step 4: Install Dependencies
With the virtual environment activated, install required Python libraries:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not included, manually install dependencies:
```bash
pip install streamlit requests spacy docx pdfplumber fuzzywuzzy nest_asyncio sentence-transformers
```

---

## Step 5: Run the Application
To start the **Legal Citation Manager**, use:
```bash
streamlit run citations.py
```

This will launch the Streamlit app, and you’ll see an output like:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```
Open this **URL in your browser** to use the application.
