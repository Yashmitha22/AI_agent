from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent

load_dotenv()

class ResearchResponse(BaseModel):
    topic : str
    summary : str
    sources : list[str]
    tools_used:list[str]

llm = ChatOpenAI(model="gpt-4o-mini")
parser = PydanticOutputParser(pydatic_object=ResearchResponse)

prompt = ChatMessagePromptTemplate.from_messages(
    [
        (
            "system",
            """you are a research assistant that will help generate a research paper.
               Answer the user query and use necessary tools.
               Wrap the output in this format and provide no other text\n{format_instructions}
               """,
               
        ),
        ("placeholder","{chat_history}"),
        ("human","{query}"),
        ("placeholder","{agent_scratchpad}"),

    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent (
    llm=llm,
    prompt=prompt,
    tools=[]

)

agent_executor = AgentExecutor(agent=agent,tools=[],verbose=True)
raw_response = agent_executor.invoke({"queri":"What is the capital of France??"})
#print the statement
print(raw_response)
