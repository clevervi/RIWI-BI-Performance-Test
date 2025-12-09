# Conexión Power BI con PostgreSQL  
## Análisis de Datos - Configuración de Power BI  

**Objetivo:** Conectar Power BI a la base de datos `RWVentas` en PostgreSQL para crear un modelo de datos confiable siguiendo el esquema de base de datos proporcionado (`modelo_rwventas.sql`).  

---

## 📋 Criterios de Aceptación  

✅ Conexión estable y funcional  
✅ Modelo estrella correctamente implementado  
✅ Documentación con capturas del modelo en Power BI  
✅ Validación de integridad y consistencia de datos  

---

## 1. Prerequisitos  

### Software Necesario:  
- **Power BI Desktop** (última versión)  
- **PostgreSQL** instalado y ejecutándose  
- **Base de datos RWVentas** configurada con las tablas del script `modelo_rwventas.sql`  
- Credenciales de acceso (usuario, contraseña, host, puerto)  

### Información de Conexión:  
```
Host: localhost (o IP del servidor)  
Puerto: 5432  
Base de datos: RWVentas  
Usuario: [tu_usuario]  
Contraseña: [tu_contraseña]  
```

---

## 2. Configuración de Conexión Power BI ↔ PostgreSQL  

### Paso 1: Abrir Power BI Desktop  
1. Inicia **Power BI Desktop**  
2. Haz clic en **"Obtener datos"** en la cinta de opciones  
3. O usa el menú: **Inicio → Obtener datos**  

### Paso 2: Seleccionar PostgreSQL  
1. En la ventana de "Obtener datos", busca **"PostgreSQL"**  
2. Selecciona **"PostgreSQL database"**  
3. Haz clic en **"Conectar"**  

### Paso 3: Configurar Parámetros de Conexión  
En la ventana de conexión, ingresa:  

```
Servidor: localhost:5432  
Base de datos: RWVentas  
```

**Opciones avanzadas:**  
- **Modo de conectividad de datos:** DirectQuery (para datos en tiempo real) o Import (para carga completa)  
- **Instrucción SQL (opcional):** Puedes escribir consultas personalizadas  

**Recomendación:** Usa **Import** para mejor rendimiento en análisis.  

### Paso 4: Autenticación  
1. Selecciona **"Base de datos"** en el panel izquierdo  
2. Ingresa:  
   - **Nombre de usuario:** tu_usuario_postgres  
   - **Contraseña:** tu_contraseña  
3. Marca **"Seleccionar el nivel al que se aplica la configuración"**: Base de datos  
4. Haz clic en **"Conectar"**  

### Paso 5: Seleccionar Tablas  
Una vez conectado, verás el navegador de tablas:  

1. Busca y selecciona las tablas necesarias:  
   - ✅ **fact_ventas** (tabla de hechos)  
   - ✅ **dim_producto** (dimensión)  
   - ✅ **dim_geografia** (dimensión)  
   - ✅ **dim_canal** (dimensión)  

2. **Vista previa de datos:** Haz clic en cada tabla para ver una muestra  

3. Opciones:  
   - **Cargar:** Importa directamente las tablas  
   - **Transformar datos:** Abre Power Query Editor para limpieza previa  

**Recomendación:** Usa **"Transformar datos"** para verificar y ajustar tipos de datos.  

---

## 3. Creación del Modelo Estrella  

### ¿Qué es un Modelo Estrella?  
Un **modelo estrella** es un esquema de base de datos optimizado para análisis, donde:  
- **Tabla de Hechos (Fact Table):** Contiene métricas cuantificables (ej: cantidad, precio_unitario, total_ventas)  
- **Tablas de Dimensiones (Dimension Tables):** Contienen atributos descriptivos (ej: producto, geografía, canal)  

### Estructura del Modelo RWVentas según el script SQL:  

```
        ┌─────────────────┐
        │   DIM_PRODUCTO  │
        │   (Producto)    │
        └────────┬────────┘
                 │
                 │ id_producto
                 │
        ┌────────▼──────────────────────────────────────┐
        │             FACT_VENTAS                       │
        │  ────────────────────────────────             │
        │  • fecha                                      │
        │  • id_producto (FK)                           │
        │  • id_geografia (FK)                          |
        │  • id_canal (FK)                              |
        │  • cantidad                                   |
        │  • precio_unitario                            |
        │  • descuento                                  |
        │  • costo_envio                                |
        │  • total_ventas                               |
        └────────┬───────────────────────────┬──────────┘
                 │                           │
     id_geografia│                  id_canal │
                 │                           │
        ┌────────▼─────────┐       ┌─────────▼─────────┐
        │ DIM_GEOGRAFIA    │       │   DIM_CANAL       │
        │──────────────────│       │───────────────────│
        │• id_geografia    │       │• id_canal         │
        │• ciudad          │       │• tipo_venta       │
        │• pais            │       │• tipo_cliente     │
        └──────────────────┘       └───────────────────┘
```

### Configuración de Relaciones en Power BI:  

