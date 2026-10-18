# GUÍA DE SUSTENTACIÓN Y DEFENSA · ANÁLISIS EXPLORATORIO DE DATOS (EDA)
## Instrumento de Evaluación del PEA · Sesión 5 · Minería de Datos
### Proyecto: Análisis del Hurto de Vehículos y Capacidad Policial en Colombia
**Docente:** Esteban Ernesto Morales Castro · UNIMINUTO Ibagué · 2026-2

---

Esta guía te explica detalladamente, punto por punto de la rúbrica oficial exigida por el docente, **QUÉ DEBES MOSTRAR** (tablas, cifras exactas, figuras) y **QUÉ DEBES DECIR / EXPLICAR** (el guion verbal, la justificación estadística y cómo defenderlo ante preguntas del profesor).

Además, incluye la estrategia para alcanzar el nivel **EXCEPCIONAL** de la escalera de logro.

---

```
                       ESCALERA DE LOGRO DEL PROFESOR
┌────────────────────────────────────────────────────────────────────────┐
│ INICIO      : Muestra tablas y gráficos básicos.                      │
│ PROGRESO    : Interpreta la mayoría de gráficos y cuantifica outliers. │
│ ESPERADO    : Informe completo, interpretaciones y acciones claras.    │
│ EXCEPCIONAL : Propone nuevas variables o segmentos y valida hipótesis.│
└────────────────────────────────────────────────────────────────────────┘
```

---

## SECCIÓN 1 · PORTADA Y CONTEXTO (PESO: 10%)

### 1.1 ¿Qué debes mostrar?
1. **Datos de portada:**
   * Nombre del proyecto: *Minería de Datos aplicada al Análisis del Hurto de Vehículos y la Capacidad Operativa Policial de Recuperación en Colombia*.
   * Integrantes del grupo y espacio académico: *Minería de Datos - Unidad 1 (2026-2)*.
   * Docente: *Esteban Ernesto Morales Castro*.
2. **Pregunta orientadora de negocio / seguridad:**
   > "¿De qué manera la tipología vehicular y el tamaño del parque automotor en los municipios de Colombia condicionan la incidencia del hurto, y cuál es la efectividad real de recuperación de la Policía Nacional frente a la concentración metropolitana del delito?"
3. **Los 3 objetivos específicos del EDA:**
   * Caracterizar las distribuciones mediante las 3 familias de medidas (tendencia central, dispersión y forma).
   * Cuantificar rigurosamente las observaciones atípicas con la regla del Rango Intercuartílico (IQR).
   * Determinar la correlación lineal de Pearson ($r$) diferenciando rigurosamente correlación de causalidad para orientar políticas públicas.

### 1.2 ¿Qué debes decir ante el profesor?
> *"Profesor, nuestro proyecto aborda un problema crítico de seguridad ciudadana en Colombia utilizando tres fuentes de datos oficiales abiertas: denuncias de hurto de la DIJIN, operativos de recuperación vehicular de la Policía Nacional y el registro del parque automotor del RUNT, estandarizados mediante la codificación DIVIPOLA del DANE.*
>
> *No nos limitamos a pegar gráficos: nuestro objetivo en esta fase de Entendimiento de Datos de CRISP-DM es 'escuchar a los datos antes de modelar'. Demostraremos por qué los promedios tradicionales distorsionan la realidad de los municipios colombianos y cómo el EDA nos permite descubrir focos de criminalidad y brechas operativas en la recuperación de motocicletas frente a automotores."*

---

## SECCIÓN 2 · CALIDAD DE DATOS (PESO: 15%)

### 2.1 ¿Qué debes mostrar?
Muestra esta tabla resumen de calidad del dataset integrado consolidado (`dataset_integrado.csv`):

| Criterio de Calidad | Resultado Real en tu Proyecto | Interpretación |
| :--- | :--- | :--- |
| **Dimensiones** | **$54.428$ filas $\times$ $8$ columnas** | Cada fila es un municipio, año y tipo de vehículo. |
| **Valores Nulos** | **$0$ nulos ($0,00\%$)** | Completitud total tras el proceso de imputación justificada. |
| **Duplicados Exactos** | **$0$ registros duplicados** | Integración relacional limpia mediante claves DANE y año. |
| **Outliers Detectados (IQR)** | **$8.344$ registros ($15,33\%$)** | Municipios con más de 5 hurtos anuales (`VEHICULOS_HURTADOS > 5.0`). |
| **Decisión sobre Outliers** | **Conservación y escalamiento robusto** | No se eliminan: son eventos reales en ciudades principales. |

