from tools.task_reminder import add_task

add_task_config = {
    "function": add_task,
    "schema": {
        "name": "add_task",
        "description": "Add a specified task to the user's Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task description or details"
                },
                "time": {
                    "type": "string",
                    "description": "The time for the task in (YYYY-MM-DD HH:MM) format"
                }
            },
            "required": ["task"]
        }
    }
}