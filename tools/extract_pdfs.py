#!/usr/bin/env python3
"""
PDF to Markdown Converter for Prompt Guides Repository

OVERVIEW:
This script extracts text content from PDF files and converts them to markdown format.
It processes configured PDF files in the repository and creates corresponding markdown files.

FEATURES:
- Text extraction and cleaning from PDF documents
- Structure preservation with heading detection
- Batch processing of configured PDF files
- Automatic markdown formatting with page markers
- Text normalization and bullet point handling

USAGE:
    python extract_pdfs.py
    
    # Script processes PDF files configured in the main() function
    # Place PDF files in repository root and update the pdf_files list
    # Generated markdown files will be created in the same directory

DEPENDENCIES:
    PyMuPDF (fitz): pip install pymupdf>=1.26.0
    
CONFIGURATION:
    Edit the pdf_files list in main() function to add new PDF files:
    - 'path': PDF filename (in repository root)
    - 'title': Title for generated markdown
    - 'output': Output markdown filename

OUTPUT:
    - Structured markdown files with preserved document hierarchy
    - Page markers for reference (<!-- Page N -->)
    - Cleaned text with proper formatting
    - Heading detection and markdown conversion
"""

import fitz  # PyMuPDF
import os
import re
from typing import Dict, List, Tuple

def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove trailing/leading whitespace
    text = text.strip()
    # Fix common PDF extraction issues
    text = text.replace('\uf020', ' ')  # Replace bullet characters
    text = text.replace('\uf0b7', '• ')  # Replace bullet characters
    text = text.replace('\u2022', '• ')  # Replace bullet characters
    return text

def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """Extract text from PDF with page information."""
    try:
        doc = fitz.open(pdf_path)
        pages_content = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            if text.strip():  # Only add pages with content
                pages_content.append({
                    'page_number': page_num + 1,
                    'text': clean_text(text)
                })
        
        doc.close()
        return pages_content
        
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return []

def format_as_markdown(pages_content: List[Dict], title: str, source_file: str) -> str:
    """Convert extracted content to markdown format."""
    
    markdown_lines = [
        f"# {title}",
        "",
        f"*Extracted from: {source_file}*",
        "",
        "---",
        ""
    ]
    
    current_section = ""
    
    for page_data in pages_content:
        page_num = page_data['page_number']
        text = page_data['text']
        
        # Skip pages that are too short (likely page numbers, headers, etc.)
        if len(text) < 50:
            continue
            
        # Add page marker for reference
        markdown_lines.append(f"<!-- Page {page_num} -->")
        markdown_lines.append("")
        
        # Process text line by line
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect headings (lines that are short and don't end with punctuation)
            if (len(line) < 100 and 
                not line.endswith('.') and 
                not line.endswith(',') and 
                not line.endswith(':') and
                line.isupper() or 
                (line[0].isupper() and len(line.split()) <= 8)):
                
                # Determine heading level based on content
                if any(keyword in line.lower() for keyword in ['chapter', 'part', 'section']):
                    markdown_lines.append(f"## {line}")
                elif any(keyword in line.lower() for keyword in ['introduction', 'conclusion', 'overview']):
                    markdown_lines.append(f"## {line}")
                else:
                    markdown_lines.append(f"### {line}")
                markdown_lines.append("")
                current_section = line
            else:
                # Regular paragraph text
                # Check if it's a bullet point
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    markdown_lines.append(f"{line}")
                else:
                    markdown_lines.append(line)
                markdown_lines.append("")
        
        markdown_lines.append("")
    
    return '\n'.join(markdown_lines)

def main():
    """Main function to process PDF files."""
    
    # Define the PDF files to process
    pdf_files = [
        {
            'path': '2025-01-18-pdf-1-TechAI-Goolge-whitepaper_Prompt Engineering_v4.pdf',
            'title': 'Google AI Tech Whitepaper: Prompt Engineering Guide',
            'output': 'google-ai-tech-whitepaper-prompt-engineering.md'
        },
        {
            'path': 'gemini-for-google-workspace-prompting-guide-101.pdf',
            'title': 'Gemini for Google Workspace: Prompting Guide 101',
            'output': 'gemini-google-workspace-prompting-guide.md'
        }
    ]
    
    # Check if we're in the right directory
    if not os.path.exists('README.md'):
        print("Error: Please run this script from the prompt-guides repository root directory")
        return
    
    # Process each PDF file
    for pdf_info in pdf_files:
        pdf_path = pdf_info['path']
        
        if not os.path.exists(pdf_path):
            print(f"Warning: PDF file not found: {pdf_path}")
            continue
            
        print(f"Processing {pdf_path}...")
        
        # Extract content
        pages_content = extract_text_from_pdf(pdf_path)
        
        if not pages_content:
            print(f"Error: No content extracted from {pdf_path}")
            continue
        
        # Convert to markdown
        markdown_content = format_as_markdown(
            pages_content, 
            pdf_info['title'], 
            pdf_path
        )
        
        # Write markdown file
        output_path = pdf_info['output']
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✓ Created {output_path} ({len(pages_content)} pages processed)")
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
    
    print("\nPDF extraction completed!")
    print("\nNext steps:")
    print("1. Review the generated markdown files")
    print("2. Update README.md to include the new files")
    print("3. Consider removing the original PDF files to save space")

if __name__ == "__main__":
    main()