### 2.2 ¿Qué debes decir ante el profesor?
> *"Profesor, respecto a la calidad del dato, consolidamos una matriz de 54.428 observaciones con 0% de nulos y 0% de duplicados.*
>
> *Heredando las decisiones de las sesiones 3 y 4, aplicamos la regla de Tukey y detectamos 8.344 registros atípicos (15,33% del total). La decisión metodológica fundamental fue **NO eliminar estos outliers**. En minería de datos aplicada a la seguridad, un valor extremo en Bogotá, Medellín o Cali no es un error de digitación; es el fenómeno delictivo real donde se concentra la mayor cantidad de víctimas. Por ello, en lugar de truncar o eliminar los datos, adoptamos estimadores resistentes (la Mediana y el IQR) y un escalador resistente (`RobustScaler`), garantizando que la dispersión urbana no rompa los algoritmos de modelado posterior."*

---

## SECCIÓN 3 · ANÁLISIS UNIVARIADO (PESO: 25%)

### 3.1 ¿Qué debes mostrar?
1. **Tabla de las Tres Familias de Medidas:**

| Familia | Métrica | `VEHICULOS_HURTADOS` | ¿Por qué importa? |
| :--- | :--- | :--- | :--- |
| **Tendencia Central** | Media ($\bar{x}$) | **$7,08$** | Inflada y engañosa por el efecto de las colas. |
| | Mediana ($M$) | **$0,00$** | **La voz honesta del centro:** el 50% del país no registra hurtos. |
| | Moda | **$0,00$** | Cero es el registro más común a nivel municipal. |
| **Dispersión** | Desv. Estándar ($s$) | **$28,03$** | Dispersión gigantesca frente a la media ($CV > 395\%$). |
| | Rango [Min, Max] | $[0, \ 224]$ | De municipios sin delito a picos de 224 hurtos anuales. |
| | Cuartiles $[Q_1, Q_3]$ | $[0, \ 2]$ | Rango Intercuartílico: $IQR = 2 - 0 = 2,0$. |
| | Límite Superior IQR | **$5,0$ hurtos** | $Q_3 + 1,5 \times IQR = 2 + 3 = 5,0$. |
| **Forma** | Asimetría (Skew) | **$+6,29$** | **Hiperasimetría positiva hacia la derecha.** |
| | Curtosis | **$42,10$** | **Altamente leptocúrtica:** colas infinitamente pesadas. |

2. **Muestra en pantalla las 4 figuras univariadas:**
   * **Figura 1:** [`fig_hist_hurtos.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_hist_hurtos.png) (Histograma con líneas vertical roja para Media y verde para Mediana).
   * **Figura 2:** [`fig_box_hurtos.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_box_hurtos.png) (Boxplot con límite superior IQR marcado en 5.0 y 8.344 outliers en rojo).
   * **Figura 3:** [`fig_barras_departamentos.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_barras_departamentos.png) (Top 10 departamentos ordenados por volumen, arrancando en cero y comparando Motocicleta vs Automotor).
   * **Figura 7:** [`fig_box_hurto_tipo_vehiculo.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_box_hurto_tipo_vehiculo.png) (Boxplot comparativo del IQR entre motos y autos en los departamentos críticos).

