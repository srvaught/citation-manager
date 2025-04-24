Download Python 3.8+
https://www.python.org/downloads/

Download Git
https://git-scm.com/downloads

Download Microsoft C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Run PowerShell as administrator:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

```bash
git clone https://github.com/srvaught/citation-manager.git
```

```bash
cd citation-manager
```

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
python -m spacy download en_core_web_sm
```

```bash
streamlit run citations.py
```

URL to visit: http://localhost:8501
