import os
import logging
class Journal:
    def __init__(self, journal_id, name):
        self.journal_id = journal_id
        self.name = name

    def to_dict(self):
        return {
            "journal_id": self.journal_id,
            "name": self.name
        }

class JournalEntry:
    def __init__(self, entry_id, journal_id, title, content, date, image_path=None):
        self.entry_id = entry_id
        self.journal_id = journal_id
        self.title = title
        self.content = content
        self.date = date
        self.image_path = image_path

    def to_dict(self):
        entry_dict = {
            "entry_id": self.entry_id,
            "journal_id": self.journal_id,
            "title": self.title,
            "content": self.content,
            "date": self.date,
        }
        if self.image_path:
            entry_dict["image_url"] = f"http://127.0.0.1:5000/uploads/{os.path.basename(self.image_path)}"
        else:
            entry_dict["image_url"] = None
        return entry_dict