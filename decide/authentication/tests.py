
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from base.tests import BaseTestCase
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from django.test.testcases import LiveServerTestCase
from base import mods


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
        data = {'username': 'testingUser',
                'password': '123', 'password2': '456'}
        response = self.client.post(
            '/authentication/register_user/', data, format='json')
        msg = response.json()['error']
        self.assertEqual(msg, 'Contraseñas no coinciden')
        self.assertEqual(response.status_code, 400)

    def test_registeruser_form(self):
        data = {'username': 'testingUser',
                'password': '123', 'password2': '123'}
        response = self.client.post(
            '/authentication/register_user/', data, format='json')
        self.assertEqual(response.status_code, 302)

    def test_loginuser_form(self):
        data_login = {'username': 'testingUser', 'password': '123'}
        response = self.client.post(
            '/authentication/login_form/', data_login, format='json')
        self.assertEqual(response.status_code, 200)

    def test_registeruser_existingusername(self):
        data_login = {'username': 'voter1',
                      'password': '123456', 'password2': '123456'}
        response = self.client.post(
            '/authentication/register_user/', data_login, format='json')
        msg = response.json()['error']
        self.assertEqual(msg, 'Ya existe este nombre de usuario')
        self.assertEqual(response.status_code, 400)

    def test_login_ldap_positive(self):
        body_form = {'username': 'foobar', 'password': 'test'}
        response = self.client.post(
            '/authentication/loginLDAP/', body_form, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_ldap_negative(self):
        body_form = {'username': 'foobar', 'password': 'contrasenyaMal'}
        response = self.client.post(
            '/authentication/loginLDAP/', body_form, format='json')
        self.assertEqual(response.status_code, 400)


# class SeleniumLandingPageTestCase(LiveServerTestCase):
#     def setUp(self):
#         self.base = BaseTestCase()
#         self.base.setUp()
#         chrome_options = Options()
#         chrome_options.add_argument("--window-size=1920,1080")
#         chrome_options.headless = True
#         self.driver = webdriver.Chrome(chrome_options=chrome_options)

#     def tearDown(self):
#         self.driver.quit()

#     def test_good_redirects_menu(self):

#         self.driver.get(f'{self.live_server_url}/authentication/welcome')
#         self.driver.find_element_by_id("methodsbutton").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/welcome/#portfolio')

#         self.driver.find_element_by_id("aboutbutton").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/welcome/#about')

#         self.driver.find_element_by_class_name("navbar-brand").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/welcome/#page-top')

#     def test_redirects_signin(self):
#         self.driver.get(f'{self.live_server_url}/authentication/welcome')

#         self.driver.find_element_by_id("signinbutton").click()
#         self.driver.find_element_by_id("ldaplogin").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

#         self.driver.execute_script("window.history.go(-1)")
#         self.driver.find_element_by_id("signinbutton").click()
#         self.driver.find_element_by_id("userlogin").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

#     def test_redirects_signup(self):
#         self.driver.get(f'{self.live_server_url}/authentication/welcome')
#         self.driver.find_element_by_id("signupbutton").click()
#         self.driver.find_element_by_id("signupuser").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

#     def test_redirects_logout(self):
#         self.driver.get(f'{self.live_server_url}/authentication/welcome')
#         self.driver.find_element_by_id("signinbutton").click()
#         self.driver.find_element_by_id("userlogin").click()
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

#         self.driver.find_element_by_name('username').send_keys("noadmin")
#         self.driver.find_element_by_name('password').send_keys("qwerty",Keys.ENTER)
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/bienvenida/')
#         self.driver.find_element_by_id("signoffbutton").click()
#         self.assertEqual(self.driver.current_url,f'{self.live_server_url}/authentication/userlogout/')

# class SeleniumTestCase(LiveServerTestCase):

#     def setUp(self):
#         self.base = BaseTestCase()
#         self.base.setUp()

#         options = webdriver.ChromeOptions()
#         # options.add_argument("--no-sandbox")
#         # options.add_argument("--disable-dev-shm-usage")
#         # options.add_argument("--headless")
#         self.driver = webdriver.Chrome(options=options)
#         super().setUp()

#     def tearDown(self):
#         super().tearDown()
#         self.driver.close()
#         self.driver.quit()
#         self.base.tearDown()

#     def test_register_user(self):
#         self.driver.get(f'{self.live_server_url}/authentication/login_form/')
#         self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(4) > .link").click()

#         self.driver.find_element_by_name('username').send_keys("userUser")
#         self.driver.find_element_by_name('password').send_keys("asd123")
#         self.driver.find_element_by_name('password2').send_keys("asd123",Keys.ENTER)

#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/login_form/')

#         self.driver.find_element_by_name('username').send_keys("userUser")
#         self.driver.find_element_by_name('password').send_keys("asd123",Keys.ENTER)

#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/bienvenida/')

#     def test_login_success(self):
#         self.driver.get(f'{self.live_server_url}/authentication/login_form/')
#         self.driver.find_element_by_name('username').send_keys("noadmin")
#         self.driver.find_element_by_name('password').send_keys("qwerty",Keys.ENTER)
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/bienvenida/')

# class SeleniumLDAPViewTestCase(LiveServerTestCase):

#     def setUp(self):
#         self.base = BaseTestCase()
#         self.base.setUp()

#         options = webdriver.ChromeOptions()
#         # options.add_argument("--no-sandbox")
#         # options.add_argument("--disable-dev-shm-usage")
#         # options.add_argument("--headless")
#         self.driver = webdriver.Chrome(options=options)
#         super().setUp()

#     def tearDown(self):
#         super().tearDown()
#         self.driver.close()
#         self.driver.quit()
#         self.base.tearDown()

#     def test_login_ldap_positive(self):
#         self.driver.get(f"{self.live_server_url}/authentication/login_form/")
#         self.driver.find_element(By.LINK_TEXT, "here").click()
#         self.driver.find_element(By.NAME, "username").send_keys("foobar")
#         self.driver.find_element(By.NAME, "password").send_keys("test")
#         self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

#         #Si el usuario inicia sesion de manera exitosa se muestra Welcome usuario en la esquina superior derecha
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/loginLDAP/')
#         self.assertTrue(self.driver.find_element_by_xpath('/html/body/nav/div/div/ul[3]'))
#         self.assertTrue(self.driver.find_element_by_xpath('/html/body/nav/div/div/ul[3]/ul/li[2]/a').get_attribute('innerHTML')=="Welcome foo")

#     def test_login_ldap_negative(self):
#         self.driver.get(f"{self.live_server_url}/authentication/login_form/")
#         self.driver.find_element(By.LINK_TEXT, "here").click()
#         self.driver.find_element(By.NAME, "username").send_keys("foobar")
#         self.driver.find_element(By.NAME, "password").send_keys("contrasenyaMAl")
#         self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

#         #Si el usuario inicia sesion de manera exitosa no se muestra Welcome usuario en la esquina superior derecha (mismo xpath que para el test positivo)
#         self.assertTrue(self.driver.current_url==f'{self.live_server_url}/authentication/loginLDAP/')
#         self.assertRaises(NoSuchElementException, self.driver.find_element_by_xpath, '/html/body/nav/div/div/ul[3]')
