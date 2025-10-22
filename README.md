
# P![gify](https://github.com/user-attachments/assets/458b8f62-cfe9-4114-8277-7ece42cca54f)
araGlow – Reimagine Your Words

An **AI-powered text transformation system** built with Streamlit, Groq, and Hugging Face. ParaGlow provides high-speed, intelligent summarization and advanced text rephrasing capabilities through a modern, responsive user interface.

The project utilizes a professional, **refactored, and scalable architecture**, ensuring clear separation of configuration, application logic, and styling for easy maintenance and deployment.

***

## 🚀 Features

* **Intelligent Summarization:** Provides two distinct modes: Abstractive (Hugging Face BART) and Extractive.
* **High-Speed Paraphrasing:** Leverages Groq's LPU-based architecture for near-instant text rephrasing.
* **Live Text Analytics:** A **new feature** that displays real-time word count, character count, and estimated reading time beneath the input box.
* **Dynamic UI:** Custom, modern interface built with external CSS for easy themeing.
* **Configuration-Driven:** Uses `config.yaml` for file paths and `.env` for managing secret API keys.

***

## 🏗️ Architecture

The project's structure emphasizes modularity and separation of concerns:

```

Infosys\_Data\_Preprocessing-main/
├── app.py                          \# Main Streamlit application entry point
├── config.yaml                     \# Configuration settings (file paths, artifacts)
├── style.css                       \# All custom CSS styling and themes
├── README.md                       \# This file
├── requirements.txt                \# Python dependencies
│
├── logs/
│   └── app.log                     \# Central application log file
│
└── src/
├── **init**.py                 \# Python package marker
├── exception.py                \# Custom exception handling class (logs detailed tracebacks)
├── logger.py                   \# Centralized application logging setup
├── utils.py                    \# Utility functions (load\_config, load\_css)
│
└── mvp/
├── processor.py            \# Main Model Processor
├── hf\_summarizer.py        \# Abstractive summarizer module
├── text\_extractor.py       \# Extractive summarizer module
└── groq\_rewriter.py        \# Groq paraphraser module

````

***

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Rapidly built web interface and reactive UI |
| **Backend** | Python 3.10+ | Core application logic and API integration |
| **AI/LLM** | Hugging Face BART | Provides Abstractive Summarization capability |
| **Inference** | Groq (LPU) | Provides high-speed, low-latency Paraphrasing |
| **Configuration** | `PyYAML`, `python-dotenv` | Manages structured settings and sensitive environment variables |

***

## 🔧 Installation

### Local Development

1.  **Clone the repository**
    ```bash
    git clone <your-repository-url>
    cd Infosys_Data_Preprocessing-main
    ```

2.  **Create and activate virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    Create a **`.env`** file in the root directory:
    ```ini
    HF_API_KEY="YOUR_HUGGINGFACE_KEY_GOES_HERE"
    GROQ_API_KEY="YOUR_GROQ_KEY_GOES_HERE"
    ```

5.  **Start the application**
    ```bash
    streamlit run app.py
    ```

## 🧪 Testing

The refactored architecture allows for testing individual components to ensure reliability.

*Open a terminal with your `(venv)` active and your `.env` file present.*

```bash
# Test the overall model integration and flow
python src/mvp/processor.py

# Test a specific component (e.g., Groq Paraphraser)
python src/mvp/groq_rewriter.py
````

-----

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\!

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/enhanced-analytics`)
3.  Commit your changes (`git commit -m 'Added estimated reading time metric'`)
4.  Push to the branch (`git push origin feature/enhanced-analytics`)
5.  Open a Pull Request

-----

## 🔮 Future Enhancements

  * Integration with multi-modal LLMs for complex text analysis.
  * Ability to summarize external documents (`.pdf`, `.txt`).
  * Batch processing capability.
  * Advanced controls for paraphrasing tone (e.g., "more formal," "more casual").

<!-- end list -->

```
```
