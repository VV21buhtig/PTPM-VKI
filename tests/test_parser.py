import os
import unittest
from src.parser import ForumParser
from src.database import DatabaseRepository


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        self.db = DatabaseRepository(":memory:")
        fixture_path = os.path.join(os.path.dirname(__file__), "fixture.html")
        with open(fixture_path, "r", encoding="utf-8") as f:
            self.sample_html = f.read()

    def tearDown(self):
        self.db.close()

    def test_parse_html_extracts_correct_data(self):
        parsed_data = self.parser.parse_html(self.sample_html)
        self.assertEqual(len(parsed_data), 2)
        self.assertEqual(parsed_data[0]["id"], 101)
        self.assertEqual(parsed_data[0]["name"], "ponchik")
        self.assertEqual(parsed_data[0]["message"], "<p>Всем привет! Я на <b>Arch Linux</b>.</p>")

    def test_save_to_db_integration(self):
        parsed_data = self.parser.parse_html(self.sample_html)
        saved_count = self.parser.save_to_db(parsed_data, self.db)
        self.assertEqual(saved_count, 2)

        post_from_db = self.db.get_by_id(102)
        self.assertIsNotNone(post_from_db)
        self.assertEqual(post_from_db["name"], "moderator")


if __name__ == "__main__":
    unittest.main()
