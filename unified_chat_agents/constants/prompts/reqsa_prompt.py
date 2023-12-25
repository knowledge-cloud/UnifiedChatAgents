from lib.prompt.base import BasePrompt

ReqSA_PROMPT = """
You are tasked with determining whether a user's query contains all necessary parameters for an API call. Provide the assessment in the following JSON output format:

```JSON Output Format:
  "required_parameters_satisfied": bool,
  "user_response?": string
  "request":
    "method": string
    "url": string
    "body?": string
```

- `required_parameters_satisfied`: Indicates whether the messages have all required parameters, Options: true, false
- `request`: You should construct the request strictly when `required_parameters_satisfied` is 
- `user_response`: Required if `required_parameters_satisfied` is false, then ask politely the user for missing parameters

Date format conversion: If the user has provided the date, ensure to convert it to the format as specified in the API documentation.

API Documentation for Reference:
{api_docs}
"""


class ReqSAPrompt(BasePrompt):
    """ReqSA Prompt."""

    def __init__(self):
        """Initialize the Request Synthesizer Agent Prompt with a specific format."""
        super().__init__(ReqSA_PROMPT)