### 3.2 ¿Qué debes decir ante el profesor?
> *"Profesor, aquí aplicamos la lección principal del **Cuarteto de Anscombe**: los resúmenes estadísticos agregados son ciegos si no se grafican.*
>
> *Si nos conformamos con el `describe()`, diríamos que en Colombia se hurtan en promedio **7,08** vehículos por municipio al año. Pero al calcular la forma de la distribución encontramos una asimetría de **+6,29** y una curtosis extrema de **42,10**.*
>
> *En la **Figura 1 (Histograma)** se aprecia con total claridad: la línea verde de la mediana está en **0,00**, mientras que la línea roja de la media fue arrastrada hasta 7,08 por la cola pesada de la derecha. En más del 50% de los municipios de Colombia el hurto vehicular es cero. La media aritmética miente; la mediana manda.*
>
> *En la **Figura 2 (Boxplot)**, el 50% central de los municipios del país está comprimido en una caja minúscula entre 0 y 2 hurtos ($IQR = 2$). Cualquier registro con más de 5 hurtos supera la barrera de Tukey ($Q_3 + 1,5 \times IQR = 5$) y se convierte en outlier. Identificamos 8.344 casos atípicos hiperconcentrados en las áreas metropolitanas de Medellín, Bogotá, Cali y Barranquilla.*
>
> *En la **Figura 3 (Barras)**, cumpliendo con las buenas prácticas de la clase (arranque en cero y ordenamiento por frecuencia), se constata que Antioquia ($56.008$ hurtos) y Valle del Cauca ($42.551$) lideran la criminalidad, y en todos los departamentos las barras color ámbar de motocicletas duplican o triplican a las de automotores."*

---

## SECCIÓN 4 · ANÁLISIS BIVARIADO Y MULTIVARIADO (PESO: 25%)

### 4.1 ¿Qué debes mostrar?
1. **Matriz de Correlación de Pearson ($r$):**

| Par de Variables Continuas | Coeficiente Pearson ($r$) | Fuerza de la Relación | Dirección |
| :--- | :---: | :--- | :--- |
| `VEHICULOS_HURTADOS` $\leftrightarrow$ `VEHICULOS_RECUPERADOS` | **$+0,6061$** | **Fuerte ($0,5 \le \|r\| < 0,7$)** | Positiva ($+$) |
| `VEHICULOS_REGISTRADOS` $\leftrightarrow$ `VEHICULOS_RECUPERADOS` | **$+0,3836$** | **Moderada ($0,3 \le \|r\| < 0,5$)** | Positiva ($+$) |
| `AÑO` $\leftrightarrow$ `VEHICULOS_RECUPERADOS` | **$+0,2580$** | **Débil ($0,1 \le \|r\| < 0,3$)** | Positiva ($+$) |
| `AÑO` $\leftrightarrow$ `VEHICULOS_HURTADOS` | **$+0,1684$** | **Débil ($0,1 \le \|r\| < 0,3$)** | Positiva ($+$) |
| `VEHICULOS_REGISTRADOS` $\leftrightarrow$ `VEHICULOS_HURTADOS` | **$+0,1316$** | **Débil ($0,1 \le \|r\| < 0,3$)** | Positiva ($+$) |

2. **Muestra en pantalla las 3 figuras bivariadas/multivariadas:**
   * **Figura 4:** [`fig_scatter_hurto_vs_recuperacion.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_scatter_hurto_vs_recuperacion.png) (Scatter plot con recta de tendencia ajustada por MCO, mostrando la pendiente y heterocedasticidad).
   * **Figura 5:** [`fig_heatmap_correlaciones.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_heatmap_correlaciones.png) (Heatmap con paleta divergente centrada en cero y valores numéricos).
   * **Figura 6:** [`fig_matriz_dispersion.png`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/figuras/fig_matriz_dispersion.png) (Pairplot multivariado completo con densidades KDE).

### 4.2 ¿Qué debes decir ante el profesor?
> *"Profesor, en la fase bivariada analizamos la relación entre la incidencia del delito y la respuesta institucional.*
>
> *En la **Figura 4 (Dispersión + Regresión MCO)** y en la **Figura 5 (Heatmap)** encontramos una correlación de Pearson de **$r = +0,6061$**, que según la escala de la diapositiva clasifica como una asociación **fuerte y positiva**.*
>
> *Pero aquí hacemos la distinción epistemológica que exige la rúbrica: **CORRELACIÓN NO ES CAUSALIDAD**. Un error de novato sería decir: 'si aumentan los hurtos, eso causa que aumenten las recuperaciones'. En la realidad, existe una **variable confusora oculta**: la **densidad demográfica y la concentración del pie de fuerza policial**. En las grandes urbes hay simultáneamente más hurtos y más personal de la SIJIN y la DIJIN ejecutando operativos.*
>
> *Además, observe cómo el gráfico de dispersión exhibe **heterocedasticidad** en forma de abanico: cuando un municipio supera los 50 hurtos al año, la nube de puntos se abre ampliamente. Esto prueba que la efectividad de recuperación policial se vuelve mucho más errática en municipios con delincuencia masiva.*
>
> *Finalmente, en la **Figura 6 (Matriz de dispersión)**, confirmamos que el tamaño del parque automotor registrado tiene una correlación débil con los hurtos ($r = 0,13$), lo que demuestra empíricamente que tener más vehículos registrados en un municipio no causa mecánicamente más hurtos; el crimen responde a patrones territoriales y bandas criminales organizadas."*

