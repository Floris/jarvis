# Jarvis - AI Code Project Generator

Jarvis is a Python-based AI code project generator that uses OpenAI's GPT-3.5-turbo model to generate code for your projects. It asks a series of questions to gather information about your project and generates a prompt based on the answers, which includes instructions and generated code.

## Installation

To install Jarvis, use [Poetry](https://python-poetry.org/), a package manager for Python. Once Poetry is installed, run the following command:

```
poetry install
```

This will install all the necessary dependencies for the project.

## How to Use

Choose between utilizing a predefined prompt from `prompts/prompt.txt` or creating a custom prompt by answering a set of questions.

To initiate Jarvis, run the command below:

```
python app/javis.py
```

The script will then ask a series of questions to collect necessary information. Once completed, it will create a prompt based on the responses and any additional guidance provided.

The generated prompt will be used to create the project structure using OpenAI's GPT-3.5-turbo model.

If you need to give feedback, you can do so; otherwise, execute the following command:

```
create_code
```

The code will be generated in the specified directory:

```
/generated/{project_title}
```

To terminate the script, enter the command:

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
