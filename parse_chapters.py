#!/usr/bin/env python3
"""
Parse the index.html file and extract chapters with their content.
Each h1 tag represents a chapter.
"""

from bs4 import BeautifulSoup
import json
import re

def parse_chapters(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the main content area
    main_content = soup.find('div', class_='stackedit__html')
    
    if not main_content:
        print("Could not find main content area")
        return None
    
    # Extract chapters
    chapters = []
    current_chapter = None
    chapter_content = []
    
    for element in main_content.children:
        if element.name == 'h1':
            # Save previous chapter if exists
            if current_chapter:
                chapters.append({
                    'id': current_chapter.get('id', ''),
                    'title': current_chapter.get_text().strip(),
                    'content': ''.join(str(tag) for tag in chapter_content)
                })
            
            # Start new chapter
            current_chapter = element
            chapter_content = []
        elif current_chapter:
            # Add content to current chapter
            chapter_content.append(element)
    
    # Don't forget the last chapter
    if current_chapter:
        chapters.append({
            'id': current_chapter.get('id', ''),
            'title': current_chapter.get_text().strip(),
            'content': ''.join(str(tag) for tag in chapter_content)
        })
    
    return chapters

if __name__ == '__main__':
    chapters = parse_chapters('/app/index.html')
    
    if chapters:
        print(f"Found {len(chapters)} chapters:")
        for i, chapter in enumerate(chapters):
            print(f"{i+1}. {chapter['title']} (ID: {chapter['id']})")
            print(f"   Content length: {len(chapter['content'])} characters")
        
        # Save to JSON
        with open('/app/chapters.json', 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        
        print("\nChapters saved to chapters.json")