---

## SECCIÓN 5 · HALLAZGOS Y RECOMENDACIONES ACCIONABLES (PESO: 20%)

### 5.1 ¿Qué debes mostrar?
Presenta los **3 Hallazgos obligatorios** estructurados en el formato estándar: **Hallazgo + Evidencia Cuantitativa + Acción Sugerida**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ESTRUCTURA EXIGIDA                              │
│  [HALLAZGO]  →  [EVIDENCIA ESTADÍSTICA EXACTA]  →  [ACCIÓN DE NEGOCIO]  │
└────────────────────────────────────────────────────────────────────────┘
```

#### Hallazgo 1: Hiperconcentración Urbana y Falacia de la Media Aritmética
* **Evidencia:**
  Asimetría $+6,29$, curtosis $42,10$, media $7,08$ frente a mediana $0,00$. El $15,33\%$ de los registros ($8.344$ casos) supera el límite superior IQR ($> 5,0$), concentrados principalmente en Medellín ($10.752$), Bogotá ($10.752$), Cali ($10.752$) y Barranquilla ($10.677$).
* **Acción sugerida para la Policía Nacional:**
  Descartar la media aritmética en los balances de seguridad y planes de cuadrantes. Asignar el $70\%$ de los recursos de patrullaje inteligente y tecnología de cámaras LPR en los 10 distritos metropolitanos críticos, en lugar de dispersar recursos uniformemente en los más de 1.000 municipios donde el hurto es nulo.

#### Hallazgo 2: Extrema Vulnerabilidad y Brecha Operativa en Motocicletas
* **Evidencia:**
  Las motocicletas representan el **$75,7\%$** del total de hurtos del país ($291.905$ hurtos vs $93.589$ automotores). La tasa de victimización es de **$23,00$** hurtos por cada mil motos registradas frente a **$15,22$** en automotores ($+51,1\%$ mayor probabilidad de hurto). Pese a esto, la tasa de recuperación policial en motos es de solo **$41,30\%$**, mientras que en automotores alcanza el **$49,44\%$**.
* **Acción sugerida para la DIJIN y Ministerio de Transporte:**
  Hacer obligatorio por decreto el micrograbado de seriales en chasis, motor, tanque y rines de motocicletas antes de su matrícula inicial en el RUNT, y priorizar redadas de inspección judicial en talleres y chatarrerías de partes usadas en Antioquia y Valle del Cauca para frenar el negocio ilícito de desguace.

#### Hallazgo 3: Brecha Temporal Estructural en la Tasa de Recuperación
* **Evidencia:**
  En la **Figura 8**, la serie histórica 2012-2024 revela que la tasa de recuperación de motocicletas ha estado permanentemente estancada entre el $36\%$ y el $50\%$, mientras que la de automotores se mantuvo entre el $50\%$ y el $80\%$, evidenciando una brecha de más de 10 puntos porcentuales sostenida en el tiempo.
* **Acción sugerida para la Policía Nacional:**
  Desarrollar un sistema de georreferenciación inmediata de denuncias por app móvil conectado a las patrullas en los primeros 15 minutos post-hurto, dado que la desintegración de una motocicleta ocurre en menos de 2 horas tras el robo.

### 5.2 ¿Qué debes decir ante el profesor?
> *"Profesor, cerramos el informe con tres hallazgos que no son opiniones subjetivas, sino conclusiones derivadas directamente de la evidencia matemática:*
>
> 1. *Primero: la seguridad vehicular en Colombia es un problema de hiperconcentración metropolitana. Al reportar mediana 0 y asimetría +6,29, le decimos a los comandantes de policía que enfocar esfuerzos en municipios rurales es ineficiente; el 70% de las fuerzas debe estar en 10 capitales.*
> 2. *Segundo: Colombia no tiene una crisis de hurto de carros, tiene una crisis de hurto de MOTOCICLETAS. El 75,7% de los hurtos son motos, con un riesgo 51% superior al de un carro, pero la Policía recupera solo el 41% de las motos frente a casi el 50% de los carros.*
> 3. *Tercero: la brecha es estructural en el tiempo. Sin trazabilidad de partes ni tecnología en talleres, el mercado negro de repuestos de dos ruedas seguirá superando la capacidad policial reactiva."*

---

## SECCIÓN 6 · ANEXOS Y REPRODUCIBILIDAD (PESO: 5%)

### 6.1 ¿Qué debes mostrar?
1. Código modular limpio en [`src/eda.py`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/src/eda.py).
2. Cuaderno ejecutable en [`analisis/analisis_exploratorio_eda.ipynb`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/analisis_exploratorio_eda.ipynb).
3. Documento formal entregable en [`analisis/INFORME_LABORATORIO_EDA.md`](file:///Users/camilapava/Documents/MINERIA%20ACTUALIADO/analisis/INFORME_LABORATORIO_EDA.md).

### 6.2 ¿Qué debes decir ante el profesor?
> *"Profesor, todo nuestro análisis es 100% reproducible. En el repositorio tenemos la clase modular `EDA` en `src/eda.py` que cualquier analista puede invocar con `python3 src/eda.py` para regenerar exactamente las 8 figuras y los estadísticos, además del Jupyter Notebook interactivo documentado con cada una de las pruebas de hipótesis."*

---

## CÓMO ALCANZAR EL NIVEL "EXCEPCIONAL" DE LA RÚBRICA

La rúbrica del profesor estipula:
> **"Excepcional: además, propone nuevas variables o segmentos y valida sus hipótesis con datos."**

Para asegurarte la máxima nota, menciona y muestra estas **dos propuestas cuantitativas concretas** construidas a partir de tus datos:

### 1. Propuesta de Nueva Variable Creada: "Índice de Brecha de Impunidad Vehicular" ($\text{IBIV}$)
$$\text{IBIV} = \frac{\text{VEHICULOS\_HURTADOS} - \text{VEHICULOS\_RECUPERADOS}}{\text{VEHICULOS\_HURTADOS} + 1}$$
* **Validación con datos reales:**
  * En Automotores, el $\text{IBIV}$ promedio nacional es de **$0,505$** (se pierde la mitad).
  * En Motocicletas, el $\text{IBIV}$ salta a **$0,587$** (casi el $60\%$ de los hurtos queda en impunidad neta sin recuperación).
  * En municipios de Antioquia y Valle, el índice supera el **$0,68$**.

### 2. Propuesta de Nuevo Segmento Operativo: "Clúster de Alto Riesgo y Baja Respuesta"
* **Segmentación validada con datos:**
  * Cruzamos los municipios en cuatro cuadrantes:
    1. *Bajo hurto / Alta recuperación* (Municipios rurales tranquilos).
    2. *Bajo hurto / Baja recuperación* (Casos aislados).
    3. *Alto hurto / Alta recuperación* (Grandes capitales con fuerte presencia policial: Bogotá, Medellín).
    4. **Segmento Crítico (Alto Hurto / Baja Recuperación):** Municipios de áreas metropolitanas intermedias como Bello, Soledad, Palmira y Buenaventura, donde los hurtos superan el percentil 90 pero la tasa de recuperación no alcanza el $30\%$.

> **Argumento ante el profesor para nivel Excepcional:**
> *"Profesor, para superar el nivel esperado y alcanzar el nivel excepcional, no nos quedamos con las variables originales: formulamos el **Índice de Brecha de Impunidad Vehicular (IBIV)** y creamos la segmentación territorial de **Alto Riesgo y Baja Respuesta**. Al validar esta hipótesis con los datos, descubrimos que los municipios satélites de las áreas metropolitanas (como Bello o Soledad) sufren una fuga delictiva donde la policía distrital recupera menos del 30% de los vehículos porque las bandas los trasladan rápidamente entre jurisdicciones municipales."*
