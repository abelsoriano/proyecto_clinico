# Sistema de Gestión Clínica con Django


### Sistema para clínica de Optometría que necesita gestionar el diagnóstico de sus pacientes y la venta de los productos Ópticos para los mismos.

---


## Cuenta con un Sistema de Usuarios con los siguientes roles


1. ### Secretaría
    > 📌 Puede agregar, modificar o eliminar los turnos de los Pacientes.


2. ### Profesional médico
    > 📌 Puede agregar observaciones al historial médico de sus pacientes, ver el listado de Pacientes filtrando por día, mes o año.

    > 📌 Solo puede ver los pacientes atendidos que se le fueron asignados.


3. ### Ventas
    > 📌 Puede generar un pedido para el paciente, donde detalla los productos que quiere adquirir, el precio, un subtotal, tipo de pago (tarjeta de crédito, debido, billetera virtual o efectivo).

    > 🛍 El producto tiene nombre, si está clasificado como Lente tendrá la opción de
    Lejos/Cerca, Izquierda/Derecha, si incluye Armazón o no.

    > ⏳ Una vez que se genera el pedido queda en estado “Pendiente”.

    > 👷‍♀️ El rol de Ventas puede cambiar el estado a “Pedido” o mandarlo a “Taller”.



4. ### Taller
    > 📌 Solo visualiza la lista de pedidos (con todos los detalles de los productos sin
    los precios).

    > 📌 El Taller puede confirmar cambiando el estado del pedido a “Finalizado” 🎉.


5. ### Gerencia

    > 📌 Puede visualizar todos los datos y realizar los siguientes reportes 👇
    1. Pacientes que asistieron a los turnos en la semana/mes.
    2. Pacientes que no asistieron a los turnos en la semana/mes.  
    3. Pacientes que hicieron por lo menos un Pedido en la semana/mes.
    4. Productos más vendidos en el mes.
    5. Ventas totales por mes clasificadas por Vendedores.


## Para iniciar el sistema

> Crear un entorno virtual e instalar lo que haya en requerimientos.txt

> Crear las migraciones python manage.py makemigrations

> Migrar a la base de datos python manage.py migrate

> Ejecutar el script inicial python manage.py runscript inicial

> OPCIONAL Cargar datos de prueba python manage.py loaddata datosfake.json