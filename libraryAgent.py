from connection import run_config
from agents import Agent, Runner, function_tool, RunContextWrapper, enable_verbose_stdout_logging
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

# ------------------- MODEL -------------------
class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool

# ------------------- USER INPUT -------------------
book_id = input("Enter Book ID: ")
book_title = input("Enter Book Title: ")
author_name = input("Enter Author Name: ")
availability_input = input("Is the book available? (yes/no): ")

# simple if-else to convert input into True/False
if availability_input.lower() == "yes":
    is_available = True
else:
    is_available = False

# ------------------- CONTEXT DATA -------------------
library_book = LibraryBook(
    book_id=book_id,
    book_title=book_title,
    author_name=author_name,
    is_available=is_available
)

# ------------------- TOOL -------------------
@function_tool()
def get_book_info(ctx: RunContextWrapper[LibraryBook]) -> str:
    return (
        "====== Library Book Record ======\n"
        f"Book ID        : {ctx.context.book_id}\n"
        f"Title          : {ctx.context.book_title}\n"
        f"Author         : {ctx.context.author_name}\n"
        f"Availability   : {'Available' if ctx.context.is_available else 'Not Available'}\n"
        "================================="
    )

# ------------------- AGENT -------------------
library_agent = Agent(
    name="library_agent",
    instructions="You are a helpful library assistant. Always provide book details clearly.",
    tools=[get_book_info],
    output_type=str
)

# ------------------- RUNNER -------------------
result = Runner.run_sync(
    library_agent,
    "Show me the library book details",
    run_config=run_config,
    context=library_book,
)

print(result.final_output)
