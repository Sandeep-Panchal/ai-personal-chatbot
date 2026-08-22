from pathlib import Path

class PromptLoading:
    
    def __init__(self):
        
        self.CHAT_SYSTEM_PROMPT = "chat_system_prompt.txt"
        self.TITLE_PROMPT = "title_prompt.txt"
        self.SUMMARY_PROMPT = "summary_prompt.txt"

    def load_prompt(self, filename: Path) -> str:

        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / filename
        )

        return prompt_path.read_text(encoding="utf-8").strip()