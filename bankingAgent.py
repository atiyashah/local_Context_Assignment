from connection import run_config
from agents import Agent, Runner, function_tool, RunContextWrapper,enable_verbose_stdout_logging
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()

# ------------------- MODEL -------------------
class BankAccount(BaseModel):
    account_number: str
    customer_name: str
    account_balance: float
    account_type: str

# ------------------- CONTEXT DATA -------------------
bank_account = BankAccount(
    account_number="ACC-1001",
    customer_name="Atiya shah",
     account_balance=75500.50,
     account_type="savings",
    
)

# ------------------- TOOL -------------------
@function_tool()
def get_user_info(ctx: RunContextWrapper[BankAccount]) -> str:
    return (
        "------ Account Information ------\n"
        f"Customer Name   : {ctx.context.customer_name}\n"
        f"Account Number  : {ctx.context.account_number}\n"
        f"Account Type    : {ctx.context.account_type}\n"
        f"Account Balance : {ctx.context.account_balance}\n"
        "---------------------------------"
    )

# ------------------- AGENT -------------------
personal_agent = Agent(
    name="personal_agent",
    instructions = "You are a personal banking agent. Always return account details in a professional formatted report.",
    tools=[get_user_info],
    output_type=str
)

# ------------------- RUNNER -------------------
result = Runner.run_sync(
    personal_agent,
    "show me a bank account detail of user",
    run_config=run_config,
    context=bank_account,
)

print(result.final_output)
