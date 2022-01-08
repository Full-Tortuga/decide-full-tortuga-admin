[![Admin Build CI](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/django.yml)
[![Admin Frontend CI](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/react.yml/badge.svg?branch=main)](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/react.yml)

[![Test Deployment CD](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/herokuDevelop.yml/badge.svg?branch=main)](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/herokuDevelop.yml)
[![Test Deployment CD](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/herokuMain.yml/badge.svg?branch=main)](https://github.com/Full-Tortuga/decide-full-tortuga-admin/actions/workflows/herokuMain.yml)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/94a85eaa0e974c71af6899ea3b0d27e0)](https://www.codacy.com/app/Wadobo/decide?utm_source=github.com&utm_medium=referral&utm_content=wadobo/decide&utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/94a85eaa0e974c71af6899ea3b0d27e0)](https://www.codacy.com/app/Wadobo/decide?utm_source=github.com&utm_medium=referral&utm_content=wadobo/decide&utm_campaign=Badge_Coverage)

Plataforma voto electrónico educativa

El objetivo de este proyecto es implementar una plataforma de voto
electrónico seguro, que cumpla una serie de garantías básicas, como la
anonimicidad y el secreto del voto.

Se trata de un proyecto educativo, pensado para el estudio de sistemas de
votación, por lo que prima la simplicidad por encima de la eficiencia
cuando sea posible. Por lo tanto se asumen algunas carencias para permitir
que sea entendible y extensible.

## Subsistemas, apps y proyecto base

El proyecto se divide en [subsistemas](doc/subsistemas.md), los cuales estarán desacoplados
entre ellos. Para conseguir esto, los subsistemas se conectarán entre si mediante API y necesitamos un proyecto base donde configurar las ruts de estas API.

Este proyecto Django estará dividido en apps (subsistemas y proyecto base), donde cualquier app podrá ser reemplazada individualmente.

## Gateway

Para ofrecer un punto de entrada conocido para todos los subsistemas
existe el llamado **gateway** que no es más que una ruta disponible
que redirigirá todas las peticiones al subsistema correspondiente, de
tal forma que cualquier cliente que use la API no tiene por qué saber
en qué servidor está desplegado cada subsistema.

La ruta se compone de:

    http://DOMINIO/gateway/SUBSISTEMA/RUTA/EN/EL/SUBSISTEMA

Por ejemplo para acceder al subsistema de autenticación y hacer la petición
al endpoint de /authentication/login/ deberíamos hacer la petición a la
siguiente ruta:

    http://DOMINIO/gateway/authentication/login/

Otro ejemplo sería para obtener una votación por id:

    http://DOMINIO/gateway/voting/?id=1

A nivel interno, el módulo `mods` ofrece esta funcionalidad, pero el
gateway es útil para hacer uso desde peticiones de cliente, por ejemplo
en el javascript de la cabina de votación o la visualización de resultados,
y también para módulos externos que no sean aplicaciones django.

## Configurar y ejecutar el proyecto

Para configurar el proyecto, podremos crearnos un fichero local_settings.py basado en el
local_settings.example.py, donde podremos configurar la ruta de nuestras apps o escoger que módulos
ejecutar.

Se hará uso de la base de datos MongoDB, para el correcto funcionamiento de la aplicación será necesaria la instalación de dicha base de datos siguiendo las instrucciones de la documentación oficial según el SO que estemos utilizando:

Windows: - https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/

Ubuntu: - https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

WSL: - https://docs.microsoft.com/es-es/windows/wsl/tutorials/wsl-database#install-mongodb

MacOs: - https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/

Una vez hecho esto, y corriendo la base de datos, será necesario instalar las dependencias del proyecto, las cuales están en el
fichero requirements.txt:

    pip install -r requirements.txt

En caso de fallo al instalar las dependencias, es necesario instalas el paquete wheel y volver al comando anterior:
pip install wheel

Entramos en la carpeta del proyecto (cd decide) y realizamos las migraciones correspondientes para preparar la base de datos:

Además, será necesario instalar las dependencias correspondientes al panel de control desarrollado con
React. Para ello, primero se deberán tener instaldas las siguientes librerías de js con sus correspondientes
versiones: Node=14.15.0, npm=7.8.0.

A continuación, entramos en la carpeta del panel (cd decide_panel) y ejecutamos el siguiente comando:

    npm install

Situados en el directorio raíz del proyecto, entramos en la carpeta del proyecto (cd decide) y
realizamos la primera migración para preparar la base de datos que utilizaremos:

    ./manage.py makemigrations
    ./mange.py migrate

Por último, ya podremos ejecutar el módulos o módulos seleccionados en la configuración de la
siguiente manera:

    ./manage.py runserver

También debemos lanzar el panel de control, para ello dentro de la carpeta decide_panel ejecutamos:

    npm start

## Nuevo panel de administración

Para configurar el nuevo panel de control de administración se deben seguir los siguientes pasos. (se deben haber instalado los nuevos requirements y configurado la nueva base de datos tal y como se describe previamente)

Se recuerda que se debe copiar el archivo de configuración local de ejemplo:

- `cp local_settings.example.py local_settings.py`

### setup

- `cd /decide/administration/frontend`
- `npm install && npm run build`
- abrir `http://localhost:8000/administration` en el navegador
- hacer login con un superusuario

# Pasos a seguir para configurar y iniciar el cliente LDAP

La instalación se ha realizado y probado en sistemas Ubuntu, no puedo garantizarles que funcione en otras distribuciones o sistemas operativos.
Para cualquier información adicional visite la documentación oficial de los paquetes.

## Prerequisitos

Instale las siguientes dependencias

```sh
apt-get install build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev tox lcov valgrind
```

## Iniciar servidor LDAP desde docker

Abra un nuevo contenedor con el cliente mínimo de open ldap en su equipo, para ello utilice las siguientes instrucciones.

```sh
docker run  -p 389:389 \
            -d carvilgar1us/decideldap
```

Para verificar que el contenedor está corriendo correctamente el servicio slapd, pruebe el siguiente
comando en su máquina HOST.

```sh
ldapsearch -x -b "dc=decide, dc=org" -H ldap://:389
```

La consola debe de devolver:
\# extended LDIF
\#
\# LDAPv3
\# base <dc=decide, dc=org> with scope subtree
\# filter: (objectclass=\*)
\# requesting: ALL
\#

\# decide.org
dn: dc=decide,dc=org
objectClass: top
objectClass: dcObject
objectClass: organization
o:: RGVjaWRlIHBsYXRhZm9ybWEgZGUgdm90byBlbGVjdHLDg8Kzbmljbw==
dc: decide

\# admin, decide.org
dn: cn=admin,dc=decide,dc=org
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator

Si es lo que usted ha obtenido entonces puede continuar.

## Añadir objetos a la organización

### Organitational Units

A continuación añadiremos las _Organitational Units_(ou) a nuestra organización,para ello cree un fichero con extensión ldif y ejecútelo con privilegios root **En su maquina HOST**.

```sh
sudo su -
```

Cree un fichero con extensión ldif.

```sh
vim basedn.ldif
```

En el fichero que ha creado previamente copie lo siguiente.

```sh
dn: ou=people,dc=decide,dc=org
objectClass: organizationalUnit
ou: people

dn: ou=groups,dc=decide,dc=org
objectClass: organizationalUnit
ou: groups
```

Finalmente, ejecute el siguiente comando

```sh
ldapadd -x -D cn=admin,dc=decide,dc=org -W -f basedn.ldif
```

si obtiene la siguiente respuesta usted ha realizado correctamente este paso.

```
adding new entry "ou=people,dc=decide,dc=org"
adding new entry "ou=groups,dc=decide,dc=org"
```

### Usuarios

Para añadir usuarios genere una contraseña mediante el comando y cópiela en el portapapeles, la necesitará para el siguiente paso

```sh
slappasswd
```

y cree un fichero con la siguiente información y recuerde copiar la contraseña que generó en el paso anterior en **userPassword**:

```sh
vim ldapusers.ldif
```

Y a continuación, copie lo siguiente.

```sh
dn: uid=foobar,ou=people,dc=decide,dc=org
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: foo
sn: bar
mail: foobar@gmail.com
userPassword: {SSHA}Zn4/E5f+Ork7WZF/alrpMuHHGufC3x0k
loginShell: /bin/bash
uidNumber: 2000
gidNumber: 2000
homeDirectory: /home/foobar


dn: cn=foobar,ou=groups,dc=decide,dc=org
objectClass: posixGroup
cn: foobar
gidNumber: 2000
memberUid: foobar
```

y ejecutelo mediante la siguiente instruccion:

```sh
ldapadd -x -D cn=admin,dc=decide,dc=org -W -f ldapusers.ldif
```

sabrá que ha realizado bien el paso anterior si obtine la siguiente salida:

```
adding new entry "uid=foobar,ou=people,dc=decide,dc=org"

adding new entry "cn=foobar,ou=groups,dc=decide,dc=org"
```

## Dependencias Django para LDAP

Para finalizar, debe instalar las dependencias que django necesarias para la comunicación con el cliente LDAP.
Para ello, borre su local_settings.py y ejecute el comando pip para instalar las nuevas dependencias:

```sh
pip install -r requirements.txt
```

una vez finalizada la instalación copie el local settings que se le ofrece como plantilla y vuelva a configurar todo como se enseñó en clases de práticas y modifique el campo **AUTH_LDAP_SERVER_URI** de la configuración LDAP con la url de sus servidor y **AUTH_LDAP_BIND_PASSWORD** con la constraseña que puso en la instalación de openLDAP.

Puede probar que funcione haciendo una petición desde Postman
![alt text](https://i.imgur.com/3a4xwaZ.png)

---

## Ejecutar con docker

Existe una configuración de docker compose que lanza 3 contenedores, uno
para el servidor de base de datos, otro para el django y otro con un
servidor web nginx para servir los ficheros estáticos y hacer de proxy al
servidor django:

- decide_db
- decide_web
- decide_nginx

Además se crean dos volúmenes, uno para los ficheros estáticos y medias del
proyecto y otro para la base de datos postgresql, de esta forma los
contenedores se pueden destruir sin miedo a perder datos:

- decide_db
- decide_static

Se puede editar el fichero docker-settings.py para modificar el settings
del proyecto django antes de crear las imágenes del contenedor.

Crear imágenes y lanzar contenedores:

    $ cd docker
    $ docker-compose up -d

Parar contenedores:

    $ docker-compose down

Crear un usuario administrador:

    $ docker exec -ti decide_web ./manage.py createsuperuser

Lanzar la consola django:

    $ docker exec -ti decide_web ./manage.py shell

Lanzar tests:

    $ docker exec -ti decide_web ./manage.py test

Lanzar una consola SQL:

    $ docker exec -ti decide_db ash -c "su - postgres -c 'psql postgres'"

## Ejecutar con vagrant + ansible

Existe una configuración de vagrant que crea una máquina virtual con todo
lo necesario instalado y listo para funcionar. La configuración está en
vagrant/Vagrantfile y por defecto utiliza Virtualbox, por lo que para
que esto funcione debes tener instalado en tu sistema vagrant y Virtualbox.

Crear la máquina virtual con vagrant:

    $ cd vagrant
    $ vagrant up

Una vez creada podremos acceder a la web, con el usuario admin/admin:

http://localhost:8080/admin

Acceder por ssh a la máquina:

    $ vagrant ssh

Esto nos dará una consola con el usuario vagrant, que tiene permisos de
sudo, por lo que podremos acceder al usuario administrador con:

    $ sudo su

Parar la máquina virtual:

    $ vagrant stop

Una vez parada la máquina podemos volver a lanzarla con `vagrant up`.

Eliminar la máquina virtual:

    $ vagrant destroy

## Ansible

El provisionamiento de la aplicación con vagrant está hecho con Ansible,
algo que nos permite utilizarlo de forma independiente para provisionar
una instalación de Decide en uno o varios servidores remotos con un
simple comando.

    $ cd vagrant
    $ ansible-playbook -i inventory playbook.yml

Para que esto funcione debes definir un fichero [inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)
con los servidores destino.

Los scripts de ansible están divididos en varios ficheros .yml donde
se definen las diferentes tareas, por lo que es posible lanzar partes
independientes:

- packages.yml, dependencias del sistema
- user.yml, creación de usuario decide
- python.yml, git clone del repositorio e instalación de dependencias python en virtualenv
- files.yml, ficheros de configuración, systemd, nginx y local_settings.py
- database.yml, creación de usuario y base de datos postgres
- django.yml, comandos django básicos y creación de usuario admin
- services.yml, reinicio de servicios, decide, nginx y postgres

Por ejemplo este comando sólo reinicia los servicios en el servidor:

    $ ansible-playbook -i inventory -t services

El provisionamiento de ansible está diseñado para funcionar con **ubuntu/bionic64**,
para funcionar con otras distribuciones es posible que haga falta modificar
el fichero packages.yml.

## Versionado

El versionado de API está hecho utilizando Django Rest Framework, y la forma
elegida para este versionado es mediante [parámetros de búsqueda](https://www.django-rest-framework.org/api-guide/versioning/#queryparameterversioning),
podemos cambiarlo a parámetros en la URL o en el nombre del HOST, hay diferentes
tipos de versionado disponibles en Django Rest Framework, podemos verlos
[aqui](https://www.django-rest-framework.org/api-guide/versioning/#versioning).

Nosotros hemos escogido el de por parámetros por ser el más sencillo, y hemos
creado un ejemplo para que veamos su uso, podemos verlo en voting/views.py

Si nosotros queremos que la salida que nos da la llamada a la API /voting/, sea
diferente en la versión 2, solo tenemos que comprobar en la versión nos está
llegando, y hacer lo que queramos, por ejemplo:

```
    def get(self, request, *args, **kwargs):
        version = request.version  # Con request.version obtenemos la versión
        if version not in settings.ALLOWED_VERSIONS:  # Versiones permitidas
            version = settings.DEFAULT_VERSION  # Si no existe: versión por defecto
        # En el caso de usar la versión 2, usamos un serializador diferente
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer
        return super().get(request, *args, **kwargs)
```

Para llamar a las diferentes versiones, haremos lo siguiente:

- /voting/?version=v1
- /voting/?version=v2

## Test de estrés con Locust

Antes de empezar, comentaré para que sirven las pruebas de estrés. A veces necesitamos soportar que
nuestra aplicación ofrezca una cantidad de peticiones por segundo, porque habrá mucha gente entrando
a la misma vez, y ante este estrés, tenemos que comprobar como se comporta nuestra aplicación.

No es lo mismo que cuando la estresemos nos de un error 500 a que nos devuelva la petición de otro
usuario. Con estos test conseguiremos comprobar cual es ese comportamiento, y quizás mejorar la
velocidad de las peticiones para permitir más peticiones por segundo.

Para ejecutar los test de estrés utilizando locust, necesitaremos tener instalado locust:

    $ pip install locust

Una vez instalado, necesitaremos tener un fichero locustfile.py donde tengamos la configuración de
lo que vamos a ejecutar. En nuestro caso, tenemos hecho dos ejemplos:

1.  Visualizer: entra en el visualizador de una votación para ver cuantas peticiones puede aguantar.

    Para ejecutar el test de Visualizer, tenemos que tener en cuenta que entra en la votación 1, por lo
    que necesitaremos tenerla creada para que funcione correctamente, una vez hecho esto, podemos
    comenzar a probar con el siguiente comando (dentro de la carpeta loadtest):

        $ locust Visualizer

    Esto abrirá un servidor que podremos ver en el navegador, el mismo comando nos dirá el puerto.
    Cuando se abra, nos preguntará cuantos usuarios queremos que hagan peticiones a la vez, y como
    queremos que vaya creciendo hasta llegar a ese número. Por ejemplo, si ponemos 100 y 5, estaremos
    creando 5 nuevos usuarios cada segundo hasta llegar a 100.

2.  Voters: utilizaremos usuarios previamente creados, y haremos una secuencia de peticiones: login,
    getuser y store. Sería lo que realizaría un usuario cuando va a votar, por lo que con este ejemplo
    estaremos comprobando cuantas votaciones podemos hacer.

        Para ejecutar el test de Voter, necesitaremos realizar varios preparos. Necesitaremos la votación 1
        abierta, y necesitaremos crear una serie de usuarios en el censo de esta votación, para que cuando
        hagamos el test, estos usuario puedan autenticarse y votar correctamente. Para facilitar esta
        tarea, hemos creado el script de python gen_census.py, en el cual creamos los usuarios que
        tenemos dentro del fichero voters.json y los añadimos al censo utilizando la librería requests.
        Para que este script funcione, necesitaremos tener instalado request:

            $ pip install requests

        Una vez instalado, ejecutamos el script:

            $ python gen_census.py

        Tras esto, ya podremos comenzar el test de estrés de votantes:

            $ locust Voters

Importante mirar bien el fichero locustfile.py, donde existen algunas configuraciones que podremos
cambiar, dependiendo del HOST donde queramos hacer las pruebas y del id de la votación.

A tener en cuenta:

- En un servidor local, con un postgres que por defecto nos viene limitado a 100 usuarios
  concurrentes, cuando pongamos más de 100, lo normal es que empiecen a fallar muchas peticiones.
- Si hacemos las pruebas en local, donde tenemos activado el modo debug de Django, lo normal es que
  las peticiones tarden algo más y consigamos menos RPS (Peticiones por segundo).
