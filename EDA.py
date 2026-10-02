import pandas as pd
import numpy as np

# ---------------------------------------------------------------------
# Análisis A1: perfilamiento
# ---------------------------------------------------------------------

def perfilamiento_eda(
    df,
    nombre="dataset",
    columna_fecha="fecha_hora",
    frecuencia="1min",
    valores_centinela=None
):
    """
    Realiza el perfilamiento inicial de un conjunto de datos temporales.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame a analizar.

    nombre : str
        Nombre identificador del conjunto de datos.

    columna_fecha : str
        Nombre de la columna que contiene la fecha/hora.

    frecuencia : str
        Frecuencia temporal esperada. Para datos minutales: '1min'.

    valores_centinela : list
        Lista de valores que representan datos inválidos o ausentes.
        Ejemplo: [-99,-999, -9999, -2000].

    Retorna
    -------
    dict
        Diccionario con los resultados del perfilamiento.
    """

    # ---------------------------------------------------------
    # 1. Copia para no modificar el DataFrame original
    # ---------------------------------------------------------
    data = df.copy()

    if valores_centinela is None:
        valores_centinela = [-99,-999, -9999, -2000]

    # ---------------------------------------------------------
    # 2. Conversión de fecha/hora
    # ---------------------------------------------------------
    if columna_fecha not in data.columns:
        raise ValueError(
            f"La columna '{columna_fecha}' no existe en el DataFrame."
        )

    data[columna_fecha] = pd.to_datetime(
        data[columna_fecha],
        errors="coerce"
    )

    # ---------------------------------------------------------
    # 3. Información general
    # ---------------------------------------------------------
    n_filas = len(data)
    n_columnas = len(data.columns)

    memoria_mb = data.memory_usage(deep=True).sum() / (1024 ** 2)

    # ---------------------------------------------------------
    # 4. Tipos de datos
    # ---------------------------------------------------------
    tipos = pd.DataFrame({
        "columna": data.columns,
        "tipo_dato": data.dtypes.astype(str).values
    })

    # ---------------------------------------------------------
    # 5. Nulos
    # ---------------------------------------------------------
    data_c=data.copy()
    fec_ini=data_c.fecha_hora[0]
    fec_fin=data_c.fecha_hora[len(data_c)-1]
    fecha_completa=pd.date_range(fec_ini,fec_fin,freq='min')
    fecha_completa=pd.DataFrame(fecha_completa, columns=['fecha_c'])
    fecha_completa.index=fecha_completa.iloc[:,0]
    data_c=data_c.sort_values(by='fecha_hora', ascending=True)
    data_c.index=pd.to_datetime(data_c['fecha_hora'], format='%Y-%m-%d %H:%M:%S')
    data_c_fecha=pd.DataFrame(pd.to_datetime(data_c['fecha_hora'], format='%Y-%m-%d %H:%M:%S'), columns =['fecha'])
    concat=pd.concat([fecha_completa,data_c] ,axis=1)
    concat=concat.loc[:,data.columns]
    nulos = pd.DataFrame({
        "columna": concat.columns,
        "n_nulos": concat.isna().sum().values,
        "porcentaje_nulos": (
            concat.isna().mean().values * 100
        )
    })

    # ---------------------------------------------------------
    # 6. Valores centinela
    # ---------------------------------------------------------
    centinelas = []

    for columna in data.columns:

        # Solo analizar columnas numéricas
        if pd.api.types.is_numeric_dtype(data[columna]):

            for valor in valores_centinela:

                cantidad = (data[columna] == valor).sum()

                if cantidad > 0:
                    centinelas.append({
                        "columna": columna,
                        "valor_centinela": valor,
                        "cantidad": cantidad,
                        "porcentaje": (
                            cantidad / n_filas * 100
                            if n_filas > 0 else 0
                        )
                    })

    centinelas = pd.DataFrame(centinelas)

    # Si no se encontraron centinelas
    if centinelas.empty:
        centinelas = pd.DataFrame(
            columns=[
                "columna",
                "valor_centinela",
                "cantidad",
                "porcentaje"
            ]
        )

    # ---------------------------------------------------------
    # 7. Estadísticas numéricas y rangos
    # ---------------------------------------------------------
    data_con_cal=df.copy()
    data_con_cal=data_con_cal[(data_con_cal.calidad==1)|(data_con_cal.calidad==2)]
    columnas_numericas = data_con_cal.select_dtypes(
        include=np.number
    ).columns

    if len(columnas_numericas) > 0:

        rangos = data_con_cal[columnas_numericas].describe().T

        rangos = rangos[
            ["count", "min", "max"]
        ].reset_index()

        rangos.rename(
            columns={
                "index": "columna",
                "count": "n_validos"
            },
            inplace=True
        )

    else:

        rangos = pd.DataFrame(
            columns=[
                "columna",
                "n_validos",
                "min",
                "max"
            ]
        )

    # ---------------------------------------------------------
    # 8. Duplicados
    # ---------------------------------------------------------
    n_duplicados_filas = data.duplicated().sum()

    porcentaje_duplicados = (
        n_duplicados_filas / n_filas * 100
        if n_filas > 0 else 0
    )

    # Duplicados considerando solamente la fecha/hora
    n_duplicados_temporales = data[columna_fecha].duplicated().sum()

    # ---------------------------------------------------------
    # 9. Orden temporal
    # ---------------------------------------------------------
    fechas = data[columna_fecha].dropna()

    if len(fechas) > 1:

        esta_ordenado = fechas.is_monotonic_increasing
        esta_estrictamente_ordenado = fechas.is_monotonic_increasing and \
            fechas.is_unique

    else:

        esta_ordenado = True
        esta_estrictamente_ordenado = True

    # ---------------------------------------------------------
    # 10. Rango temporal
    # ---------------------------------------------------------
    if len(fechas) > 0:

        fecha_inicio = fechas.min()
        fecha_fin = fechas.max()
        duracion = fecha_fin - fecha_inicio

    else:

        fecha_inicio = None
        fecha_fin = None
        duracion = None

    # ---------------------------------------------------------
    # 11. Regularidad temporal
    # ---------------------------------------------------------
    if len(fechas) > 1:

        fechas_ordenadas = fechas.sort_values()

        diferencias = fechas_ordenadas.diff().dropna()

        frecuencia_esperada = pd.Timedelta(frecuencia)

        n_intervalos = len(diferencias)

        n_intervalos_esperados = (
            diferencias == frecuencia_esperada
        ).sum()

        n_intervalos_mayores = (
            diferencias > frecuencia_esperada
        ).sum()

        n_intervalos_menores = (
            diferencias < frecuencia_esperada
        ).sum()

        porcentaje_regularidad = (
            n_intervalos_esperados / n_intervalos * 100
            if n_intervalos > 0 else 100
        )

        # Diferencias diferentes a la frecuencia esperada
        intervalos_irregulares = (
            diferencias[
                diferencias != frecuencia_esperada
            ]
        )

        # Minutos faltantes estimados
        minutos_faltantes = (
            (diferencias / frecuencia_esperada - 1)
            .clip(lower=0)
            .sum()
        )

        intervalo_minimo = diferencias.min()
        intervalo_maximo = diferencias.max()

    else:

        n_intervalos = 0
        n_intervalos_esperados = 0
        n_intervalos_mayores = 0
        n_intervalos_menores = 0
        porcentaje_regularidad = np.nan
        intervalos_irregulares = pd.Series(dtype="timedelta64[ns]")
        minutos_faltantes = np.nan
        intervalo_minimo = pd.NaT
        intervalo_maximo = pd.NaT

    # ---------------------------------------------------------
    # 12. Resumen temporal
    # ---------------------------------------------------------
    resumen_temporal = pd.DataFrame({
        "indicador": [
            "Fecha inicial",
            "Fecha final",
            "Duración",
            "Ordenado cronológicamente",
            "Orden estrictamente creciente",
            "Duplicados temporales",
            "Intervalos temporales",
            "Intervalos de 1 minuto",
            "Intervalos mayores a 1 minuto",
            "Intervalos menores a 1 minuto",
            "Regularidad temporal (%)",
            "Minutos faltantes estimados",
            "Intervalo mínimo",
            "Intervalo máximo"
        ],
        "valor": [
            fecha_inicio,
            fecha_fin,
            duracion,
            esta_ordenado,
            esta_estrictamente_ordenado,
            n_duplicados_temporales,
            n_intervalos,
            n_intervalos_esperados,
            n_intervalos_mayores,
            n_intervalos_menores,
            porcentaje_regularidad,
            minutos_faltantes,
            intervalo_minimo,
            intervalo_maximo
        ]
    })

    # ---------------------------------------------------------
    # 13. Resumen general
    # ---------------------------------------------------------
    resumen_general = pd.DataFrame({
        "indicador": [
            "Dataset",
            "Filas",
            "Columnas",
            "Memoria (MB)",
            "Filas duplicadas",
            "% filas duplicadas",
            "Columnas numéricas",
            "Columnas categóricas",
            "Nulos totales"
        ],
        "valor": [
            nombre,
            n_filas,
            n_columnas,
            round(memoria_mb, 2),
            n_duplicados_filas,
            round(porcentaje_duplicados, 2),
            len(data.select_dtypes(include=np.number).columns),
            len(data.select_dtypes(exclude=np.number).columns),
            concat.codigo.isna().sum().sum()
        ]
    })

    # ---------------------------------------------------------
    # 14. Resultado final
    # ---------------------------------------------------------
    resultado = {
        "nombre": nombre,
        "resumen_general": resumen_general,
        "tipos": tipos,
        "nulos": nulos,
        "centinelas": centinelas,
        "rangos": rangos,
        "resumen_temporal": resumen_temporal,
    }

    # ---------------------------------------------------------
    # REPORTE DE PERFILAMIENTO
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print(f"PERFILAMIENTO EDA: {nombre}")
    print("=" * 80)

    # ---------------------------------------------------------
    # 1. Información general
    # ---------------------------------------------------------

    print("\n[1] INFORMACIÓN GENERAL")
    print("-" * 80)

    print(f"Número de registros       : {n_filas:,}")
    print(f"Número de columnas        : {n_columnas}")
    print(f"Memoria utilizada         : {memoria_mb:.2f} MB")
    print(f"Filas duplicadas          : {n_duplicados_filas:,}")
    print(f"% filas duplicadas        : {porcentaje_duplicados:.2f}%")
    print(f"Nulos explícitos totales  : {concat.codigo.isna().sum().sum():,}")


    # ---------------------------------------------------------
    # 2. Tipos de datos
    # ---------------------------------------------------------

    print("\n[2] TIPOS DE DATOS")
    print("-" * 80)

    print(
        tipos.to_string(index=False)
    )


    # ---------------------------------------------------------
    # 3. Nulos
    # ---------------------------------------------------------

    print("\n[3] NULOS EXPLÍCITOS")
    print("-" * 80)

    print(
        nulos.to_string(
            index=False,
            formatters={
                "porcentaje_nulos": "{:.2f}%".format
            }
        )
    )


    # ---------------------------------------------------------
    # 4. Valores centinela
    # ---------------------------------------------------------

    print("\n[4] VALORES CENTINELA")
    print("-" * 80)

    if centinelas.empty:

        print("No se encontraron valores centinela.")

    else:

        print(
            centinelas.to_string(
                index=False,
                formatters={
                    "porcentaje": "{:.2f}%".format
                }
            )
        )


    # ---------------------------------------------------------
    # 5. Rangos
    # ---------------------------------------------------------

    print("\n[5] RANGOS DE VARIABLES NUMÉRICAS")
    print("-" * 80)

    if rangos.empty:

        print("No existen variables numéricas.")

    else:

        print(
            rangos.to_string(
                index=False
            )
        )


    # ---------------------------------------------------------
    # 6. Análisis temporal
    # ---------------------------------------------------------

    print("\n[6] ANÁLISIS TEMPORAL")
    print("-" * 80)

    print(f"Fecha inicial             : {fecha_inicio}")
    print(f"Fecha final               : {fecha_fin}")
    print(f"Duración                  : {duracion}")
    print(f"Frecuencia esperada       : {frecuencia}")
    print(f"Orden cronológico         : {esta_ordenado}")
    print(f"Orden estrictamente creciente : {esta_estrictamente_ordenado}")
    print(f"Duplicados temporales     : {n_duplicados_temporales:,}")
    print(f"Intervalos analizados     : {n_intervalos:,}")
    print(f"Intervalos de 1 minuto    : {n_intervalos_esperados:,}")
    print(f"Intervalos > 1 minuto     : {n_intervalos_mayores:,}")
    print(f"Intervalos < 1 minuto     : {n_intervalos_menores:,}")
    print(f"Regularidad temporal      : {porcentaje_regularidad:.2f}%")
    print(f"Minutos faltantes         : {minutos_faltantes:,.0f}")
    print(f"Intervalo mínimo          : {intervalo_minimo}")
    print(f"Intervalo máximo          : {intervalo_maximo}")


    # ---------------------------------------------------------
    # 7. Fin del reporte
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("FIN DEL PERFILAMIENTO")
    print("=" * 80)

