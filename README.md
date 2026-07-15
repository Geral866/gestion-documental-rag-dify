# Gestión Documental Inteligente con RAG Local

Sistema local de consulta documental mediante Inteligencia Artificial y arquitectura **RAG (Retrieval-Augmented Generation)**.

El proyecto permite cargar, indexar y consultar documentos académicos utilizando una base de conocimiento en **Dify**, modelos locales ejecutados mediante **Ollama** y procesamiento completamente local.

> **IMPORTANTE:** Los documentos utilizados en este proyecto contienen información académica. El sistema debe ejecutarse en un entorno local. No se deben cargar los documentos en APIs externas ni servicios públicos de Inteligencia Artificial.

---

# 1. Tecnologías utilizadas

El proyecto utiliza las siguientes tecnologías:

| Tecnología       | Función                                               |
| ---------------- | ----------------------------------------------------- |
| Docker Desktop   | Ejecución de los contenedores de Dify                 |
| WSL 2            | Entorno Linux utilizado por Docker en Windows         |
| Dify             | Creación y administración del flujo RAG               |
| Ollama           | Ejecución local de modelos de Inteligencia Artificial |
| Gemma 3          | Modelo de lenguaje utilizado para generar respuestas  |
| Nomic Embed Text | Modelo utilizado para generar embeddings              |
| Git              | Clonación del repositorio de Dify                     |
| PowerShell       | Ejecución de comandos en Windows                      |

---

# 2. Arquitectura del sistema

El sistema funciona de la siguiente manera:

```text
Usuario
   |
   v
Navegador Web
   |
   v
Dify
http://localhost:8080
   |
   v
Base de Conocimiento
   |
   v
Nomic Embed Text
   |
   v
Recuperación de información RAG
   |
   v
Gemma 3
   |
   v
Respuesta al usuario
```

Dify se ejecuta mediante Docker.

Ollama se instala directamente en Windows.

La comunicación entre Dify y Ollama se realiza utilizando:

```text
http://host.docker.internal:11434
```

---

# 3. Requisitos del equipo

Antes de iniciar se recomienda contar con:

* Windows 10 o Windows 11.
* Virtualización habilitada en la BIOS.
* WSL 2.
* Docker Desktop.
* Git.
* Ollama.
* Mínimo 8 GB de memoria RAM.
* Espacio disponible en disco para Docker y los modelos de Ollama.

No es obligatorio disponer de una GPU dedicada.

Debido a las limitaciones de hardware encontradas durante las pruebas, se utiliza **Gemma 3** en lugar de Llama 3.

Llama 3 presentó un mayor consumo de recursos y tiempos de respuesta elevados en el equipo de pruebas.

---

# 4. Orden obligatorio de instalación

Para desplegar el proyecto desde cero siga este orden:

```text
1. Instalar WSL 2
2. Instalar Docker Desktop
3. Instalar Git
4. Instalar Ollama
5. Descargar Gemma 3
6. Descargar Nomic Embed Text
7. Verificar Ollama
8. Clonar Dify
9. Configurar Dify
10. Iniciar los contenedores
11. Crear la cuenta administrativa de Dify
12. Configurar Ollama como proveedor de modelos
13. Configurar Gemma 3
14. Configurar Nomic Embed Text
15. Crear la base de conocimiento
16. Cargar los documentos
17. Crear el chatbot
18. Asociar la base de conocimiento
19. Configurar el prompt
20. Publicar la aplicación
21. Ejecutar una consulta de prueba
```

No se recomienda cambiar este orden.

---

# 5. Instalación de WSL 2

Abra **PowerShell como Administrador**.

Ejecute:

```powershell
wsl --install
```

Espere a que termine la instalación.

Reinicie el equipo.

Después del reinicio abra PowerShell y ejecute:

```powershell
wsl --status
```

También puede verificar las distribuciones instaladas utilizando:

```powershell
wsl --list --verbose
```

Debe observar una distribución utilizando la versión `2`.

Ejemplo:

```text
NAME              STATE           VERSION
Ubuntu            Stopped         2
```

Si la versión mostrada es `1`, ejecute:

```powershell
wsl --set-default-version 2
```

---

# 6. Instalación de Docker Desktop

Instale Docker Desktop para Windows.

Durante la instalación permita el uso del backend basado en **WSL 2**.

Después de instalar Docker Desktop:

1. Reinicie el equipo si el instalador lo solicita.
2. Abra Docker Desktop.
3. Espere hasta que Docker indique que el motor está iniciado.

