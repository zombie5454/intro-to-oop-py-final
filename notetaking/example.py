# Yes its empty on purpose (I just want the folder structures XD)
from dotenv import load_dotenv
import os
import json
import requests
from datetime import date

# Example reference: https://www.python-engineer.com/posts/note-taking-python/
class NotionClient:
    def __init__(self) -> None:
        self.header = {
            "Authorization": "Bearer " + os.getenv('NOTION_INTEGRATION_TOKEN'),
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22",
        }
        self.db_id = os.getenv("NOTION_DB_ID")
    
    def create_note(self, title, content):
        api = "https://api.notion.com/v1/pages"
        data = {
            "parent": {"database_id": self.db_id},
            "properties": {
                "Title": {
                    "title": [{
                        "text": {
                            "content": title
                        }
                    }]
                },
                "CreatedAt": {
                    "date": {
                        "start": date.today().isoformat(),
                        "end": None
                    }
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        }
        req_body = json.dumps(data)
        res = requests.post(api, headers=self.header, data=req_body)
        print(res.status_code)
        print(res.json())
        return res


if __name__ == "__main__":
    load_dotenv()
    nC = NotionClient()
    nC.create_note("Test#1", "This is some sweet sweet text")