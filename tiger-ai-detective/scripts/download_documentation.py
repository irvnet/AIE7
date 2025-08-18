#!/usr/bin/env python3
"""
Documentation Downloader for IBM Tiger Team Support System
Downloads IBM documentation files from the sources catalog for RAG system.
"""

import json
import os
import requests
import sys
from pathlib import Path
from urllib.parse import urlparse
import time
from typing import List, Dict

def load_sources_catalog() -> List[Dict]:
    """Load the sources catalog from JSON file"""
    catalog_path = Path("data/sources.catalog.json")
    if not catalog_path.exists():
        print(f"❌ Sources catalog not found at {catalog_path}")
        return []
    
    with open(catalog_path, 'r') as f:
        return json.load(f)

def create_download_directory() -> Path:
    """Create the download directory for documentation"""
    download_dir = Path("data/documentation")
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir

def download_file(url: str, filename: str, download_dir: Path) -> bool:
    """Download a file from URL to the download directory"""
    file_path = download_dir / filename
    
    # Skip if file already exists
    if file_path.exists():
        print(f"⏭️  Skipping {filename} (already exists)")
        return True
    
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

def get_filename_from_url(url: str, title: str) -> str:
    """Generate a filename from URL and title"""
    # Try to get filename from URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    if path.endswith('.pdf'):
        return os.path.basename(path)
    
    # Create filename from title
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    return f"{safe_title}.pdf"

def download_documentation():
    """Main function to download documentation files"""
    print("🚀 Starting IBM Documentation Download...")
    
    # Load sources catalog
    sources = load_sources_catalog()
    if not sources:
        return
    
    # Create download directory
    download_dir = create_download_directory()
    print(f"📁 Download directory: {download_dir}")
    
    # Filter for downloadable PDF files
    pdf_sources = [
        source for source in sources 
        if source.get('downloadable_pdf', False) and source.get('format') == 'PDF'
    ]
    
    print(f"📋 Found {len(pdf_sources)} downloadable PDF sources")
    
    # Download files
    successful_downloads = 0
    failed_downloads = 0
    
    for source in pdf_sources:
        product = source['product']
        title = source['title']
        url = source['url']
        
        print(f"\n📦 Processing: {product} - {title}")
        
        filename = get_filename_from_url(url, title)
        success = download_file(url, filename, download_dir)
        
        if success:
            successful_downloads += 1
        else:
            failed_downloads += 1
        
        # Add delay to be respectful to servers
        time.sleep(1)
    
    # Summary
    print(f"\n🎉 Download Summary:")
    print(f"✅ Successful: {successful_downloads}")
    print(f"❌ Failed: {failed_downloads}")
    print(f"📁 Files saved to: {download_dir}")
    
    # List downloaded files
    if successful_downloads > 0:
        print(f"\n📚 Downloaded Files:")
        for file_path in download_dir.glob("*.pdf"):
            print(f"  - {file_path.name}")

def main():
    """Main entry point"""
    try:
        download_documentation()
    except KeyboardInterrupt:
        print("\n⏹️  Download interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
