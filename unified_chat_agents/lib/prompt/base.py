from abc import ABC
from string import Formatter
from typing import List, LiteralString

formatter = Formatter()


class BasePrompt(ABC):
    _template: LiteralString
    _input_variables: List[str]

    def __init__(self, template: LiteralString):
        """Initialize the Prompt with a template string."""
        self.template = template

    @property
    def template(self):
        """Get the template string."""
        return self._template

    @template.setter
    def template(self, value):
        """
        Set the template string.
        When the template is set, the input variables are automatically updated.
        """
        self._template = value
        self._input_variables = self._get_input_variables()

    @property
    def input_variables(self):
        """Get the list of input variables."""
        return self._input_variables

    def _get_input_variables(self) -> List[str]:
        """
        Parse the template and extract the field names.
        Remove duplicates from the list of input variables.
        """
        input_variables = [field_name for _, field_name, _, _ in formatter.parse(
            self._template) if field_name is not None]
        input_variables = list(set(input_variables))
        return input_variables

    def get_prompt(self, **kwargs: str) -> str:
        """
        Get the prompt.
        Check if all input variables are present in the provided arguments.
        Format the template with the provided arguments and return the result.
        """
        for input_variable in self._input_variables:
            if input_variable not in kwargs:
                raise KeyError(
                    f"Input variable `{input_variable}` is missing in kwargs."
                )
        return self._template.format(**kwargs)
