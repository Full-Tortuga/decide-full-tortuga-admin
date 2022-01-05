
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base.tests import BaseTestCase
from base import mods

from local_settings import AUTH_LDAP_SERVER_URI

class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post(
            '/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        # self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post(
            '/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(
            user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post(
            '/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(
            user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post(
            '/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(
            user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post(
            '/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post(
            '/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post(
            '/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(
            '/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'admin'})
        response = self.client.post(
            '/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    # incremento

    def test_getusers_API(self):
        response = self.client.get(
            '/authentication/users/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_getuser_API(self):
        data = {'username': 'user1', 'password': '12345'}
        response = self.client.post(
            '/authentication/users/', data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            '/authentication/users/', format='json')
        self.assertEqual(response.status_code, 200)

        users = response.json()

        id = users[-1]['id']
        response = self.client.get(
            f'/authentication/users/{id}/', format='json')
        user = response.json()
        self.assertEqual(user['id'], id)
        self.assertEqual(user['username'], 'user1')

    def test_notfound_user_API(self):
        response = self.client.get(
            '/authentication/users/100/', format='json')
        self.assertEqual(response.status_code, 404)

    def test_postuser_API(self):
        data = {'username': 'user2', 'password': '12345'}
        response = self.client.post(
            '/authentication/users/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_postuser_alreadyexists_API(self):
        response = self.client.get(
            '/authentication/users/', format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()[0]
        username = user['username']
        data = {'username': username, 'password': '12345'}
        response = self.client.post(
            '/authentication/users/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_postuser_withoutusername_API(self):
        data = {'password': '12345'}
        response = self.client.post(
            '/authentication/users/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_postuser_withoutpassword_API(self):
        data = {'username': 'user3'}
        response = self.client.post(
            '/authentication/users/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_putuser_API(self):
        response = self.client.get(
            '/authentication/users/', format='json')
        self.assertEqual(response.status_code, 200)

        users = response.json()

        id = users[-1]['id']
        response = self.client.get(
            f'/authentication/users/{id}/', format='json')
        user = response.json()
        self.assertEqual(user['id'], id)

        username = user['username']
        data = {'username': username+'X', 'password': '12345'}
        response = self.client.put(
            f'/authentication/users/{id}/', data, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f'/authentication/users/{id}/', format='json')
        user = response.json()
        self.assertEqual(user['id'], id)
        self.assertEqual(user['username'], username+'X')

    def test_putuser_username_alreadyexists_API(self):
        response = self.client.get(
            '/authentication/users/', format='json')
        self.assertEqual(response.status_code, 200)

        users = response.json()

        id1 = users[-1]['id']
        id2 = users[-2]['id']
        response = self.client.get(
            f'/authentication/users/{id2}/', format='json')
        user = response.json()

        username = user['username']
        data = {'username': username, 'password': '12345'}
        response = self.client.put(
            f'/authentication/users/{id1}/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_deleteuser_API(self):
        data = {'username': 'user5', 'password': '12345'}
        response = self.client.post(
            '/authentication/users/', data,  format='json')
        self.assertEqual(response.status_code, 201)

        user = response.json()
        id = user['id']

        response = self.client.delete(
            f'/authentication/users/{id}/', format='json')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            f'/authentication/users/{id}/', format='json')
        self.assertEqual(response.status_code, 404)

    def test_deleteuser_doesntexist_API(self):
        response = self.client.delete(
            '/authentication/users/100/', format='json')
        self.assertEqual(response.status_code, 404)


    def test_differentpasswords_register(self):
        data = {'username':'testingUser', 'password': '123', 'password2':'456'}
        response = self.client.post(
            '/authentication/register_user/', data, format='json')
        msg = response.json()['error']
        self.assertEqual(msg, 'Contraseñas no coinciden')
        self.assertEqual(response.status_code, 400) 

    def test_registeruser_form(self):
        data = {'username':'testingUser', 'password': '123', 'password2':'123'}
        response = self.client.post(
            '/authentication/register_user/', data, format='json')
        self.assertEqual(response.status_code, 302)

    def test_loginuser_form(self):
        data_login = {'username':'testingUser', 'password': '123'}
        response = self.client.post(
            '/authentication/login_form/', data_login, format='json')
        self.assertEqual(response.status_code, 200)

    def test_registeruser_existingusername(self):
        data_login = {'username':'voter1', 'password': '123456', 'password2':'123456'}
        response = self.client.post(
            '/authentication/register_user/', data_login, format='json')
        msg = response.json()['error']
        self.assertEqual(msg, 'Ya existe este nombre de usuario')
        self.assertEqual(response.status_code, 400)

    #
    #   TODO: Arreglar tests, estos tests asumen que el sistema ya tiene registrado un usuario 'foobar' en ldap,
    #   lo cual es erroneo, tiene que registrarse dicho usuario en el setup de los tests
    #
    # def test_login_ldap_positive(self):
    #     body_form = {'username': 'foobar', 'password': 'test'}
    #     response = self.client.post(
    #         '/authentication/loginLDAP/', body_form, format='json')
    #     self.assertEqual(response.status_code, 200)
    # def test_login_ldap_negative(self):
    #     body_form = {'username': 'foobar', 'password': 'contrasenyaMal'}
    #     response = self.client.post(
    #         '/authentication/loginLDAP/', body_form, format='json')
    #     self.assertEqual(response.status_code, 400)



class SeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        super().setUp()            
            
    def tearDown(self):
        super().tearDown()
        self.driver.close()
        self.driver.quit()
        self.base.tearDown()

    def test_register_user(self):
        self.driver.get(f'{self.live_server_url}/authentication/login_form/')
        self.driver.find_elements_by_class_name("controller")[1].click()

        self.driver.find_element_by_name('username').send_keys("userUser")
        self.driver.find_element_by_name('password').send_keys("asd123")
        self.driver.find_element_by_name('password2').send_keys("asd123",Keys.ENTER)

        self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

        self.driver.find_element_by_name('username').send_keys("userUser")
        self.driver.find_element_by_name('password').send_keys("asd123",Keys.ENTER)
        
        self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/bienvenida/')
        self.driver.quit()

    def test_login_success(self):                    
        self.driver.get(f'{self.live_server_url}/authentication/login_form/')
        self.driver.find_element_by_name('username').send_keys("noadmin")
        self.driver.find_element_by_name('password').send_keys("qwerty",Keys.ENTER)
        
        self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/bienvenida/')
        self.driver.quit()