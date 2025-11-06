import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
import os
import platform
import traceback
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a Crypto Event Tracker AI Agent. Your role is to help users find and track cryptocurrency events worldwide.

You have access to these tools:
1. search_crypto_events - Search for any cryptocurrency events (conferences, launches, upgrades, airdrops, etc.)
2. search_specific_coin - Search for events related to a specific cryptocurrency

Your capabilities:
- Search for upcoming crypto events with specific dates
- Track events for ANY cryptocurrency mentioned in recent news
- Identify event categories (conference, launch, upgrade, airdrop, summit, announcement)
- Extract event details like dates, locations, and descriptions
- Filter out past events and only show upcoming/future events

When users ask about crypto events:
1. Determine which tool to use based on their query
2. Call the appropriate tool with relevant search parameters
3. Present the results in a clear, organized format
4. Highlight events with specific dates separately from general announcements
5. Provide source links for verification

Be proactive, helpful, and enthusiastic about crypto events. If results show "Unknown" for coin names, still present the event information clearly.
"""

class CryptoEventAgent:
    def __init__(self):
        self.session = None
        self.tools = []
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    
    def format_tools_for_openai(self):
        """Converting MCP tools to OpenAI function format"""
        openai_tools = []
        for tool in self.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
        return openai_tools
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """Calling MCP tool and return results"""
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text
    
    async def chat(self, user_message: str):
        """Processing user message with GPT-4 and execute tools"""
        # Adding user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Getting tools in OpenAI format
        openai_tools = self.format_tools_for_openai()
        
        # Calling GPT-4
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_history,
            tools=openai_tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        
        if assistant_message.tool_calls:
            # Adding assistant's tool call to history
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # Executing each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f" Calling tool: {tool_name}")
                print(f" Arguments: {json.dumps(tool_args, indent=2)}")
                
                # Calling the tool
                tool_result = await self.call_tool(tool_name, tool_args)
                
                print(f"Tool executed successfully\n")
                
                # Adding tool result to history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
            
            
            final_response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history
            )
            
            final_message = final_response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            
            return final_message
        else:
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content
            })
            return assistant_message.content
    
    async def close(self):
        """Closing the session"""
        if hasattr(self,'session')and self.session:
            await self.session.close()

async def main():
    """Running the agent"""
    agent = CryptoEventAgent()
    server_parameters=StdioServerParameters(
        command="python",
        args=["server.py"],
        env=os.environ,
        capture_output=False
    )
    
    try:
        # Connecting to MCP server using context manager
        print("Starting stdio_client")
        async with stdio_client(server_parameters)as (read_stream,write_stream):
            print("Creating Session")
            agent.session=ClientSession(read_stream,write_stream)
            print("Waiting for MCP server to initialize")
            await agent.session.initialize()
            print("MCP server initialized!Connected to server")

            tools_list=await agent.session.list_tools()
            agent.tools=tools_list.tools

            print(f"\nAvailable tools:{[tool.name for tool in agent.tools]}\n")
            print("Crypto Event Tracker Agent Started")
            print("Ask me about any cryptocurrency events")
            print("Examples:")
            print("What Bitcoin events are coming up?")
            print("Search for ethereum conferences")
            print("Any Solana airdrops happening?")
            print("Show me all crypto events this month")
            print("\n Type 'exit' , 'quit',or 'bye' to stop\n")
            print("="*60 + "\n")

            while True:
                user_input=await asyncio.to_thread(input,"You:")
                if user_input.lower() in ["exit","quit","bye"]:
                    print("\n Goodbye!stay updated with crypto events!")
                    break
                if not user_input:
                    continue
                print()

                response=await agent.chat(user_input)
                print(f"Agent:{response}\n")
                print("="*60 +"\n")
    except KeyboardInterrupt:
        print("\n\n Interrupted.Shutting down...")
    except Exception as e:
        print(f"\n Errr:{e}")
        traceback.print_exc()

if __name__=="__main__":
    if platform.system()=="windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
