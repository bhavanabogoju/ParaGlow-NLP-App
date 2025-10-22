# src/utils.py
import yaml

def load_config(config_path="config.yaml"):
    """
    Loads the config.yaml file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_css(file_path):
    """
    Loads a CSS file and returns it as a string
    to be injected into Streamlit.
    """
    with open(file_path) as f:
        return f.read()