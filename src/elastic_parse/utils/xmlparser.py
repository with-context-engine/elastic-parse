import xml.etree.ElementTree as ET
from typing import List
import typer
import sys

def get_urls_from_sitemap_file(filepath: str) -> List[str]:
    """
    Reads URLs from a local sitemap XML file.
    
    Args:
        filepath (str): Path to the XML sitemap file
        
    Returns:
        List[str]: List of URLs extracted from the sitemap that match the Elasticsearch docs pattern
        
    Example:
        urls = get_urls_from_sitemap_file('data/sitemap.xml')
    """
    try:
        # Parse the XML file
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Define the namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Extract all URLs from the loc elements and filter for ES docs
        base_url = "https://www.elastic.co/guide/en/elasticsearch/reference/current/"
        urls = [
            loc.text for loc in root.findall('.//ns:loc', namespace)
            if loc.text and loc.text.startswith(base_url)
        ]
        
        return urls
        
    except Exception as e:
        print(f"Error parsing sitemap file: {e}")
        return []

app = typer.Typer()

@app.command()
def extract_urls(
    filepath: str = typer.Argument(..., help="Path to the XML sitemap file"),
    output: str = typer.Option(None, "--output", "-o", help="Output file to save URLs (if not provided, prints to stdout)")
):
    """
    Extract URLs from a sitemap XML file and print them or save to a file.
    
    Example:
        # Print URLs to stdout
        $ python -m elastic_parse.utils.xml extract-urls data/sitemap.xml
        
        # Save URLs to a file
        $ python -m elastic_parse.utils.xml extract-urls data/sitemap.xml -o urls.txt
    """
    urls = get_urls_from_sitemap_file(filepath)
    
    if not urls:
        typer.echo("No URLs found in the sitemap file.")
        raise typer.Exit(code=1)
    
    if output:
        try:
            with open(output, 'w') as f:
                for url in urls:
                    f.write(f"{url}\n")
            typer.echo(f"Extracted {len(urls)} URLs to {output}")
        except Exception as e:
            typer.echo(f"Error writing to output file: {e}")
            raise typer.Exit(code=1)
    else:
        for url in urls:
            typer.echo(url)
        typer.echo(f"\nTotal URLs found: {len(urls)}")

if __name__ == "__main__":
    app()