Abra PowerShell.

Ejecute:

```powershell
docker --version
```

Debe aparecer la versión instalada.

Después ejecute:

```powershell
docker compose version
```

Finalmente pruebe Docker:

```powershell
docker run hello-world
```

Si aparece el mensaje:

```text
Hello from Docker!
```

Docker está funcionando correctamente.

---

# 7. Instalación de Git

Instale Git para Windows.

Después de finalizar la instalación cierre y abra nuevamente PowerShell.

Ejecute:

```powershell
git --version
```

Debe aparecer la versión instalada.

Ejemplo:

```text
git version 2.x.x
```

---

# 8. Instalación de Ollama

Instale Ollama directamente en Windows.

> Ollama NO debe instalarse dentro de los contenedores de Dify.

Después de instalar Ollama cierre y abra nuevamente PowerShell.

Ejecute:

```powershell
ollama --version
```

Si aparece la versión de Ollama la instalación fue correcta.

Verifique que el servicio responda:

```powershell
curl.exe http://localhost:11434/api/tags
```

Si Ollama está funcionando correctamente se mostrará una respuesta en formato JSON.

---

# 9. Descargar Gemma 3

El modelo de lenguaje utilizado en el proyecto es **Gemma 3**.

Ejecute:

```powershell
ollama pull gemma3
```

Espere hasta que la descarga llegue al `100%`.

Después verifique los modelos instalados:

```powershell
ollama list
```

Debe aparecer `gemma3` en la lista.

Ejemplo:

```text
NAME                ID              SIZE
gemma3:latest       XXXXXXXX        XXXX
```

Pruebe el modelo:

```powershell
ollama run gemma3
```

Cuando aparezca el campo para escribir una consulta ingrese:

```text
Hola
```

Si el modelo responde correctamente, escriba:

```text
/bye
```

Esto cerrará la conversación con el modelo.

---

# 10. Descargar el modelo de embeddings

El proyecto utiliza **Nomic Embed Text** para generar los vectores de los documentos.

Ejecute:

```powershell
ollama pull nomic-embed-text
```

Espere hasta finalizar la descarga.

Verifique nuevamente:

```powershell
ollama list
```

Debe observar los dos modelos:

```text
gemma3
nomic-embed-text
```

---

# 11. Verificar Ollama

Ejecute:

```powershell
curl.exe http://localhost:11434/api/tags
```

La respuesta debe incluir los modelos instalados.

También puede ejecutar:

```powershell
ollama list
```

Para consultar los modelos actualmente cargados en memoria:

```powershell
ollama ps
```

> `ollama list` muestra los modelos instalados.
>
> `ollama ps` muestra los modelos actualmente cargados o ejecutándose.

---

# 12. Organización de los documentos

Cree la siguiente carpeta:

```text
C:\Proyecto_Delfin
```

Dentro cree:

```text
C:\Proyecto_Delfin\Base_Conocimiento
```

Organice los documentos por estudiante.

Ejemplo:

```text
C:\Proyecto_Delfin
|
└── Base_Conocimiento
    |
    ├── Estudiante_01
    |   ├── documento_soporte_01.pdf
    |   └── documento_soporte_02.pdf
    |
    ├── Estudiante_02
    |   ├── documento_soporte_01.pdf
    |   └── documento_soporte_02.pdf
    |
    ├── Estudiante_03
    |   └── ...
    |
    └── Estudiante_12
        └── ...
```

## Advertencia de privacidad

La carpeta:

```text
C:\Proyecto_Delfin\Base_Conocimiento
```

NO debe estar dentro de:

```text
OneDrive
Google Drive
Dropbox
```

Los documentos deben permanecer almacenados localmente.

---

# 13. Clonar Dify

Verifique primero que Docker Desktop esté abierto.

Abra PowerShell.

Diríjase a la carpeta del proyecto:

```powershell
cd C:\Proyecto_Delfin
```

Clone el repositorio de Dify:

```powershell
git clone https://github.com/langgenius/dify.git
```

Espere hasta finalizar la descarga.

Verifique que exista la carpeta:

```text
C:\Proyecto_Delfin\dify
```

Ingrese al directorio Docker:

```powershell
cd C:\Proyecto_Delfin\dify\docker
```

---

# 14. Crear el archivo de configuración de Dify

Dentro de:

```text
C:\Proyecto_Delfin\dify\docker
```

Ejecute en PowerShell:

```powershell
Copy-Item .env.example .env
```

Verifique que el archivo exista:

```powershell
Get-ChildItem .env
```

