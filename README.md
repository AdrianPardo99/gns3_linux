# ¿Qué es GNS3?
Es un software que permite emular/simular un entorno (topología) de red en el cual se puede desplegar una plataforma de comunicación de varios equipos de cómputo virtual (VPCS) o maquinas virtuales con sistema operativo
# Instalación de GNS3

## Windows

Dentro de los requerimientos mínimos tenemos lo siguiente:

* Sistema Operativo Windows 7 o superior
* 2 Procesadores o más
* Virtualización habilitada desde la BIOS
* 4 GB de RAM
* 1 GB de almacenamiento para la aplicación
* Más GB para la instalación de otros medios (Routers, VMs, etc)

Se puede seguir la siguiente guía de instalación: [GNS3](https://docs.gns3.com/docs/getting-started/installation/windows/)

## Linux

Dependiendo de la distro es necesario descargar 1 o varios software que puede generar o entenderse como dependencias, por ello podemos escribir los siguientes comandos para instalar los software fuentes:

__Software a descargar de los repositorios dependiendo la distribución__

Para este caso es necesario instalar los siguientes paquetes o su equivalente de acuerdo a la distribución que se este trabajando:

* git
* gcc
* flex
* bison
* libpcap o pcap
* elfutils
* libuuid
* python3-tornado
* python3-netifaces
* python3-dev
* python3-pip
* python3-setuptools
* python3-PyQt4
* python3-zmq
* wireshark
* tunctl (En caso de crear una interfaz virtual para comunicar)

__Software directo de GNS3__
```bash
  # Con git descargaremos lo siguiente
  # Dynamips
  git clone https://github.com/GNS3/dynamips.git
  cd dynamips
  mkdir build
  cmake ..
  sudo make install
  cd ../..
  # VPCS
  git clone https://github.com/GNS3/vpcs.git
  cd vpcs/src
  ./mk.sh
  sudo cp vpcs /usr/local/bin
  cd ../..
  # Iniparser
  git clone http://github.com/ndevilla/iniparser.git
  cd iniparser
  make
  sudo cp libiniparser.* /usr/lib/
  sudo cp src/iniparser.h /usr/local/include
  sudo cp src/dictionary.h /usr/local/include
  cd ..
  # Ubridge
  git clone https://github.com/GNS3/ubridge.git
  cd ubridge
  make
  sudo make install
```

__Para GNS3__

* gns3-server
* gns3-gui

Para los repositorios o lo que pueda faltar se puede consultar
* [aquí (Debian)](https://docs.gns3.com/docs/getting-started/installation/linux)
* [aquí (Fedora)](https://computingforgeeks.com/how-to-install-gns3-on-fedora-29-fedora-28/)

# Virtualización de alguna VM
Para algunos casos o topologías es necesario virtualizar un sistema operativo el cual pueda trabajarse en la misma topología para brindar algún servicio en caso de que este sea un servidor o en su defecto este sea un cliente el cual consumirá cierto servicio en el entorno de red.

En muchos casos y muchos tutoriales se leerá que es muy fácil usar VmWare o Virtualbox, los cuales indirectamente son software de licencia y muchas veces nos daremos de topes a la hora de instalar o de realizar nuestras tareas, por ello mejor usaremos el confiable Qemu/KVM el cual aprovecha al menos en un 100\% en Linux todo nuestro hardware el cual puede incluso virtualizar arquitecturas de otro ensamblador, ya sea ARM, i386 u otro tipo de ensamblador.

__Linux__

Instalación de algunos paquetes y libs que son necesarios:

* libvirt
* kvm
* qemu-system
* virt-manager
* virt-tools

# Configuración de Routers Cisco
Muchas veces nos veremos en la necesidad de configurar no solo a nivel de enrutamiento estático, de levantar alguna interfaz de red, muchas veces vamos a tener que decirle a nuestros routers, donde se encuentran nuestros servidores y en muchas otras ocasiones tendremos que administrar usuarios que tengan acceso a nuestros dispositivos vía protocolos como:
* SSH
* Telnet

## Un repaso rápido de IP y Mascaras de Red
Muchas veces tendremos que hacer uso Variable Length Subnet Mask (Mascara de Subred de Tamaño Variable) (VLSM), con IPs de distintas clases, pero inicialmente debemos conocer la tabla de direcciones IP para saber el rango disponible y el como se puede trabajar.

| Clase | Rango | Rango en binario | Prefijo de mascara de red | Mascara de Red |
| ----- | ----- | ---------------- | ------------------------- | -------------- |
|  A    | 1 - 126 | 0xxxxxxx - 01111110 | 8 | 255.0.0.0 |
|  B    | 128.0 - 191.255 | 10xxxxxx - 10111111 | 16 | 255.255.0.0 |
|  C    | 192.0.0 - 223.255.255 | 110xxxxx - 11011111 | 24 | 255.255.255.0 |

El resto de Clases no se utilizan debido a que funcionan como clases de IPs para Multicast o para otro fin.

Por ello pensemos que en la Clase A no se incluye el grupo de IPs 127 ya que este es usado directamente para el loopback o el localhost de nuestros mismo equipos.

Por otro lado un ejemplo de como hacer uso de clases es el siguiente:

Tenemos la IP 10.10.0.5 de la clase A, por ello obtendremos los siguientes datos:

| IP | ID de Red | Primer IP | Ultima IP | Dirección de Broadcast | Mascara de Red | Clase |
| -- | --------- | --------- | --------- | ---------------------- | -------------- | ----- |
| 10.10.0.5 | 10.0.0.0 | 10.0.0.1 | 10.255.255.254 | 10.255.255.255.255 | 255.0.0.0 | A |

Al obtener esto debemos destacar lo siguiente para trabajar y encontrar esta tabla de forma rápida, por ello primero debemos conocer inicialmente la clase de IP que es, a lo cual en este caso es inicialmente una clase A por lo cual la mascara de red es de 8 bits, con ello convertiremos nuestra IP que nos dan a binario y la mascara de red la convertiremos de igual manera a binario:

__10.10.0.5__ es equivalente a binario __00001010.00001010.00000000.00000101__

__255.0.0.0__ es equivalente a binario __11111111.00000000.00000000.00000000__

Con esto primero haremos la operación a nivel de bits como _AND_ la cual nos devolvera lo siguiente

__10.0.0.0__ siendo equivalente de la operación and __00001010.00000000.00000000.00000000__ que es nuestro ID de Red

Para obtener la dirección de Broadcast haremos uso de la operación _NOT_ en la mascara de red, lo cual nos otorga lo siguiente:

__0.255.255.255__ es equivalente a binario __00000000.11111111.11111111.11111111__

Obteniendo esto haremos uso de la compuerta _OR_ en el ID de Red

__10.255.255.255__ es equivalente a binario __00001010.11111111.11111111.11111111__

Y para obtener finalmente la primer y última IP solo haremos uso de la suma de 1 bit al último octeto del ID de red y la resta de 1 bit al último octeto de la dirección de Broadcast

__10.0.0.1 hasta 10.255.255.254__ siendo este nuestro rango util de IPs

Finalmente esto es para el caso de las IPs por clases, por ello es necesario pensar que son muchas direcciones IPs las que se quedan sin uso, por lo cual se puede crear una subred la cual tendrá una mascara de red distinta, la cual permitirá el ahorro de IPs y podrá reusar estas otras direcciones IP en muchos más dispositivo, un ejemplo de ello puede ser:

Se tiene el conjunto de direcciones IP de clase C __192.168.100.0/24__ En la cuales se plantea solo realizar uso de las primeras 5 IPs para un área local mientras que 15 IPs se harán uso para conectar y crear otra área de trabajo, la solución a este ejemplo sería hacer lo siguiente:

* Primero debemos preguntar si este número de IPs que vamos a usar consideran ya el uso de Gateway y por otro lado si ya se considera así mismo las direcciones de Broadcast y de ID de Red, en caso de que no se consideren esto es sumas 1 host más por cada elemento faltante para construir la subred

* Convertir el número de host a utilizar a binario por ejemplo: __5 hosts más los 3 elementos (Gateway, Broadcast e Identificador)__ que es igual a hacer uso de __8 hosts__ por ello su conversión a octeto sería __00001000__, mientras que haciendo lo mismo para el caso de los __18 hosts__ sería __00010010__ a lo cual nos daremos cuenta que para este caso se ven 2 bits del rango en 1, por lo cual esto no es factible para realizar el subneteo de nuestras direcciones, por ello recoreremos 1 bit a la izquiera y eliminaremos el bit más cercano de la derecha para realizar el subneteo quedando de forma decimal como __32 hosts__ siendo su equivalente en binario como __00100000__ de modo que los bits con cero a la derecha despues del 1 es lo que utilizaremos para trabajar y asignar direcciones IP, por ello sabemos que para las mascaras de red son 4 octetos por lo cual son 32 bits para trabajar, tomando en cuenta lo mencionado para el subneteo para los casos:

* __32 hosts__ se necesitan __5 bits__ por ello haremos la operación _32-5=27 bits_
* __8 hosts__ se necesitan __3 bits__ por ello haremos la operación _32-3=29 bits_

Por tanto nuestras direcciones quedaran como __192.168.100.x/27 y 192.168.100.y/29__, pero como seleccionaremos o asignaremos los valores para _x_ o _y_, pensemos de forma sencilla asignaremos el primer ID de Red a aquella subred que tenga el prefijo más pequeño, por lo cual tendremos que elegir primero a la que tiene la variable _x_, quedando como:

* __192.168.100.0/27__
  * ID de Red: 192.168.100.0 = 11000000.10101000.01100100.00000000
  * Mascara de Red: 255.255.255.224 = 11111111.11111111.11111111.11100000
  * Aplicando las operaciones pertinentes tendremos
    * Primer IP: 192.168.100.1
    * Ultima IP: 192.168.100.30
    * IP de Broadcast: 192.168.100.31
  * Cubriendo totalmente la demanda de 18 hosts teniendo 14 hosts que podemos usar más tarde en esa subred

Para el caso y deseo de que las direcciones de subneteo sean contiguas usaremos la IP que sigue después de la IP de Broadcast de la subred que ya construimos __192.168.100.0/27__:

* __192.168.100.32/29__
  * ID de Red: 192.168.100.32 = 11000000.10101000.01100100.00100000
  * Mascara de Red: 255.255.255.248 = 11111111.11111111.11111111.11111000
  * Aplicando las operaciones pertinentes tendremos
    * Primer IP: 192.168.100.33
    * Ultima IP: 192.168.100.38
    * IP de Broadcast: 192.168.100.39
  * Cubriendo el total de hosts deseados sin desperdiciar ningún hosts de modo que esta subred es la exacta para el conjunto de direcciones

Y de esta forma hemos concluido con el subneteo de las demas direcciones IP, de modo en que el resto de Hosts por el momento son resguardados, en caso de que se desee hacer una nueva subred con más hosts es necesario rehacer las operaciones pertinentes para que de este modo no se desperdicien IPs.

### Valores decimales dependiendo del prefijo de mascara de red

* _0_ = _0.0.0.0_
* _1_ = _128.0.0.0_
* _2_ = _192.0.0.0_
* _3_ = _224.0.0.0_
* _4_ = _240.0.0.0_
* _5_ = _248.0.0.0_
* _6_ = _252.0.0.0_
* _7_ = _254.0.0.0_
* _8_ = _255.0.0.0_
* _9_ =  _255.128.0.0_
* _10_ =  _255.192.0.0_
* _11_ =  _255.224.0.0_
* _12_ =  _255.240.0.0_
* _13_ =  _255.248.0.0_
* _14_ =  _255.252.0.0_
* _15_ =  _255.254.0.0_
* _16_ =  _255.255.0.0_
* _17_ =  _255.255.128.0_
* _18_ =  _255.255.192.0_
* _19_ =  _255.255.224.0_
* _20_ =  _255.255.240.0_
* _21_ =  _255.255.248.0_
* _22_ =  _255.255.252.0_
* _23_ =  _255.255.254.0_
* _24_ =  _255.255.255.0_
* _25_ =  _255.255.255.128_
* _26_ =  _255.255.255.192_
* _27_ =  _255.255.255.224_
* _28_ =  _255.255.255.240_
* _29_ =  _255.255.255.248_
* _30_ =  _255.255.255.252_
* _31_ =  _255.255.255.254_
* _32_ =  _255.255.255.255_

La cual estos prefijos representan la cantidad de bits que utilizan para la mascara, mientras para que saber cuantos hosts puede utilizar cada mascara es tan sencillo como _2^{32-prefijo de red}_ tomando en cuenta que es necesario recalcar que en la cantidad de hosts es necesario considerar la IP del Gateway, el ID de Red y la dirección de Broadcast para que no exista ningún problema a la hora de realizar el subneteo.

## Levantando interfaces de red con una IP
Para esto tomaremos de ejemplo un Router 1 cuya IP contiene los datos: __192.168.0.0/24__ a traves de la interfaz __FastEthernet 0/0__ lo cual es abreviada en GNS3 como __f0/0__

Para ello debemos hacer lo siguiente:
```bash
  # Para este punto debemos estar en el modo exec del router es decir que aparezca
  #   el mismo simbolo con el que estoy realizando este comentario "#" y no ">"
  conf t
    int f0/0
      ip add 192.168.0.1 255.255.255.0
      no sh
      end
  wr
```
Con esto finalmente podemos resaltar y hacer que las instrucciones a seguir para levantar cualquier interfaz y dirección como:
```bash
  conf t
    int <aquí_va_la_interfaz_con_su_identificador>
      ip add <IP_util_dentro_del_rango_de_IPs_primera_o_ultima_disponible> <Mascara_de_Red>
      no sh
      end
  wr
```
Para el caso de que se configuren múltiples interfaces en 1 router cambiar la palabra __end__ por un __exit__ para no repetir sentencias de comandos innecesariamente
## Creando Enrutamientos
Muchas veces
