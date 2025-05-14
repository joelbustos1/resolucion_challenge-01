# 🛡️ API Vulnerable - Challenge01

Este proyecto contiene una API simple en python, intencionalmente vulnerable, para utilizar con propositos educativos.

## 🚀 Requisitos

- Docker
- Python 3.11+

## 🐳 Uso con Docker

```bash
docker build -t challenge01 .
docker run challenge01
```

## 🔍 Endpoints

- POST /login
- GET /userdata/<user_id>


## 🎯 Objetivo del Desafío

1. Analiza el código fuente, investiga los enpoints y probarlos
2. Encontra vulnerabilidades de seguridad y explotalas
3. Redacta un breve informe donde expliques:
- Las vulnerabilidades encontradas
- Cómo las explotastes
- Qué impacto tienen
- Cómo se pueden mitigar

¡Buena suerte!

## Resolución
logre identificar varias vulnerabilidades que comprometen la seguridad de la app pero primero que nada quiero ir mencionando el paso a paso que fui haciendo:
1. primero que anda tuve buildear y correr el challenge con los comandos dados en la consigna.
   
2. una vez con la imagen de docker corriendo y con la direccion dada prosegui con el otro paso.
   
![Image](https://github.com/user-attachments/assets/99507e5f-4e57-4457-a82f-726e37c44d04)

3. para este ejercicio use la tool burpsuite que ayuda justamente en el analisis de la seguridad en una app web pudiendo hacer pequeños pentestings.
 
4. una vez abierta la tool me dirigi a la pestaña de proxy y abri su navegador para empezar a capturar las peticiones de los endpoints, una vez abierto me dirigi a pegar la direccion dada anteriormente (http://127.0.0.1:5000).
   
>[!NOTE]
>interfaz de burpsuite
>
![Image](https://github.com/user-attachments/assets/afbbfa40-caf6-4a05-99a8-4449e93fcd33)

>[!NOTE]
>Navegador
>
![Image](https://github.com/user-attachments/assets/0ca22389-2b59-4d4a-8d65-20dc68f24504)

5. una vez hecho esto ya vamos a poder ir capturando el trafico de los endpoints dados e ir viendo el http history con las peticiones realizadas, una vez hago esto selecciono el endpoint al cual quiero pegarlo y lo mando al repeater de burpsuite, pero antes revise el codigo fuente de la app y encontre a simple vista varias vulnerabilidades que a continuacion muestro:

>[!NOTE]
>HTTP history, click derecho en la request deseada y la mandamos al repeater. Luego retomo con esto
>

![Image](https://github.com/user-attachments/assets/4c74e609-087f-4b8a-bc88-cbb41e5e848e)

>[!NOTE]
>fragmento del codigo de la app

![Image](https://github.com/user-attachments/assets/bc0e0037-b6b4-47da-a4b0-d227e27e64b9)

podemos ver como primero que nada que se usa una secret_key predecible ya que si no se establece la variable de entorno SECRET_KEY se va a usar por defecto 'mysecretkey', luego al definir la funcion init_db se estan hardcodeando credenciales de usuarios. 

>[!WARNING]
>explotando estas vulnerabilidades
>

hice un programa basico para poder generar un token valido sin necesidad de credenciales.

![Image](https://github.com/user-attachments/assets/3ef2832e-e346-434b-90b6-a5fe1f576338)

probando token generado para hitear el endpoint userdata/<user_id>, para esto se usa el repeater y usamos el header authorization donde ahi vamos a darle el valor del token generado con el programa.

![Image](https://github.com/user-attachments/assets/ff438a43-fcb8-4495-9555-cda0c6c79b6c)

se puede ver como se genera exitosamente el codigo 200 seguido de un OK, esto significa que la solicitud se realizo con exito.

sigamos con la otra vulnerabilidad, el hardcodeo de las credenciales de usuario. Podemos usar esas credenciales en el metodo POST del endpoint login para que asi nos genere una token valido para una autenticacion, es importante usar el content-type con el valor application/json ya que es lo que espera el endpoint login, debajo generamos el objeto con las credenciales que tenemos en el codigo.

![Image](https://github.com/user-attachments/assets/c28a3048-6c97-4187-b47a-8482d60909bf)
