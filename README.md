# CoderHouse-DE
## Proyecto de consumo de APIS e ingesta a Redshift

![API MARVEL](https://github.com/RE-Vincent/CoderHouse-DE/blob/main/images/etf.jpg)

Para hacer uso de la API debes de registrate en la siguiente url https://site.financialmodelingprep.com/ y accederas a todo el contenido de de los mercados como los etf, acciones y mucho más.
Despues de registrarte obtendras una clave pública que es necesarias para poder realizar las consultas.
En este ejemplo usamos los datos de las ETFs y se realizaron algunas modificaciones para solo trabajar con una cantidad limitada de información.
A continuación una breve descripción de los datos:
- symbol: identificador unico del personaje.
- name: nombre del personje.
- price: resumen del personaje.
- exchange: fecha de modificación.
- exchangeShortName: image del personaje.
- type: url.
- date: número de comics.

Para replicar este projecto deberá de levantar una VM, en este caso se utilizó los servicios de google. La VM es recomendable que cuente como mínimo 4GB de RAM y 10 de disco.  

A continuación se presenta la arquitectura del projecto.  

![Arquitectura](https://github.com/RE-Vincent/CoderHouse-DE/blob/main/images/API_ETF.drawio.svg)

1. Construimos la maquina virtual en google cloud.  
- Podemos construirla de forma manual desde el servicio de Compute Engine.  
- También podemos construirla utilizando terraform, para ello debemos de tenerlo instalado en nuestra maquina, [guía](https://www.terraform.io/downloads).  
2. Una Vez instalado Terraform ejecuta lo siguiente.  
```bash 
terraform init
terraform plan
terraform apply
```
  
3. Revisar si se instaló docker y docker compose, de no ser así instalarlo con la siguiente línea.  
```bash 
./initscript_chef.sh
```
  
4. Ahora nos ubicamos en la carpeta airflow.  
- Creamos un archivo .env con las variables necesarias.  
- Para obtener la variable AIRFLOW_UID, ejecutamos:  
```bash 
echo $UID
```
  
5. Nuestro pipeline consta de tres tareas, si cualquier tarea falla nos enviará una notificación al correo.  
![pipeline](https://github.com/RE-Vincent/CoderHouse-DE/blob/main/images/pipeline_etf.png)
  
6. Configuración del correo para poder recibir las notificaciones.  
- Entramos a la configuración de la cuenta gmail.  
- Vamos al apartado de seguridad.  
- Activamos la verificación en dos pasos.  
- Buscamos "contraseña de aplicación".  
- Generamos nuestra contraseña y estacolocamos en nuestro archivo .env lo siguiente smtp_user: gmail, smtp_password: contraseña.  

7. Divertirse.  
