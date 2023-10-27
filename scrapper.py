import os
import csv
import sys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

"""

Para ver resultados y telegrama, la URL se compone de

https://resultados.gob.ar/elecciones/1/89759/1/-1/-1/<DISTRITO>/<SECCION>/<CIRCUITO>/<COMICIO>/<MESA>

Ej: https://resultados.gob.ar/elecciones/1/89759/1/-1/-1/Chubut/Escalante/00089/ESCUELA-PROVINCIAL-N%C2%B0-104/0701500970X
"""
URL = "https://resultados.gob.ar/elecciones/1/0/1/-1/-1"


# Ignorar porque tiran algunos errores
IGNORAR_MUNICIPIO = [
    "Junín",
    "Carlos Casares",
    "General Rodríguez",
    "José C. Paz",
    "Malvinas Argentinas",
    "Morón",
    "Pilar",
    "Tigre",
]

class Scrapper:

    def esperar_elemento(self, xpath):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def listar_y_guardar_items(self, attr, id_menu, op=True):
        if op:
            self.driver.find_element(By.XPATH, f'//*[@id="{id_menu}"]').find_element(By.XPATH, '..').find_element(By.TAG_NAME, 'button').click()

        if not attr:
            [attr.append(e.text) for e in self.driver.find_elements(By.XPATH, f'//*[@id="{id_menu}"]/li')]
        return sorted(attr)

    def reactivar_selector(self, id_menu):
        self.driver.find_element(By.XPATH, f'//*[@id="{id_menu}"]').find_element(By.XPATH, '..').find_element(By.TAG_NAME, 'button').click()

    def buenos_aires(self):
        boton_filtro_xpath = '//*[@id="root"]/div[2]/div[2]/div[1]/div[2]/div[1]/button'
        options = Options()
        options.add_argument("--force-device-scale-factor=0.50") # El scale es por un tema del scroll que aveces no lee los elemenos porque estaban "escondidos" por el scroll
        options.add_argument("--high-dpi-support=0.50")
        options.add_argument("--window-size=1600,1080")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(URL)

        # Abrir filtro
        self.esperar_elemento(boton_filtro_xpath)
        self.driver.find_element(By.XPATH, boton_filtro_xpath).click()
        self.driver.find_element(By.XPATH, f'//*[@id="downshift-1-toggle-button"]').click()


        distritos = list()
        seccion_primera = list()
        seccion_segunda = list()
        municipios = list()
        circuitos = list()
        localidades = list()
        mesas = list()
        items = list()
        items_municipio = []
        for distrito in self.listar_y_guardar_items(distritos, "menu-2", op=False):
            if distrito != "Buenos Aires":
                continue
            print(f"--> {distrito} <--")

            self.driver.find_element(By.XPATH, f'//*[@id="menu-2"]/li[text()="{distrito}"]').click()

            for seccion_1 in self.listar_y_guardar_items(seccion_primera, "menu-3"):
                self.driver.find_element(By.XPATH, f'//*[@id="menu-3"]/li[text()="{seccion_1}"]').click()

                for seccion_2 in self.listar_y_guardar_items(seccion_segunda, "menu-4"):
                    self.driver.find_element(By.XPATH, f'//*[@id="menu-4"]/li[text()="{seccion_2}"]').click()

                    for municipio in self.listar_y_guardar_items(municipios, "menu-5"):
                        if os.path.exists(f"{municipio}.csv"):
                            print(f"Municipio completado: {municipio}")
                            continue

                        if municipio in IGNORAR_MUNICIPIO:
                            print(f"Ignorar municipio: {municipio}")
                            continue

                        items_municipio = []
                        self.driver.find_element(By.XPATH, f'//*[@id="menu-5"]/li[text()="{municipio}"]').click()

                        for circuito in self.listar_y_guardar_items(circuitos, "menu-6"):
                            self.driver.find_element(By.XPATH, f'//*[@id="menu-6"]/li[text()="{circuito}"]').click()

                            for local in self.listar_y_guardar_items(localidades, "menu-7"):
                                self.driver.find_element(By.XPATH, f'//*[@id="menu-7"]/li[text()="{local}"]').click()

                                for mesa in self.listar_y_guardar_items(mesas, "menu-8"):
                                    self.driver.find_element(By.XPATH, f'//*[@id="menu-8"]/li[text()="{mesa}"]').click()
                                    link_mesa = self.driver.find_element(By.XPATH, '//a[text()="Aplicar filtros"]').get_attribute('href')
                                    print(link_mesa)
                                    print("--> Siguiente mesa")
                                    self.reactivar_selector("menu-8")
                                    itemmesa = [
                                        distrito,
                                        seccion_1,
                                        seccion_2,
                                        municipio,
                                        circuito,
                                        local,
                                        mesa,
                                        link_mesa
                                    ]
                                    items.append(itemmesa)
                                    items_municipio.append(itemmesa)
                                mesas.clear()
                                self.reactivar_selector("menu-7")
                            localidades.clear()
                            self.reactivar_selector("menu-6")
                        circuitos.clear()
                        self.reactivar_selector("menu-5")
                    self.guardar_csv(items_municipio, nombre=f"{municipio}.csv")
                    municipios.clear()
                    self.reactivar_selector("menu-4")
                seccion_segunda.clear()
                self.reactivar_selector("menu-3")
            seccion_primera.clear()
            self.reactivar_selector("menu-2")


        self.driver.close()
        self.guardar_csv(items)

    def guardar_csv(self, items, nombre="urls.csv"):
        if not items:
            print(f"No hay items para guardar en {nombre}")
            return
        with open(nombre, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for item in items:
                writer.writerow(item)


if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.buenos_aires()
