import sqlite3
from typing import List, Any


class DataBase:
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)

    def list_test_cases(self) -> List[Any]:
        c = self.connection.cursor()
        c.execute('SELECT * FROM tcm_testcase')
        return c.fetchall()

    def delete_test_case(self, test_name: str) -> None:
        c = self.connection.cursor()
        c.execute('DELETE FROM tcm_testcase WHERE name=?', (test_name,))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
