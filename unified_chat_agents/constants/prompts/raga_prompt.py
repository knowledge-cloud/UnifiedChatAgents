from lib.prompt.base import BasePrompt


class RAGAPrompt(BasePrompt):
    """RAGA Prompt."""

    RAGA_PROMPT = """
    As RAGA, your role is to perform RAG search on API documentation and find the relevant API documentation that matches the user's intent.
    
    Output Response Format:
    Your output response should always be a JSON object. The JSON object should include the key 'doc_id' and the value should be the doc_id of the relevant API documentation.

    API Documentations:
    {api_details}
    """

    def __init__(self):
        """Initialize the Retrieval Augmented Generation Agent Prompt with a specific format."""
        super().__init__(self.RAGA_PROMPT)