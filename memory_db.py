import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class MemoryDB:
    def __init__(self, db_file="memory.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                persona_description TEXT NOT NULL,
                output TEXT,
                description TEXT,
                tags TEXT,  -- JSON array of tags
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT TRUE
            )
        ''')
        self.conn.commit()

    def save_run(self, product: str, persona: str, output: str, description: str = "", tags: List[str] = None):
        """Save a run with structured data extraction"""
        if not isinstance(output, str):
            output = str(output)
        
        # Try to extract structured data from output
        if not description or not tags:
            description, tags = self._extract_structured_data(output)
        
        tags_json = json.dumps(tags) if tags else "[]"
        
        self.conn.execute(
            '''INSERT INTO runs (product_name, persona_description, output, description, tags) 
               VALUES (?, ?, ?, ?, ?)''',
            (product, persona, output, description, tags_json)
        )
        self.conn.commit()

    def _extract_structured_data(self, output: str) -> Tuple[str, List[str]]:
        """Extract description and tags from the output text"""
        description = ""
        tags = []
        
        # Simple parsing - you might want to make this more sophisticated
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            if 'description:' in line.lower():
                description = line.split(':', 1)[1].strip()
            elif 'tags:' in line.lower():
                tag_text = line.split(':', 1)[1].strip()
                # Extract tags from various formats
                tags = [tag.strip(' "\'') for tag in tag_text.replace('[', '').replace(']', '').split(',')]
                tags = [tag for tag in tags if tag]  # Remove empty strings
        
        return description, tags

    def fetch_last_run(self) -> Optional[Tuple]:
        """Fetch the most recent run"""
        cursor = self.conn.execute(
            'SELECT product_name, persona_description, output, timestamp FROM runs ORDER BY id DESC LIMIT 1'
        )
        return cursor.fetchone()
    def fetch_exact_run(self, product: str, persona: str) -> Optional[Dict]:
        """Fetch an exact previous run for given product and persona"""
        cursor = self.conn.execute(
            '''SELECT product_name, persona_description, output, description, tags, timestamp 
               FROM runs 
               WHERE product_name = ? AND persona_description = ? 
               ORDER BY id DESC LIMIT 1''',
            (product, persona)
        )
        row = cursor.fetchone()
        if row:
            try:
                tags = json.loads(row[4]) if row[4] else []
            except:
                tags = []
            return {
                'product': row[0],
                'persona': row[1],
                'output': row[2],
                'description': row[3],
                'tags': tags,
                'timestamp': row[5]
            }
        return None

    def fetch_similar_runs(self, product: str, persona: str, limit: int = 3) -> List[Tuple]:
        """Find similar runs based on product or persona"""
        cursor = self.conn.execute(
            '''SELECT product_name, persona_description, description, tags, timestamp 
               FROM runs 
               WHERE product_name LIKE ? OR persona_description LIKE ?
               ORDER BY id DESC LIMIT ?''',
            (f'%{product}%', f'%{persona}%', limit)
        )
        return cursor.fetchall()

    def get_popular_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most frequently used tags"""
        cursor = self.conn.execute('SELECT tags FROM runs WHERE tags IS NOT NULL')
        all_tags = []
        
        for (tags_json,) in cursor.fetchall():
            try:
                tags = json.loads(tags_json)
                all_tags.extend(tags)
            except:
                continue
        
        # Count tag frequency
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Return sorted by frequency
        return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

    def get_run_history(self, limit: int = 10) -> List[Dict]:
        """Get formatted run history"""
        cursor = self.conn.execute(
            '''SELECT product_name, persona_description, description, tags, timestamp 
               FROM runs ORDER BY id DESC LIMIT ?''',
            (limit,)
        )
        
        history = []
        for row in cursor.fetchall():
            try:
                tags = json.loads(row[3]) if row[3] else []
            except:
                tags = []
            
            history.append({
                'product': row[0],
                'persona': row[1],
                'description': row[2],
                'tags': tags,
                'timestamp': row[4]
            })
        
        return history

    def fetch_all_runs(self):
        cursor = self.conn.execute(
            'SELECT product_name, persona_description, output, timestamp FROM runs ORDER BY id DESC'
        )
        return cursor.fetchall()

    def close(self):
        self.conn.close()
