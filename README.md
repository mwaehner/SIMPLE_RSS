Prerequisitos necesarios y forma de instalación en Ubuntu:

1- Python3 

```sudo apt-get install python3.6```

2- Pip (debería venir con python3)

``` sudo apt install python-pip``` 

3- Virtualenv . Recomendable trabajar sobre un virtual env para tener aisladas las dependencias del proyecto.

```pip install virtualenv```

Dependencias del proyecto

1- Primero crear un virtualenv corriendo desde la terminal 

```virtualenv myenv```

2- Luego correr 

```. myenv/bin/activate```

3- Una vez dentro del virtual env, correr:

```pip install -r requirements.txt```

Esto instalará automáticamente todas las dependencias del proyecto.

Ejecutando el proyecto

1- Antes de ejecutar el proyecto es necesario correr las migraciones.

```python manage.py migrate```

2- Para ejecutar finalmente, 

```python manage.py runserver```

Corriendo los tests


1- ```python manage.py test```

Comandos personalizados

-importsubscriptions: importa suscripciones que esten descritas en un archivo en formato OPML, como el de test_utils/opml_subscriptions.xml. 
Se usa así:

```python manage.py importsubscriptions --subscriptions <opml file> --user_ids <userid> <userid> ... <userid>```

Por ejemplo:

```python manage.py importsubscriptions --subscriptions test_utils/opml_subscriptions.xml --user_ids 2```

Si no se especifica ningún user_id, se importarán las suscripciones para todos los usuarios.



