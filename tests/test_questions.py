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
        "no",
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
    assert app.answers["project_name"]["answer"] == "Test Project"
    assert app.answers["project_name"]["question"] == "Project name?"

    assert (
        app.answers["project_description"]["answer"]
        == "A test project for demonstration purposes."
    )
    assert (
        app.answers["project_description"]["question"]
        == "Please provide a description of the project."
    )

    assert (
        app.answers["technical_description"]["answer"]
        == "Demonstrate how the project works."
    )
    assert (
        app.answers["technical_description"]["question"]
        == "Describe the technical aspects of the project."
    )

    assert app.answers["programming_languages"]["answer"] == "Python"
    assert (
        app.answers["programming_languages"]["question"]
        == "What programming languages will be used?"
    )

    assert app.answers["dependencies"]["answer"] == "pytest"
    assert app.answers["dependencies"]["question"] == "What dependencies will be used?"

    assert app.answers["package_manager"]["answer"] == "pip"
    assert (
        app.answers["package_manager"]["question"]
        == "What package manager will be used? (pip, npm, etc.)"
    )

    assert app.answers["project_structure"]["answer"] == "no"
    assert (
        app.answers["project_structure"]["question"]
        == "Do you want us to provide the project structure?"
    )

    assert app.answers["describe_project_structure"]["answer"] == "src, tests"
    assert (
        app.answers["describe_project_structure"]["question"]
        == "Describe the project structure."
    )

    assert app.answers["usage_instructions"]["answer"] == "yes"
    assert (
        app.answers["usage_instructions"]["question"]
        == "Do you want us to provide usage instructions for the project."
    )

    assert app.answers["test_instructions"]["answer"] == "yes"
    assert (
        app.answers["test_instructions"]["question"]
        == "Do you want us to provide test instructions for the project."
    )

    assert app.answers["license"]["answer"] == "MIT"
    assert app.answers["license"]["question"] == "Specify the license for the project."

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
