import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
from langgraph.types import Command
load_dotenv()

import asyncio
from typing import Dict, Any
import logging
import re

st.header("MCP Client")
st.sidebar.title("MCP Client")
# Reduce verbose logging
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("langchain_mcp_adapters").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)

def extract_number_from_response(response_text):
    """Extract the final numeric result from math response"""
    # Find all numbers in the response
    numbers = re.findall(r'\d+', response_text)
    if numbers:
        return int(numbers[-1])  # Return the last number found
    return None

async def main():
    connections: Dict[str, Any] = {
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
    
    client = MultiServerMCPClient(connections)

    # import os
    # groq_key = os.getenv("GROQ_API_KEY")
    # if groq_key:
    #     os.environ["GROQ_API_KEY"] = groq_key

    tools = await client.get_tools()
    model = ChatOllama(model="llama3.2:latest")
    agent = create_react_agent(model, tools)
    # math_response = await agent.ainvoke({"input": "What is 10 + 20?"})
    math_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What is (3 + 5) * 12?"}
        ]
    })
    
    # Print only the final answer
    math_result = None
    if isinstance(math_response, dict) and 'messages' in math_response:
        final_message = math_response['messages'][-1]
        if hasattr(final_message, 'content'):
            math_answer = final_message.content
            print(f"Math Answer: {math_answer}")
            # Extract the numeric result
            math_result = extract_number_from_response(math_answer)
            if math_result:
                print(f"Extracted number : {math_result}")
                st.write(f"Extracted number : {math_result}")
        else:
            print(f"Math Answer: {final_message}")
            st.write(f"Math Answer: {final_message}")
    else:
        print(f"Math Response: {math_response}")
        st.write(f"Math Response: {math_response}")

    # Use the math result in weather query
    weather_query = "What is weather in "+str(math_result)+"?"
    if math_result:
        weather_query = f"What is weather in "+str(math_result)+"? The temperature should be around {math_result} degrees."
    
    weather_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": weather_query}
        ]
    })

    if isinstance(weather_response, dict) and 'messages' in weather_response:
        final_message = weather_response['messages'][-1]
        if hasattr(final_message, 'content'):
            print(f"Weather Answer: {final_message.content}")
            st.write(f"Weather Answer: {final_message.content}")
        else:
            print(f"Weather Answer: {final_message}")
            st.write(f"Weather Answer: {final_message}")
    else:
        print(f"Weather Response: {weather_response}")
        st.write(f"Weather Response: {weather_response}")

if __name__ == "__main__":
    asyncio.run(main())