import langchain
from langchain_experimental.plan_and_execute import load_agent_executor
from langchain_experimental.plan_and_execute.agent_executor import PlanAndExecute
from langchain_experimental.plan_and_execute.planners.chat_planner import (
    load_chat_planner,
)
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.tools import BaseTool, StructuredTool, Tool, tool

from langchain.embeddings import OpenAIEmbeddings

import key_config
import get_tools

with open("prompt/prompt_plan.txt") as f:
    contents = f.read()

model = ChatOpenAI(
    model="gpt-3.5-turbo-0613",
    # model="gpt-4-0613",
    temperature=0,
    max_tokens=2048,
)
system_prompt = contents

planner = load_chat_planner(model, system_prompt)

tools = [
    Tool.from_function(
        func=get_tools.get_db_schema,
        name="Get database schema",
        description="get table and field definition from database, input is string 'DB'.",
    ),
    Tool.from_function(
        func=get_tools.get_meta_data,
        name="Get meta data",
        description="get meta data from database, input is string 'Meta'.",
    ),
    Tool.from_function(
        func=get_tools.get_code_info,
        name="Get code information",
        description="get related information from source code as per the user query, input is the string of user query",
    ),
]

executor = load_agent_executor(model, tools, verbose=True)

agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

langchain.debug = True
# agent.run("What is the change logic of the data concept attribute 'product_dca2'?")
agent.run("attribute 'product_dca2'")
