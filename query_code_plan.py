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
    max_tokens=1024,
)
system_prompt = contents

planner = load_chat_planner(model, system_prompt)

tools = [
    Tool.from_function(
        func=get_tools.get_data_model,
        name="Get data model",
        description="get data model from meta schema.",
    ),
    Tool.from_function(
        func=get_tools.get_data_info,
        name="Get data information",
        description="get data information",
    ),
]

executor = load_agent_executor(model, tools, verbose=True)

agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

langchain.debug = True
agent.run("What is the change logic of the attribute 'maturity date'?")
