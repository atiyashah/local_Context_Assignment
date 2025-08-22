from connection import run_config
from agents import Agent, Runner, function_tool, RunContextWrapper, enable_verbose_stdout_logging
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

# ------------------- MODEL -------------------
class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int

# ------------------- CONTEXT DATA -------------------
student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

# ------------------- TOOL -------------------
@function_tool()
def get_student_info(ctx: RunContextWrapper[StudentProfile]) -> str:
    return (
        "------ Student Profile ------\n"
        f"Student Name     : {ctx.context.student_name}\n"
        f"Student ID       : {ctx.context.student_id}\n"
        f"Current Semester : {ctx.context.current_semester}\n"
        f"Total Courses    : {ctx.context.total_courses}\n"
        "------------------------------"
    )

# ------------------- AGENT -------------------
student_agent = Agent(
    name="student_agent",
    instructions="You are a student agent. Always return student details in a professional formatted report.",
    tools=[get_student_info],
    output_type=str
)

# ------------------- RUNNER -------------------
result = Runner.run_sync(
    student_agent,
    "show me student details",
    run_config=run_config,
    context=student,
)

print(result.final_output)
