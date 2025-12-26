import streamlit as st
import asyncio
import json
from mistralai import Mistral
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
import os
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small-2506"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

st.set_page_config(page_title="AI Agent", )
st.title("🤖 AI Agent")

if "mcp_session" not in st.session_state:
    st.session_state.messages = []
    st.session_state.tools = []
    
    server_params = StdioServerParameters(command="python", args=["server.py"])
    
async def get_agent_response(user_input):
    server_params = StdioServerParameters(command="python", args=["server.py"])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
      
            tools_resp = await session.list_tools()
            mistral_tools = [{
                "type": "function",
                "function": {
                    "name": t.name, 
                    "description": t.description, 
                    "parameters": t.inputSchema
                }
            } for t in tools_resp.tools]

            messages = [
                {"role": "system", "content": "You are a helpful weekend assistant."},
                {"role": "user", "content": user_input}
            ]

       
            response = await mistral_client.chat.complete_async(
                model=MODEL, messages=messages, tools=mistral_tools
            )
            
            msg = response.choices[0].message
    
            if msg.tool_calls:
                messages.append(msg)
                for tool_call in msg.tool_calls:
                    with st.status(f"Running {tool_call.function.name}...", expanded=False):
                        res = await session.call_tool(
                            tool_call.function.name, 
                            json.loads(tool_call.function.arguments)
                        )
                        st.write(res.content)
                    
                    messages.append({
                        "role": "tool", 
                        "name": tool_call.function.name, 
                        "tool_call_id": tool_call.id, 
                        "content": str(res.content)
                    })
                
                final_res = await mistral_client.chat.complete_async(model=MODEL, messages=messages)
                return final_res.choices[0].message.content
            
            return msg.content

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What should I do this weekend?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = asyncio.run(get_agent_response(prompt))
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})