Debe aparecer:

```text
.env
```

> En Windows PowerShell se recomienda utilizar `Copy-Item`.
>
> El comando `cp .env.example .env` también puede funcionar como alias, pero esta guía utiliza la sintaxis nativa de PowerShell.

---

# 15. Iniciar Dify

Confirme que se encuentra en:

```text
C:\Proyecto_Delfin\dify\docker
```

Ejecute:

```powershell
docker compose up -d
```

Docker comenzará a descargar y crear los servicios necesarios.

Este proceso puede tardar varios minutos durante la primera ejecución.

Cuando termine ejecute:

```powershell
docker compose ps
```

Revise que los servicios principales estén iniciados.

Si necesita revisar todos los contenedores:

```powershell
docker ps
```

---

# 16. Acceder a Dify

Abra el navegador.

Ingrese a:

```text
http://localhost:8080
```

En el primer acceso Dify solicitará crear la cuenta administrativa.

Complete los datos solicitados.

Después inicie sesión.

Si la página no abre espere uno o dos minutos y ejecute:

```powershell
docker compose ps
```

Si existen servicios reiniciándose revise los registros:

```powershell
docker compose logs --tail 100
```

---

# 17. Configurar Ollama en Dify

Dentro de Dify ingrese a:

```text
Settings
→ Model Provider
→ Ollama
```

También puede aparecer traducido como:

```text
Configuración
→ Proveedor de modelos
→ Ollama
```

La URL de Ollama debe ser:

```text
http://host.docker.internal:11434
```

NO utilice:

```text
http://localhost:11434
```

desde la configuración del proveedor en Dify.

## ¿Por qué?

Dify se ejecuta dentro de Docker.

Dentro de un contenedor:

```text
localhost
```

hace referencia al propio contenedor.

La dirección:

```text
host.docker.internal
```

permite que Dify se comunique con Ollama instalado directamente en Windows.

---

# 18. Configurar Gemma 3 en Dify

En el proveedor Ollama agregue el modelo de lenguaje.

Configure:

```text
Model Name: gemma3
Model Type: LLM
Base URL: http://host.docker.internal:11434
```

Guarde la configuración.

Si Dify solicita el nombre completo del modelo revise:

```powershell
ollama list
```

Utilice exactamente el nombre mostrado por Ollama.

Por ejemplo:

```text
gemma3:latest
```

Es importante utilizar el nombre real mostrado en el equipo.

---

# 19. Configurar Nomic Embed Text

Agregue un nuevo modelo dentro del proveedor Ollama.

Configure:

```text
Model Name: nomic-embed-text
Model Type: Text Embedding
Base URL: http://host.docker.internal:11434
```

Guarde la configuración.

Si Dify solicita el nombre completo utilice el nombre mostrado por:

```powershell
ollama list
```

Ejemplo:

```text
nomic-embed-text:latest
```

---

# 20. Crear la Base de Conocimiento

Dentro de Dify ingrese al módulo:

```text
Knowledge
```

Seleccione:

```text
Create Knowledge
```

Cree una nueva base de conocimiento.

Ejemplo de nombre:

```text
Base_Conocimiento_Delfin
```

Seleccione la opción para importar documentos.

Cargue los documentos almacenados en:

```text
C:\Proyecto_Delfin\Base_Conocimiento
```

Seleccione el modelo de embeddings:

```text
nomic-embed-text
```

Seleccione el procesamiento automático si está disponible.

Inicie la indexación.

---

# 21. Esperar la indexación de los documentos

Dify comenzará a:

```text
Leer documentos
      ↓
Dividir el contenido en fragmentos
      ↓
Enviar el texto a Nomic Embed Text
      ↓
Generar embeddings
      ↓
Crear los vectores
      ↓
Guardar la información en la base de conocimiento
```

Espere hasta que los documentos aparezcan con estado:

```text
Completed
```

No continúe con la creación del chatbot si los documentos permanecen en:

```text
Processing
```

o presentan:

```text
Error
```

---

# 22. Crear el chatbot

Ingrese al módulo:

```text
Studio
```

Seleccione:

```text
Create App
```

Seleccione una aplicación conversacional compatible con el flujo configurado.

En el entorno utilizado durante el proyecto se trabajó con un chatbot conectado a la base de conocimiento.

Asigne un nombre.

Ejemplo:

```text
Asistente_Delfin_Chat
```

---

# 23. Seleccionar Gemma 3

Dentro de la configuración de la aplicación seleccione:

```text
gemma3
```

