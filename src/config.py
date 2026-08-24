from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class ApplicationSettings(BaseModel):

    app_name: str = "AI Personal ChatBot"
    page_title: str = "AI Personal ChatBot"
    page_icon: str = "🤖"

class LLMSettings(BaseModel):

    example_query: str = "Hello, how are you?"
    provider: str = "ollama"
    model_name: str = "gemma2:2b"
    # ollama_url: str = "http://ollama:11434"
    ollama_url: str = "http://127.0.0.1:11434"
    # model_name: str = "gemma4:latest"
    # model_name: str = "llama3.1:8b"
    stream: bool = True
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0
    )

class SummarySettings(BaseModel):
    STEP_THRESHOLD: int = 10
    KEEP_LAST_MESSAGES: int = 2

    @property
    def NEXT_MESSAGES_COUNT(self) -> int:
        return self.STEP_THRESHOLD - self.KEEP_LAST_MESSAGES

class APISettings(BaseModel):

    chat_url: str = "http://127.0.0.1:8000/api/chat"
    session_url: str = "http://127.0.0.1:8000/api/sessions"

    # chat_url: str = "http://host.docker.internal:8000/api/chat"
    # session_url: str = "http://host.docker.internal:8000/api/sessions"

    # chat_url: str = "http://backend:8000/api/chat"
    # session_url: str = "http://backend:8000/api/sessions"

    headers: dict = {
        'Content-Type': 'application/json'
        }

class Settings(BaseSettings):

    app: ApplicationSettings = ApplicationSettings()
    llm: LLMSettings = LLMSettings()
    summary_settings: SummarySettings = SummarySettings()
    api_settings: APISettings = APISettings()

settings = Settings()
    
    