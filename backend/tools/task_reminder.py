import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("Krishta Bot/task_reminder")

def add_task(task: str, time: Optional[str] = None) -> dict:
    """Add a task to the user's Google Calendar
    
    Args:
        task (str): The task description to be added
        time (str, optional): The time for the task in ISO format (YYYY-MM-DD HH:MM)
    
    Returns:
        dict: Response containing success status and message
    """
    try:
        logger.info(f"Task reminder called - Task: {task}, Time: {time}")
        
        # Validate inputs
        if not task:
            return {
                "success": False,
                "message": "Task description cannot be empty"
            }
            
        # Parse time if provided
        task_time = None
        if time:
            try:
                task_time = datetime.fromisoformat(time)
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid time format. Please use YYYY-MM-DD HH:MM"
                }
        
        # TODO: Implement Google Calendar integration
        # For now, just log the attempt
        logger.info(f"Would add task: {task} at time: {task_time}")
        
        return {
            "success": True,
            "message": f"Task '{task}' would be added" + (f" at {time}" if time else "")
        }
        
    except Exception as e:
        logger.error(f"Error adding task: {str(e)}")
        return {
            "success": False,
            "message": f"Error adding task: {str(e)}"
        }