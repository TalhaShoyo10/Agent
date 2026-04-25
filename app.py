from ui.gradio import demo
from agent.agent_setup import get_agent
from rag.get_namespace import get_namespace
from pathlib import Path

get_agent(None)
get_namespace(None)
demo.queue().launch(allowed_paths=[str(Path(__file__).parent / "graphics"), str(Path(__file__).parent / "images")])