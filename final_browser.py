import asyncio
import re
from playwright.async_api import async_playwright

class SmartBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def start(self):
        """Start browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.set_viewport_size({"width": 1280, "height": 720})
            print("✅ Browser ready!")
            return True
        except Exception as e:
            print(f"❌ Failed to start: {e}")
            return False
    
    async def close(self):
        """Close browser"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
    
    def parse_command(self, command):
        """Parse command into steps"""
        steps = []
        command_lower = command.lower()
        
        # Extract URL
        url_match = re.search(r'(?:go to|open|go|visit)\s+([^\s,]+\.(?:com|in|org|net|co\.in))', command_lower)
        if url_match:
            url = url_match.group(1)
            if not url.startswith('http'):
                url = 'https://' + url
            steps.append(('navigate', url))
        
        # Extract location setting
        location_match = re.search(r'set.*?location.*?(?:to|to the)\s+([a-zA-Z]+)', command_lower)
        if location_match:
            steps.append(('set_location', location_match.group(1).capitalize()))
        
        # Extract search query (flexible pattern to handle typos like "seach", "serch")
        search_match = re.search(r'(?:search|seach|serch).*?(?:for|for the)\s+(.+?)(?:\s*,|\s+and\s+select|\s+and\s+click|$)', command_lower)
        if search_match:
            query = search_match.group(1).strip()
            # Clean up query - remove trailing words like "select", "click", "and"
            query = re.sub(r'\s*,\s*$', '', query)  # Remove trailing comma
            query = re.sub(r'\s+and\s+(select|click).*$', '', query)  # Remove select/click instructions
            query = query.strip()
            steps.append(('search', query))

        # Detect follow-up: "in amazon.in search for ..."
        amazon_followup = re.search(r'in\s+amazon\.?in\s+(?:search|seach|serch)\s+(?:for|for the)\s+(.+?)(?:\s*,|\s+and\s+select|\s+and\s+click|$)', command_lower)
        if amazon_followup:
            amazon_query = amazon_followup.group(1).strip()
            amazon_query = re.sub(r'\s*,\s*$', '', amazon_query)
            amazon_query = re.sub(r'\s+and\s+(select|click).*$', '', amazon_query)
            amazon_query = amazon_query.strip()
            steps.append(('navigate', 'https://amazon.in'))
            steps.append(('search', amazon_query))
        
        # Extract click action (more flexible - detect various click patterns)
        click_patterns = [
            'click first', 'click on first', 'click the first',
            'select first', 'select the first', 'select on first',
            'open first', 'open the first', 'open on first',
            'click on the first video', 'click first video',
            'play first', 'play the first', 'play first video'
        ]
        if any(keyword in command_lower for keyword in click_patterns):
            steps.append(('click_first', None))
        
        return steps
    
    async def execute_steps(self, steps):
        """Execute parsed steps"""
        for action, data in steps:
            try:
                if action == 'navigate':
                    print(f"\n🌐 Going to {data}...")
                    await self.page.goto(data, timeout=30000)
                    await asyncio.sleep(2)
                    print(f"✅ Loaded: {await self.page.title()}")
                
                elif action == 'set_location':
                    print(f"\n📍 Setting location to {data}...")
                    # Try to find and click location
                    try:
                        # Look for location text
                        location_elem = self.page.locator(f'text=/{data}/i').first
                        await location_elem.click(timeout=3000)
                        await asyncio.sleep(2)
                        print(f"✅ Location set!")
                    except:
                        print(f"⚠️  Please set location manually to {data}")
                
                elif action == 'search':
                    print(f"\n🔍 Searching for: {data}")
                    
                    # Site-specific search selectors
                    selectors = [
                        ('input#twotabsearchtextbox', 'Amazon'),  # Amazon
                        ('textarea[name="q"]', 'Google'),  # Google
                        ('input#search', 'YouTube'),  # YouTube
                        ('input[type="search"]', 'Generic'),
                        ('input[placeholder*="search" i]', 'Generic'),
                    ]
                    
                    found = False
                    for selector, site in selectors:
                        try:
                            search_box = await self.page.wait_for_selector(selector, timeout=3000)
                            await search_box.fill(data)
                            await search_box.press('Enter')
                            await asyncio.sleep(2)
                            print(f"✅ Search completed on {site}!")
                            found = True
                            break
                        except:
                            continue
                    
                    if not found:
                        print("⚠️  Could not find search box")
                
                elif action == 'click_first':
                    print(f"\n👆 Clicking first result...")
                    try:
                        # YouTube video selectors (try multiple as YouTube updates frequently)
                        youtube_selectors = [
                            'ytd-video-renderer a#video-title',  # YouTube video title link
                            'a#video-title',  # YouTube video title (shorter)
                            'ytd-video-renderer #thumbnail',  # YouTube thumbnail
                            'ytd-video-renderer',  # YouTube video container
                            'div#dismissible a#thumbnail',  # YouTube thumbnail with dismissible
                        ]
                        
                        # Amazon search result selectors (they change often)
                        amazon_selectors = [
                            'div[data-component-type="s-search-result"] h2 a',  # Amazon product title
                            'div.s-result-item h2 a',  # Amazon result item
                            'span.a-size-medium.a-color-base.a-text-normal',  # Amazon product name span
                            '.s-product-image-container a',  # Amazon product image link
                            'div[data-cy="title-recipe"] a',  # Amazon title recipe
                        ]
                        
                        # Try other sites
                        other_selectors = [
                            'h3 a',  # Google
                        ]
                        
                        all_selectors = youtube_selectors + amazon_selectors + other_selectors
                        
                        for selector in all_selectors:
                            try:
                                first_result = await self.page.wait_for_selector(selector, timeout=3000)
                                if first_result:
                                    await first_result.click()
                                    await asyncio.sleep(3)
                                    print(f"✅ Clicked first result!")
                                    print(f"   Selector used: {selector}")
                                    return
                            except Exception as e:
                                continue
                        
                        # If no selector worked, try getting all links and click the first product link
                        print("⚠️  Trying alternative method...")
                        try:
                            # Get all links on the page
                            links = await self.page.query_selector_all('a[href*="/dp/"]')  # Amazon product links
                            if links and len(links) > 0:
                                await links[0].click()
                                await asyncio.sleep(3)
                                print(f"✅ Clicked first result using alternative method!")
                                return
                        except:
                            pass
                        
                        print("⚠️  Could not find first result to click")
                    except Exception as e:
                        print(f"⚠️  Error clicking: {e}")
            
            except Exception as e:
                print(f"❌ Error in step '{action}': {e}")
    
    async def execute_command(self, command):
        """Main execution"""
        print(f"\n📝 Command: {command}")
        steps = self.parse_command(command)
        
        if not steps:
            print("❌ Could not understand command")
            return
        
        print(f"📋 Steps: {len(steps)}")
        for i, (action, data) in enumerate(steps, 1):
            print(f"   {i}. {action}: {data}")
        
        await self.execute_steps(steps)
        print(f"\n✅ Done! Page: {await self.page.title()}")

async def main():
    print("\n🚀 Smart Browser Automation (No API Required!)")
    print("=" * 70)
    
    browser = SmartBrowser()
    if not await browser.start():
        return
    
    print("\n📝 Example commands:")
    print("  • go to google.com and search for python tutorials")
    print("  • go amazon.in and search for laptop, click first result")
    print("  • open youtube.com and search for music videos")
    print("  • go bookmyshow.in, set location to bangalore, search for Eesha")
    print("=" * 70)
    
    while True:
        try:
            print("\n" + "=" * 70)
            command = input("🎯 Command: ").strip()
            
            if command.lower() in ['exit', 'quit', 'q']:
                break
            
            if command:
                await browser.execute_command(command)
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    await browser.close()
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
