# Perfilamiento de datos de estaciones SIATA

## 1. Objetivo

Este repositorio documenta el perfilamiento exploratorio de datos (EDA) realizado sobre cuatro estaciones de las redes de monitoreo del Valle de Aburrá:

- **Estación meteorológica 367 — Joaquín Vallejo - Meteorológica**
- **Estación de nivel 803 — Q. La Aguadita - Colinas de Enciso**
- **Estación de piranómetro 6004 — Piranómetro Parque de las Aguas**
- **Estación pluviométrica 35 — I.E. Joaquín Vallejo Arbeláez**

El objetivo del análisis es caracterizar la estructura y consistencia inicial de las series temporales respondiendo Tarea A: Análisis exploratorio de datos (EDA), módulo 1 - A1. Perfilamiento, con énfasis en:

1. tipos de datos;
2. rangos de las variables;
3. valores nulos;
4. valores centinela;
5. registros duplicados;
6. orden temporal;
7. regularidad del índice temporal.

El análisis se implementa mediante la función `perfilamiento_eda()` definida en `EDA.py` y se ejecuta sobre las cuatro estaciones desde `Exploracion.ipynb`.

> **Nota:** este README documenta el contexto de las redes, las estaciones y la lógica del código. Los resultados numéricos del perfilamiento deben obtenerse ejecutando el notebook sobre los archivos de medición correspondientes. Los archivos de metadatos suministrados permiten documentar las estaciones, pero no contienen las series de medición que analiza `perfilamiento_eda()`.

---

## 2. Contexto general: ruta del dato

Las redes de monitoreo parten de sensores instalados en puntos de interés para medir variables ambientales. Los datos generados son transmitidos mediante tecnologías de comunicación, almacenados en servidores y bases de datos y posteriormente procesados para su consulta y análisis. Esta ruta permite conservar un registro histórico y realizar evaluaciones de calidad sobre la información recopilada.

Los cuatro conjuntos analizados corresponden a redes con diferentes variables, sensores y características físicas de medición. Por esta razón, el perfilamiento debe interpretarse teniendo en cuenta la naturaleza de cada variable y los indicadores de calidad definidos para cada red.

---

# 3. Red meteorológica

## 3.1 Generalidades

La red meteorológica está conformada por sensores multiparamétricos que registran información minutal de diferentes variables ambientales relacionadas con los fenómenos atmosféricos y el clima del Valle de Aburrá. Su operación comenzó en **2012** y la resolución temporal documentada es de **1 minuto**.

Las variables disponibles en esta red son:

| Variable | Unidad |
|---|---|
| Precipitación | mm |
| Temperatura superficial | °C |
| Presión atmosférica | hPa |
| Humedad relativa | % |
| Velocidad promedio del viento | m/s |
| Dirección promedio del viento | grados (°) |
| Velocidad máxima del viento | m/s |
| Dirección máxima del viento | grados (°) |

## 3.2 Estación meteorológica 367

| Campo | Valor |
|---|---|
| Código | 367 |
| Nombre | Joaquín Vallejo - Meteorológica |
| Red | Meteorológica |
| Latitud | 6.255245 |
| Longitud | -75.542478 |
| Barrio/Vereda | La Ladera |
| Comuna/Corregimiento | 08 Villa Hermosa |
| Municipio | Medellín |
| Subcuenca | Q. Santa Elena |
| Fecha de instalación | 2019-03-18 |

**Consideraciones para el perfilamiento:** la columna `calidad` debe conservarse como variable de control del análisis.

---

# 4. Red de nivel

## 4.1 Generalidades

La red de nivel está compuesta por estaciones que miden la distancia entre el sensor y la lámina de agua de ríos o quebradas. Utiliza ondas electromagnéticas o ultrasonido para monitorear las fluctuaciones del río Medellín y de algunas de las principales quebradas del Valle de Aburrá. La operación comenzó en **2012**, con una resolución temporal de **1 minuto** y unidad de medición en **centímetros (cm)**. 

## 4.2 Estación de nivel 803

| Campo | Valor |
|---|---|
| Código | 803 |
| Nombre | Q. La Aguadita - Colinas De Enciso |
| Red | Nivel |
| Latitud | 6.253750 |
| Longitud | -75.544067 |
| Barrio/Vereda | Los Mangos |
| Comuna/Corregimiento | 8 Villa Hermosa |
| Municipio | Medellín |
| Subcuenca | Q. Santa Elena |
| Fecha de instalación | 2025-04-14 |


