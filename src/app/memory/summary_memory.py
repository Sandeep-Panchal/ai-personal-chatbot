from datetime import datetime

from src.config import settings
from src.app.agents.summary_agent import SummaryAgent
from src.app.database.repositories.message_repository import MessageRepository
from src.app.database.repositories.summary_repository import SummaryRepository

class SummaryMemory:

    def __init__(self):

        self.summary_repo = SummaryRepository()
        self.message_repo = MessageRepository()
        self.summary_agent = SummaryAgent()

    def should_summarize(self, session_id: str) -> tuple[bool, int | None]:
    
        """
        Decide whether a new conversation summary should be generated.

        Returns:
            (True, start_message_num)  -> Generate summary
            (False, None)              -> Do nothing
        """

        metadata = self.summary_metadata(session_id=session_id)

        trigger_count = (
            settings.summary_settings.STEP_THRESHOLD
            + metadata["last_summary_until"]
            )

        if metadata["conversation_count"] == trigger_count:
            return True, metadata["last_summary_until"] + 1

        return False, None

    def summary_metadata(self, session_id: str) -> dict:

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

        return {
            "conversation_count": conversation_count,
            "last_summary_until": last_summary_until,
            "previous_summary": previous_summary,
            "summary_version": summary_version
        }
    
    def update_summary(self, session_id: str) -> None:

        metadata = self.summary_metadata(session_id=session_id)

        conversation = self.message_repo.fetch_messages_range(
            session_id=session_id,
            offset=metadata["last_summary_until"],
        )

        summary = self.summary_agent.generate_summary(
            new_conversation=conversation,
            previous_summary=metadata["previous_summary"],
        )

        covers_until_message_id = metadata["conversation_count"] - settings.summary_settings.KEEP_LAST_MESSAGES

        self.summary_repo.insert_summary(
            session_id=session_id,
            summary_version=metadata["summary_version"],
            messages_summary=summary,
            covers_until_message_id=covers_until_message_id,
            created_at=datetime.now(),
        )

    # def should_summarize(
    #         self,
    #         conversation_count: int,
    #         last_summary_until: int,
    #     ) -> tuple[bool, int | None]:

    #     """
    #     Decide whether a new conversation summary should be generated.

    #     Returns:
    #         (True, start_message_num)  -> Generate summary
    #         (False, None)              -> Do nothing
    #     """

    #     trigger_count = (
    #                     settings.summary_settings.STEP_THRESHOLD
    #                     + last_summary_until
    #                 )

    #     if conversation_count == trigger_count:
    #         return True, last_summary_until + 1

    #     return False, None

    # def update_summary(self, session_id: str) -> None:

    #     conversation_count = self.message_repo.fetch_conversation_count(session_id)

    #     last_summary = self.summary_repo.fetch_last_summary_by_session_id(session_id)

    #     if last_summary:
    #         last_summary_until = last_summary.covers_until_message_id
    #         previous_summary = last_summary.messages_summary
    #         summary_version = last_summary.summary_version + 1
    #     else:
    #         last_summary_until = 0
    #         previous_summary = None
    #         summary_version = 1

    #     summarize, start_message_num = self.should_summarize(
    #                             conversation_count=conversation_count,
    #                             last_summary_until=last_summary_until,
    #                         )

    #     if summarize:

    #         offset = start_message_num - 1

    #         conversation = self.message_repo.fetch_messages_range(
    #             session_id=session_id,
    #             offset=offset,
    #         )

    #         summary = self.summary_agent.generate_summary(
    #             new_conversation=conversation,
    #             previous_summary=previous_summary,
    #         )

    #         covers_until_message_id = conversation_count - settings.summary_settings.KEEP_LAST_MESSAGES

    #         self.summary_repo.insert_summary(
    #             session_id=session_id,
    #             summary_version=summary_version,
    #             messages_summary=summary,
    #             covers_until_message_id=covers_until_message_id,
    #             created_at=datetime.now(),
    #         )

if __name__ == "__main__":

    from app.llm.ollama_call import OllamaClient

    ollama = OllamaClient()

    summary_memory = SummaryMemory(ollama.client)

    session_id = "7a364242-a2a9-488f-a311-117d1b3c21c5"

    summary = summary_memory.update_summary(session_id)

    print(summary)