# Minería de Datos - Análisis del Hurto de Vehículos y Capacidad Policial en Colombia

## Descripción

Proyecto de minería de datos enfocado en el análisis del hurto de automotores y motocicletas y la capacidad policial de recuperación en Colombia, integrando información del crecimiento del parque automotor (RUNT), denuncias de hurto (Policía Nacional / DIJIN), recuperaciones vehiculares y la división político-administrativa (DANE / DIVIPOLA) para realizar procesos de diagnóstico de calidad, integración relacional, transformación, escalamiento y reducción de datos mediante PCA.

## Objetivo

Analizar la relación entre el parque automotor registrado, la incidencia de hurtos y la efectividad operativa de recuperación en los municipios colombianos, aplicando la metodología CRISP-DM y técnicas de minería de datos para encontrar patrones críticos de seguridad y reducir la dimensionalidad de la información.

## Datasets

### 1. Hurto de Vehículos

Dataset obtenido de Datos Abiertos Colombia (Policía Nacional de Colombia / DIJIN).

Contiene **386.071 registros y 8 columnas**:

* `FECHA HECHO`
* `COD_DEPTO`
* `DEPARTAMENTO`
* `COD_MUNI`
* `MUNICIPIO`
* `TIPO DELITO`
* `ZONA`
* `CANTIDAD`

### 2. Recuperación de Vehículos

Dataset obtenido de Datos Abiertos Colombia (Policía Nacional de Colombia / DIJIN).

Contiene **286.258 registros y 6 columnas**:

* `DEPARTAMENTO`
* `MUNICIPIO`
* `CODIGO DANE`
* `CLASE BIEN`
* `FECHA HECHO`
* `CANTIDAD`

### 3. Crecimiento del Parque Automotor

Dataset obtenido de Datos Abiertos Colombia (RUNT / Ministerio de Transporte).

Contiene **191.640 registros y 9 columnas**:

* `NOMBRE_DEPARTAMENTO`
* `NOMBRE_MUNICIPIO`
* `NOMBRE_SERVICIO`
* `ESTADO_DEL_VEHICULO`
* `NOMBRE_DE_LA_CLASE`
* `FECHA DE REGISTRO`
* `CANTIDAD`
* `MES DE PUBLICACION`
* `AÑO DE PUBLICACIÓN`

### 4. Municipios DANE

Diccionario oficial DIVIPOLA del DANE que contiene **1.153 municipios y códigos departamentales a 5 dígitos**.

## Integración de los datos

Las fuentes se procesan, limpian y relacionan mediante el código municipal DANE, el año del evento y la tipología vehicular canónica (Motocicleta vs Automotor), consolidando el conjunto de datos unificado:

`dataset/dataset_integrado.csv` y `dataset/dataset_integrado.xlsx`

El dataset integrado contiene **54.428 registros y 8 variables** principales:
* `AÑO`
* `CODIGO_DANE_MUNICIPIO`
* `DEPARTAMENTO`
* `MUNICIPIO`
* `TIPO_VEHICULO`
* `VEHICULOS_REGISTRADOS`
* `VEHICULOS_HURTADOS`
* `VEHICULOS_RECUPERADOS`

## Transformación y reducción

El proceso se encuentra organizado en la clase:

`src/transformacion.py`

Se realizan:

* Tratamiento de valores nulos y atípicos (imputación justificada y winsorización en percentil 99).
* Demostración empírica del sesgo en la distancia euclídea por variables no estandarizadas ("El Gancho").
* Codificación de variables categóricas nominales mediante One-Hot Encoding.
* Comparación de métodos de escalamiento (`MinMaxScaler`, `StandardScaler`, `RobustScaler`).
* Escalamiento mediante `RobustScaler` para garantizar resistencia frente a grandes áreas metropolitanas con alta dispersión.
* Discretización de variables continuas (`KBinsDiscretizer`).
* Reducción de dimensionalidad mediante PCA.

El proceso se documenta principalmente en:

`analisis/transformacion_escalabilidad.ipynb`

El análisis general y limpieza del proyecto se encuentra en:

`analisis/analisis_datos.ipynb`

## PCA

Se seleccionaron las componentes principales sobre las variables continuas estandarizadas, conservando aproximadamente entre el **80.40 % y el 100 % de la varianza explicada**.

El resultado se guarda en:

`dataset/dataset_reducido.csv`

El dataset reducido contiene **54.428 registros y 9 columnas**:

* `AÑO`
* `CODIGO_DANE_MUNICIPIO`
* `DEPARTAMENTO`
* `MUNICIPIO`
* `TIPO_VEHICULO`
* `PC1`
* `PC2`
* `PC3`
* `VEHICULOS_HURTADOS`

## Análisis Exploratorio de Datos (EDA) · Sesión 5

El análisis exploratorio formal se implementa de manera modular en:

`src/eda.py` y se documenta en `analisis/analisis_exploratorio_eda.ipynb` e `analisis/INFORME_LABORATORIO_EDA.md`.

Se evalúan:

* **Tres familias de medidas estadísticas**:
  * *Tendencia central*: Media ($\bar{x} = 7.08$), Mediana ($M = 0.00$), Moda ($0.00$).
  * *Dispersión*: Desviación estándar ($s = 28.03$), Rango $[0, 224]$, Cuartiles $[Q_1=0, Q_3=2]$ e $IQR = 2.0$.
  * *Forma*: Asimetría de Fisher-Pearson ($+6.29$, hiperasimetría a la derecha) y Curtosis ($42.10$, fuertemente leptocúrtica).
* **Demostración de Anscombe en la criminalidad**: Por qué el `describe()` oculta la realidad; la media de $7.08$ hurtos está inflada por capitales metropolitanas, mientras que más del $50\%$ de los municipios tiene $0$ hurtos (la mediana manda).
* **Cuantificación formal de atípicos (Regla IQR)**: Identificación de $8.344$ registros ($15.33\%$) por encima de $Q_3 + 1.5 \times IQR = 5.0$, concentrados en Medellín, Bogotá D.C., Cali y Barranquilla.
* **Correlación de Pearson ($r$)**: Asociación fuerte y positiva ($r = 0.6061$) entre hurtos y recuperaciones policiales, distinguiendo co-ocurrencia operativa de causalidad.
* **Informe oficial de laboratorio**: Documento con las 6 secciones exigidas por el instrumento del PEA para el Avance 1.

## Visualizaciones (Galería Completa EDA)

Las figuras generadas en alta resolución ($150$ DPI) bajo estándares de honestidad visual (títulos-hallazgo, unidades explícitas, barras desde cero, sin gráficos 3D) se encuentran en `analisis/figuras/`:

1. `fig_hist_hurtos.png`: Histograma con líneas de media ($\bar{x}=7.08$) y mediana ($M=0.00$), exhibiendo la asimetría positiva.
2. `fig_box_hurtos.png`: Boxplot con límite superior IQR ($5.0$) y los $8.344$ outliers metropolitanos.
3. `fig_barras_departamentos.png`: Top 10 departamentos con mayor criminalidad desglosado por tipología (Motocicletas vs Automotores).
4. `fig_scatter_hurto_vs_recuperacion.png`: Diagrama de dispersión con recta de tendencia ajustada por MCO (Pearson $r=0.61$).
5. `fig_heatmap_correlaciones.png`: Mapa de calor de la matriz de correlaciones de Pearson entre las variables continuas.
6. `fig_matriz_dispersion.png`: Matriz de dispersión multivariada (Pairplot) con curvas de densidad KDE en diagonal.
7. `fig_box_hurto_tipo_vehiculo.png`: Comparación del rango intercuartílico en departamentos críticos (Motocicletas triplican la dispersión).
8. `fig_tendencia_temporal_tasa_recuperacion.png`: Tendencia multianual que revela la brecha estructural de efectividad policial en motocicletas ($41.3\%$ vs $49.4\%$ en autos).

## Clasificación II · Sesión 8 (Torneo: Árbol vs Naive Bayes vs KNN)

La Sesión 8 se encuentra implementada en:
* Módulo modular: `src/clasificacion.py`
* Cuaderno interactivo reproducible: `analisis/sesion8_clasificacion_nb_knn.ipynb`
* Documento técnico y guion de sustentación: `analisis/TORNEO_CLASIFICACION_SESION8.md`

Principales resultados del torneo sobre $54.428$ observaciones (partición 75% train / 25% test con semilla 42 y estratificación):
* **Árbol de Decisión (prof=4):** **Ganador del torneo con 82,71% de Accuracy y 82,75% de F1-Score**. Inferencia instantánea ($0,0015$ s) y máxima interpretabilidad jurídica en 4 reglas.
* **Gaussian Naive Bayes (GaussianNB):** Entrenamiento ultrarrápido ($0,0036$ s), pero exactitud de **70,46%** por doble conteo de evidencia derivado de la correlación entre parque y recuperaciones.
* **KNN (k=5) con Pipeline StandardScaler:** **81,13% de Accuracy**. Demostración empírica de que sin escalamiento decae a **80,31%** (el parque automotor secuestra la distancia euclidiana).
* **Exploración de $k$:** Se demostró sobreajuste en $k=1$ (brecha de $9,15\%$), equilibrio óptimo en $k=31$ ($82,55\%$) y subajuste con $k=51$.
* **Figuras generadas:** `fig_sesion8_torneo_comparacion.png`, `fig_sesion8_efecto_k_knn.png` y `fig_sesion8_matrices_confusion.png`.

## Clustering · Sesión 9 (Segmentación No Supervisada: K-Means y Jerárquico)

La Sesión 9 se encuentra implementada en:
* Módulo modular: `src/clustering.py`
* Cuaderno interactivo reproducible: `analisis/sesion9_clustering_kmeans_jerarquico.ipynb`
* Documento técnico y guion de sustentación: `analisis/SEGMENTACION_CLUSTERING_SESION9.md`
* Dataset enriquecido: `dataset/dataset_con_clusters.csv`