---

# 5. Red de piranómetros

## 5.1 Generalidades

La red de piranómetros está compuesta por sensores que miden la **radiación solar total que llega a la superficie**. Esta información es relevante para estudiar fenómenos meteorológicos cercanos a la superficie y para evaluar condiciones meteorológicas relacionadas con la calidad del aire en el Valle de Aburrá. La operación comenzó en **2016**, con resolución temporal de **1 minuto** y unidad de medición **W/m²**.

## 5.2 Estación de piranómetro 6004

| Campo | Valor |
|---|---|
| Código | 6004 |
| Nombre | Piranómetro Parque de las Aguas |
| Red | Piranómetro |
| Latitud | 6.406612 |
| Longitud | -75.419344 |
| Barrio/Vereda | Filo Verde |
| Comuna/Corregimiento | No reportado en el metadato |
| Municipio | Barbosa |
| Subcuenca | Río Aburrá-Medellín |
| Fecha de instalación | 2017-05-05 |

---

# 6. Red pluviométrica

## 6.1 Generalidades

La red pluviométrica está compuesta por estaciones de **cazoleta o tipo basculante**. Mediante las dimensiones calibradas del colector y las cazoletas, estas estaciones miden la precipitación en un punto y la expresan como lámina de precipitación líquida en superficie, en **milímetros (mm)**. Un milímetro de lluvia corresponde a un litro de agua precipitada por metro cuadrado de superficie.

La operación comenzó en **2010**. Entre 2010 y 2012 se utilizó una resolución de 5 minutos y un sensor por estación; desde 2012 la resolución pasó a 1 minuto y cada punto cuenta con dos pluviómetros, denominados `p1` y `p2`, para proporcionar redundancia y apoyar la identificación de fallas. 

## 6.2 Estación pluviométrica 35

| Campo | Valor |
|---|---|
| Código | 35 |
| Nombre | I.E. Joaquin Vallejo Arbelaez |
| Red | Pluviométrica |
| Latitud | 6.255245 |
| Longitud | -75.542478 |
| Barrio/Vereda | La Ladera |
| Comuna/Corregimiento | 08 Villa Hermosa |
| Municipio | Medellín |
| Subcuenca | Q. Santa Elena |
| Fecha de instalación | 2010-01-28 |

**Consideraciones para el perfilamiento:** desde 2012 la red utiliza dos sensores por estación (`p1` y `p2`). Por ello, la presencia de dos series de precipitación permite revisar tanto la integridad individual de cada sensor como su comportamiento conjunto. La columna `calidad` debe utilizarse para contextualizar los rangos y posibles anomalías.

---
### Consideraciones de calidad

La columna `calidad` clasifica la confiabilidad del registro. todos los manuales documenta los indicadores, donde se considerará como relevante para el análisis estadístico (min/max) sobre todos los indicadores asociados a un dato confiable, como lo es: 

- `1`: calidad confiable en tiempo real.
- `2`: calidad confiable no obtenida en tiempo real.
---

# 7. Estructura del perfilamiento implementado

El análisis se centraliza en la función:

```python
perfilamiento_eda(
    df,
    nombre="dataset",
    columna_fecha="fecha_hora",
    frecuencia="1min",
    valores_centinela=None
)
```

La función recibe un `DataFrame`, el nombre del conjunto de datos, la columna temporal, la frecuencia esperada y, opcionalmente, los valores centinela. Si no se especifican valores centinela, el código utiliza:

```python
[-99, -999, -9999, -2000]
```

## 7.1 Conversión de fecha/hora

La columna `fecha_hora` se convierte mediante `pd.to_datetime(..., errors="coerce")`. Esto permite transformar fechas válidas a un tipo temporal y convertir a `NaT` aquellas que no puedan interpretarse.

## 7.2 Tipos de datos

Se genera una tabla con el nombre de cada columna y su tipo de dato (`dtype`). Esto permite identificar si las variables fueron cargadas como numéricas, texto u otros tipos.

## 7.3 Nulos

Para evaluar la completitud temporal, el código:

