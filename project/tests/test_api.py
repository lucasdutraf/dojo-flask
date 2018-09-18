import unittest, json

from project import db
from project.tests.base import BaseTestCase
from project.api.models import Task


def add_task(title, description):
    task = Task(title, description)
    db.session.add(task)
    db.session.commit()
    return task

class TestApi(BaseTestCase):
    def test_get_all_tasks(self):
        add_task('EPS', 'Tirar SS')
        add_task('MDS', 'Tirar SS')
        
        with self.client:
            response = self.client.get('/api/tasks')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['tasks']), 2)

            self.assertIn('success', data['status'])

            self.assertIn('EPS', data['data']['tasks'][0]['title'])
            self.assertIn('Tirar SS', data['data']['tasks'][0]['description'])

            self.assertIn('MDS', data['data']['tasks'][1]['title'])
            self.assertIn('Tirar SS', data['data']['tasks'][1]['description'])   

    def test_get_single_task(self):
        task = add_task('EPS', 'Tirar SS')

        with self.client:
            response = self.client.get(f'/api/tasks/{task.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])

            self.assertIn('EPS', data['data']['title'])
            self.assertIn('Tirar SS', data['data']['description'])

    def test_get_single_task_no_id(self):
        with self.client:
            response = self.client.get('/api/tasks/asd')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Task not found', data['message'])

    def test_get_single_task_inexistent_id(self):
        with self.client:
            response = self.client.get('/api/tasks/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Task not found', data['message'])

    def test_add_task(self):
        with self.client:
            response = self.client.post(
                '/api/tasks',
                data = json.dumps({
                    'title': 'EPS',
                    'description': 'Tirar SS'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            
            self.assertEqual(response.status_code, 201)
            self.assertIn('Task EPS - Tirar SS was created!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_add_task_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/api/tasks',
                data = json.dumps({}),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_title(self):
        with self.client:
            response = self.client.post(
                '/api/tasks',
                data = json.dumps({
                    'description': 'Testar 400'
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_description(self):
        with self.client:
            response = self.client.post(
                '/api/tasks',
                data = json.dumps({
                    'title': 'Testes'
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_change_task_status_done(self):
        task = add_task('EPS', 'Tirar SS')        

        with self.client:
            response = self.client.patch(
                f'/api/tasks/{task.id}',
                data = json.dumps({
                    'done': True
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('Task completed!', data['data']['task_status'])
            self.assertIn('success', data['status'])

    def test_change_task_status_undone(self):
        task = add_task('EPS', 'Tirar SS')        

        with self.client:
            response = self.client.patch(
                f'/api/tasks/{task.id}',
                data = json.dumps({
                    'done': False
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('Task not complete!', data['data']['task_status'])
            self.assertIn('success', data['status'])

    def test_remove_task(self):
        task = add_task('EPS', 'Tirar MS')

        with self.client:
            response = self.client.delete(f'/api/tasks/{task.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('Task deleted!', data['data']['message'])      
            self.assertIn('success', data['status'])                  

if __name__ == '__main__':
    unittest.main()