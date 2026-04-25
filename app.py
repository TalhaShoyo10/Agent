from ui.gradio import demo
from agent.agent_setup import get_agent
from rag.get_namespace import get_namespace
from pathlib import Path

css_path = Path(__file__).parent / "school_theme.css"
get_agent(None)
get_namespace(None)
demo.queue().launch()