1. toma la primera y última fecha;
2. construye un índice completo con frecuencia de 1 minuto;
3. ordena los datos por `fecha_hora`;
4. utiliza la fecha como índice;
5. concatena la secuencia temporal esperada con los registros observados; y
6. calcula cantidad y porcentaje de valores `NaN` por columna.

Esto permite que los espacios ausentes en la secuencia temporal se reflejen como nulos al comparar la serie observada contra el índice esperado.

## 7.4 Valores centinela

El código revisa los valores centinela únicamente en columnas numéricas. Para cada columna y cada valor configurado, calcula la cantidad de apariciones y su porcentaje respecto al total de filas.

**Importante:** la lista predeterminada del código es más amplia. El manual de red meteorológica y pluviometría documenta `-999`, mientras que el de piranómetros documenta `-9999`.

## 7.5 Rangos

Para calcular los rangos, el código primero filtra los registros cuya columna `calidad` sea igual a `1` o `2`. Después selecciona las columnas numéricas y obtiene `count`, `min` y `max`. fileciteturn0file4L139-L164


## 7.6 Duplicados

Se calculan dos tipos de duplicados:

- duplicados completos de fila;
- duplicados de la variable temporal `fecha_hora`.

Esto permite diferenciar registros completamente repetidos de múltiples observaciones asociadas al mismo instante temporal. 

## 7.7 Orden temporal

El código comprueba si las fechas son:

- monótonamente crecientes;
- estrictamente crecientes, es decir, crecientes y sin fechas repetidas.

La segunda condición es especialmente útil para series temporales porque combina el orden cronológico con la ausencia de duplicados temporales.

## 7.8 Rango temporal

Se obtiene:

- fecha inicial;
- fecha final;
- duración total del periodo analizado.

## 7.9 Regularidad temporal

La frecuencia esperada se establece en **1 minuto**. Para evaluar la regularidad, el código ordena las fechas, calcula las diferencias consecutivas y las compara con un `Timedelta` de 1 minuto.

Se reportan:

- número total de intervalos;
- intervalos exactamente de 1 minuto;
- intervalos mayores de 1 minuto;
- intervalos menores de 1 minuto;
- porcentaje de regularidad;
- minutos faltantes estimados;
- intervalo mínimo;
- intervalo máximo.


La regularidad se calcula como:

```text
intervalos de 1 minuto / total de intervalos × 100
```

Por tanto, un porcentaje inferior al 100 % indica que existen intervalos temporales diferentes a la frecuencia esperada. Los intervalos mayores de un minuto son utilizados además para estimar minutos faltantes. 

---

# 8. Interpretación de los resultados

El perfilamiento debe leerse en dos niveles:

### Nivel 1 — Estructura y completitud

Permite responder:

- ¿Qué columnas contiene cada conjunto?
- ¿Qué tipo de dato tiene cada columna?
- ¿Existen valores `NaN`?
- ¿Existen valores centinela?
- ¿Hay registros duplicados?
- ¿La fecha está ordenada?
- ¿Hay fechas repetidas?

### Nivel 2 — Consistencia temporal y física

Permite responder:

- ¿La serie conserva la frecuencia esperada de 1 minuto?
- ¿Cuántos intervalos se apartan de esa frecuencia?
- ¿Cuál es el rango observado?
- ¿El rango corresponde a registros considerados confiables?
- ¿Los valores extremos deben interpretarse a la luz de la variable y de los indicadores de calidad?

Esta segunda lectura es importante porque un comportamiento que estadísticamente parece anómalo puede tener una explicación asociada a la naturaleza de la variable, al sensor o al proceso de adquisición.


---

# 9. Fuentes documentales
Todos la documentación fue descargada desde: https://datos.siata.gov.co/

- **Generalidades — Repositorio de Datos, Red de piranómetros.** Código `P-GAA-SIATA-111`, versión 01.
- **Generalidades — Repositorio de Datos, Red de nivel.** Código `P-GAA-SIATA-110`, versión 01.
- **Generalidades — Repositorio de Datos, Red pluviométrica.** Código `P-GAA-SIATA-107`, versión 01.
- **Generalidades — Repositorio de Datos, Red meteorológica.** Código `P-GAA-SIATA-108`, versión 01.
- **Metadatos de estaciones:** archivos de estaciones meteorológicas, nivel, piranómetros y pluviometría suministrados para el análisis.
- **Implementación:** `EDA.py`.
- **Ejecución del análisis:** `Exploracion.ipynb`.
