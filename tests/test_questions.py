import unittest.mock
from unittest.mock import patch

import pytest

from app.questions import QuestionApp


def test_ask_questions():
    """Test that the ask_questions method works correctly"""

    # Set the return values of the mocked input function
    input_side_effect = [
        "Test Project",
        "A test project for demonstration purposes.",
        "Demonstrate how the project works.",
        "Python",
        "pytest",
        "pip",
        "src, tests",
        "yes",
        "yes",
        "MIT",
        "",
    ]

    # Create an instance of the QuestionApp
    app = QuestionApp()

    with unittest.mock.patch("builtins.input", side_effect=input_side_effect):
        app.ask_questions()

    # Check that the answers dictionary is populated correctly
    assert app.answers["project_name"] == "Test Project"
    assert (
        app.answers["project_description"]
        == "A test project for demonstration purposes."
    )
    assert app.answers["technical_description"] == "Demonstrate how the project works."
    assert app.answers["programming_languages"] == "Python"
    assert app.answers["dependencies"] == "pytest"
    assert app.answers["package_manager"] == "pip"
    assert app.answers["project_structure"] == "src, tests"
    assert app.answers["usage_instructions"] == "yes"
    assert app.answers["test_instructions"] == "yes"
    assert app.answers["license"] == "MIT"
    assert "notes" not in app.answers


def test_ask_questions_raises_exception():
    """
    Test that the ask_questions method raises an exception if a non-optional question is left blank
    """

    app = QuestionApp()

    # Set up a question where the answer cannot be left blank
    app.questions = [
        {
            "id": "q1",
            "question": "This question cannot be left blank",
            "optional": False,
            "depends_on": None,
        },
    ]

    # Mock the input function to simulate leaving the answer blank
    with patch("builtins.input", return_value=""):
        with pytest.raises(ValueError) as excinfo:
            app.ask_questions()

    assert (
        str(excinfo.value)
        == "Non-optional question 'This question cannot be left blank' cannot be left blank."
    )
