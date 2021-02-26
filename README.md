# ¿Qué es GNS3?
Es un software que permite emular/simular un entorno (topología) de red en el cual se puede desplegar una plataforma de comunicación de varios equipos de cómputo virtual (VPCS) o maquinas virtuales con sistema operativo
# Instalación de GNS3

## Windows

Dentro de los requerimientos minimos tenemos lo siguiente:

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
Para algunos casos o topologías es necesario virtualizar un sistema operativo el cual pueda trabajarse en la misma topología para brindar algun servicio en caso de que este sea un servidor o en su defecto este sea un cliente el cual consumira cierto servicio en el entorno de red.

En muchos casos y muchos tutoriales se leera que es muy facil usar VmWare o Virtualbox, los cuales indirectamente son software de licencia y muchas veces nos daremos de topes a la hora de instalar o de realizar nuestras tareas, por ello mejor usaremos el confiable Qemu/KVM el cual aprovecha al menos en un 100\% en Linux todo nuestro hardware el cual puede incluso virtualizar arquitecturas de otro ensamblador, ya sea ARM, i386 u otro tipo de ensamblador.

__Linux__

Instalación de algunos paquetes y libs que son necesarios:

* libvirt
* kvm
* qemu-system
* virt-manager
* virt-tools

