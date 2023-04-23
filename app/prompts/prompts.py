from prompts.prompt_generator import PromptGenerator

commands = [
    (
        "Add information to memory",
        "memory_add",
        {
            "string": "<information_to_add>",
        },
    ),
    (
        "Start GPT Agent",
        "start_agent",
        {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"},
    ),
    (
        "Message GPT Agent",
        "message_agent",
        {"key": "<key>", "message": "<message>"},
    ),
    (
        "List GPT Agents",
        "list_agents",
        {
            "reason": "<reason>",
        },
    ),
    (
        "Delete GPT Agent",
        "delete_agent",
        {"key": "<key>"},
    ),
    (
        "Write to file",
        "write_to_file",
        {
            "file": "<file>",
            "text": "<text_or_full_code_string>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
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
            "text": "<text_or_full_code_string>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Update file",
        "update_file",
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
    (
        "Ask for help",
        "human_feedback",
        {
            "question": "<text>",
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
    (
        "Do Nothing",
        "do_nothing",
        {
            "reason": "<reason>",
            "reflection": "<reflection_about_what_happened>",
        },
    ),
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
    # prompt_generator.add_constraint("No user assistance")
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


def construct_prompt(name: str, role: str, goals: list[str]) -> str:
    prompt_start = (
        "Your decisions must always be made independently without"
        " seeking user assistance. Play to your strengths as an LLM and pursue"
        " simple strategies with no legal complications."
        ""
    )

    # Construct full prompt
    full_prompt = f"You are {name}, {role}\n{prompt_start}\n\nGOALS:\n\n"

    # ai_goals
    for i, goal in enumerate(goals):
        full_prompt += f"{i+1}. {goal}\n"

    full_prompt += f"\n\n{get_prompt()}"
    return full_prompt
