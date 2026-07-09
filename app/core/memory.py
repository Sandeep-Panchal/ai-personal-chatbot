
class MemoryManager:

    def __init__(self):

        self.memory_dict = {
            "session_id": "",
            "messages": []
        }

    def get_history(self,
                    session_id: str,
                    human_message: str,
                    ai_message: str
                    ):

        if not self.memory_dict.get("session_id", ""):
            self.memory_dict["session_id"] = session_id
        
        message_dict = {
            "human_message": human_message,
            "ai_message": ai_message
            }

        self.memory_dict["messages"].append(message_dict)

        return self.memory_dict
    
if __name__=="__main__":

    obj = MemoryManager()

    run = True
    i = 0
    sess = "123"
    while run:
        i = i+1
        if i == 4:
            run = False
        
        human_message = f"hi - {i}"
        ai_message = f"bye - {i}"

        response = obj.get_history(sess, human_message, ai_message)

    print(response)






        


