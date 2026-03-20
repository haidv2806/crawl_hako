"""
Utility script để quản lý danh sách skip URLs

Các chức năng:
- Xem danh sách skip URLs
- Thêm URL vào skip list
- Xóa URL khỏi skip list
- Làm sạch skip list
"""

import argparse
import json
from pathlib import Path
from config import (
    should_skip_url,
    add_skip_url,
    add_skip_urls_batch,
    get_skip_urls_count,
    print_skip_urls_stats,
    SKIP_URLS_FILE
)


def load_skip_urls():
    """Load skip URLs from file"""
    if SKIP_URLS_FILE.exists():
        with open(SKIP_URLS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f).get('urls', []))
    return set()


def save_skip_urls(urls_set):
    """Save skip URLs to file"""
    with open(SKIP_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'urls': sorted(list(urls_set)),
            'count': len(urls_set)
        }, f, indent=2, ensure_ascii=False)


def view_skip_urls():
    """View all skip URLs"""
    print_skip_urls_stats()


def add_url(url):
    """Add single URL to skip list"""
    add_skip_url(url)


def add_urls_from_file(file_path):
    """Add URLs from text file (one URL per line)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        added = add_skip_urls_batch(urls)
        print(f"✅ Imported {added} new URLs from {file_path}")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error: {e}")


def remove_url(url):
    """Remove URL from skip list"""
    urls = load_skip_urls()
    
    if url in urls:
        urls.remove(url)
        save_skip_urls(urls)
        print(f"✅ Removed from skip list: {url}")
    else:
        print(f"ℹ️ URL not found in skip list: {url}")


def clear_skip_list():
    """Clear all skip URLs"""
    confirm = input("⚠️ Are you sure you want to clear all skip URLs? (yes/no): ")
    
    if confirm.lower() == 'yes':
        save_skip_urls(set())
        print("✅ Skip list cleared")
    else:
        print("❌ Cancelled")


def export_skip_urls(output_file):
    """Export skip URLs to text file"""
    urls = load_skip_urls()
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in sorted(urls):
                f.write(url + '\n')
        
        print(f"✅ Exported {len(urls)} URLs to {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")


def check_url(url):
    """Check if URL is in skip list"""
    if should_skip_url(url):
        print(f"✅ URL is in skip list: {url}")
    else:
        print(f"❌ URL is NOT in skip list: {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage skip URLs list")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # View command
    subparsers.add_parser('view', help='View all skip URLs')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add URL to skip list')
    add_parser.add_argument('url', help='URL to add')
    
    # Add from file command
    import_parser = subparsers.add_parser('import', help='Import URLs from file')
    import_parser.add_argument('file', help='File path (one URL per line)')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove URL from skip list')
    remove_parser.add_argument('url', help='URL to remove')
    
    # Clear command
    subparsers.add_parser('clear', help='Clear all skip URLs')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export skip URLs to file')
    export_parser.add_argument('output', help='Output file path')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if URL is in skip list')
    check_parser.add_argument('url', help='URL to check')
    
    # Count command
    subparsers.add_parser('count', help='Show count of skip URLs')
    
    args = parser.parse_args()
    
    if args.command == 'view':
        view_skip_urls()
    
    elif args.command == 'add':
        add_url(args.url)
    
    elif args.command == 'import':
        add_urls_from_file(args.file)
    
    elif args.command == 'remove':
        remove_url(args.url)
    
    elif args.command == 'clear':
        clear_skip_list()
    
    elif args.command == 'export':
        export_skip_urls(args.output)
    
    elif args.command == 'check':
        check_url(args.url)
    
    elif args.command == 'count':
        count = get_skip_urls_count()
        print(f"📊 Total skip URLs: {count}")
    
    else:
        parser.print_help()
