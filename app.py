# app.py
import streamlit as st
import os
import sys
from dotenv import load_dotenv

# --- Imports are updated with new module names ---
from src.logger import logger
from src.exception import CustomException
from src.utils import load_config, load_css

# --- This is the main import update ---
from src.mvp.processor import ParaGlowProcessor

# -------------------------
# Load Config & Env
# -------------------------
logger.info("Application starting...")
try:
    # Load config from config.yaml
    config = load_config()
    load_dotenv() # Load keys from .env

    HF_API_KEY = os.getenv("HF_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Get the CSS file path from our config
    CSS_PATH = config['artifacts']['style_css_path']

except Exception as e:
    # Use our new custom exception for error logging
    raise CustomException(e, sys)

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(
    page_title="ParaGlow",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Load CSS
# -------------------------
try:
    # Load the external CSS file using our util function
    st.markdown(f"<style>{load_css(CSS_PATH)}</style>", unsafe_allow_html=True)
    logger.info("Custom CSS loaded successfully.")
except Exception as e:
    logger.error(f"Error loading CSS: {e}")
    st.error("Error: Could not load page styling.")

# -------------------------
# Helper: pipeline loader
# -------------------------
@st.cache_resource
def get_pipeline():
    logger.info("Attempting to load ParaGlowProcessor...")
    # --- Use the new class name ---
    return ParaGlowProcessor()

# If API key missing -> stop
if not HF_API_KEY:
    logger.error("HF_API_KEY is missing from .env file.")
    st.markdown(
        "<div class='neo-card'><h3 style='margin:0'>⚠️ Missing Hugging Face API Key</h3>"
        "<p style='color: var(--text-secondary); margin-top: 12px;'>Add <code>HF_API_KEY</code> to your .env and restart. The UI is ready; the backend needs the key.</p></div>",
        unsafe_allow_html=True
    )
    st.stop()

# Try to initialize the pipeline
try:
    pipeline = get_pipeline()
    pipeline_ready = True
    logger.info("ParaGlowProcessor loaded successfully.")
except Exception as e:
    pipeline = None
    pipeline_ready = False
    logger.error(f"Failed to initialize ParaGlowProcessor.")
    CustomException(e, sys)
    st.error(f"Failed to initialize ParaGlowProcessor. Check logs for details.")

# -------------------------
# Modern Header
# -------------------------
st.markdown(
    "<div class='neo-card' style='margin-bottom:16px;'>"
    "<div class='header-row'>"
    "<div style='display:flex;flex-direction:column;'>"
    "<div style='display:flex;align-items:center;gap:12px;'>"
    "<div style='font-size:30px'>📝</div>"

    # --- Title is updated ---
    "<div><div class='app-title'>ParaGlow – Reimagine Your Words</div></div>"

    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# --- START: Main Content Area (Ensure this section is correct) ---
# -------------------------
# Main Content Area
# -------------------------
col1, col2 = st.columns([1, 1], gap="large")

# --- Column 1: Input and Analytics ---
with col1:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📄 Input Text</div>", unsafe_allow_html=True)

    input_text = st.text_area(
        "text_input",
        height=300, # Made this a bit shorter to make room
        placeholder="Paste your article, notes, or any text...",
        label_visibility="collapsed"
    )

    # --- NEW: LIVE ANALYTICS DASHBOARD ---
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

    # Calculate stats (ensure correct indentation here)
    if input_text:
        word_count = len(input_text.split())
        char_count = len(input_text)
        # Avg reading speed is ~200 words per minute
        reading_time = round(word_count / 200, 2) if word_count > 0 else 0
    else:
        word_count = 0
        char_count = 0
        reading_time = 0

    # Display stats in 3 columns
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.metric(label="Word Count", value=f"{word_count:,}")
    with stat_col2:
        st.metric(label="Character Count", value=f"{char_count:,}")
    with stat_col3:
        st.metric(label="Reading Time (min)", value=f"{reading_time}")

    # --- END OF ANALYTICS FEATURE ---

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True) # Spacer

    # Buttons are now below the stats
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        summarize_btn = st.button("✨ Summarize", use_container_width=True)
    with button_col2:
        paraphrase_btn = st.button("🔄 Paraphrase", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
# --- END OF COLUMN 1 ---


# --- Column 2: Output ---
with col2:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Output</div>", unsafe_allow_html=True)

    # Initialize session state if needed
    if 'last_action' not in st.session_state:
        st.session_state.last_action = None
    if 'output_text' not in st.session_state:
        st.session_state.output_text = ""
    if 'last_triggered' not in st.session_state: # Track which button caused the output
         st.session_state.last_triggered = ""

    # Check which button was pressed (ensure correct indentation here)
    method = st.session_state.get('summarization_method', 'Abstractive') # Get sidebar value safely
    length = st.session_state.get('summary_length', 'Medium') # Get sidebar value safely

    if summarize_btn:
        st.session_state.last_action = 'summarize'
        st.session_state.last_triggered = 'summarize' # Record button press
    if paraphrase_btn:
        st.session_state.last_action = 'paraphrase'
        st.session_state.last_triggered = 'paraphrase' # Record button press

    # Process based on last action and input text
    if not input_text:
        st.info("👈 Enter text in the input panel and select an action")
        st.session_state.output_text = "" # Clear output if input is empty
    elif st.session_state.last_action: # Only process if an action was triggered *this run*
        action = st.session_state.last_action
        if action == 'summarize':
            if not pipeline_ready:
                st.error("Summarization backend not available. Check API key and pipeline logs.")
                st.session_state.output_text = ""
            else:
                with st.spinner("🔮 Generating your summary..."):
                    try:
                        logger.info(f"Generating summary. Method: {method}, Length: {length}")
                        summary = pipeline.summarize(input_text, method=method.lower(), length=length.lower())
                        st.session_state.output_text = f"✅ Summary generated successfully!\n\n{summary}" # Store result with success message
                        logger.info("Summary generated.")
                    except Exception as e:
                        CustomException(e, sys)
                        st.error("An error occurred while generating the summary. Check logs for details.")
                        st.session_state.output_text = ""

        elif action == 'paraphrase':
            if not pipeline_ready or pipeline.paraphraser is None: # Check if paraphraser is loaded
                st.error("Paraphrase backend not available. Check API key and pipeline logs.")
                st.session_state.output_text = ""
            else:
                with st.spinner("🔮 Paraphrasing your text..."):
                    try:
                        logger.info("Generating paraphrase...")
                        paraphrased = pipeline.paraphrase(input_text)
                        st.session_state.output_text = f"✅ Paraphrase completed successfully!\n\n{paraphrased}" # Store result with success message
                        logger.info("Paraphrase generated.")
                    except Exception as e:
                        CustomException(e, sys)
                        st.error("An error occurred while paraphrasing. Check logs for details.")
                        st.session_state.output_text = ""

        # Reset last action after processing to prevent re-running on refresh
        st.session_state.last_action = None

    # Display the stored output text (or initial message)
    if st.session_state.output_text:
        is_success = st.session_state.output_text.startswith("✅")

        if is_success:
             st.success(st.session_state.output_text.split("\n\n", 1)[0]) # Show success message separately
             # Ensure there's content after the success message before splitting
             output_display = st.session_state.output_text.split("\n\n", 1)[1] if "\n\n" in st.session_state.output_text else ""
        else:
             # If it's not a success message (e.g., error or initial info), display it directly
             output_display = st.session_state.output_text

        st.text_area("output_display", value=output_display, height=350, label_visibility="collapsed", key="output_area") # Use key to prevent rerender issues

        # Only show download button if there's actual text content
        if output_display:
            st.download_button(
                 label=f"⬇️ Download {'Summary' if st.session_state.last_triggered == 'summarize' else 'Paraphrase'}",
                 data=output_display,
                 file_name=f"{st.session_state.last_triggered}.txt",
                 mime="text/plain",
                 use_container_width=True
             )
    # If no output and no input, show the initial message
    elif not input_text:
        st.info("👈 Enter text in the input panel and select an action")


    st.markdown("</div>", unsafe_allow_html=True)
# --- END OF COLUMN 2 ---
# --- END: Main Content Area ---

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ Configuration</div>", unsafe_allow_html=True)

    # --- Radio Buttons for Summarization Method ---
    # Retrieve value from session state if it exists, otherwise use index
    method_index = 1 if st.session_state.get('summarization_method', 'Abstractive') == 'Abstractive' else 0
    method = st.radio(
        "Summarization Method",
        ["Extractive", "Abstractive"],
        index=method_index, 
        key='summarization_method', # Key to store selection in session state
        help="Choose how the summary is generated: Extractive picks sentences, Abstractive creates new ones."
    )

    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    # --- Slider for Summary Length ---
    length_options = ["Short", "Medium", "Long"]
    length = st.select_slider(
        "Summary Length",
        options=length_options,
        value=st.session_state.get('summary_length', 'Medium'), # Retrieve value or default
        key='summary_length', # Key to store selection
        help="Control the approximate length of the generated summary."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Status Card ---
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔐 System Status</div>", unsafe_allow_html=True)

    if pipeline_ready:
        st.markdown(
            "<div class='status-badge status-success'>✓ Pipeline Active</div>",
            unsafe_allow_html=True
        )
        # Display partial API key for confirmation (if key exists)
        if HF_API_KEY:
             st.caption(f"🔑 HF Key: `{HF_API_KEY[:4]}...{HF_API_KEY[-4:]}`")
        if GROQ_API_KEY:
             st.caption(f"🔑 Groq Key: `{GROQ_API_KEY[:4]}...{GROQ_API_KEY[-4:]}`")

    else:
        st.markdown(
            "<div class='status-badge status-error'>✗ Pipeline Error</div>",
            unsafe_allow_html=True
        )
        st.caption("Check terminal logs for details.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Modern Footer
# -------------------------
st.markdown(
    """
    <div class='footer'>
        Built with <span class='footer-highlight'>♥</span> using Streamlit, Hugging Face & Groq
        <br>
        <span style='font-size: 12px; color: var(--text-muted);'>ParaGlow UI • 2025</span>
    </div>
    """,
    unsafe_allow_html=True,
)