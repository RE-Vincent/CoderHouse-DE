# CoderHouse-DE
## Proyecto de consumo de APIS e ingesta a Redshift

![API MARVEL](https://github.com/RE-Vincent/CoderHouse-DE/blob/main/images/ultron_marvel.jpg)

Para hacer uso de la API debes de registrate en la siguiente url http://developer.marvel.com/ y accederas a todo el contenido de Marvel como los personajes, los comics, las películas, los videojuegos y mucho más.
Despues de registrarte obtendras una clave pública y una privada que son necesarias para poder realizar las consultas.
En este ejemplo usamos los datos de los personajes y se realizaron algunas modificaciones para solo trabajar con una cantidad limitada de información.
A continuación una breve descripción de los datos:
- id: identificador unico del personaje.
- name: nombre del personje.
- description: resumen del personaje.
- modified: fecha de modificación.
- thumbnail: image del personaje.
- resourceURI: url.
- comics: número de comics.
- series: número de series.
- stories: número de stories.
- events: número de eventos en los que participó.
