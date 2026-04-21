import asyncio
import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import BadRequestError
from mcp_use import MCPAgent, MCPClient

# Completely disable all MCP logging except critical errors
logging.getLogger('mcp_use').setLevel(logging.CRITICAL)
logging.getLogger('httpx').setLevel(logging.CRITICAL)
logging.getLogger('httpcore').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('mcp_use.telemetry.telemetry').setLevel(logging.CRITICAL)

async def main():
    # Disable telemetry
    os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"
    
    # Load environment variables
    load_dotenv()

    # Create configuration dictionary
    config = {
      "mcpServers": {
        "playwright": {
          "command": "npx",
          "args": ["-y", "@playwright/mcp@latest"]
        },
        "airbnb": {
          "command": "npx",
          "args": ["-y", "@openbnb/mcp-server-airbnb"]
        },
        "duckduckgo-search": {
          "command": "npx",
          "args": ["-y", "ddg-mcp-search@latest"],
          "env": {
            "npm_config_cache": "/Users/mahithr/.cursor/worktrees/mcpdemo/ysk/.npm-cache"
          }
        }
      }
    }

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)

    # Create LLM with Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    
    # Create agent with the client
    agent = MCPAgent(
        llm=llm, 
        client=client, 
        max_steps=30, 
        verbose=False
    )

    print("\n🚀 MCP Agent Ready!")
    print("=" * 70)
    print("📝 This agent can:")
    print("  • 🌐 Browse websites with Playwright")
    print("  • 🏠 Search Airbnb for hotels")
    print("  • 🔍 Search the web with DuckDuckGo")
    print("\n💡 Example questions:")
    print("  • go to youtube.com and search for python tutorials")
    print("  • find hotels in Paris")
    print("  • search for latest AI news")
    print("=" * 70)
    
    # Interactive loop
    while True:
        try:
            user_query = input("\n🎯 Your question (or 'exit' to quit): ").strip()
            
            if not user_query:
                continue
                
            if user_query.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye!")
                break
            
            print("\n" + "=" * 70)
            print(f"📝 Processing: {user_query}")
            print("=" * 70)
            print("⏳ Working on it...\n")
            
            # Add guardrails for Airbnb tool parameters
            prompt = (
                "IMPORTANT: When you call the airbnb_search tool, "
                "pass minPrice and maxPrice as numbers (no quotes). "
                "If you are unsure about price, omit minPrice/maxPrice. "
                f"User request: {user_query}"
            )

            # Run the agent
            try:
                result = await agent.run(prompt)
            except BadRequestError as e:
                # Show a user-friendly message and continue the loop
                print("\n⚠️  Airbnb request failed because price values were not numeric.")
                print("   Tip: Try asking without price filters, e.g.:")
                print("   • find hotels in Paris for 2 guests")
                continue
            
            print("\n" + "=" * 70)
            print("✅ FINAL RESULT:")
            print("=" * 70)
            
            # Display result in a clean format
            if isinstance(result, str):
                # Clean up the result
                result = result.strip()
                if result:
                    print(result)
                else:
                    print("No result returned.")
            else:
                print(result)
            
            print("=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\n💡 Tip: Try browser automation directly:")
            print("   • For browser: uv run final_browser.py")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())