#### Paso 1: Acceder a Vista de Modelo  
1. En Power BI Desktop, haz clic en el icono **"Modelo"** en el panel izquierdo  
2. Verás un diagrama de todas las tablas cargadas  

#### Paso 2: Crear Relaciones  

**Relación 1: FACT_VENTAS → DIM_PRODUCTO**  
- Arrastra `id_producto` de `FACT_VENTAS` a `id_producto` de `DIM_PRODUCTO`  
- Configuración:  
  - **Cardinalidad:** Muchos a uno (*:1)  
  - **Dirección del filtro cruzado:** Única (desde dimensión a hechos)  
  - **Activar relación:** Sí  

**Relación 2: FACT_VENTAS → DIM_GEOGRAFIA**  
- Arrastra `id_geografia` de `FACT_VENTAS` a `id_geografia` de `DIM_GEOGRAFIA`  
- Configuración:  
  - **Cardinalidad:** Muchos a uno (*:1)  
  - **Dirección del filtro cruzado:** Única  
  - **Activar relación:** Sí  

**Relación 3: FACT_VENTAS → DIM_CANAL**  
- Arrastra `id_canal` de `FACT_VENTAS` a `id_canal` de `DIM_CANAL`  
- Configuración:  
  - **Cardinalidad:** Muchos a uno (*:1)  
  - **Dirección del filtro cruzado:** Única  
  - **Activar relación:** Sí  

#### Paso 3: Validar Relaciones  
✅ Verifica que las líneas de relación conecten correctamente las tablas  
✅ Las relaciones deben mostrar "1" en el lado de dimensión y "*" en el lado de hechos  
✅ No debe haber relaciones ambiguas o circulares  

---

## 4. Transformación y Validación de Datos  

### En Power Query Editor:  

#### 4.1. Validar Tipos de Datos  
Para cada tabla, verifica:  

**FACT_VENTAS:**  
- `fecha`: Fecha/Hora  
- `id_producto`: Número entero  
- `id_geografia`: Número entero  
- `id_canal`: Número entero  
- `cantidad`: Número decimal  
- `precio_unitario`: Número decimal  
- `descuento`: Número decimal  
- `costo_envio`: Número decimal  
- `total_ventas`: Número decimal  

**DIM_PRODUCTO:**  
- `id_producto`: Número entero  
- `producto`: Texto  
- `tipo_producto`: Texto  

**DIM_GEOGRAFIA:**  
- `id_geografia`: Número entero  
- `ciudad`: Texto  
- `pais`: Texto  

**DIM_CANAL:**  
- `id_canal`: Número entero  
- `tipo_venta`: Texto  
- `tipo_cliente`: Texto  

#### 4.2. Eliminar Columnas Innecesarias  
- Elimina columnas que no se usarán en análisis  
- Ejemplo: Campos de auditoría internos, timestamps de sistema  

#### 4.3. Crear Columnas Calculadas (si es necesario)  
```
// Ejemplo: Crear columna de Margen  
Margen = [total_ventas] - ([cantidad] * [precio_unitario])  

// Ejemplo: Categorizar por región  
Region = IF([pais] = "Colombia", "Local", "Internacional")  
```

#### 4.4. Aplicar y Cerrar  
- Revisa todos los cambios en la vista de "Columnas"  
- Haz clic en **"Cerrar y aplicar"** para cargar datos al modelo  

---

## 5. Validación de Integridad y Consistencia  

### 5.1. Verificar Cardinalidad  
```
// Medida para verificar claves únicas en dimensiones  
Productos_Unicos = DISTINCTCOUNT(DIM_PRODUCTO[id_producto])  
Geografia_Unica = DISTINCTCOUNT(DIM_GEOGRAFIA[id_geografia])  
Canales_Unicos = DISTINCTCOUNT(DIM_CANAL[id_canal])  

// Comparar con total de filas  
Total_Filas_Productos = COUNTROWS(DIM_PRODUCTO)  
```

**✅ Resultado esperado:** Productos_Unicos debe ser igual a Total_Filas_Productos  

### 5.2. Validar Relaciones con DAX  
```
// Contar ventas por producto  
Ventas_Por_Producto =   
CALCULATE(  
    COUNTROWS(FACT_VENTAS),  
    ALLEXCEPT(FACT_VENTAS, DIM_PRODUCTO[id_producto])  
)  
```

### 5.3. Verificar Datos Huérfanos  
```
// Detectar ventas sin producto asignado  
Ventas_Sin_Producto =   
CALCULATE(  
    COUNTROWS(FACT_VENTAS),  
    ISBLANK(RELATED(DIM_PRODUCTO[producto]))  
)  
```

**✅ Resultado esperado:** Debe ser 0  

### 5.4. Validar Totales  
```
// Comparar total de ventas calculado vs. almacenado  
Total_Ventas_Calculado = SUMX(FACT_VENTAS, [cantidad] * [precio_unitario])  
Total_Ventas_Almacenado = SUM(FACT_VENTAS[total_ventas])  

// Diferencia  
Diferencia_Ventas = [Total_Ventas_Calculado] - [Total_Ventas_Almacenado]  
```

