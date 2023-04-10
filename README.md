# Jarvis - AI Code Project Generator

Jarvis is a Python-based AI code project generator that uses OpenAI's GPT-3.5-turbo model to generate code for your projects. It asks a series of questions to gather information about your project and generates a prompt based on the answers, which includes instructions and generated code.

## Installation

To install Jarvis, use [Poetry](https://python-poetry.org/), a package manager for Python. Once Poetry is installed, run the following command:

```
poetry install
```

This will install all the necessary dependencies for the project.

## Usage

To run Jarvis, execute the following command:

```
python main.py
```

This will start the script that asks a series of questions to gather information.
Once all the questions are answered, the application generates a prompt based on the answers and additional instructions.

Prompt will then generate a project. Which will be saved in this folder:

```
/generated/{project}
```

## API Key

To use Jarvis, you need an OpenAI API key. To set up your API key, create a `settings.py` file in the `app/settings` directory of the project and add the following code:

```
api_key = "YOUR_API_KEY"
```

Replace YOUR_API_KEY with your actual API key.

## License

Jarvis is licensed under the MIT License.
