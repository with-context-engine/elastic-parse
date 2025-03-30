import os
import pytest
import tempfile
from typing import List
from src.elastic_parse.utils.xmlparser import get_urls_from_sitemap_file

class TestXmlParser:
    """
    Test suite for the XML parser utility.
    """
    def test_get_urls_from_sitemap_file(self):
        """
        Test the get_urls_from_sitemap_file function.
        """
        # Create a temporary sitemap file for testing
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as temp_file:
            temp_file.write(b'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.elastic.co/guide/en/elasticsearch/reference/current/test1.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.elastic.co/guide/en/elasticsearch/reference/current/test2.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.example.com/not-elastic-doc.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>''')
        
        try:
            # Test the function
            urls = get_urls_from_sitemap_file(temp_file.name)
            
            # Verify results
            assert isinstance(urls, List)
            assert len(urls) == 2
            assert "https://www.elastic.co/guide/en/elasticsearch/reference/current/test1.html" in urls
            assert "https://www.elastic.co/guide/en/elasticsearch/reference/current/test2.html" in urls
            assert "https://www.example.com/not-elastic-doc.html" not in urls
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)
    
    def test_get_urls_from_nonexistent_file(self):
        # Test with a file that doesn't exist
        urls = get_urls_from_sitemap_file("nonexistent_file.xml")
        assert urls == []
    
    def test_get_urls_from_invalid_xml(self):
        # Create a temporary file with invalid XML
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as temp_file:
            temp_file.write(b'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.elastic.co/guide/en/elasticsearch/reference/current/test1.html</loc>
    <changefreq>weekly
  </url>
</urlset>''')
        
        try:
            # Test the function with invalid XML
            urls = get_urls_from_sitemap_file(temp_file.name)
            assert urls == []
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)
