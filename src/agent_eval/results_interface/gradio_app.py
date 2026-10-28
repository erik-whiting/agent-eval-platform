"""Optional read-only viewer: python -m agent_eval.results_interface.gradio_app PATH."""
import sys
from pathlib import Path
from agent_eval.results_interface.summary import load_records, summarize

def main():
    import gradio as gr
    records = load_records(Path(sys.argv[1]))
    with gr.Blocks(title="Agent Evaluation Results") as app:
        gr.Markdown("# Agent evaluation results\nOffline smoke results are not research findings.")
        gr.JSON(value=summarize(records), label="Configuration summary")
        gr.JSON(value=records, label="Run records")
    app.launch(server_name="127.0.0.1", share=False)

if __name__ == "__main__":
    main()
