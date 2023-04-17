from prompts.prompt_generator import PromptGenerator

commands = [
    (
        "Start Coding Agent",
        "start_coding_agent",
        {
            "name": "<name>",
            "file": "<file>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Ask AI question",
        "ask_ai_question",
        {
            "prompt": "<prompt>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Write to file",
        "write_to_file",
        {
            "file": "<file>",
            "text": "<text>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    # (
    #     "Create file",
    #     "create_file",
    #     {
    #         "file": "<file>",
    #         "text": "<text_or_blank>",
    #         "reason": "<reason>",
    #         "reflection": "<reflection_about_what_happened>",
    #     },
    # ),
    (
        "Read file",
        "read_file",
        {
            "file": "<file>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Append to file",
        "append_to_file",
        {
            "file": "<file>",
            "text": "<text>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Delete file",
        "delete_file",
        {
            "file": "<file>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Search Files",
        "search_files",
        {
            "directory": "<directory>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    # (
    #     "Execute Python File",
    #     "execute_python_file",
    #     {
    #         "file": "<file>",
    #         "reason": "<reason>",
    #         "reflection": "<reflection_about_what_happened>",
    #     },
    # ),
    # (
    #     "Do Nothing",
    #     "do_nothing",
    #     {
    #         "reason": "<reason>",
    #         "reflection": "<reflection_about_what_happened>",
    #     },
    # ),
    (
        "Shutdown",
        "shutdown",
        {
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
]


def get_prompt() -> str:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.
    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "~4000 word limit for short term memory. Your short term memory is short, so"
        " immediately save important information to files."
    )
    prompt_generator.add_constraint(
        "If you are unsure how you previously did something or want to recall past"
        " events, thinking about similar events will help you remember."
    )
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint(
        'Exclusively use the commands listed in double quotes e.g. "command name"'
    )

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource(
        "GPT-3.5 powered Agents for delegation of simple tasks."
    )
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        "Continuously review and analyze your actions to ensure you are performing to"
        " the best of your abilities."
    )
    prompt_generator.add_performance_evaluation(
        "Constructively self-criticize your big-picture behavior constantly."
    )
    prompt_generator.add_performance_evaluation(
        "Reflect on past decisions and strategies to refine your approach."
    )
    prompt_generator.add_performance_evaluation(
        "Every command has a cost, so be smart and efficient. Aim to complete tasks in"
        " the least number of steps."
    )

    # Generate the prompt string
    return prompt_generator.generate_prompt_string()
