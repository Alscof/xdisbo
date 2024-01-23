import time
import os
from langchain.tools import tool
from crewai import Agent, Task, Process, Crew
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Together

from langchain_community.tools import DuckDuckGoSearchRun

from langchain.tools import Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.schema import HumanMessage, SystemMessage

from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.llms import OpenAI

from datetime import date

today = date.today()


DDGsearch = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="research analysis",
        func=DDGsearch,
        description="A search engine. Useful for when you need to answer questions about current events. Input should be a search query."
    )]

os.environ[ "api_key"] = st.secrets["api_key"]
api_base = "https://openrouter.ai/api/v1"
model = "openchat/openchat-7b"
os.environ[ "SERPAPI_API_KEY"] = st.secrets["SERPAPI_API_KEY"]

# To Load Local models through Ollama
mistral = ChatOpenAI(
    api_key=api_key,
    base_url=api_base,
    model=model,
    temperature=0.0,
    max_tokens=400
    
)

#tools = load_tools(["serpapi"], llm=mistral)


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered is not None:
        llm = mistral
        system_message = SystemMessage(content= f"You are an Professional forex trading assistant who monitors current and the latest market events to forecast the market ahead of {today}. \
                    search web for information to forecast the market {today} using the tools {tools} impacting the forex market. you only answer questions about forex currency \
                    trading and currency economic news for the date of {today} and economic calendar for forecasts for date of {today} from latest forecast feeds of https://fxdaily.com, https://forexlive.com and https://reuters.com. You provide the latest information \
                    happening now or today {today} before considering taking about old information. for latest economic calendar news check https://www.investing.com/economic-calendar/ \
                    focus on the news headlines forecasting the market and movement of GBP, USD, NZD, AUD, EUR, JPY, CAD, CHF, Gold and Oil events only. \
                    give a detailed explainatin of your observations and thoughts showing how you came to your conclusion for the answers you give. \
                    don't answer anything beyond this scope. your answers must always be less than 1600 characters in length. \
                    "),
        memory = ConversationBufferMemory(memory_key="chat_history")
        agent = initialize_agent(
            tools, 
            llm,
            system_message = system_message,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            agent_kwargs={
             "system_message": system_message
            }
            
            )
        
        output_1=agent.run(f"{today}, {user_input}")



    return output_1



