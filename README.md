
Artefacto: Guía Técnica de Configuración Local y Despliegue RAG
Autora: Yeraldin Arboleda Quintero
Docente Investigador: Ricardo Andrés Santa Quintero (U. Libre)
Fecha de Publicación: Junio 2026
-->
Guía Técnica de Configuración Local y Despliegue RAG


Proyecto: Gestión Documental con Agentes de IA
Autora: Yeraldin Arboleda Quintero
Institución: Universidad Libre — Facultad de Ingeniería 
Programa DELFÍN — Pasantía de Investigación | Junio 2026
Tutor: Ricardo Andrés Santa Quintero (U. Libre)




Tabla de Contenidos


Introducción
Requisitos Previos
Instalación y Configuración
Arquitectura del Sistema
Guía de Uso Paso a Paso
Resolución de Problemas (FAQ)
Glosario
Referencias



1. Introducción

Objetivo del documento:
El presente manual documenta los procesos de instalación, configuración y operación del prototipo local de Gestión Documental Inteligente, diseñado bajo una arquitectura de Generación Aumentada por Recuperación (RAG). Cubre desde el despliegue inicial del entorno hasta la ejecución de consultas analíticas sobre los documentos soporte de los estudiantes.

Alcance:
Este manual cubre:


El despliegue del entorno de contenedores mediante Docker Desktop.
La orquestación del flujo de IA en Dify (v0.6+).
La conexión con modelos de lenguaje locales a través de Ollama.
El procedimiento para realizar consultas analíticas seguras sobre aproximadamente 100 documentos soporte organizados en 12 carpetas de estudiantes, de manera 100% aislada sin transmisión de datos a servicios externos.


Audiencia objetivo:
Docente investigador del proyecto, tutores institucionales, evaluadores del Programa DELFÍN y futuros desarrolladores que continúen con la expansión de la plataforma.


⚠️ Aviso de Privacidad: Todos los documentos procesados por este sistema contienen información académica sensible de estudiantes. Por instrucción explícita del tutor investigador, el prototipo opera únicamente en entorno local. Está estrictamente prohibido subir estos archivos a servicios de nube, APIs externas o herramientas de IA en línea.




2. Requisitos Previos

RequisitoVersión mínimaNotasDocker Desktopv4.x +Necesario para la contenerización y ejecución local de DifyWSL2 (Windows)v2.0 +Subsistema de Linux, obligatorio para rendimiento en WindowsDify (Local)v0.6 +Orquestador RAG y de agentes de IA, desplegado vía Docker ComposeOllamav0.1 +Servidor local de LLMs y embeddings, instalado de forma nativaModelo LLMLlama 3 (8B)Modelo de lenguaje principal para inferencia privadaModelo de EmbeddingsNomic Embed TextModelo local para vectorización e indexación de archivos


3. Instalación y Configuración

3.1 Organización de los Documentos Fuente

Antes de iniciar cualquier configuración de software, organice los documentos descargados desde OneDrive en la siguiente estructura de carpetas local:

C:\Proyecto_Delfin\
└── Base_Conocimiento\
    ├── Estudiante_01\
    │   ├── documento_soporte_01.pdf
    │   └── documento_soporte_02.pdf
    ├── Estudiante_02\
    │   └── ...
    └── Estudiante_12\
        └── ...


🔒 Regla de oro: Esta carpeta no debe sincronizarse con OneDrive personal, Google Drive ni ningún servicio en la nube.




3.2 Despliegue del Servidor de Modelos (Ollama)

Ollama debe instalarse de forma nativa en el sistema operativo (no dentro de Docker). Una vez instalado, descargue los dos modelos necesarios ejecutando en la terminal:

bash# Modelo de lenguaje principal (Meta Llama 3, 8B parámetros)
ollama run llama3

# Modelo de embeddings para vectorización local de documentos
ollama pull nomic-embed-text

Verifique que Ollama está activo y escuchando en su puerto por defecto:

bash# Debe responder con la lista de modelos descargados
curl http://localhost:11434/api/tags


⚠️ Nota de Seguridad Crítica: Toda la computación de tensores, inferencia de texto y vectorización de documentos se realiza directamente en la memoria RAM/VRAM de la máquina local. Ningún dato sensible es transmitido a APIs externas.




3.3 Despliegue de la Plataforma RAG (Dify)

Clone el repositorio oficial de Dify y levante los contenedores mediante Docker Compose:

bash# Clonar repositorio oficial
git clone https://github.com/langgenius/dify.git
cd dify/docker

# Copiar el archivo de configuración de entorno
cp .env.example .env

# Iniciar todos los servicios en segundo plano
docker compose up -d

Una vez completado, acceda a la plataforma en su navegador:

http://localhost:8080


4. Arquitectura del Sistema

El siguiente diagrama ilustra el flujo de datos y la relación entre los componentes del sistema, todo operando dentro del entorno local (localhost):

+-------------------------------------------------------------------------+
|                     COMPUTADOR LOCAL (LOCALHOST)                        |
|                                                                         |
|   [Navegador Web] <--> [Dify : Puerto 8080] <--> [Ollama : Puerto 11434]|
|          ^                      ^                          ^            |
|          |                      |                          |            |
|    Interfaz de             Base de                   Inferencia Local   |
|      Usuario               Conocimiento              Llama 3 / Nomic    |
|                          (12 carpetas /                                 |
|                          ~100 documentos)                               |
|                                                                         |
|   [Scripts Python] --> [Analítica Sprint S004] --> [Dashboard HTML/JS]  |
+-------------------------------------------------------------------------+

Elemento / ComponenteFunciónSección Knowledge (Dify)Permite crear la base vectorial cargando los archivos soporte de forma privada.Configuración de ProveedoresMenú donde se enlaza http://host.docker.internal:11434/ para conectar con Ollama.Studio (Dify)Área de desarrollo del Agente Virtual donde se define el prompt del sistema.Scripts PythonGeneran métricas de evaluación del RAG para el Sprint S004.Dashboard HTML/JS/CSSPresenta los resultados analíticos en el navegador local (http://localhost/...).


5. Guía de Uso Paso a Paso

Caso de Uso: Carga de Documentos e Interrogación Privada del Agente

Paso 1 — Integración de Modelos en Dify:
Ingrese a http://localhost:8080, diríjase a Settings → Model Provider, seleccione Ollama y configure:


LLM: llama3
Modelo de Embeddings: nomic-embed-text
URL del proveedor: http://host.docker.internal:11434



💡 La dirección host.docker.internal es el puente que permite a los contenedores Docker comunicarse con servicios nativos del sistema operativo (como Ollama).



Paso 2 — Indexación Vectorial (Knowledge Base):
Vaya a la pestaña Knowledge, cree una nueva base de conocimiento local y cargue los archivos soporte extraídos de las 12 carpetas de estudiantes. Configure el procesamiento en modo automático usando el modelo de embeddings nomic-embed-text.

Paso 3 — Orquestación del Agente (Studio):
Vaya a Studio, cree un nuevo Agente de Chat, asígnele la base de conocimiento creada en el paso anterior y defina el prompt del sistema para restringir las respuestas exclusivamente al contexto documental provisto.


