
# El scrapper genera las URL de cada mesa de las elecciones 2023 para despues descargar el telegrama.

https://resultados.gob.ar/elecciones/1/53261/1/-1/-1/Buenos-Aires/Secci%C3%B3n-Cuarta/Leandro-N.-Alem/Leandro-N.-Alem/00553/ESCUELA-EP-N%C2%B08%2FES-N%C2%B06/0206600046X

```
pip install -r requirements
python scrapper.py
```


TODO:
 - Hay que seguir con otros distritos que tienen diferentes formas de filtrar la info
 - Armar el scrapper que vaya a la URL de la mesa y descargue el telegrama que esta en una imagen base64
 - Ordenar archivos en otra carpeta
 - Ignorar archivos .csv
 - Agregar black, flake8, etc.


