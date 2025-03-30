import asyncio
import os
from crawl4ai import AsyncWebCrawler
import typer
from typing import List

from elastic_parse.utils.xmlparser import get_urls_from_sitemap_file
from elastic_parse.utils.configs import run_config

async def process_sitemap(sitemap_path: str, url_index: int = 0, output_dir: str = "output"):
    """
    Process a sitemap file and extract content from the URL at the specified index.
    
    Args:
        sitemap_path (str): Path to the sitemap XML file
        url_index (int): Index of the URL to process from the sitemap
        output_dir (str): Directory to save markdown files
        
    Returns:
        None
    """
    # Get URLs from sitemap file
    urls = get_urls_from_sitemap_file(sitemap_path)
    
    if not urls:
        print("No URLs found in the sitemap file.")
        return
    
    if url_index >= len(urls):
        print(f"URL index {url_index} is out of range. Only {len(urls)} URLs available.")
        return
    
    # Use the URL at the specified index from the sitemap
    selected_url = urls[url_index]
    print(f"Using URL: {selected_url}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=selected_url,
            config=run_config
        )
        
        # Extract filename from URL
        filename = selected_url.split('/')[-1].replace('.html', '.md')
        output_path = os.path.join(output_dir, filename)
        
        # Save markdown content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.markdown.raw_markdown)
            
        print(f"Saved markdown content to {output_path}")

def main(
    sitemap_path: str = typer.Argument("data/sitemap.xml", help="Path to the sitemap XML file"),
    url_index: int = typer.Option(0, "--index", "-i", help="Index of the URL to process from the sitemap"),
    output_dir: str = typer.Option("output", "--output", "-o", help="Directory to save markdown files")
):
    """Process a sitemap file and extract content from the URL at the specified index.
    
    Example:
        # Process the default sitemap file (first URL)
        $ python3 -m elastic_parse.extract
        
        # Process a specific URL by index
        $ python3 -m elastic_parse.extract --index 400
        
        # Process a custom sitemap file with specific URL index
        $ python3 -m elastic_parse.extract path/to/sitemap.xml --index 5
        
        # Specify output directory
        $ python3 -m elastic_parse.extract path/to/sitemap.xml -i 10 -o custom_output
    """
    asyncio.run(process_sitemap(sitemap_path, url_index, output_dir))

if __name__ == "__main__":
    typer.run(main)