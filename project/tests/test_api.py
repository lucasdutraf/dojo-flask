import unittest, json

from project import db
from project.tests.base import BaseTestCase
from project.api.models import Task

if __name__ == '__main__':
    unittest.main()


def add_task(title, description):
    task = Task(title, description)
    db.session.add(task)
    db.session.commit()
    return task 

class TestApi(BaseTestCase):
    def test_get_all_tasks(self):
        add_task("sou lindo", "tenho fome")
        add_task("ele eh lindo", "saleh")
        add_task("ontem? hoje?", "q?")

        with self.client:
            response = self.client.get("/api/tasks")
            response_data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data["data"]["tasks"]), 3)
