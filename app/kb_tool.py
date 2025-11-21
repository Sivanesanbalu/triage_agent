import json
from pathlib import Path

class KnowledgeBaseTool:
    def __init__(self):
        # Load KB on init
        try:
            file_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"
            with open(file_path, "r") as f:
                self.kb_data = json.load(f)
        except Exception as e:
            print(f"Error loading KB: {e}")
            self.kb_data = []

    def search(self, query: str, top_k: int = 3) -> list:
        """
        Simple scoring: Match words in ticket against KB title and symptoms.
        """
        query_words = set(query.lower().split())
        scored_results = []

        for entry in self.kb_data:
            score = 0
            # Check title overlap
            for word in entry['title'].lower().split():
                if word in query_words:
                    score += 2  # Higher weight for title
            
            # Check symptoms overlap
            for symptom in entry['symptoms']:
                if any(word in symptom.lower() for word in query_words):
                    score += 1
            
            if score > 0:
                scored_results.append((score, entry))

        # Sort by score desc
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K items (just the data, not the score)
        return [item[1] for item in scored_results[:top_k]]

# Singleton instance
kb_tool = KnowledgeBaseTool()