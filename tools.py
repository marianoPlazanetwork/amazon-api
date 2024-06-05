#Importar librerías
import re
import sys
import random
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Función de Intervalo de tiempo aleatorio entre cada solicitud realizada al servidor.
# Puede disminuir el intervalo de tiempo para realizar un scraping más rápido, sin embargo, 
# Se recomienda que no lo haga, ya que puede dañar el servidor y Amazon puede prohibir su dirección IP.
# Realizar el scraping responsablemente:
def tiempoAlea(val):
    ranges = [i for i in range(3, val+1)]
    return random.choice(ranges)


# Función de los agentes de usuaio para el servidor
def agenteUsuario():
    with open('user-agents.txt') as f:
        agente = f.read().split("\n")
        return random.choice(agente)


# Esto ayuda a evitar arrojar un error cuando no hay ningún elemento.
class TryExcept:
    def text(self, element):
        try:
            return element.inner_text().strip()
        except AttributeError:
            return "NO_AVAILABLE"

    def attributes(self, element, attr):
        try:
            return element.get_attribute(attr)
        except AttributeError:
            return "NO_AVAILABLE"

#función principal del código, se ingresa el enlace, dirigue hacia el producto y realiza la búsqueda y extracción de información
def scraping(head, term = ""):
    datosAmazon = []
    catchClause = TryExcept()
    
    #variables donde almacena que se quiere buscar y el enlace de amazon
    # produbuscar = str(input("Ingresa el nombre del producto que quieres buscar: "))
    produbuscar = term
    produinser = produbuscar.replace(" ","+")
    ingresoProducto = f"https://www.amazon.com/s?k={produinser}&language=en_US"   
    
    # Patrón de expresiones regulares para verificar si el enlace ingresado es el enlace de Amazon correcto:
    amazon_link_pattern = re.search("^https://www.amazon.com/s\?.+", ingresoProducto)
    if amazon_link_pattern == None:
        print(f"Enlace no válido. Ingrese un enlace de Amazon que incluya la categoría de producto de su elección.")
        sys.exit()
    
    with sync_playwright() as play:
        navegador = play.chromium.launch(headless=head, slow_mo=10*1000)
        pagina = navegador.new_page(user_agent=agenteUsuario())
        pagina.goto(ingresoProducto)

        pagina.wait_for_timeout(timeout=tiempoAlea(4)*1000)

        ##################### Selectores XPATH ###########################################################################################################
        # La siguiente variable es para el producto buscado, podría haber más de dos elementos para él.
        # try:
        #     print(pagina)
        #     nombreProducto = pagina.locator("//div[@id='departments']/ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-medium']/li[@class='a-spacing-micro s-navigation-indent-1']/span[@class='a-list-item']/span[@class='a-size-base a-color-base']").inner_text().strip()
        # except AttributeError:
        #     nombreProducto = pagina.locator("//div[@id='departments']/ul[@class='a-unordered-list a-nostyle a-vertical a-spacing-medium']/li[@class='a-spacing-micro']/span[@class='a-list-item']").inner_text().strip()
        
        totalPaginasUno = "//span[@class='s-pagination-item s-pagination-disabled']"
        totalPaginasDos = "//span[@class='s-pagination-strip']/a"
        siguienteBoton = "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"

        contenidoPrincipal = "//div[@data-component-type='s-search-result']"

        enlace = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"
        precio = "//span[@data-a-color='base']/span[@class='a-offscreen']"
        precioAnterior = "//span[@data-a-color='secondary']/span[@class='a-offscreen']"
        califica = "//span[@class='a-declarative']/a/i/span[@class='a-icon-alt']"
        numCalifica = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style']/span[@class='a-size-base s-underline-text']"
        imagen = "//img[@class='s-image s-image-optimized-rendering']"
        ###################################################################################################################################################
        # print(nombreProducto)
        
        try:
            pagina.wait_for_selector(contenidoPrincipal, timeout=0)
        except PlaywrightTimeoutError:
            print(f"Error al cargar contenido. Vuelva a intentarlo en unos minutos.")
            return []
        
        try:
            ultimaPagina = pagina.query_selector(
                totalPaginasUno).inner_text().strip()
        except AttributeError:
            ultimaPagina = pagina.query_selector_all(totalPaginasDos)[-2].get_attribute('aria-label').split()[-1]

        print(f"El número de Páginas es: {ultimaPagina}.")
        print(f"Realizando Scraping a: {produbuscar}.")
        
        # changeUltimapagina
        # ultimaPagina = "2"

        for click in range(1, int(ultimaPagina)):
            print(f"Página de Scraping N° {click}")
            pagina.wait_for_timeout(timeout=tiempoAlea(8)*1000)
            for content in pagina.query_selector_all(contenidoPrincipal):
                datos = {
                    "Producto": catchClause.text(content.query_selector(enlace)),
                    # Número de Identificación Estándar de Amazon(ASIN)
                    "ASIN": catchClause.attributes(content, 'data-asin'),
                    "Precio": catchClause.text(content.query_selector(precio)),
                    "Precio Original": catchClause.text(content.query_selector(precioAnterior)),
                    "Calificación": catchClause.text(content.query_selector(califica)),
                    "Num de Calificaciones": re.sub(r"[()]", "", catchClause.text(content.query_selector(numCalifica))),
                    "Enlace Producto": f"""http://www.amazon.com{catchClause.attributes(content.query_selector(enlace), 'href')}""",
                    "Imagen": f"""{catchClause.attributes(content.query_selector(imagen), 'src')}""",
                }
                #Agregando información recolectada
                datosAmazon.append(datos)

            try:
                pagina.query_selector(siguienteBoton).click()
            except AttributeError:
                print(f"Hay problemas con la sección {pagina.url} | Número: {click}")
                break
            except:
                break

        navegador.close()

    print(f"Scraping realizado con Exito. Se guardará un archivo CSV")
    # print(datosAmazon)
    # if (len(datosAmazon) > 0):
    #     print(datosAmazon[0])
    
    return datosAmazon
    #Guardamos el resultado en un archivo Excel y lo imprimimos   
    # df = pd.DataFrame(datosAmazon)
    # df.to_excel(f"{produbuscar}.xlsx", index=False)
    # print(f"{produbuscar} Se ha guardado con éxito")
    # dfrecien = pd.read_excel(f"{produbuscar}.xlsx")
    # print(dfrecien)

