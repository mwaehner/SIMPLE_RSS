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

1- Antes de ejecutar el proyecto es necesario hacer y correr las migraciones. Primero hacemos:

```python manage.py makemigrations```

y luego

```python manage.py migrate```

2- Para ejecutar finalmente, 

```python manage.py runserver```

Corriendo los tests

1- ```python manage.py test```

(aún no hay)



