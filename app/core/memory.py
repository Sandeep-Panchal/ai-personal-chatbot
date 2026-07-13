class MemoryManager:

    def __init__(self):

        self.memory_dict = {
            "session_id": "",
            "messages": []
        }

    def get_history(self,
                    session_id: str,
                    user_message: str,
                    ai_message: str
                    ):

        if not self.memory_dict.get("session_id", ""):
            self.memory_dict["session_id"] = session_id

        if ai_message:

            assistant_msg_dict = {
                "role": "assistant",
                "content": ai_message
                }

            self.memory_dict["messages"].append(assistant_msg_dict)
        
        user_msg_dict = {
            "role": "user",
            "content": user_message
            }
        
        self.memory_dict["messages"].append(user_msg_dict)

        return self.memory_dict
    
if __name__=="__main__":

    import json
    from app.llm.ollama_call import OllamaClient

    obj = MemoryManager()
    ollama_client = OllamaClient()
    
    # for response in ollama_client.ollama_chat(settings.llm.example_query):
    #     print(response, end="", flush=True)

    run = True
    i = 0
    sess = "123"
    ai_message = None
    while run:
        i = i+1
        if i == 4:
            run = False
        
        user_message = input("Enter your query: ")

        history = obj.get_history(sess, user_message, ai_message)
        history = json.dumps(history.get("messages", ""))
        ai_message = " ".join(ollama_client.ollama_chat(history))
        print(ai_message)

    print(history)






        


