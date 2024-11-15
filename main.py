#!/usr/bin/env python3

import asyncio
import os
from crawl4ai import AsyncWebCrawler
import sys
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

async def scrape_url(url, target_dir, verbose=False):
    async with AsyncWebCrawler(verbose=verbose) as crawler:
        try:
            print(f"{Fore.CYAN}Scraping {url}...")
            result = await crawler.arun(url=url)
            
            # Use the page title if available, otherwise use a sanitized URL
            page_title = result.metadata.get("title", "").strip().replace('/', '_').replace(':', '_')
            if not page_title:
                page_title = urlparse(url).netloc
            filename = os.path.join(target_dir, f"{page_title}.md")
            
            with open(filename, "w") as f:
                f.write(result.markdown)
            print(f"{Fore.GREEN}Saved content from {url} to {filename}")
        except Exception as e:
            print(f"{Fore.RED}Failed to scrape {url}: {e}")

async def main():
    print(f"{Fore.YELLOW}Welcome to the Web Scraper CLI!")
    
    # Ask for URLs
    urls = []
    while True:
        url = input(f"{Fore.BLUE}Enter a URL to scrape (or type 'done' to finish): {Style.RESET_ALL}").strip()
        if url.lower() == 'done' or not url:
            break
        if url:
            urls.append(url)
    
    if not urls:
        print(f"{Fore.YELLOW}No URLs provided. Exiting.")
        return
    
    # Ask for target directory
    target_dir = input(f"{Fore.GREEN}Enter the target directory to save the scraped content: {Style.RESET_ALL}").strip()
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
            print(f"{Fore.GREEN}Created directory: {target_dir}")
        except Exception as e:
            print(f"{Fore.RED}Failed to create directory: {e}. Exiting.")
            return
    
    # Scrape each URL
    tasks = [scrape_url(url, target_dir, verbose=True) for url in urls]
    await asyncio.gather(*tasks)

    print(f"{Fore.YELLOW}All URLs have been processed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation interrupted by user. Exiting.")
        sys.exit(1)