# Jarvis - AI Code Project Generator

Jarvis is an AI-driven Python tool that empowers you to tackle various tasks such as problem-solving, book writing, code creation, and more. This personal side project utilizes the OpenAI API to provide an interactive and dynamic coding experience.

## Installation

To install Jarvis, use [Poetry](https://python-poetry.org/), a package manager for Python. Once Poetry is installed, run the following command:

```
poetry install
```

This will install all the necessary dependencies for the project.

## How to Use

Start Weaviate

```
docker-compose up -d
```

Starting the AI.

```
python app
```

Saved files will be stored here:

```
/generated
```

Commands utilized by the AI

```
-start_coding_assistant # specialized in writing code
-start_agent
-message_agent
-list_agents
-delete_agent
-write_to_file
-read_file
-append_file
-update_file
-delete_file
-search_files
-ask_for_help
-do_nothing
-shut_down
```

## API Key

To use Jarvis, you need an OpenAI API key. To set up your API key, create a `settings.py` file in the `app/settings` directory of the project and add the following code:

```
api_key = "YOUR_API_KEY"
```

Replace YOUR_API_KEY with your actual API key.

## License

Jarvis is licensed under the MIT License.
