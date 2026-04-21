# Smart Automation Tool - Browser + Airbnb + Search

A comprehensive automation tool that understands natural language for browser automation, Airbnb searches, and web searches.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the smart automation tool (CLI):**
   ```bash
   uv run main.py
   ```
   
   **OR run just browser automation:**
   ```bash
   uv run final_browser.py
   ```

3. **Run the new web frontend (Streamlit):**
   ```bash
   uv run streamlit run frontend.py
   ```

4. **Give commands in natural language!**

## 📝 Example Commands

### Browser Automation
```
🎯 go to google.com and search for python tutorials
🎯 go amazon.in and search for laptop, click first result
🎯 open youtube.com and search for music videos
🎯 go bookmyshow.in, set location to bangalore, search for Eesha
```

### Airbnb Search
```
🏠 find hotels in Paris for 2 guests
🏠 search airbnb in Tokyo from 2024-03-01 to 2024-03-10
🏠 find places to stay in New York for 4 people
```

### Web Search
```
🔍 search for latest AI news
🔍 find information about Python programming
🔍 what is machine learning
```

## ✨ Features

### Browser Automation
- ✅ **Natural language understanding** - No coding required
- ✅ **Multi-step commands** - Navigate → Set location → Search → Click
- ✅ **Site-specific** - Works with Amazon, Google, YouTube, BookMyShow, etc.
- ✅ **Shows execution steps** - Transparent about what it's doing
- ✅ **Visual browser** - See the automation happen in real-time

### Airbnb Search
- ✅ **Find hotels and stays** - Search by location, dates, guests
- ✅ **Flexible queries** - Natural language location and date parsing
- ✅ **Real Airbnb results** - Uses official Airbnb MCP server

### Web Search
- ✅ **DuckDuckGo integration** - Private web search
- ✅ **Quick answers** - Get information without opening browser
- ✅ **No API keys** - Built-in search functionality

## 🎯 Supported Actions

### Browser
1. **Navigate** - `go to [website]`, `open [website]`
2. **Search** - `search for [query]`
3. **Set Location** - `set location to [city]`
4. **Click** - `click first result`, `select first`, `play first video`

### Airbnb
1. **Search by location** - `find hotels in [city]`
2. **Specify guests** - `for [number] guests`
3. **Add dates** - `from [YYYY-MM-DD] to [YYYY-MM-DD]`

### Web Search
1. **General search** - `search for [query]`
2. **Information lookup** - `what is [topic]`
3. **Find content** - `find information about [topic]`

## 📂 Project Structure

```
mcpdemo/
├── main.py               # 🎯 Main automation script (Browser + Airbnb + Search)
├── final_browser.py      # 🌐 Standalone browser automation
├── frontend.py           # 🖥️ Streamlit UI (prompts + results)
├── browser_mcp.json      # ⚙️  MCP server configuration
├── pyproject.toml        # 📦 Python dependencies
├── .env                  # 🔑 Environment variables (optional)
└── README.md             # 📄 This file
```

## 🛠️ How It Works

### Main Tool (`main.py`)
1. **Detects intent** - Determines if it's browser, Airbnb, or web search
2. **Routes to handler** - Calls appropriate automation module
3. **Executes command** - Performs the requested action
4. **Shows results** - Displays output in terminal

### Browser Only (`final_browser.py`)
1. **Parses your command** - Extracts URL, search queries, locations, actions
2. **Shows the steps** - Displays what it will do before executing
3. **Executes with Playwright** - Automates the browser
4. **Handles multiple steps** - Can chain actions together

## 🎨 Command Examples

### 🌐 Browser Automation Examples

#### Google
```
go to google.com and search for python tutorials
go google.com and search for machine learning
```

#### Amazon
```
go amazon.in and search for laptop
go to amazon.in and search for black shirt, click first result
go amazon.in and search for apple iphone 15 pro max, select first
```

#### YouTube
```
go youtube.com and search for music videos
open youtube.com and search for cooking recipes
go to youtube.com and search for python tutorials and play first video
```

#### BookMyShow
```
go bookmyshow.in, set location to bangalore, search for Eesha
go bookmyshow.in and set location to mumbai and search for movie Pushpa
```

### 🏠 Airbnb Search Examples

```
find hotels in Paris
find hotels in Paris for 2 guests
search airbnb in Tokyo from 2024-03-01 to 2024-03-10
find places to stay in New York for 4 people
search accommodation in London for 2 adults from 2024-06-15 to 2024-06-20
```

### 🔍 Web Search Examples

```
search for latest AI news
find information about Python programming
what is machine learning
who is the president of USA
search web for best restaurants in bangalore
```

## 🔧 Technical Details

- **Language:** Python 3.12
- **Browser:** Chromium (via Playwright)
- **Airbnb:** Official @openbnb/mcp-server-airbnb
- **Search:** DuckDuckGo (ddg-mcp-search)
- **Pattern Matching:** Regex-based natural language parsing
- **Async:** Built with asyncio for non-blocking operations
- **MCP Protocol:** Model Context Protocol for service integration

## 📦 Dependencies

- `playwright` - Browser automation
- `mcp-use` - MCP client library
- `python-dotenv` - Environment variables
- `asyncio` - Async operations

## 🤝 Contributing

This is a demo project. Feel free to extend it with more sites and actions!

## 📄 License

MIT License

---

**Made with ❤️ using Playwright and Python**
