I can certainly generate a highly detailed README.md for your ParaGlow project that strictly adheres to the format, style, and structure of the advanced example you provided.This version incorporates all your refactored module names and the new features (like the analytics dashboard) into the detailed, professional template.ParaGlow – Reimagine Your WordsAn AI-powered text transformation system built with Streamlit, Groq, and Hugging Face. ParaGlow provides high-speed, intelligent summarization and advanced text rephrasing capabilities through a modern, responsive user interface.

🚀 FeaturesIntelligent Summarization: Provides two distinct modes: Abstractive (Hugging Face BART) and Extractive.High-Speed Paraphrasing: Leverages Groq's LPU-based architecture for near-instant text rephrasing.Live Text Analytics: A new feature that displays real-time word count, character count, and estimated reading time beneath the input box.Dynamic UI: Custom, modern interface built with external CSS for easy themeing.Scalable Architecture: Code is fully refactored into modular components (src) for better maintainability.

🏗️ ArchitectureInfosys_Data_Preprocessing-main/
├── app.py                          # Main Streamlit application entry point
├── config.yaml                     # Configuration settings (file paths, artifacts)
├── style.css                       # All custom CSS styling and themes
├── README.md                       # This file
├── requirements.txt                # Python dependencies
│
├── logs/
│   └── app.log                     # Central application log file
│
└── src/
    ├── __init__.py                 # Python package marker
    ├── exception.py                # Custom exception handling class (logs detailed tracebacks)
    ├── logger.py                   # Centralized application logging setup
    ├── utils.py                    # Utility functions (load_config, load_css)
    │
    └── mvp/
        ├── processor.py            # Main Model Processor (initializes and calls worker classes)
        ├── hf_summarizer.py        # Abstractive summarizer module (Hugging Face API calls)
        ├── text_extractor.py       # Extractive summarizer module
        └── groq_rewriter.py        # Groq paraphraser module (Groq API calls)
🛠️ Tech StackComponentTechnologyRoleFrontendStreamlitRapidly built web interface and reactive UIBackendPython 3.10+Core application logic and API integrationAI/LLMHugging Face BARTProvides Abstractive Summarization capabilityInferenceGroq (LPU)Provides high-speed, low-latency ParaphrasingConfigurationPyYAML, python-dotenvManages structured settings and sensitive environment variables📋 PrerequisitesPython 3.10 or higherA Hugging Face Account & API KeyA Groq Account & API Key🔧 InstallationLocal DevelopmentClone the repositoryBashgit clone <your-repository-url>
cd Infosys_Data_Preprocessing-main
Create and activate virtual environmentBashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependenciesBashpip install -r requirements.txt
Set up environment variablesCreate a .env file in the root directory:Ini, TOMLHF_API_KEY="YOUR_HUGGINGFACE_KEY_GOES_HERE"
GROQ_API_KEY="YOUR_GROQ_KEY_GOES_HERE"
Start the applicationBashstreamlit run app.py
Access the applicationOpen your browser and navigate to: http://localhost:8501📊 ConfigurationThe application uses a configuration system centralized in config.yaml and loaded via src/utils.py. Key settings include:log_file_path: Defines the path for detailed application logging.style_css_path: Defines the path to the custom UI theme file (style.css).🔄 Model Processor PipelineThe ParaGlowProcessor is the core engine, handling secure model initialization:Key Loading: Loads HF_API_KEY and GROQ_API_KEY from the environment.Model Instantiation: Creates separate instances of HFSummarizer, TextExtractor, and GroqRewriter.Flow Management: Directs input text to the correct model based on the user's selected mode (Summarize/Paraphrase).🤖 API UsageAlthough this is a Streamlit app, the core logic is accessible via Python.Example Function CallPython# Assuming the necessary dependencies are installed
from src.mvp.processor import ParaGlowProcessor
import os

processor = ParaGlowProcessor(os.getenv("HF_API_KEY"), os.getenv("GROQ_API_KEY"))
text = "The new software update dramatically improved performance."
paraphrase_output = processor.paraphrase(text)

print(paraphrase_output)
🧪 TestingThe refactored, modular architecture allows for easy unit testing of individual components.Open a terminal with your (venv) active and your .env file present.Bash# Test the overall model integration and flow
python src/mvp/processor.py

# Test a specific component (e.g., Groq Paraphraser)
python src/mvp/groq_rewriter.py
🤝 ContributingContributions, issues, and feature requests are welcome!Fork the repositoryCreate a feature branch (git checkout -b feature/enhanced-analytics)Commit your changes (git commit -m 'Added estimated reading time metric')Push to the branch (git push origin feature/enhanced-analytics)Open a Pull Request🆘 SupportFor support or questions, please open an issue in the GitHub repository.🔮 Future EnhancementsIntegration with multi-modal LLMs for complex text analysis.Ability to summarize external documents (.pdf, .txt).Batch processing capability.Advanced controls for paraphrasing tone (e.g., "more formal," "more casual").