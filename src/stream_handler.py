from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.tokens = []

    def on_llm_new_token(self, token : str, **kwargs):
        self.tokens.append(token)
        self.container.markdown("".join(self.tokens))
    
    @property
    def final_answer(self):
        return "".join(self.tokens)