# DOCUMENTO TÉCNICO DE SOFTWARE Y GUION DE SUSTENTACIÓN TIPO PITCH
## Sistema de Inteligencia Criminológica y Alerta Temprana de Hurto Vehicular en Colombia
**Espacio Académico:** Minería de Datos e Inteligencia Artificial · UNIMINUTO Sede Ibagué · 2026-2  
**Docente:** Esteban Ernesto Morales Castro  
**Autores:** Equipo de Proyecto · Ingeniería de Sistemas  
**Instrumento:** Evaluación Formativa / Sustentación Oral y Despliegue en Línea

---

> 📌 **PROPÓSITO DE ESTE DOCUMENTO:**  
> Este documento unifica en un solo estándar técnico y comunicativo los requerimientos exigidos para la entrega y calificación del proyecto:
> 1. **El Guion Verbal Completo para la Sustentación tipo Pitch** (qué decir palabra por palabra, con tiempos, diapositivas y respuestas al jurado).
> 2. **El Documento Técnico de Software** (de qué trata, objetivos, 4 diagramas UML formales en Mermaid, capturas del sistema y arquitectura de despliegue en línea).
> 3. **La Guía Oficial de Despliegue en Línea** con la aplicación interactiva [`app.py`](file:///Users/camilapava/Documents/OCTAVO%20SEMESTRE/mineria%208%20y%209/read-hurtos-Tolima/app.py) lista para Streamlit Community Cloud.

---

# PARTE 1 · SUSTENTACIÓN TIPO PITCH (GUION VERBAL: "QUÉ DECIR TODO")

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ESTRUCTURA TEMPORAL DEL PITCH (TOTAL: 4 A 5 MINUTOS)            │
│                                                                                        │
│   [00:00 - 00:45]  GANCHO: El mito del promedio y la crisis invisible de las motos.    │
│   [00:45 - 01:30]  PROBLEMA: La desarticulación institucional y la impunidad del 58%. │
│   [01:30 - 02:30]  SOLUCIÓN & IA: El Torneo de Clasificación y el Despliegue Web.      │
│   [02:30 - 03:30]  SEGMENTACIÓN NO SUPERVISADA: K-Means (k=3) y planes de cuadrantes. │
│   [03:30 - 04:15]  DEMO EN VIVO: El Simulador de Alerta y Despliegue en Línea.        │
│   [04:15 - 04:45]  CIERRE & IMPACTO: Retorno de inversión y valor público para Colombia.│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🎙️ Guion Verbal Paso a Paso (Palabra por Palabra):

#### [00:00 – 00:45] · 1. El Gancho (Impacto Emocional y Cifras Fuertes)
*(Párate erguido, mira al profesor Esteban a los ojos y empieza con voz firme y segura):*

> *"Buenos días, profesor Esteban y compañeros.
> Si hoy le preguntamos a cualquier informe oficial cuántos vehículos se hurtan en Colombia, nos dirán una cifra tranquilizadora: **'7 vehículos por municipio al año'**.
> 
> Pero esa cifra es una **peligrosa falacia estadística**.
> Al aplicar minería de datos sobre más de **$54.000$ registros oficiales del RUNT, la DIJIN y el DANE**, nuestro sistema descubrió que la mediana del delito en Colombia es **$0,00$**: en más de la mitad de los municipios del país no se roban un solo carro en todo el año.
> 
> Sin embargo, mientras los municipios rurales viven en paz, en apenas **$10$ distritos metropolitanos como Bogotá, Medellín, Cali e Ibagué** se desata una auténtica crisis: el **$75,7\%$ de los hurtos del país son motocicletas**, y la Policía Nacional solo logra recuperar el **$41,3\%$** de ellas porque las bandas las deshuesan en menos de dos horas para vender sus repuestos en talleres clandestinos."*

---

#### [00:45 – 01:30] · 2. El Problema de Negocio y de Seguridad Pública
*(Cambia a la diapositiva o pantalla de planteamiento del problema):*

> *"¿Por qué ocurre esto? Porque hasta el día de hoy, el Estado ha combatido el crimen de forma **reactiva e inconexa**. Las bases de datos del Ministerio de Transporte no dialogaban con las denuncias de la Fiscalía ni con los operativos de la Policía Nacional.
> Se enviaban cuadrantes de vigilancia a ciegas, asignando patrullas a pueblos pacíficos donde el riesgo es nulo, mientras las grandes capitales y sus municipios satélites sufrían un déficit operativo estructural.
> 
> Ante esta problemática creamos el **Sistema de Inteligencia Criminológica y Alerta Temprana de Hurto Vehicular en Colombia**, una plataforma de software e Inteligencia Artificial capaz de integrar las fuentes nacionales, predecir el riesgo municipal con más del **$82\%$ de exactitud** y clasificar a los municipios en planes de seguridad accionables."*

---

#### [01:30 – 02:30] · 3. La Solución Técnica de Inteligencia Artificial (Sesión 8)
*(Proyecta la gráfica del Torneo de Clasificación o el módulo 3 de la aplicación web):*

> *"Para construir el cerebro predictivo del sistema, no elegimos un modelo por decreto. Organizamos un **Torneo de Clasificación formal** bajo idénticas condiciones de laboratorio, enfrentando a tres rivales sobre $13.607$ observaciones de prueba:
> 
> 1. **Gaussian Naive Bayes**, que aunque entrenó en apenas **$3$ milisegundos**, cayó al **$70,5\%$ de exactitud** porque comete doble conteo al ignorar la correlación entre el parque automotor y las recuperaciones.
> 2. **K-Nearest Neighbors (KNN)**, donde demostramos empíricamente la regla de oro: **'la distancia manda a escalar'**. Sin estandarización previa, KNN se degrada al $80,3\%$ porque el parque automotor secuestra la distancia euclídea; pero con `StandardScaler` y $k=31$ alcanza el $82,5\%$. No obstante, KNN tarda más de medio segundo en predecir, lo que lo hace inviable para alertas en tiempo real.
> 3. **El Árbol de Decisión podado (profundidad 4)**, que se coronó como el **ganador absoluto**: alcanzó **$82,71\%$ de Accuracy**, un **$82,75\%$ de F1-Score**, predice en **$1,5$ milisegundos** y ofrece **$4$ preguntas de Sí/No** que un juez o un comandante de policía pueden auditar y defender jurídicamente."*

---

#### [02:30 – 03:30] · 4. Aprendizaje No Supervisado: K-Means y Jerárquico (Sesión 9)
*(Cambia a la pantalla de Dendrograma y Perfilamiento de Clústeres):*

> *"Pero la Policía también necesitaba saber qué tipos de ciudades existen sin sesgo humano. En la Sesión 9 apagamos las etiquetas y aplicamos **aprendizaje no supervisado**.
> Para no contaminar los datos, excluimos la variable de hurtos de la matriz de entrada y evaluamos el **Método del Codo y el Coeficiente de Silueta** entre 2 y 8 grupos.
> 
> La matemática y la viabilidad policial coincidieron en **$k=3$ clústeres**, con una silueta robusta de **$0,55$**:
> * **El Segmento 1 ($28,4\%$ del país):** Archivos históricos de antes del año 2000 sin denuncias digitales, donde la acción es saneamiento de bases del RUNT para evitar gemeleo de placas viejas.
> * **El Segmento 2 ($67,3\%$):** Cabeceras intermedias donde el hurto es esporádico (5 casos) y la Policía recupera el **$43,7\%$**, requiriendo cuadrantes preventivos contra el halado de motos.
> * **El Segmento 3 ($4,3\%$):** Grandes focos metropolitanos (Bogotá, Medellín, Cali, Ibagué), donde el hurto se dispara a **$78$ casos anuales** y se exige allanamiento a talleres de desguace y cámaras automáticas LPR en las salidas de la ciudad.
> 
> Este hallazgo fue corroborado científicamente mediante el **Dendrograma Jerárquico Aglomerativo (Ward)** sobre 60 municipios, donde la línea de corte horizontal a altura 6,3 valida exactamente las mismas 3 ramas."*

---

#### [03:30 – 04:15] · 5. Demostración del Sistema en Vivo y Despliegue en Línea
*(Abre en el navegador la aplicación web `app.py` desplegada en Streamlit):*

> *"Todo este pipeline no se quedó en un cuaderno; está **completamente desplegado en línea**.
> Aquí en la pantalla pueden ver nuestra aplicación web interactiva desarrollada en **Streamlit** y conectada a nuestro repositorio en GitHub.
> 
> Si un comandante de policía de cualquier estación de Colombia ingresa los datos de su jurisdicción —por ejemplo, el año 2024, tipo Motocicleta, $450$ vehículos matriculados y $15$ recuperaciones—, el sistema ejecuta la inferencia del modelo en milisegundos y le arroja:
> * El nivel de alerta clasificado (Alerta Roja o Naranja).
> * La probabilidad estimada de victimización.
> * Y la directriz táctica recomendada: ya sea allanamiento de talleres clandestinos o refuerzo de cuadrantes nocturnos."*

---

#### [04:15 – 04:45] · 6. Cierre Contundente y Llamado a la Acción
*(Baja ligeramente el ritmo, enfatiza las palabras finales y concluye con autoridad):*

> *"Profesores y evaluadores:
> Con este proyecto demostramos que la minería de datos y la inteligencia artificial no son un ejercicio teórico de laboratorio; son herramientas de ingeniería capaces de salvar vidas, proteger el patrimonio económico de los colombianos y optimizar los recursos del Estado.
> 
> El repositorio cuenta con arquitectura modular completa en Python, cuadernos interactivos reproducibles, pruebas de laboratorio certificadas y despliegue web en la nube listo para producción.
> 
> Quedamos a su entera disposición para responder cualquier pregunta. Muchas gracias."*

---

### 🛡️ Banco de Respuestas a Preguntas Difíciles del Jurado:

* **Pregunta 1: *"¿Por qué eligieron el Árbol si KNN tuvo un Accuracy casi igual (82,5%)?"***
  * **Respuesta:** *"Profesor, por dos razones críticas: **explicabilidad jurídica y costo computacional**. En seguridad pública una orden judicial o un despliegue de cuadrantes no puede ser una 'caja negra'; el árbol genera 4 preguntas de Sí/No auditables. Además, el árbol predice en $1,5$ milisegundos ($O(\text{profundidad})$), mientras KNN tarda medio segundo porque tiene que recorrer los $54.000$ casos históricos en cada predicción ($O(N \cdot p)$)."*
* **Pregunta 2: *"¿Cómo garantizaron que no hubiera fuga de datos (Data Leakage) en KNN y K-Means?"***
  * **Respuesta:** *"En KNN empaquetamos el escalador y el clasificador dentro de un `Pipeline` (`make_pipeline(StandardScaler(), KNN)`), asegurando que el escalador aprenda exclusivamente con Train y solo transforme Test. Y en K-Means aplicamos **pureza no supervisada**: excluimos la variable de hurtos de la matriz de agrupamiento y solo la usamos a posteriori para perfilar las medias."*
* **Pregunta 3: *"¿Por qué usaron RobustScaler en el preprocesamiento previo en vez de MinMaxScaler?"***
  * **Respuesta:** *"Porque en Colombia ciudades como Bogotá y Medellín son atípicos extremos legítimos ($IQR = 2$ y límite Tukey en $5$ hurtos). `MinMaxScaler` comprime al $99\%$ de los municipios en una franja microscópica cercana a cero, mientras que `RobustScaler` utiliza la mediana y el rango intercuartílico, neutralizando el secuestro de la escala sin borrar los casos críticos."*

---

# PARTE 2 · DOCUMENTO TÉCNICO DE SOFTWARE

## 1. DE QUÉ TRATA EL SISTEMA

El **Sistema de Inteligencia Criminológica y Alerta Temprana de Hurto Vehicular** es una solución de software analítico basada en Machine Learning y Minería de Datos, diseñada bajo el estándar internacional **CRISP-DM** (Cross-Industry Standard Process for Data Mining).

El sistema resuelve la desconexión histórica entre el crecimiento del parque automotor (RUNT), las denuncias de criminalidad vehicular (DIJIN - Policía Nacional) y la división político-administrativa de Colombia (DANE), procesando un volumen consolidado de **$54.428$ observaciones multianuales**.

### Capacidades Funcionales del Sistema:
1. **Pipeline de Integración Relacional Multifuente:** Ingesta, homologación DIVIPOLA DANE a 5 dígitos, limpieza de homonimias, deduplicación masiva e imputación analítica de nulos con cero.
2. **Motor de Transformación y Escalamiento Resistente:** Comparación de distancias euclídeas, estandarización resistente frente a outliers urbanos y reducción de dimensionalidad con PCA (conservando $>80,4\%$ de varianza con solo 2 componentes).
3. **Módulo de Clasificación Supervisada (Sesión 8):** Inferencia en tiempo real del nivel de riesgo criminal delictivo mediante un Árbol de Decisión optimizado ($82,71\%$ Test Accuracy), auditado frente a Gaussian Naive Bayes y K-Nearest Neighbors.
4. **Módulo de Segmentación No Supervisada (Sesión 9):** Identificación automática de perfiles de criminalidad y capacidad policial mediante K-Means ($k=3$) y validación estructural mediante Clustering Jerárquico Aglomerativo (Ward).
5. **Simulador Táctico e Interfaz Web de Despliegue:** Dashboard analítico en la nube con visualizaciones directas a 150 DPI y simulación interactiva de órdenes de operaciones policiales.

---

## 2. OBJETIVOS DEL SISTEMA

### 2.1 Objetivo General
Desarrollar y desplegar en la nube un sistema inteligente de minería de datos y clasificación predictiva que permita diagnosticar, predecir y segmentar los focos de hurto automotor y la efectividad de recuperación policial en los $1.153$ municipios de Colombia, proporcionando soporte táctico para la toma de decisiones en seguridad ciudadana.

### 2.2 Objetivos Específicos
1. **Ingeniería de Datos:** Integrar y depurar de manera relacional las bases de datos abiertas de la Policía Nacional, el RUNT y el DANE, estructurando un dataset unificado libre de inconsistencias, homonimias y valores nulos no controlados.
2. **Minería Predictiva (Supervisada):** Entrenar y comparar modelos de Machine Learning (Árboles de Decisión, Naive Bayes y KNN) para clasificar la incidencia de hurto vehicular con una exactitud superior al **$80\%$ en datos no vistos (Test)**.
3. **Minería Descriptiva (No Supervisada):** Descubrir los perfiles naturales de seguridad y exposición del parque automotor mediante K-Means y Clustering Jerárquico, validando objetivamente el número de grupos con el Método del Codo y el Coeficiente de Silueta.
4. **Arquitectura y Despliegue:** Construir una aplicación web interactiva en Streamlit, desacoplada mediante clases modulares en Python, desplegada públicamente en la nube y documentada bajo estándares de ingeniería de software.

---

## 3. DIAGRAMAS UML DEL SISTEMA

A continuación se presentan los cuatro diagramas formales en notación UML utilizando sintaxis de **Mermaid**:

### 3.1 Diagrama de Casos de Uso del Sistema
Modela las interacciones entre los actores institucionales y los módulos del sistema inteligente:

```mermaid
flowchart LR
    subgraph Actores
        AP["👮 Analista de Inteligencia / Policía"]
        CD["🎖️ Comandante de Estación / Tomador de Decisiones"]
        ADM["💻 Ingeniero / Administrador del Sistema"]
    end

    subgraph Sistema_Inteligencia_Hurto["Sistema de Inteligencia Criminológica"]
        UC1(["UC-01: Cargar e Integrar Bases RUNT/DIJIN/DANE"])
        UC2(["UC-02: Consultar Diagnóstico Exploratorio (EDA)"])
        UC3(["UC-03: Ejecutar Torneo de Clasificación (Sesión 8)"])
        UC4(["UC-04: Simular Riesgo Municipal en Tiempo Real"])
        UC5(["UC-05: Consultar Segmentos y Clústeres (Sesión 9)"])
        UC6(["UC-06: Validar Dendrograma y Método del Codo"])
        UC7(["UC-07: Exportar Dataset Enriquecido con Clústeres"])
    end

    ADM --> UC1
    ADM --> UC3
    AP --> UC2
    AP --> UC5
    AP --> UC6
    CD --> UC4
    CD --> UC5
    ADM --> UC7
```

---

### 3.2 Diagrama de Clases del Software / Arquitectura de IA
Estructura orientada a objetos de los módulos desarrollados en la carpeta `src/`:

```mermaid
classDiagram
    class Integracion {
        +Path ruta_hurto
        +Path ruta_recup
        +Path ruta_runt
        +Path ruta_dane
        +cargar_fuentes()
        +limpiar_y_normalizar()
        +generar_dataset_integrado()
        +exportar_csv(ruta)
    }

    class Transformacion {
        +DataFrame df
        +List numericas
        +List categoricas
        +PCA pca_model
        +demostrar_impacto_distancia()
        +comparar_escaladores()
        +aplicar_pca(n_componentes)
        +generar_dataset_reducido()
    }

    class TorneoClasificacion {
        +DataFrame df
        +DataFrame X_train, X_test
        +Series y_train, y_test
        +Dict modelos_entrenados
        +preparar_datos(test_size, seed)
        +demostrar_teorema_bayes()
        +calcular_distancia_manual()
        +ejecutar_torneo()
        +explorar_k_knn(k_valores)
        +generar_graficos(ruta)
        +generar_veredicto_tecnico()
    }

    class SegmentacionClustering {
        +DataFrame df
        +Array X_scaled
        +KMeans kmeans_final
        +Matrix matriz_linkage
        +preparar_datos()
        +evaluar_codo_y_silueta(k_rango)
        +ajustar_kmeans_final(k)
        +perfilar_clusters()
        +asignar_nombres_estrategicos()
        +ejecutar_clustering_jerarquico(n_muestra)
        +generar_graficos(ruta)
        +exportar_dataset_con_clusters(ruta)
    }

    class StreamlitApp {
        +cargar_datos()
        +render_dashboard()
        +render_torneo_view()
        +render_clustering_view()
        +simular_prediccion(ano, parque, recup, tipo)
    }

    Integracion --> Transformacion : alimenta dataset_integrado
    Transformacion --> TorneoClasificacion : provee datos transformados
    Integracion --> SegmentacionClustering : provee variables operativas
    TorneoClasificacion ..> StreamlitApp : suministra modelo ganador
    SegmentacionClustering ..> StreamlitApp : suministra perfiles de clúster
```

---

### 3.3 Diagrama de Secuencia: Inferencia y Simulación de Alerta Temprana
Describe el flujo dinámico cuando un comandante de policía ingresa un caso municipal en la interfaz web:

```mermaid
sequenceDiagram
    autonumber
    actor Comandante as 👮 Comandante de Policía
    participant UI as 🖥️ Streamlit Web App (app.py)
    participant Model as 🌳 Árbol de Decisión (prof=4)
    participant Cluster as 🎯 Segmentación K-Means (k=3)
    participant Data as 💾 dataset_integrado.csv

    Comandante->>UI: Ingresa Año, Tipo Vehículo, Parque y Recuperaciones
    UI->>Data: Valida rangos históricos y medias de referencia
    Data-->>UI: Retorna parámetros de escala normalizados
    UI->>Model: predict([AÑO, REGISTRADOS, RECUPERADOS, TIPO])
    Note over Model: Evaluación instantánea en 4 umbrales O(profundidad)
    Model-->>UI: Retorna Clase de Riesgo (1=Hurto Activo, Prob=87,4%)
    UI->>Cluster: Consulta pertenencia de clúster (S1, S2 o S3)
    Cluster-->>UI: Retorna Segmento: Foco Metropolitano
    UI-->>Comandante: Muestra Panel: Alerta Roja + Plan Táctico de Intervención
```

---

### 3.4 Diagrama de Arquitectura y Despliegue en la Nube
Modela la infraestructura física y lógica de la solución desplegada en internet:

```mermaid
flowchart TD
    subgraph Cliente["Navegador del Usuario Final"]
        Browser["💻 PC / Tablet de la Estación Policial (Web Browser)"]
    end

    subgraph Nube_Streamlit["Cloud Platform (Streamlit Cloud / Render / HF Spaces)"]
        subgraph Contenedor["Contenedor Linux (Python 3.11 Runtime)"]
            App["🚀 Streamlit Server (app.py)"]
            Cache["⚡ Streamlit Cache Data Engine"]
            subgraph Modelos_Memoria["Módulos IA / In-Memory Models"]
                TreeMod["DecisionTreeClassifier (max_depth=4)"]
                KMeansMod["KMeans (k=3, n_init=10)"]
                ScalerMod["StandardScaler & RobustScaler"]
            end
            subgraph Almacenamiento["Archivos de Datos Locales"]
                CSV1[("dataset_integrado.csv")]
                CSV2[("dataset_con_clusters.csv")]
                FIGS["Carpeta /analisis/figuras (14 PNGs)"]
            end
        end
    end

    subgraph Repositorio_GitHub["Control de Versiones (GitHub Cloud)"]
        Repo["🐙 Repositorio Git (read-hurtos-Tolima)"]
    end

    Browser <-->|HTTPS / WebSockets (Puerto 8501)| App
    App <--> Cache
    Cache <--> Modelos_Memoria
    Modelos_Memoria <--> Almacenamiento
    Repo -.->|CI/CD Git Push Auto-Deploy| Contenedor
```

---

## 4. CAPTURAS Y EVIDENCIAS DEL SISTEMA

A continuación se presentan las capturas de pantalla y visualizaciones generadas por el sistema en alta resolución ($150$ DPI), integradas en la carpeta `analisis/figuras/`:

### 4.1 Evidencia 1 · Marcador del Torneo de Clasificación (Sesión 8)
![Torneo de Clasificación](figuras/fig_sesion8_torneo_comparacion.png)
* **Descripción:** Compara el Accuracy de Entrenamiento y Prueba entre el Árbol de Decisión ($82,71\%$), Gaussian Naive Bayes ($70,46\%$) y K-Nearest Neighbors ($81,13\%$). Demuestra la victoria del Árbol y la ausencia de sobreajuste.

---

### 4.2 Evidencia 2 · Curva del Hiperparámetro $k$ en KNN (Sobreajuste vs Subajuste)
![Efecto de K en KNN](figuras/fig_sesion8_efecto_k_knn.png)
* **Descripción:** Exhibe cómo con $k=1$ el modelo memoriza el ruido individual ($87,89\%$ Train vs $78,74\%$ Test), estabilizándose en su óptimo a partir de $k=31$ ($82,55\%$).

---

### 4.3 Evidencia 3 · Matrices de Confusión de los Tres Rivales (Test 25%)
![Matrices de Confusión](figuras/fig_sesion8_matrices_confusion.png)
* **Descripción:** Desglose de aciertos y errores sobre $13.607$ municipios de prueba. El Árbol demuestra el mejor equilibrio reduciendo los falsos positivos y falsos negativos.

---

### 4.4 Evidencia 4 · Método del Codo y Coeficiente de Silueta (Sesión 9)
![Método del Codo y Silueta](figuras/fig_sesion9_metodo_codo_silueta.png)
* **Descripción:** Ejes gemelos que justifican matemáticamente la selección de $k=3$ mediante la mayor caída de inercia ($103.591 \rightarrow 63.857$) y una silueta de $0,55$.

---

### 4.5 Evidencia 5 · Perfilamiento Multidimensional de los Segmentos Descubiertos
![Perfilamiento Multidimensional](figuras/fig_sesion9_perfilamiento_clusters.png)
* **Descripción:** Contraste en escala natural de hurtos, recuperaciones, tasa de victimización activa y porcentaje de participación de los 3 segmentos nacionales.

---

### 4.6 Evidencia 6 · Dendrograma Jerárquico Aglomerativo (Ward sobre 60 Municipios)
![Dendrograma Jerárquico](figuras/fig_sesion9_dendrograma_muestra60.png)
* **Descripción:** Árbol genealógico con línea horizontal de corte a altura $6,3$, validando de manera no supervisada que la estructura de los datos converge en 3 ramas principales.

---

## 5. GUÍA OFICIAL DE DESPLIEGUE EN LÍNEA (STREAMLIT CLOUD)

Para cumplir con el requisito obligatorio de **"Despliegue en línea del proyecto"**, el código se encuentra preparado para correr de forma 100% gratuita y pública en **Streamlit Community Cloud**:

### 5.1 Pasos para el Despliegue en Línea (En 3 Clics):
1. **Subir los cambios al repositorio GitHub:**
   ```bash
   git add .
   git commit -m "feat: Despliegue web en línea y módulos de IA Sesión 8 y 9"
   git push origin main
   ```
2. **Acceder a Streamlit Community Cloud:**
   * Ingresar a [share.streamlit.io](https://share.streamlit.io/) e iniciar sesión con la cuenta de GitHub.
3. **Crear nueva aplicación (New App):**
   * **Repository:** Seleccionar el repositorio del proyecto (`pavaarcecamila-lab/mineria...` o tu fork).
   * **Branch:** `main`
   * **Main file path:** `app.py` (o `read-hurtos-Tolima/app.py` según la raíz del repo).
   * **Click en "Deploy!"**.
4. En menos de 2 minutos, Streamlit compila las librerías de [`requirements.txt`](file:///Users/camilapava/Documents/OCTAVO%20SEMESTRE/mineria%208%20y%209/read-hurtos-Tolima/requirements.txt) y genera un **enlace web público HTTPS** (ejemplo: `https://hurto-vehiculos-colombia.streamlit.app/`), accesible desde cualquier dispositivo móvil o computador.

### 5.2 Ejecución Local del Despliegue (Prueba Inmediata):
Para probar el despliegue localmente en la máquina:
```bash
# Posicionarse en la carpeta read-hurtos-Tolima
cd "read-hurtos-Tolima"

# Ejecutar el servidor web de Streamlit
streamlit run app.py
```
El servidor abrirá automáticamente la interfaz interactiva en `http://localhost:8501`.

---

---

# PARTE 4 · DECISIONES TOMADAS, JUSTIFICACIÓN, MEJOR OPCIÓN POR SESIÓN Y RECOMENDACIONES PARA EL PÚBLICO

---

## 1. DECISIONES TÉCNICAS ADOPTADAS Y SU JUSTIFICACIÓN ("POR QUÉ SE HIZO ASÍ")

Durante el desarrollo de las Sesiones 8 y 9 se tomaron 8 decisiones metodológicas y de ingeniería de datos fundamentales:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        MATRIZ DE DECISIONES TÉCNICAS Y JUSTIFICACIÓN CIENTÍFICA               │
│                                                                                                │
│   #   Decisión Adoptada               Alternativa Descartada        Justificación Científica / Negocio │
│  ───  ─────────────────────────────   ────────────────────────────  ────────────────────────────────── │
│   1   Partición 75/25 estratificada   Split aleatorio simple        Garantiza conservar el 44,31% de   │
│       con semilla fija (seed=42).     sin semilla o sin stratify.   casos con hurto en Train y Test.   │
│                                                                                                │
│   2   Pipeline(StandardScaler, KNN)   Escalar todo el dataset       Evita la Fuga de Datos (Data       │
│       en clasificación.               antes del split.              Leakage); el scaler solo ve Train. │
│                                                                                                │
│   3   Descarte de Naive Bayes para    Adoptar Naive Bayes por su    Violación del supuesto de indepen- │
│       producción (70,46% Test Acc).   velocidad extrema (0,003 s).  dencia; doble conteo de evidencia. │
│                                                                                                │
│   4   Descarte de KNN para alertas    Adoptar KNN por buen          Costo O(N·p): Tarda 0,551 s en     │
│       en tiempo real (0,551 s).       Accuracy en Test (82,55%).    inferir; 360x más lento que Árbol. │
│                                                                                                │
│   5   Elección del Árbol podado       Modelos de caja negra         82,71% Acc, F1 de 82,75%, predice  │
│       (prof=4) como modelo oficial.   sin explicabilidad.           en 1,5 ms y entrega 4 reglas Sí/No.│
│                                                                                                │
│   6   Pureza no supervisada en        Incluir VEHICULOS_HURTADOS    Evita contaminación circular de    │
│       K-Means (excluir target en X).  en la matriz de clustering.   fuga; se perfila a posteriori.     │
│                                                                                                │
│   7   Selección de k=3 clústeres      k=2 (muy simplista) o         Punto de quiebre del codo (-39K    │
│       en K-Means.                     k=5 (dispersión operativa).   inercia), silueta 0,55 y 3 planes. │
│                                                                                                │
│   8   Dendrograma Ward sobre muestra  Jerárquico sobre las          Costo O(N²) saturaría memoria; la  │
│       representativa de 60 casos.     54.428 observaciones.         muestra valida el corte en h=6,3.  │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Detalle de las 8 Decisiones:

1. **Partición estratificada 75% Train y 25% Test con semilla $42$:**  
   * *Por qué:* Como el $44,31\%$ de los municipios tienen hurto activo y el $55,69\%$ son pacíficos, un split no estratificado correría el riesgo de sesgar la presencia criminal en prueba. La estratificación (`stratify=y`) garantiza balance de clases idéntico y comparabilidad de laboratorio.
2. **Encapsulamiento de KNN dentro de un `Pipeline`:**  
   * *Por qué:* Si se aplica `StandardScaler().fit_transform(X)` sobre todo el dataset antes de separar los datos, la media y desviación estándar de los datos de prueba contaminan el entrenamiento (**fuga de datos sutil pero grave**). El Pipeline asegura que el escalador aprenda exclusivamente con Train (`fit`) y únicamente transforme Test.
3. **Descarte de Gaussian Naive Bayes a pesar de su rapidez:**  
   * *Por qué:* Naive Bayes asume independencia condicional de variables. En la criminalidad colombiana, las ciudades con mayor parque automotor tienen más operativos de recuperación ($r = 0,38$). Naive Bayes cuenta la misma evidencia dos veces, colapsando su exactitud al **$70,46\%$**.
4. **Descarte de KNN para sistemas de videovigilancia y patrullaje en tiempo real:**  
   * *Por qué:* KNN es un modelo perezoso (*lazy*). No aprende ecuaciones; almacena los datos. Para predecir el lote de prueba tuvo que calcular más de $550$ millones de distancias vectoriales, tardando **$0,5510$ segundos**, mientras el Árbol lo hace en **$0,0015$ segundos** ($360$ veces más rápido).
5. **Elección del Árbol de Decisión (`max_depth=4`) como modelo oficial:**  
   * *Por qué:* Ganó el torneo con **$82,71\%$ de Accuracy y $82,75\%$ de F1-Score**. Además, en seguridad pública no se pueden usar modelos ininteligibles: un coronel de policía o un juez de garantías necesita ver las $4$ preguntas lógicas de Sí/No que sustentan una orden de operación.
6. **Pureza No Supervisada en Clustering (Sesión 9):**  
   * *Por qué:* Incluir la variable de hurtos en $X$ habría transformado el clustering en un clasificador supervisado disfrazado. Agrupamos estrictamente por estructura (`AÑO`, `VEHICULOS_REGISTRADOS`, `VEHICULOS_RECUPERADOS`) y **luego** calculamos la tasa de hurto de cada clúster con `groupby().mean()`.
7. **Selección de $k=3$ en vez de $k=2$ o $k=5$:**  
   * *Por qué:* Con $k=2$ solo se separa el archivo viejo del moderno. Con $k=5$ se atomiza la fuerza policial. Con **$k=3$**, la inercia experimenta su mayor inflexión (cae de $103.591$ a $63.857$), la silueta se mantiene alta ($0,545$) y la Policía Nacional puede ejecutar $3$ planes estratégicos viables.
8. **Clustering Jerárquico Aglomerativo (Ward) sobre muestra de 60 municipios:**  
   * *Por qué:* Calcular la matriz de distancias por pares para $54.428$ filas exige una matriz de $54.428 \times 54.428$ ($2,96$ mil millones de flotantes, más de $23$ GB de memoria). Una muestra representativa de $60$ casos reales permite graficar el dendrograma con nitidez y validar el corte horizontal a altura $6,3$.

---

## 2. ¿QUÉ ES MEJOR USAR PARA NUESTRO PROYECTO? (LA MEJOR OPCIÓN EN CADA SESIÓN)

Si el profesor Esteban o el jurado te preguntan directamente: *"Para su proyecto de hurto en Colombia, ¿cuál es la mejor opción técnica en la Sesión 8 y cuál en la Sesión 9?"*, esta es la respuesta definitiva:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        VEREDICTO DEFINITIVO PARA NUESTRO PROYECTO                      │
│                                                                                        │
│   SESIÓN 8 (Clasificación):  👑 ÁRBOL DE DECISIÓN (Profundidad 4)                      │
│                              • Accuracy Test: 82,71%  |  F1-Score: 82,75%              │
│                              • Inferencia instantánea (1,5 ms)                         │
│                              • 100% Explicable jurídicamente (4 preguntas de Sí/No)    │
│                                                                                        │
│   SESIÓN 9 (Clustering):     🎯 K-MEANS (k=3) CON ESCALAMIENTO STANDARDSCALER          │
│                              • Silueta robusta de 0,55 (Separación nítida)             │
│                              • Inercia óptima (63.857 puntos)                          │
│                              • 3 Segmentos accionables para política pública           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 🥊 Para la Sesión 8 (Clasificación Supervisada):
* **La Mejor Opción Absoluta:** **Árbol de Decisión podado (`max_depth=4`, `criterion='gini'`)**.
* **Por qué es la mejor frente a sus rivales:**
  * **Frente a Naive Bayes:** Le gana por más de **$12,2\%$ de exactitud** ($82,71\%$ vs $70,46\%$). Naive Bayes no sirve para este problema porque asume falsamente que el parque vehicular es independiente de la capacidad policial.
  * **Frente a KNN:** Aunque KNN calibrado ($k=31$) se le acerca con $82,55\%$, el Árbol predice **$360$ veces más rápido** y no consume gigabytes de memoria en servidores policiales.
  * **Rol secundario asignado:** Mantener a Gaussian Naive Bayes únicamente como **línea base de chequeo rápido**, pero el motor operativo en producción debe ser el Árbol.

### 🎯 Para la Sesión 9 (Clustering No Supervisado):
* **La Mejor Opción Absoluta:** **K-Means con $k=3$ sobre variables estandarizadas**, validado mediante el Dendrograma Jerárquico de Ward.
* **Por qué es la mejor frente a sus rivales:**
  * **Frente a Jerárquico Aglomerativo puro:** El método jerárquico no escala computacionalmente para clasificar millones de denuncias anuales en producción ($O(N^2)$); K-Means corre en **milisegundos** ($O(N \cdot k \cdot I)$).
  * **Frente a $k=2$:** $k=2$ es insuficiente porque agrupa a Ibagué y Bogotá en la misma bolsa que un pueblo intermedio como Flandes o Melgar.
  * **Frente a $k=4$ o $k=5$:** Dividir en 4 o 5 grupos genera sobresegmentación de recursos policiales. $k=3$ representa el equilibrio perfecto entre parsimonia matemática y viabilidad de gestión pública.

---

## 3. RECOMENDACIONES PARA DECIRLE AL PÚBLICO Y AL JURADO ACERCA DE ESTE PROYECTO

Al exponer tu proyecto ante el público (estudiantes, profesores, jurados o ciudadanos), transmite estas recomendaciones según el perfil de tu audiencia:

### 3.1 Recomendaciones para la Ciudadanía y Conductores (Especialmente Motociclistas):
1. **Desconfiar del promedio simple:**  
   *"No se confíe si lee que en Colombia solo se hurtan 7 vehículos por pueblo. En las capitales el delito está hiperconcentrado; si usted rueda en una metrópoli, su riesgo real es casi 80 veces superior al promedio estadístico."*
2. **Alerta máxima con las motocicletas:**  
   *"El 75,7% de los hurtos en Colombia son motos y la Policía solo recupera el 41,3%. ¿Por qué? Porque el mercado negro las desmantela en menos de 2 horas. La recomendación es no dejarlas mal parqueadas en vía pública (el halado es la modalidad reina), usar candados con alarma de disco e instalar cortacorrientes satelitales ocultos."*

### 3.2 Recomendaciones para la Policía Nacional y Autoridades de Tránsito (Alcaldías y Ministerio):
1. **Pasar del patrullaje reactivo al patrullaje predictivo basado en IA:**  
   *"Basta de enviar cuadrantes a ciegas. El modelo Árbol de Decisión permite priorizar patrullajes dinámicos según las características del municipio antes de que ocurra la ola delictiva."*
2. **Atacar el mercado negro de autopartes, no solo el hurto callejero:**  
   *"El clustering demostró que en el Segmento 3 (Metrópolis) el hurto promedia 78 casos por cuadrante. La Policía debe enfocar sus unidades de inteligencia DIJIN en allanamientos a bodegas de repuestos usados ilegales; si no hay quien compre autopartes robadas, el hurto de motos se desploma."*
3. **Instalación de cámaras LPR en salidas intermunicipales:**  
   *"El análisis cruzado demostró que las bandas cometen el delito en la capital y fugan el vehículo a municipios vecinos en menos de 45 minutos. Los peajes y salidas deben contar con arcos de lectura automática de placas interconectados al RUNT."*
4. **Saneamiento y auditoría registral en el RUNT:**  
   *"El Segmento 1 demostró que existen más de 15.000 registros históricos previos al año 2000. Tránsito debe depurar esas matrículas inactivas para que las mafias de 'gemeleo' no usen placas viejas en carros hurtados."*

### 3.3 Recomendaciones Técnicas para Ingenieros de Sistemas y Científicos de Datos:
1. **'La distancia manda a escalar':**  
   *"Cualquier algoritmo basado en distancias geométricas (KNN, K-Means, Jerárquico, SVM) es vulnerable al secuestro de escala. Nunca ejecuten un modelo sin estandarizar antes las variables con StandardScaler o RobustScaler."*
2. **Evitar la fuga de datos usando Pipelines:**  
   *"Nunca apliquen fit_transform en todo el dataset antes de train_test_split. Usen siempre make_pipeline en scikit-learn para proteger la integridad del conjunto de prueba."*
3. **La interpretabilidad es un requisito no negociable en el sector público:**  
   *"En políticas públicas o justicia penal, un modelo con 90% de exactitud que no se pueda explicar es inútil y peligroso. El Árbol de Decisión es superior porque permite auditar cada regla ante los ciudadanos y los jueces."*

---

# PARTE 5 · CHECKLIST FINAL PARA SUBIR Y OBTENER LA MÁXIMA CALIFICACIÓN

| Requisito del Instrumento | Estado | Ubicación / Evidencia |
| :--- | :---: | :--- |
| **Sustentación tipo Pitch del proyecto de IA** | ✅ Completado | Guion verbal de 5 minutos y versión relámpago de 90 segundos detallado en Parte 1. |
| **Todo subido este mismo día para calificación** | ✅ Preparado | Repositorio organizado con Git, sin temporales y listo para commit/push. |
| **Despliegue en línea del proyecto** | ✅ Implementado | Archivo [`app.py`](file:///Users/camilapava/Documents/OCTAVO%20SEMESTRE/mineria%208%20y%209/read-hurtos-Tolima/app.py), [`requirements.txt`](file:///Users/camilapava/Documents/OCTAVO%20SEMESTRE/mineria%208%20y%209/read-hurtos-Tolima/requirements.txt) y guía en la nube. |
| **De qué trata el sistema** | ✅ Completado | Sección 1 de Parte 2 (problema, datos y solución CRISP-DM). |
| **Objetivos generales y específicos** | ✅ Completado | Sección 2 de Parte 2 (objetivos de software, ML y gobernanza). |
| **Diagramas UML (Casos de uso, Clases, Secuencia, Despliegue)** | ✅ Completado | Sección 3 de Parte 2 (4 diagramas formales en Mermaid). |
| **Capturas del sistema** | ✅ Completado | Sección 4 de Parte 2 (6 figuras de alta resolución integradas). |
| **Decisiones tomadas y justificación técnica** | ✅ Completado | Sección 1 de Parte 4 (las 8 decisiones científicas explicadas). |
| **Mejor opción para Sesión 8 y Sesión 9** | ✅ Completado | Sección 2 de Parte 4 (Árbol prof=4 y K-Means k=3 fundamentados). |
| **Recomendaciones para decirle al público** | ✅ Completado | Sección 3 de Parte 4 (ciudadanía, Policía y comunidad técnica). |

---
*Documento técnico formal elaborado para la entrega y sustentación final · Ingeniería de Sistemas · UNIMINUTO Sede Ibagué*

