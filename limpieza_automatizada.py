import pandas as pd
import numpy as np
import re
from datetime import datetime
import unicodedata
import os
from typing import Dict, List, Any, Optional

class LimpiezaAutomatizada:
    """
    Sistema automatizado y reutilizable para limpieza de datos - VERSIÓN OPTIMIZADA
    """
    
    def __init__(self, archivo_csv: str, config_limpieza: Dict = None):
        self.archivo_csv = archivo_csv
        self.df = None
        self.config_limpieza = config_limpieza or self._configuracion_predeterminada()
        self.estadisticas_limpieza = {}
        
    def _configuracion_predeterminada(self) -> Dict:
        """Configuración predeterminada para limpieza"""
        return {
            'mapeo_columnas': {
                'fecha': ['fecha', 'date', 'fecha_venta', 'fecha_compra', 'timestamp'],
                'producto': ['producto', 'product', 'item', 'articulo', 'descripcion'],
                'tipo_producto': ['tipo_producto', 'categoria', 'categoria_producto', 'tipo', 'category'],
                'cantidad': ['cantidad', 'qty', 'quantity', 'unidades', 'units'],
                'precio_unitario': ['precio_unitario', 'precio', 'price', 'unit_price', 'precio_unidad'],
                'total_ventas': ['total_ventas', 'venta_total', 'total', 'amount', 'monto_total', 'importe'],
                'tipo_venta': ['tipo_venta', 'canal_venta', 'channel', 'venta_tipo', 'sales_channel'],
                'tipo_cliente': ['tipo_cliente', 'cliente_tipo', 'customer_type', 'segmento_cliente'],
                'descuento': ['descuento', 'discount', 'descuento_porcentaje', 'discount_percent'],
                'costo_envio': ['costo_envio', 'shipping_cost', 'costo_transporte', 'envio_costo'],
                'ciudad': ['ciudad', 'city', 'localidad', 'municipio'],
                'pais': ['pais', 'country', 'paises', 'nation'],
                'region': ['region', 'state', 'estado', 'provincia'],
                'cliente_id': ['cliente_id', 'customer_id', 'id_cliente', 'client_id'],
                'producto_id': ['producto_id', 'product_id', 'id_producto', 'sku']
            },
            'reglas_limpieza': {
                'texto': {
                    'min_length': 1,
                    'max_length': 100,
                    'permitir_numeros': False,
                    'case': 'title'
                },
                'numero': {
                    'min_value': 0,
                    'max_value': 1000000,
                    'decimales': 2
                },
                'fecha': {
                    'formatos': ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S'],
                    'rango_min': '2020-01-01',
                    'rango_max': '2025-12-31'
                }
            },
            'columnas_orden_preferido': [
                'fecha', 'producto', 'tipo_producto', 'cantidad', 'precio_unitario',
                'ciudad', 'pais', 'tipo_venta', 'tipo_cliente', 'descuento', 'costo_envio'
            ]
        }
    
    def _reorganizar_datos_mal_estructurados(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reorganizar datos que están en columnas incorrectas - OPTIMIZADO"""
        print("🔄 Reorganizando datos mal estructurados...")
        
        columnas_actuales = df.columns.tolist()
        
        if len(columnas_actuales) >= 10:
            try:
                # USAR OPERACIONES VECTORIZADAS EN LUGAR DE ITERROWS
                nuevos_datos = {
                    'ciudad': df.iloc[:, 0].astype(str) if len(df.columns) > 0 else '',
                    'fecha': df.iloc[:, 1].astype(str) if len(df.columns) > 1 else '',
                    'producto': df.iloc[:, 2].astype(str) if len(df.columns) > 2 else '',
                    'tipo_producto': df.iloc[:, 3].astype(str) if len(df.columns) > 3 else '',
                    'cantidad': df.iloc[:, 4].astype(str) if len(df.columns) > 4 else '',
                    'precio_unitario': df.iloc[:, 5].astype(str) if len(df.columns) > 5 else '',
                    'tipo_venta': df.iloc[:, 6].astype(str) if len(df.columns) > 6 else '',
                    'tipo_cliente': df.iloc[:, 7].astype(str) if len(df.columns) > 7 else '',
                    'descuento': df.iloc[:, 8].astype(str) if len(df.columns) > 8 else '',
                    'costo_envio': df.iloc[:, 9].astype(str) if len(df.columns) > 9 else '',
                    'pais': 'Colombia'
                }
                
                df_corregido = pd.DataFrame(nuevos_datos)
                print(f"   ✅ Datos reorganizados: {len(df_corregido)} filas")
                return df_corregido
                
            except Exception as e:
                print(f"   ⚠ Error reorganizando datos: {e}")
                return df
        else:
            print("   ℹ️  Estructura de columnas parece correcta")
            return df
    
    def _detectar_y_corregir_pais(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detectar y corregir automáticamente el país - OPTIMIZADO"""
        print("   🗺️  Detectando países basado en ciudades...")
        
        mapeo_ciudad_pais = {
            'bogota': 'Colombia', 'medellin': 'Colombia', 'cali': 'Colombia',
            'barranquilla': 'Colombia', 'cartagena': 'Colombia', 'cucuta': 'Colombia',
            'bucaramanga': 'Colombia', 'pereira': 'Colombia', 'santa marta': 'Colombia',
            'ibague': 'Colombia', 'past': 'Colombia', 'manizales': 'Colombia',
            'monteria': 'Colombia', 'neiva': 'Colombia', 'villavicencio': 'Colombia',
            'valledupar': 'Colombia', 'armenia': 'Colombia', 'sincelejo': 'Colombia',
            'popayan': 'Colombia', 'itagui': 'Colombia', 'santiago': 'Colombia',
            'cordoba': 'Colombia', 'trujillo': 'Colombia', 'valencia': 'Colombia',
            'new york': 'Estados Unidos', 'miami': 'Estados Unidos', 'los angeles': 'Estados Unidos',
            'chicago': 'Estados Unidos', 'houston': 'Estados Unidos',
            'madrid': 'España', 'barcelona': 'España', 'valencia': 'España',
            'ciudad de mexico': 'México', 'guadalajara': 'México', 'monterrey': 'México',
            'buenos aires': 'Argentina', 'cordoba': 'Argentina', 'rosario': 'Argentina',
            'sao paulo': 'Brasil', 'rio de janeiro': 'Brasil', 'brasilia': 'Brasil',
            'lima': 'Perú', 'arequipa': 'Perú', 'trujillo': 'Perú',
            'santiago': 'Chile', 'valparaiso': 'Chile', 'concepcion': 'Chile'
        }
        
        if 'ciudad' in df.columns:
            # VECTORIZAR LA OPERACIÓN EN LUGAR DE USAR APPLY
            ciudades_clean = df['ciudad'].fillna('').astype(str).str.lower().str.strip()
            
            def buscar_pais(ciudad):
                for ciudad_mapeo, pais in mapeo_ciudad_pais.items():
                    if ciudad_mapeo == ciudad or ciudad_mapeo in ciudad or ciudad in ciudad_mapeo:
                        return pais
                return 'Desconocido'
            
            # Crear array de países usando list comprehension (más rápido que apply)
            paises = [buscar_pais(ciudad) for ciudad in ciudades_clean]
            df['pais'] = paises
            
            print(f"   ✅ Países detectados: {df['pais'].value_counts().to_dict()}")
        
        return df
    
    def detectar_estructura(self) -> Dict:
        """Detectar automáticamente la estructura del archivo - OPTIMIZADO"""
        print("🔍 DETECTANDO ESTRUCTURA DEL ARCHIVO...")
        
        try:
            # Leer solo las necesarias para análisis
            self.df = pd.read_csv(self.archivo_csv, nrows=100)
            print(f"📊 Archivo detectado: {self.archivo_csv}")
            print(f"📏 Dimensiones: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            
            columnas_originales = self.df.columns.tolist()
            print(f"📋 Columnas originales: {columnas_originales}")
            
            self.df = self._reorganizar_datos_mal_estructurados(self.df)
            mapeo_automatico = self._mapear_columnas_automatico(self.df.columns.tolist())
            tipos_datos = self._analizar_tipos_datos()
            
            return {
                'columnas_originales': columnas_originales,
                'mapeo_propuesto': mapeo_automatico,
                'tipos_datos': tipos_datos,
                'muestra_datos': self.df.head(3).to_dict('records')
            }
            
        except Exception as e:
            print(f"❌ Error detectando estructura: {e}")
            return {}
    
    def _mapear_columnas_automatico(self, columnas_originales: List[str]) -> Dict:
        """Mapear automáticamente columnas - OPTIMIZADO"""
        mapeo = {}
        columnas_mapeadas = set()
        columnas_no_mapeadas = columnas_originales.copy()
        
        # PRE-COMPUTAR TEXTOS NORMALIZADOS
        columnas_normalizadas = {col: self._normalizar_texto(col) for col in columnas_originales}
        variantes_normalizadas = {}
        
        for nombre_estandar, variantes in self.config_limpieza['mapeo_columnas'].items():
            variantes_normalizadas[nombre_estandar] = [self._normalizar_texto(v) for v in variantes]
        
        # Primera pasada: coincidencias exactas
        for col_original, col_normalizada in columnas_normalizadas.items():
            if col_original in columnas_mapeadas:
                continue
                
            for nombre_estandar, variantes in variantes_normalizadas.items():
                if col_normalizada in variantes:
                    mapeo[col_original] = nombre_estandar
                    columnas_mapeadas.add(col_original)
                    if col_original in columnas_no_mapeadas:
                        columnas_no_mapeadas.remove(col_original)
                    break
        
        # Segunda pasada: coincidencias parciales
        for col_original, col_normalizada in columnas_normalizadas.items():
            if col_original in columnas_mapeadas:
                continue
                
            for nombre_estandar, variantes in variantes_normalizadas.items():
                if any(v in col_normalizada or col_normalizada in v for v in variantes if len(col_normalizada) > 2):
                    if nombre_estandar not in mapeo.values():
                        mapeo[col_original] = nombre_estandar
                        columnas_mapeadas.add(col_original)
                        if col_original in columnas_no_mapeadas:
                            columnas_no_mapeadas.remove(col_original)
                        break
        
        # Columnas no mapeadas
        nombres_estandar_usados = set(mapeo.values())
        for i, columna in enumerate(columnas_no_mapeadas):
            nombre_estandar = f"columna_{i+1}"
            while nombre_estandar in nombres_estandar_usados:
                i += 1
                nombre_estandar = f"columna_{i+1}"
            
            mapeo[columna] = nombre_estandar
            nombres_estandar_usados.add(nombre_estandar)
        
        return mapeo
    
    def _eliminar_columnas_duplicadas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Eliminar columnas duplicadas - OPTIMIZADO"""
        columnas_vistas = set()
        columnas_a_eliminar = []
        
        for columna in df.columns:
            if columna in columnas_vistas:
                columnas_a_eliminar.append(columna)
            else:
                columnas_vistas.add(columna)
        
        if columnas_a_eliminar:
            df = df.drop(columns=columnas_a_eliminar)
            print(f"✅ Eliminadas {len(columnas_a_eliminar)} columnas duplicadas")
        
        return df
    
    def _reordenar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reordenar columnas según orden preferido - OPTIMIZADO"""
        columnas_actuales = df.columns.tolist()
        orden_preferido = self.config_limpieza.get('columnas_orden_preferido', [])
        
        columnas_ordenadas = [col for col in orden_preferido if col in columnas_actuales]
        columnas_restantes = [col for col in columnas_actuales if col not in columnas_ordenadas]
        columnas_finales = columnas_ordenadas + sorted(columnas_restantes)
        
        if columnas_finales != columnas_actuales:
            print("🔄 Reordenando columnas...")
            df = df[columnas_finales]
        
        return df
    
    def _analizar_tipos_datos(self) -> Dict:
        """Analizar tipos de datos - OPTIMIZADO"""
        tipos = {}
        for columna in self.df.columns:
            valores_unicos = self.df[columna].dropna().unique()[:5]
            tipo_probable = self._determinar_tipo_columna(self.df[columna])
            
            tipos[columna] = {
                'tipo_probable': tipo_probable,
                'valores_unicos': valores_unicos.tolist(),
                'nulos': self.df[columna].isna().sum(),
                'ejemplos': valores_unicos.tolist()[:3]
            }
        
        return tipos
    
    def _determinar_tipo_columna(self, serie: pd.Series) -> str:
        """Determinar automáticamente el tipo de columna - OPTIMIZADO"""
        if serie.empty:
            return 'desconocido'
            
        serie_str = serie.dropna().astype(str)
        
        if len(serie_str) == 0:
            return 'desconocido'
        
        # MUESTREO PARA ACELERAR (usar solo muestra de datos)
        if len(serie_str) > 1000:
            serie_muestra = serie_str.sample(n=1000, random_state=42)
        else:
            serie_muestra = serie_str
        
        # Usar operaciones vectorizadas para verificación
        fecha_count = serie_muestra.apply(self._es_fecha_valida).sum()
        if fecha_count / len(serie_muestra) > 0.5:
            return 'fecha'
        
        numerico_count = serie_muestra.apply(self._es_numerico).sum()
        if numerico_count / len(serie_muestra) > 0.8:
            return 'numero'
        
        valores_bool = ['true', 'false', '1', '0', 'si', 'no', 'sí', 'yes', 'verdadero', 'falso']
        bool_count = serie_muestra.str.lower().str.strip().isin(valores_bool).sum()
        if bool_count / len(serie_muestra) > 0.8:
            return 'booleano'
        
        return 'texto'
    
    def _es_fecha_valida(self, valor: str) -> bool:
        """Verificar si un valor es una fecha válida - OPTIMIZADO"""
        try:
            # Intentar parsing directo con pandas primero (más rápido)
            pd.to_datetime(valor, errors='raise')
            return True
        except:
            # Solo si falla, intentar formatos específicos
            formatos = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']
            for formato in formatos:
                try:
                    datetime.strptime(str(valor), formato)
                    return True
                except ValueError:
                    continue
            return False
    
    def _es_numerico(self, valor: str) -> bool:
        """Verificar si un valor es numérico - OPTIMIZADO"""
        try:
            valor_str = str(valor).strip()
            if not valor_str:
                return False
            # Verificar patron numérico con regex (más rápido)
            return bool(re.match(r'^-?\d*\.?\d+$', valor_str))
        except:
            return False
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normalizar texto para comparación - OPTIMIZADO"""
        if pd.isna(texto):
            return ""
        texto = str(texto).lower().strip()
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
        texto = re.sub(r'[^a-z0-9]', '', texto)
        return texto
    
    def aplicar_limpieza(self, mapeo_personalizado: Dict = None) -> pd.DataFrame:
        """Aplicar limpieza completa - OPTIMIZADO"""
        print("\n🧹 APLICANDO LIMPIEZA AUTOMATIZADA...")
        
        try:
            # Cargar datos con tipos optimizados
            self.df = pd.read_csv(self.archivo_csv, low_memory=False)
            registros_originales = len(self.df)
            
            self.df = self._reorganizar_datos_mal_estructurados(self.df)
            
            # Aplicar mapeo de columnas
            mapeo_final = mapeo_personalizado or self._mapear_columnas_automatico(self.df.columns.tolist())
            self.df = self.df.rename(columns=mapeo_final)
            print("✅ Columnas renombradas")
            
            self.df = self._eliminar_columnas_duplicadas(self.df)
            self.df = self._detectar_y_corregir_pais(self.df)
            
            # LIMPIEZA POR LOTES EN VEZ DE COLUMNA POR COLUMNA
            self._aplicar_limpieza_por_lotes()
            
            self._calcular_total_ventas()
            self.df = self._reordenar_columnas(self.df)
            self._calcular_estadisticas_limpieza(registros_originales)
            self._mostrar_resumen_limpieza()
            
            return self.df
            
        except Exception as e:
            print(f"❌ Error en limpieza: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def _aplicar_limpieza_por_lotes(self):
        """Aplicar limpieza por lotes en vez de columna por columna - OPTIMIZADO"""
        print("   🚀 Aplicando limpieza por lotes...")
        
        # Limpiar columnas numéricas críticas en lote
        columnas_numericas = ['cantidad', 'precio_unitario', 'descuento', 'costo_envio', 'total_ventas']
        columnas_existentes = [col for col in columnas_numericas if col in self.df.columns]
        
        if columnas_existentes:
            # CONVERTIR MÚLTIPLES COLUMNAS A LA VEZ
            self.df[columnas_existentes] = self.df[columnas_existentes].apply(
                lambda col: pd.to_numeric(col, errors='coerce')
            )
            
            # Aplicar límites y decimales
            min_val = self.config_limpieza['reglas_limpieza']['numero']['min_value']
            max_val = self.config_limpieza['reglas_limpieza']['numero']['max_value']
            decimales = self.config_limpieza['reglas_limpieza']['numero']['decimales']
            
            self.df[columnas_existentes] = self.df[columnas_existentes].clip(lower=min_val, upper=max_val)
            if decimales is not None:
                self.df[columnas_existentes] = self.df[columnas_existentes].round(decimales)
        
        # Limpiar texto en lote para columnas no numéricas
        columnas_texto = [col for col in self.df.columns 
                         if col not in columnas_numericas and self.df[col].dtype == 'object']
        
        if columnas_texto:
            self.df[columnas_texto] = self.df[columnas_texto].apply(self._limpiar_texto_vectorizado)
    
    def _limpiar_texto_vectorizado(self, serie: pd.Series) -> pd.Series:
        """Limpiar texto usando operaciones vectorizadas - OPTIMIZADO"""
        # Operaciones vectorizadas nativas de pandas (mucho más rápidas)
        serie_limpia = serie.astype(str).str.strip()
        serie_limpia = serie_limpia.str.replace(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-_\.]', ' ', regex=True)
        serie_limpia = serie_limpia.str.replace(r'\s+', ' ', regex=True).str.strip()
        serie_limpia = serie_limpia.replace('', np.nan)
        
        config_case = self.config_limpieza['reglas_limpieza']['texto']['case']
        if config_case == 'lower':
            serie_limpia = serie_limpia.str.lower()
        elif config_case == 'upper':
            serie_limpia = serie_limpia.str.upper()
        elif config_case == 'title':
            serie_limpia = serie_limpia.str.title()
        
        return serie_limpia
    
    def _calcular_total_ventas(self):
        """Calcular columna total_ventas - OPTIMIZADO"""
        if 'total_ventas' not in self.df.columns:
            if 'cantidad' in self.df.columns and 'precio_unitario' in self.df.columns:
                print("💰 Calculando columna total_ventas...")
                
                # Asegurar que sean numéricas (ya deberían estar limpias)
                if 'cantidad' not in self.df.select_dtypes(include=[np.number]):
                    self.df['cantidad'] = pd.to_numeric(self.df['cantidad'], errors='coerce')
                if 'precio_unitario' not in self.df.select_dtypes(include=[np.number]):
                    self.df['precio_unitario'] = pd.to_numeric(self.df['precio_unitario'], errors='coerce')
                
                self.df['total_ventas'] = self.df['cantidad'] * self.df['precio_unitario']
                
                if 'descuento' in self.df.columns:
                    if 'descuento' not in self.df.select_dtypes(include=[np.number]):
                        self.df['descuento'] = pd.to_numeric(self.df['descuento'], errors='coerce')
                    self.df['total_ventas'] = self.df['total_ventas'] * (1 - self.df['descuento'] / 100)
                
                print(f"   ✅ Total_ventas calculado: {len(self.df['total_ventas'].dropna())} registros válidos")
    
    def _calcular_estadisticas_limpieza(self, registros_originales: int):
        """Calcular estadísticas - OPTIMIZADO"""
        nulos_por_columna = self.df.isnull().sum()
        total_celdas = len(self.df) * len(self.df.columns)
        
        self.estadisticas_limpieza = {
            'registros_originales': registros_originales,
            'registros_finales': len(self.df),
            'columnas_finales': len(self.df.columns),
            'nulos_por_columna': nulos_por_columna.to_dict(),
            'registros_eliminados': registros_originales - len(self.df),
            'porcentaje_completitud': (1 - nulos_por_columna.sum() / total_celdas) * 100 if total_celdas > 0 else 0
        }
    
    def _mostrar_resumen_limpieza(self):
        """Mostrar resumen - OPTIMIZADO"""
        print("\n" + "="*60)
        print("📊 RESUMEN DE LIMPIEZA AUTOMATIZADA")
        print("="*60)
        
        stats = self.estadisticas_limpieza
        print(f"📈 Registros originales: {stats['registros_originales']:,}")
        print(f"📈 Registros finales: {stats['registros_finales']:,}")
        print(f"📊 Columnas finales: {stats['columnas_finales']}")
        print(f"🗑️  Registros eliminados: {stats['registros_eliminados']:,}")
        print(f"✅ Completitud: {stats['porcentaje_completitud']:.1f}%")
        
        print("\n📋 COLUMNAS FINALES:")
        for i, columna in enumerate(self.df.columns, 1):
            nulos = stats['nulos_por_columna'][columna]
            total = len(self.df)
            porcentaje_valido = ((total - nulos)/total)*100
            print(f"   {i:2d}. {columna}: {total - nulos}/{total} válidos ({porcentaje_valido:.1f}%)")
    
    def guardar_datos_limpios(self, archivo_salida: str = "datos_limpios.csv"):
        """Guardar datos limpios - OPTIMIZADO"""
        try:
            self.df = self._eliminar_columnas_duplicadas(self.df)
            self.df.to_csv(archivo_salida, index=False, encoding='utf-8')
            print(f"\n💾 Datos guardados en: {archivo_salida}")
            return True
        except Exception as e:
            print(f"❌ Error guardando archivo: {e}")
            return False

# FUNCIÓN DE USO RÁPIDO OPTIMIZADA
def limpiar_csv_automatico(archivo_csv: str, archivo_salida: str = "datos_limpios.csv") -> pd.DataFrame:
    """
    Función de uso rápido para limpieza automática - OPTIMIZADA
    """
    limpiador = LimpiezaAutomatizada(archivo_csv)
    
    # Detectar estructura con menos datos
    estructura = limpiador.detectar_estructura()
    print("\n🔍 MAPEO AUTOMÁTICO PROPUESTO:")
    for orig, nuevo in estructura['mapeo_propuesto'].items():
        print(f"   '{orig}' → '{nuevo}'")
    
    # Aplicar limpieza optimizada
    df_limpio = limpiador.aplicar_limpieza()
    
    if not df_limpio.empty:
        limpiador.guardar_datos_limpios(archivo_salida)
    
    return df_limpio

if __name__ == "__main__":
    archivo = "RWventas.csv"
    
    if os.path.exists(archivo):
        print("🚀 INICIANDO LIMPIEZA AUTOMATIZADA (VERSIÓN OPTIMIZADA)")
        df_resultado = limpiar_csv_automatico(archivo, "ventas_limpio_auto.csv")
        print("\n🎉 PROCESO COMPLETADO!")
    else:
        print(f"❌ Archivo {archivo} no encontrado")