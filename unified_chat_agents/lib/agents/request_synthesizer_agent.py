import json
from typing import List
import traceback
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from lib.chat import ChatRole, ChatMessage
from lib.toolbox import ApiToolbox
from lib.openai import OpenAIChatMessage
from constants.prompts import ReqSAPrompt
from utils.log_utils import logger
from constants.errors.chat import API_TOOLBOX_ERROR


class RequestSynthesizerAgent(BaseRedirectingAgent):
    """
    The agent can respond or redirect to another agent.
    """

    role: ChatRole = ChatRole.ReqSA

    prompt: BasePrompt = ReqSAPrompt()

    api_toolbox = ApiToolbox("https://aibnzrilz2.execute-api.ap-south-1.amazonaws.com/prod/")

    def __init__(self) -> None:
        """Initialize the RequestSynthesizerAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def predict(
        self,
        messages: List[OpenAIChatMessage],
        **kwargs
    ) -> ChatMessage:
        """Get the redirecting agent."""
        while True:
            logger.debug(
                f"RequestSynthesizerAgent::predict::while:: ######################")
            response = self.chat_completions(
                messages, {"type": "json_object"}, seed=1129902034289, **kwargs)
            formatted_response = json.loads(response)
            logger.debug(
                f"RequestSynthesizerAgent::predict::formatted_response: {formatted_response}")
            required_parameters_satisfied = formatted_response.get(
                "required_parameters_satisfied")

            logger.debug(
                f"RequestSynthesizerAgent::predict::while::required_parameters_satisfied: {required_parameters_satisfied}")
            if required_parameters_satisfied is None:
                continue

            if required_parameters_satisfied:
                request = formatted_response.get("request")
                logger.debug(
                    f"RequestSynthesizerAgent::predict::while::request: {request}")
                if request is None:
                    continue
                elif request:
                    try:
                        response = self.api_toolbox.execute_request(request)
                    except Exception as e:
                        traceback_str = traceback.format_exc()
                        logger.error(
                            f"RequestSynthesizerAgent::api_toolbox:error: {e}")
                        logger.error(
                            f"RequestSynthesizerAgent::api_toolbox:traceback: {traceback_str}")
                        return ChatMessage(
                            **{
                                "from_": self.role,
                                "to": ChatRole.USER,
                                "content": API_TOOLBOX_ERROR.format(error=e)
                            }
                        )
                    logger.debug(
                        f"RequestSynthesizerAgent::api_toolbox:response: {response}")
                    response = json.dumps(response)
                    return ChatMessage(
                        **{
                            "from_": self.role,
                            "to": ChatRole.ResSA,
                            "content": response,
                            "kwargs": kwargs
                        }
                    )
            else:
                user_response = formatted_response.get("user_response")
                logger.debug(
                    f"RequestSynthesizerAgent::predict::while::user_response: {user_response}")
                if user_response is None:
                    continue

                return ChatMessage(
                    **{
                        "from_": self.role,
                        "to": ChatRole.USER,
                        "content": user_response,
                        "kwargs": kwargs
                    }
                )