Metodología y resultados de la segmentación no supervisada:
* **Pureza No Supervisada:** Se excluyó `VEHICULOS_HURTADOS` de la matriz $X$, agrupando únicamente sobre variables estructurales escaladas (`AÑO`, `VEHICULOS_REGISTRADOS`, `VEHICULOS_RECUPERADOS`).
* **Selección de $k$:** Evaluación de $k \in [2..8]$ mediante Método del Codo y Silueta. Se seleccionó **$k=3$** por el quiebre de inercia ($103.591 \rightarrow 63.857$), silueta robusta ($0,545$) y viabilidad de 3 planes de seguridad diferenciados.
* **Los 3 Segmentos Descubiertos y Nombrados:**
  1. *S1 · Archivo Histórico Premetropolitano (Inmune):* $28,4\%$ de casos, año promedio 1974,9, hurtos nulos (era pre-digital). Acción: saneamiento registral en el RUNT.
  2. *S2 · Cabeceras Municipales con Delincuencia Contenida:* $67,3\%$ de casos, año medio 2013,7, $5,56$ hurtos promedio y $43,7\%$ de recuperación. Acción: cuadrantes preventivos y puestos de control.
  3. *S3 · Grandes Focos Metropolitanos de Hurto Masivo:* $4,3\%$ de casos (Bogotá, Medellín, Cali, Ibagué), $4.634$ vehículos de parque medio, $78,29$ hurtos y $79,6\%$ de tasa activa. Acción: inteligencia DIJIN/SIPOL contra talleres de deshuese y cámaras LPR.
* **Clustering Jerárquico Aglomerativo (Ward):** Dendrograma sobre muestra representativa de 60 municipios con corte horizontal a altura $6,3$, validando científicamente los 3 grupos.
* **Figuras generadas:** `fig_sesion9_metodo_codo_silueta.png`, `fig_sesion9_perfilamiento_clusters.png` y `fig_sesion9_dendrograma_muestra60.png`.

## Estructura del proyecto

```text
mineria-datos-accidentes-v2 / hurto-vehiculos-colombia/
│
├── dataset/
│   ├── CrecimientoParqueAutomotor.csv
│   ├── HurtoVehiculos.csv
│   ├── RecuperacionPoliciaNacional.csv
│   ├── municipios_dane.xlsx
│   ├── CrecimientoParqueAutomotor_limpio.csv
│   ├── HurtoVehiculos_limpio.csv
│   ├── RecuperacionPoliciaNacional_limpio.csv
│   ├── dataset_integrado.csv
│   ├── dataset_integrado.xlsx
│   ├── dataset_reducido.csv
│   └── dataset_con_clusters.csv
│
├── src/
│   ├── __init__.py
│   ├── hurto.py
│   ├── recuperacion.py
│   ├── parque_automotor.py
│   ├── integracion.py
│   ├── transformacion.py
│   ├── eda.py
│   ├── clasificacion.py
│   └── clustering.py
│
├── analisis/
│   ├── analisis_datos.ipynb
│   ├── transformacion_escalabilidad.ipynb
│   ├── analisis_exploratorio_eda.ipynb
│   ├── sesion8_clasificacion_nb_knn.ipynb
│   ├── sesion9_clustering_kmeans_jerarquico.ipynb
│   ├── INFORME_LABORATORIO_EDA.md
│   ├── ARBOLES_DE_DECISION_Y_ACCURACY.md
│   ├── RESULTADOS_ACCURACY_Y_ARBOLES.md
│   ├── TORNEO_CLASIFICACION_SESION8.md
│   ├── SEGMENTACION_CLUSTERING_SESION9.md
│   └── figuras/
│       ├── fig_hist_hurtos.png
│       ├── fig_box_hurtos.png
│       ├── fig_barras_departamentos.png
│       ├── fig_scatter_hurto_vs_recuperacion.png
│       ├── fig_heatmap_correlaciones.png
│       ├── fig_matriz_dispersion.png
│       ├── fig_box_hurto_tipo_vehiculo.png
│       ├── fig_tendencia_temporal_tasa_recuperacion.png
│       ├── fig_accuracy_arbol.png
│       ├── fig_sesion8_torneo_comparacion.png
│       ├── fig_sesion8_efecto_k_knn.png
│       ├── fig_sesion8_matrices_confusion.png
│       ├── fig_sesion9_metodo_codo_silueta.png
│       ├── fig_sesion9_perfilamiento_clusters.png
│       └── fig_sesion9_dendrograma_muestra60.png
│
├── .gitignore
└── README.md
```

## Resultado final

El proyecto permite integrar tres fuentes de información oficiales de Colombia y aplicar un proceso reproducible de **limpieza, integración, transformación, escalamiento, reducción de dimensionalidad (PCA), análisis exploratorio formal (EDA), clasificación supervisada (Árboles de Decisión, Naive Bayes y KNN) y segmentación no supervisada (K-Means y Jerárquico)**, obteniendo datasets y modelos predictivos y descriptivos robustos que sustentan la toma de decisiones estratégicas en seguridad vial y recuperación vehicular en Colombia.

