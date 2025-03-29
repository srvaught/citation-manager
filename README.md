# 📄 Legal Citation Manager - Setup Guide

## 🚀 Overview
The **Legal Citation Manager** is a Python-based tool that extracts and looks up legal case citations from PDF and DOCX documents. It uses **Streamlit** for an interactive UI and integrates with **CourtListener API** to fetch case details.

---

## 🔹 Step 1: Install Prerequisites
Before setting up the project, ensure you have the following installed on your system:

### ✅ Required Software:
- **Python 3.8+** → [Download Python](https://www.python.org/downloads/)
- **Git** → [Download Git](https://git-scm.com/downloads)
- **pip** (comes with Python)

To verify installations, run the following in **Command Prompt (Windows)** or **Terminal (Mac/Linux)**:
```bash
python --version  # Should return Python 3.8+
git --version     # Should return Git version
```

---

## 🔹 Step 2: Clone the GitHub Repository
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

## 🔹 Step 5: Run the Application
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

---

## 🔹 Step 6: Usage Guide
### 📌 **How to Use**:
1. **Upload** a PDF or DOCX document.
2. The tool **extracts legal citations** from the document.
3. Select a **citation** from the list.
4. Click **Fetch Cases** to get relevant case details.
5. Choose the correct case and click **Show Selected Case Details** to view case information.

### 📝 **Manual Citation Search**:
- Enter a citation manually (e.g., `384 U.S. 436`)
- Click **Search Cases** to find relevant case details.

---

## 🔹 Step 7: Updating the Project
To update the project with the latest changes from GitHub:
```bash
git pull origin main
```

To apply updates after making changes:
```bash
git add .
git commit -m "Updated citation extraction logic"
git push origin main
```

---

## 🔹 Troubleshooting
### ❓ **Common Issues & Fixes**

| Issue | Solution |
|--------|----------|
| `streamlit: command not found` | Ensure the virtual environment is activated (`citation_env\Scripts\activate` on Windows, `source citation_env/bin/activate` on Mac/Linux) |
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` to install missing dependencies |
| `Git is not recognized as a command` | Ensure Git is installed and added to system PATH |

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🚀 Next Steps
- ⭐ **Star the repo** on GitHub if you find it useful!
- **Contribute:** Fork the repository and submit pull requests.
- **Report Issues:** If you encounter bugs, report them under GitHub Issues.

**Enjoy using the Legal Citation Manager!** 🎉

