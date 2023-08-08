# sesion_7_python_avanzado

Para ejecutar el siguiente codigo :

1) Abrir consola en windows o mac 
2) Ejecutar el siguiente comando para instalar las dependencias: pip3 install -r requirements.txt o pip install -r requirements.txt 
4) Abrir el archico env_variables.sh y modificar o agregar su path donde se encuentre su proyecto
5) Ejecutar el sh : ./env_variables.sh

Nota : 
1) Este proyecto utilizala mpi4py, estuve investigando y en Windows no es necesario instalar algo extra;
En caso de tener mac usar : brew install mpi4py

2) Recordar que para ejcutar este programa se urtiliza el comando : mpiexec -n 3 python3 master.py,
Este comanddo se usa dado que estamos usando MPI; agrego documentacion :

https://mpi4py.readthedocs.io/en/stable/intro.html#what-is-mpi
https://github.com/luca-s/mpi-master-slave
