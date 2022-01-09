from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

'''
README:

Para poder ejecutar este test, se debe crear un superusuario
con el siguiente comando:

./manage.py createsuperuser

con datos:
    username: admin
    password: qwerty
y hacer bypass de la restriccion de contraseña

Entrar en http://localhost:8000/administration/users
iniciar sesión con el usuario admin
y si hubiera más usuarios creados, hay que eliminarlos
antes de realizar los tests

'''


# USER TESTS
def log_in(driver, cont):
    try:
        print("Test LogIn")
        time.sleep(2)
        driver.get('http://localhost:8000/administration/')
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/div[1]/div/input').send_keys("admin")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/div[2]/div/input').send_keys("qwerty")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/button').click()
        time.sleep(2)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def log_out(driver, cont):
    try:
        print("Test LogOut")
        driver.get('http://localhost:8000/administration/')
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[1]/button').click()
        time.sleep(1)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def incorrect_log_in(driver, cont):
    try:
        print("Test LogIn Incorrecto")
        driver.get('http://localhost:8000/administration/')
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/div[1]/div/input').send_keys("badadmin")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/div[2]/div/input').send_keys("qwerty")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/button').click()
        time.sleep(1)
        elemento = driver.find_element(
            By.XPATH, '//*[@id="content"]/div/form/div[2]/p')
        error_text = 'Unable to log in with provided credentials.'
        if elemento.text == error_text:
            print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def create_user(driver, cont):
    try:
        print("Test Create User")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/users")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[1]').click()
        time.sleep(4)
        numalea = str(random.randint(0, 9)) + \
            str(random.randint(0, 9)) + str(random.randint(0, 9))
        username = str("nuevouser" + str(numalea))
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[1]/div/input').send_keys(username)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[2]/div/input').send_keys("passwordNew")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[3]/div/input').send_keys("Nueva")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[4]/div/input').send_keys("Cuenta")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[5]/div/input').send_keys("email@gmail.com")
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/button').click()
        time.sleep(5)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def make_staff(driver, cont):
    try:
        driver.get("http://localhost:8000/administration/users")
        print("Test hacer staff")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/span/input').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[5]').click()
        #driver.find_element(By.XPATH, '')
        print("Test correctamente realizado\n")

        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def make_superuser(driver, cont):
    try:
        driver.get("http://localhost:8000/administration/users")
        print("Test hacer superuser")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/span/input').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[6]').click()
        # print(element)
        #driver.find_element(By.XPATH, '')
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def delete_user(driver, cont):
    try:
        driver.get("http://localhost:8000/administration/users")
        print("Test borrar usuario")
        driver.find_element(
            By.XPATH, '//*[@id="content"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/span/input').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[3]').click()
        time.sleep(1)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


# VOTING TESTS
def create_voting(driver, cont):
    try:
        print("Test Create Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[1]').click()
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[1]/div/input').send_keys("Nueva votacion")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[2]/div/input').send_keys("descripcion")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/div/button[2]').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[1]/div/input').send_keys("Pregunta")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[2]/div/div/input').send_keys("Opcion A")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[3]/div/div/input').send_keys("Opcion B")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/div/button[2]').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[3]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/div/button[2]').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[4]/div/div/div/label[1]/span[1]/input').click()
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/button').click()
        time.sleep(5)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def update_voting(driver, cont):
    try:
        print("Test Update Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[1]').click()
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[1]/div/input').send_keys(" editada")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[1]/div/div/div[2]/div/input').send_keys(" editada")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/div/button[2]').click()
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[1]/div/input').send_keys(" editada")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[2]/div/div/input').send_keys(" 2")
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[2]/div/div/div[3]/div/div/input').send_keys(" 2")
        time.sleep(2)
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div[3]/div/form/div[5]/button').click()
        time.sleep(5)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def delete_voting(driver, cont):
    try:
        print("Test Delete Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[3]').click()
        time.sleep(4)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def start_voting(driver, cont):
    try:
        print("Test Start Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[4]').click()
        time.sleep(4)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def stop_voting(driver, cont):
    try:
        print("Test Stop Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[4]').click()
        time.sleep(4)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


def tally_voting(driver, cont):
    try:
        print("Test Tally Voting")
        time.sleep(1)
        driver.get("http://localhost:8000/administration/votings")
        time.sleep(4)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/span/input').click()
        driver.find_element(
            By.XPATH, '//*[@id="actions"]/div/button[4]').click()
        time.sleep(4)
        print("Test correctamente realizado\n")
        return cont
    except Exception as e:
        print("Error")
        print(e)
        cont = cont + 1
        return cont


if __name__ == "__main__":
    cont = 0
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # USER TESTS
    print("USER TESTS START \n")
    cont = incorrect_log_in(driver, cont)
    cont = log_in(driver, cont)
    cont = create_user(driver, cont)
    cont = create_user(driver, cont)
    cont = create_user(driver, cont)
    cont = create_user(driver, cont)
    time.sleep(2)
    cont = make_staff(driver, cont)
    time.sleep(2)
    cont = make_superuser(driver, cont)
    time.sleep(3)
    cont = delete_user(driver, cont)
    cont = log_out(driver, cont)
    print("Se han realizado los test de User")
    print("Se han encontrado: " + str(cont) + " errores \n\n")

    # VOTING TESTS
    print("VOTING TESTS START \n")
    cont2 = 0
    cont2 = log_in(driver, cont2)
    cont2 = create_voting(driver, cont2)
    update_voting(driver, cont2)
    cont2 = start_voting(driver, cont2)
    time.sleep(3)
    cont2 = stop_voting(driver, cont2)
    time.sleep(3)
    cont2 = tally_voting(driver, cont2)
    time.sleep(3)
    cont2 = delete_voting(driver, cont2)
    print("Se han realizado los test de Votings")
    print("Se han encontrado: " + str(cont2) + " errores \n\n")
