import asyncio
import os
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

async def run_finance_agent():
    # Use absolute path to avoid Windows path issues
    server_path = os.path.abspath("finance_server.py")

    # 1. Initialize the Client (No 'async with' here anymore)
    client = MultiServerMCPClient({
    "finance": {
        # Use sys.executable to force the current Conda Python
        "command": sys.executable, 
        "args": [os.path.abspath("finance_server.py")],
        "transport": "stdio",
    }
})
    
    # 2. Retrieve tools directly from the client
    tools = await client.get_tools()
    
    # Setup your Local LLM
    llm = ChatOllama(model="llama3.1", temperature=0)
    
    # Define the Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a personal finance agent. Use tools to manage payments."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Create and Execute the Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("\n--- Testing Personal Finance Assistant ---")
    await agent_executor.ainvoke({"input": "Pay my $1000 internet bill to Internet Provider."})

if __name__ == "__main__":
    asyncio.run(run_finance_agent())