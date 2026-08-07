from datetime import datetime

from app.config import settings
from app.agents.summary_agent import SummaryAgent
from app.database.repositories.message_repository import MessageRepository
from app.database.repositories.summary_repository import SummaryRepository

class SummaryMemory:

    def __init__(self, ollama_client):

        self.summary_repo = SummaryRepository()
        self.message_repo = MessageRepository()
        self.summary_agent = SummaryAgent(ollama_client)

    def should_summarize(
                    self,
                    conversation_count: int,
                    last_summary_until: int,
                ) -> tuple[bool, int | None]:

        """
        Decide whether a new conversation summary should be generated.

        Returns:
            (True, start_message_num)  -> Generate summary
            (False, None)              -> Do nothing
        """

        trigger_count = (
                        settings.summary_settings.STEP_THRESHOLD
                        + last_summary_until
                    )

        if conversation_count == trigger_count:
            return True, last_summary_until + 1

        return False, None

    def update_summary(self, session_id: str) -> None:

        conversation_count = self.message_repo.fetch_conversation_count(session_id)

        last_summary = self.summary_repo.fetch_last_summary_by_session_id(session_id)

        if last_summary:
            last_summary_until = last_summary.covers_until_message_id
            previous_summary = last_summary.messages_summary
            summary_version = last_summary.summary_version + 1
        else:
            last_summary_until = 0
            previous_summary = None
            summary_version = 1

        summarize, start_message_num = self.should_summarize(
                                conversation_count=conversation_count,
                                last_summary_until=last_summary_until,
                            )

        print(f"start_message_num: {start_message_num}")
        if summarize:

            print(f"summarize: {summarize}")

            offset = start_message_num - 1

            conversation = self.message_repo.fetch_messages_range(
                session_id=session_id,
                offset=offset,
            )

            print(f"conversion: {conversation}")

            summary = self.summary_agent.generate_summary(
                new_conversation=conversation,
                previous_summary=previous_summary,
            )

            covers_until_message_id = conversation_count - settings.summary_settings.KEEP_LAST_MESSAGES

            self.summary_repo.insert_summary(
                session_id=session_id,
                summary_version=summary_version,
                messages_summary=summary,
                covers_until_message_id=covers_until_message_id,
                created_at=datetime.now(),
            )

if __name__ == "__main__":

    from app.llm.ollama_call import OllamaClient

    ollama = OllamaClient()

    summary_memory = SummaryMemory(ollama.client)

    session_id = "7a364242-a2a9-488f-a311-117d1b3c21c5"

    summary = summary_memory.update_summary(session_id)

    print(summary)