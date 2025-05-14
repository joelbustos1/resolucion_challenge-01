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

5. una vez hecho esto ya vamos a poder ir capturando el trafico de los endpoints dados pero antes revise el codigo fuente de la app y encontre a simple vista varias vulnerabilidades que a continuacion muestro:

![Image](https://github.com/user-attachments/assets/bc0e0037-b6b4-47da-a4b0-d227e27e64b9)