**✅ Resultado esperado:** Diferencia debe ser cercana a 0 (tolerancia de redondeo)  

---

## 6. Capturas y Documentación del Modelo  

### 📸 Capturas Requeridas:  

#### Captura 1: Vista de Modelo Completo  
- Muestra todas las tablas y sus relaciones  
- Archivo sugerido: `modelo_estrella_rwventas.png`  

**Cómo tomar la captura:**  
1. En Power BI, ve a Vista de Modelo  
2. Usa Ctrl+A para seleccionar todo  
3. Ajusta el zoom para ver todo el modelo  
4. Usa la herramienta de recortes de Windows o presiona Imprimir Pantalla  
5. Guarda la imagen  

#### Captura 2: Detalle de Relaciones  
- Haz clic en una línea de relación  
- Captura el panel de propiedades que muestra:  
  - Tablas relacionadas  
  - Columnas de unión  
  - Cardinalidad  
  - Dirección del filtro  

#### Captura 3: Transformaciones en Power Query  
- Muestra los pasos aplicados en Power Query Editor  
- Captura el panel de "Pasos aplicados"  

---

## 7. Medidas DAX Básicas  

Para facilitar el análisis, crea estas medidas:  

```
// Medida: Total de Ventas  
Total_Ventas = SUM(FACT_VENTAS[total_ventas])  

// Medida: Cantidad Total Vendida  
Cantidad_Total = SUM(FACT_VENTAS[cantidad])  

// Medida: Ticket Promedio  
Ticket_Promedio = DIVIDE([Total_Ventas], [Cantidad_Total], 0)  

// Medida: Total de Productos Únicos Vendidos  
Productos_Vendidos = DISTINCTCOUNT(FACT_VENTAS[id_producto])  

// Medida: Margen Promedio  
Margen_Promedio = AVERAGE(FACT_VENTAS[total_ventas] - (FACT_VENTAS[cantidad] * FACT_VENTAS[precio_unitario]))  
```

---

## 8. Solución de Problemas Comunes  

### ❌ Error: "No se puede conectar al servidor"  
**Solución:**  
- Verifica que PostgreSQL esté ejecutándose  
- Confirma el puerto correcto (5432 por defecto)  
- Verifica el firewall de Windows  
- Asegúrate de que pg_hba.conf permita conexiones desde Power BI  

### ❌ Error: "Error de autenticación"  
**Solución:**  
- Verifica usuario y contraseña  
- Asegúrate de que el usuario tenga permisos de lectura en las tablas  
- Confirma que el método de autenticación en PostgreSQL sea compatible  

### ❌ Error: "Relación ambigua"  
**Solución:**  
- Revisa que no haya múltiples rutas entre tablas  
- Desactiva relaciones redundantes  
- Usa funciones USERELATIONSHIP() en DAX si necesitas cambiar relaciones activas  

### ❌ Error: "Cardinalidad incorrecta"  
**Solución:**  
- Verifica que las claves primarias sean únicas en dimensiones  
- Elimina duplicados en tablas de dimensión  
- Usa DISTINCTCOUNT para validar unicidad  

---

## 9. Checklist de Validación Final  

Antes de continuar, verifica:  

- [ ] **Conexión exitosa a PostgreSQL**  
- [ ] **Todas las tablas necesarias cargadas**  
- [ ] **Relaciones creadas correctamente (modelo estrella)**  
- [ ] **Cardinalidad verificada (muchos a uno)**  
- [ ] **Tipos de datos correctos en todas las columnas**  
- [ ] **Sin datos huérfanos o nulos en claves foráneas**  
- [ ] **Medidas DAX básicas creadas**  
- [ ] **Capturas del modelo guardadas**  
- [ ] **Documentación completa**  

---

## 10. Próximos Pasos →  

Una vez completada la configuración, estarás listo para:  

✅ **Creación de Dashboards en Power BI**  
- Diseñar visualizaciones avanzadas  
- Implementar filtros y segmentadores  
- Crear KPIs interactivos  
- Publicar el dashboard  

---

## 📚 Recursos Adicionales  

- **Documentación oficial Power BI:** https://docs.microsoft.com/power-bi/  
- **Guía de DAX:** https://dax.guide/  
- **PostgreSQL y Power BI:** https://www.postgresql.org/docs/  
- **Mejores prácticas de modelado:** https://powerbi.microsoft.com/data-modeling/  

---

## ✅ Conclusiones  

### Logros:  
- ✅ Conexión estable y funcional entre Power BI y PostgreSQL  
- ✅ Modelo estrella implementado correctamente según el esquema de base de datos proporcionado  
- ✅ Relaciones validadas con cardinalidad adecuada  
- ✅ Integridad de datos verificada  
- ✅ Documentación completa con capturas  

### Estado:  
**Power BI está listo para crear dashboards interactivos** 🎉