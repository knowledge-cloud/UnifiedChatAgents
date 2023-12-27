from lib.prompt.base import BasePrompt

class UICAPrompt(BasePrompt):
    """User Intent Capture Agent Prompt."""

    UICA_PROMPT = """
    As UICA, your role is to capture the user's intent. 
    You will receive the user's messages and decide what the user wants to do. 
    
    Output Response Format:
    Your output response should always be a JSON object. The JSON object should include the key 'intent' and the value should be the user's intent.
    """

    def __init__(self):
        """Initialize the User Intent Capture Agent Prompt with a specific format."""
        super().__init__(self.UICA_PROMPT)