import google.generativeai as genai
from tools.task_reminder import add_task, get_today_date_and_time
import os

tools = [
    add_task,
    get_today_date_and_time
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=tools,
)