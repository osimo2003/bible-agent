import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

class BibleMatchingAgent:
    def __init__(self):
        # Load Bible data
        self.bible_data = self._load_bible_data()
        self.topic_to_verses = self._load_topic_index()
        
        # New Testament books in order
        self.new_testament_books = [
            "Matthew", "Mark", "Luke", "John", "Acts",
            "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
            "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
            "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
            "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
        ]
        
        # Chapters per book in New Testament
        self.book_chapters = {
            "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
            "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6,
            "Ephesians": 6, "Philippians": 4, "Colossians": 4, "1 Thessalonians": 5,
            "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
            "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
            "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
        }
    
    def _load_bible_data(self) -> Dict:
        """Load Bible verses from JSON file"""
        data_path = Path("data") / "bible_verses.json"
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # For MVP, use a small sample
            return self._create_sample_data()
    
    def _create_sample_data(self) -> Dict:
        """Create sample Bible data for MVP"""
        return {
            "verses": [
                {
                    "book": "Matthew",
                    "chapter": 1,
                    "verse": 1,
                    "text": "The book of the genealogy of Jesus Christ, the son of David, the son of Abraham."
                },
                {
                    "book": "Matthew",
                    "chapter": 1,
                    "verse": 2,
                    "text": "Abraham was the father of Isaac, and Isaac the father of Jacob, and Jacob the father of Judah and his brothers."
                },
                # Add more verses as needed
            ]
        }
    
    def _load_topic_index(self) -> Dict[str, List[str]]:
        """Load topic to verse mapping"""
        # This would be a pre-built index
        return {
            "anxiety": ["Philippians 4:6-7", "1 Peter 5:7", "Matthew 6:34"],
            "fear": ["Isaiah 41:10", "2 Timothy 1:7", "Psalm 23:4"],
            "peace": ["John 14:27", "Philippians 4:7", "Isaiah 26:3"],
            "hope": ["Jeremiah 29:11", "Romans 15:13", "Psalm 42:11"],
            "love": ["1 Corinthians 13:4-7", "John 3:16", "Romans 8:38-39"],
            "faith": ["Hebrews 11:1", "Matthew 17:20", "2 Corinthians 5:7"],
            "encouragement": ["Joshua 1:9", "Isaiah 40:31", "Romans 8:28"]
        }
    
    def get_daily_reading(self, current_book: str, last_chapter: int) -> Dict[str, Any]:
        """Get next 2 chapters for daily reading"""
        if current_book not in self.new_testament_books:
            current_book = "Matthew"
            last_chapter = 0
        
        book_index = self.new_testament_books.index(current_book)
        chapters_in_book = self.book_chapters[current_book]
        
        # Calculate next chapters
        chapter_start = last_chapter + 1
        chapter_end = chapter_start + 1  # 2 chapters per day
        
        # Check if we need to move to next book
        if chapter_end > chapters_in_book:
            # Move to next book
            if book_index + 1 < len(self.new_testament_books):
                next_book = self.new_testament_books[book_index + 1]
                return {
                    "book": next_book,
                    "chapter_start": 1,
                    "chapter_end": min(2, self.book_chapters[next_book]),
                    "is_new_book": True
                }
            else:
                # Completed New Testament!
                return {
                    "book": "Revelation",
                    "chapter_start": 22,
                    "chapter_end": 22,
                    "is_complete": True
                }
        
        return {
            "book": current_book,
            "chapter_start": chapter_start,
            "chapter_end": chapter_end,
            "is_new_book": False
        }
    
    def find_verses_by_topic(self, topic: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Find verses by topic"""
        if topic in self.topic_to_verses:
            verse_refs = self.topic_to_verses[topic][:limit]
            verses = []
            for ref in verse_refs:
                verse_data = self.get_verse_by_reference(ref)
                if verse_data:
                    verses.append(verse_data)
            return verses
        return []
    
    def get_verse_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """Get verse by reference (e.g., 'John 3:16')"""
        # Parse reference
        import re
        match = re.match(r'([1-3]?\s?[A-Za-z]+)\s+(\d+):(\d+)', reference)
        if match:
            book = match.group(1).title()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            
            # Search in data
            for verse_data in self.bible_data.get("verses", []):
                if (verse_data["book"] == book and 
                    verse_data["chapter"] == chapter and 
                    verse_data["verse"] == verse):
                    return verse_data
        
        return None
    
    def generate_reflection_question(self, book: str, chapter: int) -> str:
        """Generate reflection question for daily reading"""
        questions_by_book = {
            "Matthew": "How does this teaching apply to your life today?",
            "Mark": "What does this reveal about Jesus' character?",
            "Luke": "How does this story demonstrate God's compassion?",
            "John": "What does this say about Jesus' relationship with people?",
            "Acts": "How can you apply the early church's example?",
            "Romans": "What truth about God's grace stands out to you?",
            "Revelation": "How does this vision of eternity change your perspective?"
        }
        
        return questions_by_book.get(book, "What is God saying to you through this passage?")
