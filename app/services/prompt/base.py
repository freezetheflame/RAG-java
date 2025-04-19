class PromptTemplate:
    """
    Base class for all prompt templates.
    """

    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs) -> str:
        """
        Format the prompt template with the given keyword arguments.
        """
        return self.template.format(**kwargs)

    def generate(self,prompt: str) -> str:
        return prompt