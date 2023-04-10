from typing import TypedDict


class QuestionDict(TypedDict):
    id: str
    question: str
    optional: bool
    depends_on: str | None


class QuestionApp:
    """Class for asking questions and generating a prompt"""

    def __init__(self) -> None:
        self.questions: list[QuestionDict] = QUESTIONS
        self.answers: dict[str, str] = {}

    def ask_questions(self):
        for question_dict in self.questions:
            question = question_dict["question"]
            optional = question_dict["optional"]
            depends_on = question_dict["depends_on"]

            # If the question has a dependency and the dependency's answer is not present,
            # skip asking the current question
            if depends_on is not None and not self.answers.get(depends_on):
                continue

            # Ask the question with an optional label if the question is optional
            answer = input(f"{question}{' (optional)' if optional else ''}: ")

            # Raise an exception if a non-optional question is left blank
            if not optional and not answer.strip():
                raise ValueError(
                    f"Non-optional question '{question}' cannot be left blank."
                )

            # If the question is not optional or the question is optional and has an answer,
            # store the answer in the answers dictionary with the question ID as the key
            if not optional or (optional and answer.strip()):
                self.answers[question_dict["id"]] = answer

    def generate_prompt(self) -> str:
        """Generate a prompt based on the answers"""

        prompt = "\n\n"

        # Iterate through the answers dictionary and add them to the prompt string
        for title, content in self.answers.items():
            prompt += f"* {title.capitalize().replace('_', ' ')}\n{content}\n\n"

        # Add additional instructions to the prompt
        prompt += "* Notes\n"
        prompt += (
            "Make sure to generate code for all the files in the project structure.\n"
        )
        prompt += "Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.\n"
        return prompt.strip()


QUESTIONS: list[QuestionDict] = [
    {
        "id": "project_name",
        "question": "Project name?",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "project_description",
        "question": "Please provide a description of the project.",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "technical_description",
        "question": "Describe the technical aspects of the project.",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "programming_languages",
        "question": "What programming languages will be used?",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "dependencies",
        "question": "What dependencies will be used?",
        "optional": True,
        "depends_on": None,
    },
    {
        "id": "package_manager",
        "question": "What package manager will be used? (pip, npm, etc.)",
        "optional": False,
        "depends_on": "dependencies",
    },
    {
        "id": "project_structure",
        "question": "Describe the project structure.",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "usage_instructions",
        "question": "Do you want us to provide usage instructions for the project.",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "test_instructions",
        "question": "Do you want us to provide test instructions for the project.",
        "optional": False,
        "depends_on": None,
    },
    {
        "id": "license",
        "question": "Specify the license for the project.",
        "optional": True,
        "depends_on": None,
    },
    {
        "id": "notes",
        "question": "Any additional notes or comments?",
        "optional": True,
        "depends_on": None,
    },
]
