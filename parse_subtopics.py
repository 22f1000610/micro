#!/usr/bin/env python3
"""
Parse the index.html file and extract subtopics (h2 level).
This provides finer-grained content loading for better performance.
"""

from bs4 import BeautifulSoup
import json
import re

def parse_subtopics(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the main content area
    main_content = soup.find('div', class_='stackedit__html')
    
    if not main_content:
        print("Could not find main content area")
        return None
    
    # Extract chapters and subtopics
    structure = []
    current_chapter = None
    current_subtopic = None
    subtopic_content = []
    subtopic_counter = 0
    
    for element in main_content.children:
        if element.name == 'h1':
            # Save previous subtopic if exists
            if current_subtopic:
                structure.append({
                    'id': subtopic_counter,
                    'chapter_id': current_chapter.get('id', ''),
                    'chapter_title': current_chapter['title'],
                    'subtopic_id': current_subtopic.get('id', ''),
                    'subtopic_title': current_subtopic.get_text().strip(),
                    'content': ''.join(str(tag) for tag in subtopic_content),
                    'type': 'subtopic'
                })
                subtopic_counter += 1
            
            # Start new chapter
            current_chapter = {
                'id': element.get('id', ''),
                'title': element.get_text().strip()
            }
            current_subtopic = None
            subtopic_content = []
            
        elif element.name == 'h2':
            # Save previous subtopic if exists
            if current_subtopic and current_chapter:
                structure.append({
                    'id': subtopic_counter,
                    'chapter_id': current_chapter.get('id', ''),
                    'chapter_title': current_chapter['title'],
                    'subtopic_id': current_subtopic.get('id', ''),
                    'subtopic_title': current_subtopic.get_text().strip(),
                    'content': ''.join(str(tag) for tag in subtopic_content),
                    'type': 'subtopic'
                })
                subtopic_counter += 1
            
            # Start new subtopic
            current_subtopic = element
            subtopic_content = []
            
        elif current_chapter:
            # Add content to current subtopic
            if current_subtopic:
                subtopic_content.append(element)
            else:
                # Content before first h2 in chapter (intro)
                if not subtopic_content:
                    current_subtopic = {'id': f'intro-{current_chapter["id"]}', 'text': 'Introduction'}
                subtopic_content.append(element)
    
    # Don't forget the last subtopic
    if current_subtopic and current_chapter:
        structure.append({
            'id': subtopic_counter,
            'chapter_id': current_chapter.get('id', ''),
            'chapter_title': current_chapter['title'],
            'subtopic_id': current_subtopic.get('id', ''),
            'subtopic_title': current_subtopic.get_text().strip() if hasattr(current_subtopic, 'get_text') else current_subtopic['text'],
            'content': ''.join(str(tag) for tag in subtopic_content),
            'type': 'subtopic'
        })
    
    return structure

if __name__ == '__main__':
    subtopics = parse_subtopics('/app/index_old.html')
    
    if subtopics:
        print(f"Found {len(subtopics)} subtopics:")
        
        # Group by chapter for display
        chapters = {}
        for item in subtopics:
            ch_title = item['chapter_title']
            if ch_title not in chapters:
                chapters[ch_title] = []
            chapters[ch_title].append(item['subtopic_title'])
        
        for ch_title, subs in chapters.items():
            print(f"\n{ch_title} ({len(subs)} subtopics)")
            for sub in subs[:3]:  # Show first 3
                print(f"  - {sub}")
            if len(subs) > 3:
                print(f"  ... and {len(subs) - 3} more")
        
        # Save to JSON
        with open('/app/subtopics.json', 'w', encoding='utf-8') as f:
            json.dump(subtopics, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Subtopics saved to subtopics.json")
        print(f"  Total size: {len(json.dumps(subtopics)) / (1024*1024):.2f} MB")
