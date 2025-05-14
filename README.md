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
logre identificar varias vulnerabilidades que comprometen la seguridad de la app pero quiero ir mencionando el paso a paso que fui haciendo:
1. primero que nada tuve que buildear y correr el challenge con los comandos dados en la consigna.
   
2. una vez con la imagen de docker corriendo y con la direccion dada prosegui con el otro paso.
   
![Image](https://github.com/user-attachments/assets/99507e5f-4e57-4457-a82f-726e37c44d04)

3. para este ejercicio use la tool burpsuite que ayuda justamente en el analisis de la seguridad en una app web permitiendo realizar ejercicios de pentesting.
 
4. una vez abierta la tool me dirigi a la pestaña de proxy y abri su navegador para empezar a capturar las peticiones de los endpoints, una vez abierto me dirigi a pegar la direccion dada anteriormente (http://127.0.0.1:5000).
   
>[!NOTE]
>interfaz de burpsuite
>
![Image](https://github.com/user-attachments/assets/afbbfa40-caf6-4a05-99a8-4449e93fcd33)

>[!NOTE]
>Navegador
>
![Image](https://github.com/user-attachments/assets/0ca22389-2b59-4d4a-8d65-20dc68f24504)

5. una vez hecho esto ya voy a poder ir capturando el trafico de los endpoints dados e ir viendo el http history con las peticiones realizadas, una vez hago esto selecciono el endpoint al cual quiero pegarlo y lo mando al repeater de burpsuite, pero antes revise el codigo fuente de la app y encontre a simple vista varias vulnerabilidades que a continuacion muestro:

>[!NOTE]
>HTTP history, click derecho en la request deseada y la mandamos al repeater. Luego retomo con esto
>

![Image](https://github.com/user-attachments/assets/4c74e609-087f-4b8a-bc88-cbb41e5e848e)

>[!NOTE]
>fragmento del codigo de la app

![Image](https://github.com/user-attachments/assets/bc0e0037-b6b4-47da-a4b0-d227e27e64b9)

![Image](https://github.com/user-attachments/assets/8267570c-2d72-40f9-bad3-5e80c77d3efd)

>[!WARNING]
>explotando vulnerabilidades reconocidas en el codigo
>

# Uso de SECRET_KEY Debil o predecible

se puede ver como primero que nada se usa una secret_key predecible ya que si no se establece la variable de entorno SECRET_KEY se va a usar por defecto 'mysecretkey'.

hice un programa basico para poder generar un token valido sin necesidad de credenciales.

![Image](https://github.com/user-attachments/assets/3ef2832e-e346-434b-90b6-a5fe1f576338)

probando token generado para hitear el endpoint userdata/<user_id>, para esto se usa el repeater y uso el header authorization donde ahi voy a darle el valor del token generado con el programa.

![Image](https://github.com/user-attachments/assets/ff438a43-fcb8-4495-9555-cda0c6c79b6c)

se puede ver como se genera exitosamente el codigo 200 seguido de un OK, esto significa que la solicitud se realizo con exito.

>[!WARNING]
>Control de acceso inseguro
>
la app permite acceder a datos de cualquier usuario modificando el parametro user_id en la URL, sin verificar que el usuario autenticado tenga permisos para ver esa informacion. Esto permite que un atacante autenticado pueda acceder a datos sensibles de otros usuarios.

>[!CAUTION]
>IMPACTO
>
1. al no establecer una SECRET_KEY fuerte mediante variable de entorno, la app utiliza por defecto 'mysecretkey', lo que facilita la creacion de tokens JWT validos.
2. un atacante puede falsificar un token valido sin la necesidad de credenciales legitimas, accediendo a recursos protegidos como /userdata/<user_id>.
3. riesgo de compromiso total de autenticacion y autorizacion.

### Mitigacion:
1. generar una SECRET_KEY fuerte y aleatoria y cargarla desde variables de entorno.
2. no dejar claves sensibles por defecto en el codigo.
3. en lugar de permitir que el user_id venga por URL, extraer el ID del usuario directamente del token JWT.
4. validar siempre que el recurso solicitado pertenezca al usuario autenticado.
5. aplicar control de acceso en el backend, nunca confiar en el cliente.
   

# Credenciales hardcodeadas en el codigo fuente

sigamos con la otra vulnerabilidad, podemos ver que al definir la funcion init_db se estan hardcodeando credenciales de usuarios. Se pueden usar esas credenciales en el metodo POST del endpoint login para que asi nos genere una token valido para una autenticacion, es importante usar el content-type con el valor application/json ya que es lo que espera el endpoint login, debajo generamos el objeto con las credenciales que tenemos en el codigo.

![Image](https://github.com/user-attachments/assets/c28a3048-6c97-4187-b47a-8482d60909bf)

con el token dado se puede ir al endpoint userdata/<user_id> con el metodo GET y pegar el token en el header authentication. (genere otro token porque el que se muestra en la captura habia vencido pero es para seguir con los pasos)

![Image](https://github.com/user-attachments/assets/c0454a27-5fdd-43bc-8c00-4110d1014700)

vemos de vuelta el codigo 200 seguido de la palabra OK, es decir, se genero con exito la peticion.

>[!CAUTION]
>IMPACTO
>

1. al inicializar la base de datos (init_db()), se insertan usuarios con credenciales expuestas directamente en el código (admin:admin123).
2. estas credenciales se pueden usar para iniciar sesión de forma inmediata si el atacante tiene acceso al código.
3. facilita el acceso no autorizado, especialmente en entornos productivos mal configurados.

### Mitigacion:
1. no incluir credenciales en el codigo fuente.
2. configurar usuarios con permisos mínimos necesarios.

# Almacenamiento inseguro de contraseñas

podemos ver como esta linea de codigo contiene la contraseña en texto plano: c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
y luego tambien lo vemos en la consulta: c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
si las contraseñas estan en texto plano facilita ataques como el uso directo de las credenciales y permite su explotacion sin necesidad de brute force. Esta vulnerabilidad fue explotada en pasos anteriores.

>[!CAUTION]
>IMPACTO
>
1. las contraseñas estan guardadas en texto plano dentro de la base de datos y en el codigo.
2. si un atacante accede a la base de datos puede ver directamente todas las contraseñas.
3. permite reutilizacion de contraseñas en otros sitios si los usuarios repiten credenciales.

### Mitigacion:
1. cifrar contraseñas utilizando algoritmos como bcrypt, scrypt o argon2.
2. nunca almacenar contraseñas sin cifrado.

# Inyeccion SQL

en la seccion del login se puede ver la siguiente linea: c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
vemos una consulta SQL construida de forma insegura (inputs no validados/sanitizados).
me guie usando la siguiente pagina para poder explotar la vulnerabilidad: https://portswigger.net/web-security/sql-injection
una vez leida la pagina di con la siguiente consulta:

![Image](https://github.com/user-attachments/assets/af88e26e-5e99-4468-829b-43aa933d35ca)

en base a esta informacion y a conocer ya el username de los usuarios (admin en especifico) hice el siguiente payload en burpsuite:

![Image](https://github.com/user-attachments/assets/510bf445-e1de-49f7-903a-966a343b56d9)

pude hacer una inyeccion SQL de forma exitosa y generandome asi un token para poder luego autenticarme.

>[!CAUTION]
>IMPACTO
>
1. la linea vulnerable permite al atacante manipular la consulta SQL e iniciar sesion sin credenciales validas.
2. posibilidad de exfiltrar datos, modificar registros o ejecutar comandos destructivos en la base de datos.
3. es una de las vulnerabilidades más graves y comunes. 

### Mitigacion:
1. usar consultas parametrizadas.
2. validar y sanitizar los datos de entrada.
3. restingir los permisos de la base de datos al minimo privilegio.
