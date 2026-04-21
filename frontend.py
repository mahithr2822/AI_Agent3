"""
Simple Streamlit frontend to run:
- Browser automation (Playwright, no API keys)
- MCP Agent (Playwright + Airbnb + DuckDuckGo via Groq)
"""

import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq
from groq import BadRequestError
from mcp_use import MCPAgent, MCPClient

from final_browser import SmartBrowser


# ---------- Helpers ----------
def build_agent():
    """Create an MCP agent (Playwright + Airbnb + DuckDuckGo)"""
    load_dotenv()
    os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"

    # Check Groq API key early
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise RuntimeError("Missing GROQ_API_KEY. Add it to .env or env vars.")

    config = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["-y", "@playwright/mcp@latest"],
            },
            "airbnb": {
                "command": "npx",
                "args": ["-y", "@openbnb/mcp-server-airbnb"],
            },
            "duckduckgo-search": {
                "command": "npx",
                "args": ["-y", "ddg-mcp-search@latest"],
                "env": {
                    "npm_config_cache": "/Users/mahithr/.cursor/worktrees/mcpdemo/ysk/.npm-cache",
                },
            },
        }
    }

    client = MCPClient.from_dict(config)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_key)
    agent = MCPAgent(llm=llm, client=client, max_steps=30, verbose=False)
    return agent


async def run_browser_command(command: str):
    """Run a single browser command via SmartBrowser"""
    browser = SmartBrowser()
    try:
        if not await browser.start():
            return "Failed to start browser"
        await browser.execute_command(command)
        return "Done (browser stays open)"
    finally:
        # Keep the browser open so the user can see the page.
        # If you need to close it, manually close the Chromium window.
        pass


def run_agent_once(agent: MCPAgent, prompt: str) -> str:
    """Run MCP agent once with guardrails for Airbnb price schema"""
    wrapped = (
        "IMPORTANT: When calling airbnb_search, pass minPrice/maxPrice as numbers (no quotes). "
        "If unsure about price, omit those fields. "
        f"User request: {prompt}"
    )
    try:
        return asyncio.run(agent.run(wrapped))
    except BadRequestError:
        return (
            "Airbnb request failed because price values were not numeric.\n"
            "Try again without price filters (e.g., 'find hotels in Paris for 2 guests')."
        )
    except Exception as e:
        return f"Error: {e}"


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Smart Automation", page_icon="🤖", layout="centered")
st.title("🤖 Smart Automation")
st.caption("Browser automation + MCP agent (Playwright + Airbnb + DuckDuckGo)")

mode = st.radio(
    "Choose mode",
    ["Browser automation(Groq_API_KEY)"],
)

command = st.text_area("Enter your command", height=120)
run = st.button("Run")

if run and command.strip():
    if mode.startswith("Browser"):
        st.info("Launching browser... (Chromium will open visibly)")
        with st.spinner("Running browser automation..."):
            result = asyncio.run(run_browser_command(command.strip()))
        st.success("Finished")
        st.write(result)
    else:
        st.info("Running MCP agent (Groq)...")
        try:
            with st.spinner("Thinking..."):
                agent = build_agent()
                result = run_agent_once(agent, command.strip())
            st.success("Finished")
            st.write(result)
        except Exception as e:
            st.error(
                "Could not run MCP Agent.\n\n"
                f"{e}\n\n"
                "Tip: Ensure GROQ_API_KEY is set and valid. "
                "You can still use 'Browser automation (no API key)' mode."
            )

