# pip install numexpr

from json import load

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
tools = load_tools(["11m-math"], llm=llm)
agent = create_agent(llm, tools)

result = agent.invoke({"messages": [("user", "(12.5 * 4) + 7 의 제곱근을 계산하시오.")]})
print(result["messages"][-1].content)