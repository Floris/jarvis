# Jarvis - AI Code Project Generator

Jarvis is a Python-based AI code project generator that uses OpenAI's GPT-3.5-turbo model to generate code for your projects. It asks a series of questions to gather information about your project and generates a prompt based on the answers, which includes instructions and generated code.

## Installation

To install Jarvis, use [Poetry](https://python-poetry.org/), a package manager for Python. Once Poetry is installed, run the following command:

```
poetry install
```

This will install all the necessary dependencies for the project.

## Description

Jarvis can be used to create/ set up projects from scratch. Or just functions.

Note:

## Usage

To run Jarvis, execute the following command:

```
python main.py
```

This will start the script that asks a series of questions to gather information.
Once all the questions are answered, the application generates a prompt based on the answers and additional instructions.

This prompt is used to generate the project structure through OpenAI's GPT-3.5-turbo model.

You get the ability to provide feedback if needed, if not use the command:

```
create_code
```

This will then generate the code in the designated folder:

```
/generated/{project_title}
```

To exit the script use the command:

```
exit
```

## API Key

To use Jarvis, you need an OpenAI API key. To set up your API key, create a `settings.py` file in the `app/settings` directory of the project and add the following code:

```
api_key = "YOUR_API_KEY"
```

Replace YOUR_API_KEY with your actual API key.

## License

Jarvis is licensed under the MIT License.
