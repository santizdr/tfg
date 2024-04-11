import time
from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw

import psycopg2

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException


# Crea una tabla para ofertas de trabajo en caso de que no esté creada
def tear_up_db(connection, cursor):

    sql_create_table = """
    CREATE TABLE IF NOT EXISTS job_offer (
        id SERIAL PRIMARY KEY,
        title VARCHAR(160),
        description TEXT,
        posted_by VARCHAR(70)
    );
    """
    cursor.execute(sql_create_table)
    connection.commit()


def scrape_jobs(driver, job_cards, counter, cursor, connection):    
    # Recorre los elementos del listado
    for card in job_cards:
        job_title = posted_by = job_info = ""
        print("Iteracion: " + str(counter))
        time.sleep(1)

        # Click en oferta de trabajo. Almacena quien la publica la oferta de trabajo en variable
        card.click()
        time.sleep(3)

        try:
            job_title = card.find_element(By.CLASS_NAME, "base-search-card__title").text
            print("Titulo: " + job_title)

        except NoSuchElementException:
            print("No se pudo encontrar el elemento 'base-search-card__title'")
            counter += 1
            continue

        time.sleep(3)

        try:
            posted_by = card.find_element(By.CLASS_NAME, "hidden-nested-link").text
            print("Publicado por: " + posted_by)

        except NoSuchElementException:
            print("No se pudo encontrar el elemento 'hidden-nested-link'")
            counter += 1
            continue

        time.sleep(3)

        # Click en Mostrar más para ver la informacion de la oferta. La almacena en una variable
        try:
            # Intentar hacer clic en el botón "show more"
            time.sleep(2)

            show_more_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "show-more-less-html__button--more")))
            show_more_btn.click()
            job_info = driver.find_element(By.CSS_SELECTOR, "div.show-more-less-html__markup").text
            print(job_info)


        except (TimeoutException, ElementNotInteractableException) as e:
            print(e)
            counter += 1
            continue 

        time.sleep(3)

        # Inserta los datos de la oferta de trabajo en la tabla de la bbdd
        sql_insert = """
            INSERT INTO job_offer (title, description, posted_by)
            VALUES (%s, %s, %s);
        """

        cursor.execute(sql_insert, (job_title, job_info, posted_by))
        connection.commit()
        counter += 1

    return counter


def main(): 
    # Crea una conexion a la bbdd
    connection = psycopg2.connect(
        dbname="tfg_db",
        user="tfg_admin",
        password="tfg_secret11",
        host="localhost"
    )

    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    tear_up_db(connection, cursor)

    # Crea instancia de navegador, realiza la petición a la URL y pone pantalla completa
    driver = webdriver.Chrome(seleniumwire_options={"disable_encoding": True})
    target_url = 'https://www.linkedin.com/jobs/search?keywords=Desarrollador%20De%20Python&location=Spain&locationId=&geoId=105646813&f_TPR=r86400&position=1&pageNum=0'
    driver.get(target_url)
    driver.maximize_window()

    time.sleep(3)

    # Obtiene todos los objetos que listan las ofertas de trabajo y las almacena en una variable
    job_cards = driver.find_elements(By.CLASS_NAME, "job-search-card")
    num_job_cards = len(job_cards)
    print("INITIAL NUM JOB CARDS: " + str(num_job_cards))

    counter = 0

    while int(counter) != num_job_cards:
        counter = scrape_jobs(driver, job_cards, counter, cursor, connection)

        job_cards = driver.find_elements(By.CLASS_NAME, "job-search-card")
        num_job_cards = len(job_cards)
        print("==============")
        print("Nuevo numero de ofertas: " + str(num_job_cards))
        job_cards = job_cards[counter:]

        print("COUNTER" + str(counter))
        print(str(num_job_cards))
        print("==============")

        print("COMPROBACION")
        print(int(counter) != num_job_cards)

    # Cierra el cursor y la conexion de la bbdd
        
    
    time.sleep(3)

    cursor.close()
    connection.close()

main()