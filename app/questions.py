from typing import TypedDict


class QuestionDict(TypedDict):
    id: str
    question: str
    optional: bool
    depends_on: str | None


class AnswerDict(TypedDict):
    question: str
    answer: str


def use_prompt_from_file(file: str = "app/prompts/prompt.txt") -> str | None:
    """
    Asks the user if they want to use the prompt from the prompts/prompts.txt file.

    Args:
        file str: The path to the file containing the prompt.

    Returns:
        str | None: The prompt from the file or None if the user doesn't want to use the prompt from the file.
    """

    use_prompt_from_file = None

    while use_prompt_from_file not in ["y", "n"]:
        use_prompt_from_file = input("Use prompt from file? (y/n): ").lower()

    if use_prompt_from_file == "n":
        return None

    with open(file) as f:
        return f.read()


class QuestionApp:
    """Class for asking questions and generating a prompt"""

    def __init__(self) -> None:
        self.questions: list[QuestionDict] = QUESTIONS
        self.answers: dict[str, AnswerDict] = {}

    def ask_questions(self) -> None:
        """
        Asks the user if they want to use the prompt from the prompts/prompts.txt file.

        Returns:
            None
        """

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
                self.answers[question_dict["id"]] = AnswerDict(
                    question=question, answer=answer
                )

    def generate_prompt(self) -> str:
        """
        Generate a prompt based on the answers

        Returns:
            str: Generated prompt from the answers
        """

        prompt = "\n\n"

        # Iterate through the answers dictionary and add them to the prompt string
        for question_id in self.answers:
            prompt += f"* {self.answers[question_id]['question'].capitalize().replace('_', ' ')}\n{self.answers[question_id]['answer']}\n\n"

        # Add additional instructions to the prompt
        prompt += "Define the structure of the whole project\n"
        prompt += "Try to combine files if possible, this is for efficiency\n"

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
        "question": "What packages/ dependencies will be used?",
        "optional": True,
        "depends_on": None,
    },
    {
        "id": "package_manager",
        "question": "What package manager will be used? (pip, npm, etc.)",
        "optional": True,
        "depends_on": "dependencies",
    },
    {
        "id": "package_manager_file",
        "question": "What is the filename of the package manager file? (requirements.txt, package.json, etc.)",
        "optional": False,
        "depends_on": "package_manager",
    },
    {
        "id": "test_instructions",
        "question": "Do you want unit tests for the project?",
        "optional": True,
        "depends_on": None,
    },
    {
        "id": "test_instructions_package",
        "question": "What package will be used for unit testing? (pytest, unittest, etc.)",
        "optional": True,
        "depends_on": "test_instructions",
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
