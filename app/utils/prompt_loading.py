from pathlib import Path

class PromptLoading:
    
    def __init__(self):
        
        self.SYSTEM_PROMPT = "chat_system.txt"
        self.TITLE_PROMPT = "chat_title.txt"

    def load_prompt(self, filename: Path) -> str:

        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / filename
        )

        return prompt_path.read_text(encoding="utf-8").strip()