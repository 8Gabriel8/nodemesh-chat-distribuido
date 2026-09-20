# Conversión del nodo único en un Sistema Distribuido

Este documento presenta la evidencia de que el nodo único inicial fue convertido exitosamente en un sistema distribuido, cumpliendo con los tres requisitos establecidos: replicación del nodo en distintas computadoras, sincronización entre nodos, y uso de ngrok para interconectarlos.

---

## 1. Replicación del nodo en las demás computadoras

El mismo código del nodo (`app.py`, `Dockerfile`, `requirements.txt`) se ejecutó en **tres computadoras físicamente distintas**, cada una en su propia red, utilizando Docker para levantar el contenedor de forma independiente en cada equipo.

| Nodo | Puerto local | Cuenta de ngrok utilizada |
|---|---|---|
| Nodo A | 5001 | baseballchrist6@gmail.com |
| Nodo B | 5002 | canchecenjosegabriel@gmail.com |
| Nodo C | 5003 | 230300738@ucaribe.edu.mx |

---

## 2. Uso de ngrok para interconectar los nodos

Dado que las tres computadoras se encuentran en redes distintas, se utilizó **ngrok** para exponer cada nodo a internet mediante una dirección pública, permitiendo que se comunicaran entre sí sin necesidad de compartir la misma red local.

| Nodo | URL pública (ngrok) |
|---|---|
| Nodo A | https://half-census-cadillac.ngrok-free.dev |
| Nodo B | https://revenue-retrieval-antiquity.ngrok-free.dev |
| Nodo C | https://carried-antsy-custard.ngrok-free.dev |

**Evidencia — Terminal de ngrok del Nodo A:**

![Terminal ngrok Nodo A](terminal-ngrok-nodoA.png)

Se observa la sesión activa de ngrok exponiendo el puerto 5001 mediante la URL pública `https://half-census-cadillac.ngrok-free.dev`, junto con el registro de una petición `POST /receive` con respuesta `201 CREATED`.

**Evidencia — Terminal de ngrok del Nodo C:**

![Terminal ngrok Nodo C](terminal-ngrok-nodoC.png)

Se observa la sesión activa de ngrok exponiendo el puerto 5003 mediante la URL pública `https://carried-antsy-custard.ngrok-free.dev`, junto con el registro de una petición `POST /receive` con respuesta `201 CREATED`.

---

## 3. Sincronización entre nodos (cliente conectado al Nodo A viendo mensajes del Nodo B)

Para comprobar que un nodo recibe un mensaje y lo replica automáticamente a los demás, se realizó la siguiente prueba:

### Paso 1 — Envío del mensaje desde el Nodo B

Se envió un mensaje al Nodo B mediante una petición `POST /send`, utilizando la laptop correspondiente a dicho nodo.

![Envío de mensaje desde el Nodo B](postman-enviar-nodoB.png)

La respuesta `201 Created` confirma que el mensaje fue recibido y almacenado correctamente por el Nodo B:

```json
{
    "mensaje_guardado": {
        "autor": "Dante",
        "mensaje": "Mensaje desde el Nodo B"
    },
    "status": "ok"
}
```

### Paso 2 — Consulta del mensaje desde el Nodo A

Sin enviar ningún mensaje directamente al Nodo A, se realizó una petición `GET /messages` a su dirección pública de ngrok.

![Consulta de mensajes en el Nodo A](postman-ver-nodoA.png)

El mensaje enviado originalmente al Nodo B aparece en la respuesta del Nodo A, confirmando que la replicación automática entre nodos ubicados en computadoras distintas funciona correctamente:

```json
[
    {
        "autor": "Dante",
        "mensaje": "Mensaje desde el Nodo B"
    }
]
```

### Paso 3 — Consulta del mensaje desde el Nodo C

De la misma manera, se consultó el Nodo C, confirmando que el mensaje también llegó a esta tercera computadora.

![Consulta de mensajes en el Nodo C](postman-ver-nodoC.png)

En esta captura se observa además, en la esquina superior derecha, la cuenta de Postman correspondiente a otro integrante del equipo (Erick Daniel Reyes Torrecilla), lo que confirma que la consulta se realizó desde una perspectiva distinta a la del emisor original del mensaje.

---

## 4. Conclusión

La evidencia presentada demuestra que:

- El nodo fue replicado exitosamente en tres computadoras distintas, cada una en su propia red.
- Ngrok permitió exponer cada nodo mediante una dirección pública, posibilitando la comunicación entre computadoras sin necesidad de compartir una red local.
- Cuando un nodo recibe un mensaje nuevo, lo replica automáticamente a los demás nodos, sin intervención manual, tal como lo confirman tanto las respuestas obtenidas en Postman como los registros de las peticiones `POST /receive` en los servidores de ngrok.

Con esto, el sistema queda validado como un sistema distribuido funcional, cumpliendo con el objetivo de convertir el nodo único original en una arquitectura de múltiples nodos interconectados.
