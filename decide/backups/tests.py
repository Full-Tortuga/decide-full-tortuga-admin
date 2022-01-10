from django.test import TestCase
from .backups import *
from base.tests import BaseTestCase
# Create your tests here.
class TestBackups(BaseTestCase):
    def test_create_backups(self):
        response = self.client.post('/backups/create', "", format='json')
        self.assertEqual(response.status_code, 201)
        ls = os.listdir("./backups/backups")
        backup_test = ls[-1]
        os.system("rm -rf ./backups/backups/" + backup_test)
            
              
    def test_list_backups(self):
        response = self.client.get('/backups/list')
        self.assertEqual(response.status_code, 200)
        
        
    def test_restore_backup(self):
        self.client.post('/backups/create', "", format='json')
        ls = os.listdir("./backups/backups")
        bck_name = ls[-1]
        response = self.client.post('/backups/restore/' + bck_name)
        os.system("rm -rf ./backups/backups/" + bck_name)
        self.assertEqual(response.status_code, 200)
        
    def test_restore_backup_error(self):
        date = '30-12-2022-11:28:12'
        response = self.client.post('/backups/restore/' + date)
        self.assertEqual(response.status_code, 404)