o el nombre completo mostrado por Dify:

```text
gemma3:latest
```

Verifique que NO se encuentre seleccionado:

```text
llama3
```

Después de cambiar el modelo guarde o publique la configuración.

---

# 24. Asociar la Base de Conocimiento

Dentro de la configuración del chatbot localice la sección:

```text
Context
```

Agregue:

```text
Base_Conocimiento_Delfin
```

Verifique que la base de conocimiento aparezca asociada al chatbot.

Sin este paso el modelo responderá sin consultar los documentos.

---

# 25. Configurar el System Prompt

Utilice un prompt que limite las respuestas a la información disponible en los documentos.

Ejemplo:

```text
Eres un asistente de gestión documental académica.

Tu función es responder preguntas utilizando únicamente la información recuperada desde la base de conocimiento asociada.

Debes seguir las siguientes reglas:

1. Utiliza únicamente la información disponible en los documentos recuperados.

2. No inventes nombres, fechas, documentos, estados académicos ni información de estudiantes.

3. Si la información solicitada no se encuentra disponible en la base de conocimiento, responde claramente que no existe información suficiente en los documentos consultados.

4. Cuando exista información relevante, responde de forma clara, organizada y profesional.

5. Conserva los nombres y datos tal como aparecen en los documentos.

6. No utilices conocimiento externo para completar información faltante.

7. Si existen fuentes o referencias documentales disponibles, permite que el sistema las muestre como respaldo de la respuesta.

8. Responde de forma cordial incluso cuando no exista información suficiente.
```

Guarde la configuración.

---

# 26. Publicar la aplicación

Este paso es obligatorio.

Después de realizar cambios en:

```text
Modelo
Prompt
Contexto
Base de conocimiento
```

presione:

```text
Publish
```

o:

```text
Update
```

dependiendo de la versión de Dify.

> Si no se publica la aplicación, Dify puede continuar utilizando una configuración anterior.

---

# 27. Ejecutar una prueba

Realice primero una pregunta cuya respuesta exista claramente en los documentos.

Ejemplo:

```text
¿Qué información se encuentra disponible sobre el estudiante [NOMBRE]?
```

También puede realizar una pregunta específica sobre un documento cargado.

El resultado esperado es:

```text
Pregunta del usuario
        ↓
Dify recibe la consulta
        ↓
Consulta la Base de Conocimiento
        ↓
Recupera fragmentos relevantes
        ↓
Gemma 3 recibe el contexto
        ↓
Gemma 3 genera la respuesta
        ↓
Dify muestra la respuesta y las referencias
```

Verifique que la respuesta incluya información existente en los documentos.

Cuando Dify tenga habilitadas las referencias, compruebe que se muestren las fuentes utilizadas.

---

# 28. Orden para iniciar el proyecto después de reiniciar el equipo

Después de apagar o reiniciar el computador utilice siempre este orden.

## Paso 1. Abrir Docker Desktop

Abra Docker Desktop.

Espere hasta que Docker indique que está funcionando.

## Paso 2. Verificar Ollama

Abra PowerShell.

Ejecute:

```powershell
curl.exe http://localhost:11434/api/tags
```

Si Ollama no responde, abra la aplicación Ollama.

También puede ejecutar:

```powershell
ollama list
```

## Paso 3. Verificar Dify

Ejecute:

```powershell
cd C:\Proyecto_Delfin\dify\docker
```

Después:

```powershell
docker compose ps
```

Si los servicios no están iniciados ejecute:

```powershell
docker compose up -d
```

## Paso 4. Abrir Dify

Ingrese a:

```text
http://localhost:8080
```

## Paso 5. Realizar una consulta

Abra:

```text
Studio
→ Asistente_Delfin_Chat
```

Realice una pregunta de prueba.

---

# 29. Comandos de diagnóstico

## Ver modelos instalados

```powershell
ollama list
```

## Ver modelos activos en memoria

```powershell
ollama ps
```

## Verificar la API de Ollama

```powershell
curl.exe http://localhost:11434/api/tags
```

## Ver contenedores de Dify

```powershell
cd C:\Proyecto_Delfin\dify\docker
docker compose ps
```

## Ver todos los contenedores activos

```powershell
docker ps
```

## Ver logs de Dify

```powershell
docker compose logs --tail 100
```

## Ver logs del servicio API

Primero identifique el nombre del contenedor:

```powershell
docker ps
```

Después ejecute:

```powershell
docker logs NOMBRE_DEL_CONTENEDOR --tail 100
```

