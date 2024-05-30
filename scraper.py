import time
from tools import scraping


tiempoInicio = time.time()

# Haga falso si desea ver la automatización en vivo.
make_headless = True

scraping(make_headless)

tiempoTotal = round(time.time()-tiempoInicio, 2)
tiempoSegundos = round(tiempoTotal)
tiempoMinutos = round(tiempoTotal/60)

print(f"Tiempo Requerido: {tiempoMinutos} minutos o {tiempoSegundos} segundos")

