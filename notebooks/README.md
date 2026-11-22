# 📓 Directorio de Cuadernos Jupyter (Notebooks)

Este directorio contiene los cuadernos Jupyter del proyecto organizados cronológicamente por fases metodológicas de la investigación:

---

## 🔬 Cuadernos Principales Reproducibles

| Cuaderno | Etapa / Hito | Descripción Metodológica |
| :--- | :--- | :--- |
| **[01_eda_exploratorio.ipynb](01_eda_exploratorio.ipynb)** | **Fase 1: EDA** | Ingesta de fuentes maestras (Hurto, Recuperación, RUNT, DANE), diagnóstico de nulos y atípicos, y cruce relacional. |
| **[02_transformacion_y_escalabilidad.ipynb](02_transformacion_y_escalabilidad.ipynb)** | **Fase 2: ETL & PCA** | Estandarización con `StandardScaler`, variables dummies, reducción de dimensionalidad por PCA y exportación del dataset maestro. |
| **[03_sesion8_clasificacion_supervisada.ipynb](03_sesion8_clasificacion_supervisada.ipynb)** | **Fase 3: Clasificación** | Torneo de clasificación binaria: Árbol de Decisión vs Gaussian Naive Bayes vs KNN. Curvas de hiperparámetro $k$ y matrices de confusión. |
| **[04_sesion9_clustering_territorial.ipynb](04_sesion9_clustering_territorial.ipynb)** | **Fase 4: Segmentación** | Clustering K-Means ($k=4$), método del codo, coeficiente de silueta y dendrograma jerárquico aglomerativo (Ward). |

---

## 🧪 Cuadernos Prototipo y Experimentales (`notebooks/exploratorios/`)

* **[analisis_datos_inicial.ipynb](exploratorios/analisis_datos_inicial.ipynb):** Pruebas iniciales de ingesta de CSVs crudos y exportaciones intermedias.
* **[clustering_experimental.ipynb](exploratorios/clustering_experimental.ipynb):** Primeros experimentos de agrupación no supervisada antes de fijar $k=4$.
* **[modelos_clasificacion_v1.ipynb](exploratorios/modelos_clasificacion_v1.ipynb):** Prototipos de evaluación preliminar de modelos supervisados.