Ejemplo utilizado durante las pruebas:

```powershell
docker logs docker-api-1 --tail 50
```

El nombre del contenedor puede cambiar dependiendo del despliegue.

## Reiniciar Dify

```powershell
cd C:\Proyecto_Delfin\dify\docker
docker compose restart
```

## Detener Dify

```powershell
docker compose down
```

## Iniciar Dify nuevamente

```powershell
docker compose up -d
```

---

# 30. Resolución de problemas

| Problema                      | Posible causa                      | Solución                                |
| ----------------------------- | ---------------------------------- | --------------------------------------- |
| Dify no abre                  | Contenedores detenidos             | Ejecutar `docker compose up -d`         |
| Error 404                     | Puerto incorrecto                  | Abrir `http://localhost:8080`           |
| Connection Refused            | Dify no encuentra Ollama           | Verificar `host.docker.internal:11434`  |
| Error 502                     | Problema de comunicación           | Revisar Ollama y logs de Docker         |
| Documentos en Processing      | Embeddings lentos                  | Verificar `nomic-embed-text`            |
| Error al indexar              | Modelo de embeddings no disponible | Ejecutar `ollama pull nomic-embed-text` |
| Chat no responde              | Modelo incorrecto                  | Seleccionar Gemma 3                     |
| Chat sigue usando otro modelo | Cambios no publicados              | Presionar `Publish` o `Update`          |
| Respuesta muy lenta           | Recursos limitados                 | Revisar `ollama ps`                     |
| Respuesta sin documentos      | Base no asociada                   | Revisar `Context`                       |
| Respuesta inventada           | Prompt poco restrictivo            | Ajustar el System Prompt                |

---

# 31. Diagnóstico de respuestas lentas

Ejecute:

```powershell
ollama ps
```

Después revise los contenedores:

```powershell
docker ps
```

Revise los logs:

```powershell
cd C:\Proyecto_Delfin\dify\docker
docker compose logs --tail 100
```

Verifique nuevamente la conexión con Ollama:

```powershell
curl.exe http://localhost:11434/api/tags
```

Confirme en Dify:

```text
Modelo: Gemma 3
Embeddings: Nomic Embed Text
Base URL: http://host.docker.internal:11434
```

Finalmente confirme que la aplicación fue publicada utilizando:

```text
Publish
```

o:

```text
Update
```

---

# 32. Validación final del despliegue

Antes de considerar el sistema correctamente instalado verifique:

* [ ] WSL 2 está instalado.
* [ ] Docker Desktop inicia correctamente.
* [ ] `docker run hello-world` funciona.
* [ ] Git está instalado.
* [ ] Ollama está instalado.
* [ ] `curl.exe http://localhost:11434/api/tags` responde.
* [ ] Gemma 3 aparece en `ollama list`.
* [ ] Nomic Embed Text aparece en `ollama list`.
* [ ] Dify está desplegado.
* [ ] `docker compose ps` muestra los servicios iniciados.
* [ ] Dify abre en `http://localhost:8080`.
* [ ] Ollama está configurado en Dify.
* [ ] La URL configurada es `http://host.docker.internal:11434`.
* [ ] Gemma 3 está configurado como LLM.
* [ ] Nomic Embed Text está configurado como modelo de embeddings.
* [ ] La base de conocimiento fue creada.
* [ ] Los documentos aparecen en estado `Completed`.
* [ ] La base de conocimiento está asociada al chatbot.
* [ ] El System Prompt está configurado.
* [ ] La aplicación fue publicada.
* [ ] El chatbot responde utilizando los documentos.
* [ ] Las referencias documentales aparecen en las respuestas cuando están disponibles.

Si todos los puntos anteriores se cumplen, el entorno RAG local se encuentra correctamente desplegado.

---

# 33. Privacidad y seguridad

El sistema fue diseñado para trabajar con información académica sensible.

Todo el procesamiento debe realizarse localmente.

Los documentos no deben cargarse en:

* APIs externas.
* Servicios públicos de Inteligencia Artificial.
* Chatbots en línea.
* Plataformas externas no autorizadas.

El flujo principal funciona mediante:

```text
Dify local
+
Docker local
+
Ollama local
+
Gemma 3 local
+
Nomic Embed Text local
```

La información documental debe permanecer dentro del entorno autorizado del proyecto.

---

# 34. Autora

**Yeraldin Arboleda Quintero**

Programa DELFÍN
Pasantía de Investigación
Universidad Libre
Facultad de Ingeniería

Junio de 2026
