from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class ApplicationSettings(BaseModel):

    app_name: str = "AI Personal ChatBot"
    page_title: str = "AI Personal ChatBot"
    page_icon: str = "🤖"

class LLMSettings(BaseModel):

    example_query: str = "Hello, how are you?"
    provider: str = "ollama"
    # model_name: str = "llama3.1:8b"
    model_name: str = "gemma2:2b"
    stream: bool = True
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0
    )

class Settings(BaseSettings):

    app: ApplicationSettings = ApplicationSettings()
    llm: LLMSettings = LLMSettings()

settings = Settings()
    
    