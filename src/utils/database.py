import sqlite3


class PostDB:
    def __init__(self, table_name: str, db_name: str, db_path: str = "./data/"):
        self.conn = sqlite3.connect(db_path + db_name)
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def create_table(self, drop: bool = False):
        """Create a table in database if it does not exist yet.
        Add columns id, topic and text.

        Args:
            drop (bool, optional): Drop table if it exists. Defaults to False.
        """
        if drop:
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, text TEXT)"
        )
        self.conn.commit()

    def insert(self, topic: str, text: str):
        """Insert a row into the table with the given topic and text."""
        self.cursor.execute(f"INSERT INTO {self.table_name} (topic, text) VALUES (?, ?)", (topic, text))
        self.conn.commit()

    def get_topics(self):
        """Get all unique topics from the table.

        Returns:
            list: list of topics
        """
        self.cursor.execute(f"SELECT DISTINCT topic FROM {self.table_name}")
        return self.cursor.fetchall()

    def get_texts(self, topic: str):
        """Get all texts for a given topic.

        Args:
            topic (str): topic

        Returns:
            list: list of texts
        """
        self.cursor.execute(f"SELECT text FROM {self.table_name} WHERE topic = ?", (topic,))
        return self.cursor.fetchall()
