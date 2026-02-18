#!/usr/bin/env python3
"""
CSV to URL Extractor
Extracts Instagram post URLs from CSV file and generates a Python list or text file
"""

import csv
import sys
from pathlib import Path

# Import config for colors
try:
    from config import Colors, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    # Fallback if config not available
    class Colors:
        RESET = ""
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""
    
    def print_header(text):
        print(f"\n{'='*70}\n{text}\n{'='*70}\n")
    
    def print_success(text):
        print(f"[SUCCESS] {text}")
    
    def print_error(text):
        print(f"[ERROR] {text}")
    
    def print_warning(text):
        print(f"[WARNING] {text}")
    
    def print_info(text):
        print(f"[INFO] {text}")


def ask_for_csv(prompt="Enter path to input CSV file: "):
    """
    Ask user for a CSV file path, check existence and readability.
    Loops until a valid file is provided.
    """
    while True:
        file_path = input(f"{Colors.BLUE}{prompt}{Colors.RESET}").strip()
        
        # Remove quotes if user copied from file explorer
        file_path = file_path.strip('"').strip("'")
        
        path = Path(file_path)

        if not path.exists():
            print_error(f"File not found: {file_path}")
            continue

        if not path.is_file():
            print_error(f"Not a file: {file_path}")
            continue

        if path.suffix.lower() not in [".csv", ".txt"]:
            print_warning(f"Not a CSV file: {file_path}")
            response = input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.RESET}").lower()
            if response != 'y':
                continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                f.readline()
        except Exception as e:
            print_error(f"Cannot open file: {e}")
            continue

        print_success(f"File loaded: {path}")
        return path

"""
def ask_for_column():
    Ask user which column contains URLs
    print_info("Which column contains the URLs?")
    print("  1. 'url' (default)")
    print("  2. 'URL'")
    print("  3. Custom column name")
    print("  4. Column number (0-indexed)")
    
    choice = input(f"{Colors.BLUE}Enter choice (1-4) or press Enter for default: {Colors.RESET}").strip()
    
    if not choice or choice == "1":
        return "url"
    elif choice == "2":
        return "URL"
    elif choice == "3":
        custom = input(f"{Colors.BLUE}Enter column name: {Colors.RESET}").strip()
        return custom
    elif choice == "4":
        col_num = input(f"{Colors.BLUE}Enter column number (0-indexed): {Colors.RESET}").strip()
        try:
            return int(col_num)
        except ValueError:
            print_error("Invalid number")
            return ask_for_column()
    else:
        print_warning("Invalid choice, using default 'url'")
        return "url"


def ask_for_output_format():
    Ask user for output format
    print_info("Select output format:")
    print("  1. Python list (post_urls.py)")
    print("  2. Text file - one URL per line (post_urls.txt)")
    print("  3. Both")
    
    choice = input(f"{Colors.BLUE}Enter choice (1-3) or press Enter for 'Both': {Colors.RESET}").strip()
    
    if choice == "1":
        return "python"
    elif choice == "2":
        return "text"
    else:
        return "both"


def ask_for_output_filename(default="post_urls"):
    Ask user for output filename
    filename = input(f"{Colors.BLUE}Enter output filename (without extension, default: {default}): {Colors.RESET}").strip()
    
    if not filename:
        return default
    
    # Remove extension if user added one
    filename = filename.replace(".py", "").replace(".txt", "")
    
    return filename

"""
def extract_urls(input_csv, column_name, output_format, output_base):
    """Extract URLs from CSV and save in specified format(s)"""
    urls = []

    try:
        with open(input_csv, newline='', encoding="utf-8") as f:
            # Try as CSV first
            try:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                
                # Handle column by name
                if isinstance(column_name, str):
                    if column_name not in fieldnames:
                        print_error(f"Column '{column_name}' not found")
                        print_info(f"Available columns: {', '.join(fieldnames)}")
                        raise ValueError(f"Missing '{column_name}' column in CSV file")
                    
                    for row in reader:
                        url = row.get(column_name)
                        if url:
                            urls.append(url.strip())
                
                # Handle column by index
                else:
                    f.seek(0)
                    reader = csv.reader(f)
                    header = next(reader)
                    
                    if column_name >= len(header):
                        raise ValueError(f"Column index {column_name} out of range (max: {len(header)-1})")
                    
                    for row in reader:
                        if len(row) > column_name:
                            url = row[column_name]
                            if url:
                                urls.append(url.strip())
            
            except csv.Error:
                # If CSV parsing fails, try line by line (maybe it's just a text file)
                f.seek(0)
                print_warning("CSV parsing failed, trying line-by-line reading")
                for line in f:
                    line = line.strip()
                    if line and (line.startswith("http://") or line.startswith("https://")):
                        urls.append(line)

    except Exception as e:
        print_error(f"Error reading CSV: {e}")
        raise

    # Remove duplicates while preserving order
    urls = list(dict.fromkeys(urls))
    
    print_success(f"{len(urls)} unique URLs extracted")

    # Save outputs
    try:
        if output_format in ["python", "both"]:
            output_py = Path(f"{output_base}.py")
            with open(output_py, "w", encoding="utf-8") as f:
                f.write("# Instagram Post URLs\n")
                f.write("# Generated by csv_to_url.py\n\n")
                f.write("POST_URLS = [\n")
                for url in urls:
                    f.write(f'    "{url}",\n')
                f.write("]\n")
            print_success(f"Python file created: {output_py}")
        
        if output_format in ["text", "both"]:
            output_txt = Path(f"{output_base}.txt")
            with open(output_txt, "w", encoding="utf-8") as f:
                for url in urls:
                    f.write(f"{url}\n")
            print_success(f"Text file created: {output_txt}")

    except Exception as e:
        print_error(f"Error writing output file: {e}")
        raise


def main():
    """Main function"""
    print_header("CSV → URL EXTRACTOR")
    print_info("Extract Instagram post URLs from CSV file\n")
    
    try:
        # Step 1: Get input CSV
        input_csv = ask_for_csv()
        
        # Step 2: Get column name
        print()
        column_name = "url" #ask_for_column()
        
        # Step 3: Get output format
        print()
        output_format = "text" #ask_for_output_format()
        
        # Step 4: Get output filename
        print()
        output_base = "temp" #ask_for_output_filename()
        
        # Step 5: Extract and save
        print()
        print_info("Processing...")
        extract_urls(input_csv, column_name, output_format, output_base)
        
        print()
        print_header("EXTRACTION COMPLETE")
        
    except KeyboardInterrupt:
        print()
        print_warning("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()