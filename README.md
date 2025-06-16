## Sobre el modelo de degradación 
El código en `degradation_model.ipynb` utiliza una base de datos pública de Standford, para no subirlo al repo, dejo el link al su ubicación

https://drive.google.com/drive/folders/1mSHdfOCpTYmt3MhcqC44RVpwrRL-YhxW?usp=sharing

# Explicación del Código de Valorización de Baterías

Este repositorio contiene un modelo para la valorización económica de baterías considerando su degradación y perfil de uso.

# Modelo de Batería (`battery.py`)

Este archivo contiene la implementación del modelo de degradación de batería utilizado para simular el comportamiento y la vida útil de una batería bajo diferentes condiciones de uso.

## Descripción de la Clase

La clase principal del archivo es `BatteryModel` (o el nombre correspondiente en tu código). Esta clase permite crear una instancia de una batería con parámetros específicos y simular su degradación a lo largo del tiempo.

### Parámetros para Instanciar el Modelo

Al crear una instancia de la clase, puedes definir los siguientes parámetros:

- **`Qmax`**: Capacidad maxima inicial de la batería en Ah.
Aquí se definen los datos de una campaña de degradación para obtener la vida util de la batería (datos usualmente encontrados en el datasheet)
- **`life_cycles`**: Número máximo de ciclos equivalentes que la batería puede realizar antes de llegar al fin de vida útil.
- **`degradation_percentage`**: Estado de salud al fin de la vida útil
- **`ds_SR`**: Rango de estado de carga del perfil nominal usado para obtener los life_cycles

Ejemplo de inicialización:
```python
from models.battery import BatteryModel

battery = BatteryModel(
    Qmax=100,                    # Capacidad máxima inicial en Ah
    life_cycles=5000,            # Número máximo de ciclos equivalentes
    degradation_percentage=0.8,  # Estado de salud al fin de vida útil (por ejemplo, 80%)
    ds_SR=0.8                    # Rango de estado de carga del perfil nominal
)
```

### Funciones de Inicialización del Modelo de Batería

Al crear una instancia de la clase `Battery_Degradation_Model`, se ejecutan varias funciones de inicialización que preparan los componentes internos necesarios para simular la degradación de la batería de manera precisa. A continuación se describen las funciones principales según la implementación en `battery.py`:

#### 1. `self.setup_knn()`
Esta función configura un modelo de regresión k-Nearest Neighbors (k-NN) utilizando los datos de degradación definidos en los parámetros del modelo. El modelo k-NN se entrena para predecir el factor de degradación de la batería en función de variables como el rango de estado de carga (SR), el promedio de estado de carga (ASR) y el porcentaje de degradación estándar. Esto permite interpolar el comportamiento de degradación bajo diferentes condiciones de operación.

#### 2. `self.set_kde()`
Esta función inicializa un estimador de densidad por núcleos (Kernel Density Estimation, KDE) usando datos de valores de eta (parámetro de degradación) leídos desde un archivo CSV externo. El KDE se utiliza para introducir incertidumbre en la simulación de la degradación, permitiendo que el modelo refleje la variabilidad observada en los datos reales.

#### 3. `self.set_std_cycles()`
Esta función ajusta los parámetros internos del modelo para definir los ciclos estándar de operación. Calcula el número equivalente de ciclos de vida útil considerando el rango de estado de carga y ajusta el parámetro de degradación para que el modelo refleje correctamente la vida útil esperada al 80% de la capacidad nominal.

---

Estas funciones aseguran que el modelo de batería cuente con herramientas estadísticas y de aprendizaje necesarias para simular su comportamiento de manera realista y flexible, adaptándose a distintos perfiles de uso y condiciones de operación.

### Función `get_factor`

La función `get_factor(ssr, assr, temp)` es fundamental para el modelo, ya que calcula el factor de degradación de la batería en función de las condiciones de operación actuales:

- **`ssr`**: Rango de estado de carga del subciclo (State of Charge Range).
- **`assr`**: Promedio de estado de carga del subciclo.
- **`temp`**: Temperatura de operación.

El método utiliza el modelo k-NN para predecir el factor de degradación base, ajusta este valor según la temperatura usando un polinomio calibrado, y finalmente introduce incertidumbre mediante el muestreo del KDE. El resultado es un valor `etak` que representa el factor de degradación para ese ciclo bajo las condiciones dadas.

## Caso de Uso Completo

A continuación se muestra un ejemplo de cómo utilizar el modelo de batería definido en `battery.py`:

```python
from models.battery import Battery_Degradation_Model

# 1. Crear una instancia del modelo de batería con los parámetros principales
battery = Battery_Degradation_Model(
    Qmax=100,                    # Capacidad máxima inicial en Ah
    life_cycles=5000,            # Número máximo de ciclos equivalentes
    degradation_percentage=0.8,  # Estado de salud al fin de vida útil (por ejemplo, 80%)
    ds_SR=100                    # Rango de estado de carga del perfil nominal
)

# 2. Simular varios ciclos de operación
for ciclo in range(1, 101):
    # Definir condiciones del ciclo (pueden variar según el escenario)
    ssr = 80    # Ejemplo: rango de SOC del subciclo
    assr = 50   # Ejemplo: SOC promedio del subciclo
    temperatura = 30

    # 3. Calcular el factor de degradación para este ciclo
    factor = battery.get_factor(
        ssr=ssr,
        assr=assr,
        temp=temperatura
    )

    # 4. Actualizar el estado de salud de la batería (ejemplo simple)
    battery.parameters["Qmax"] *= factor

    print(f"Ciclo {ciclo}: Capacidad restante = {battery.parameters['Qmax']:.2f} Ah")

    # 5. Verificar si la batería ha llegado al fin de vida útil
    if battery.parameters["Qmax"] <= (100 * battery.parameters["degradation_percentage"]):
        print("La batería ha llegado al fin de su vida útil.")
        break
```

Este flujo permite simular la degradación de la batería ciclo a ciclo, considerando las condiciones de operación y los parámetros definidos en la instancia del modelo.

## Resumen

- **`Battery_Degradation_Model`** permite simular la degradación de una batería bajo diferentes condiciones.
- Las funciones de inicialización configuran los modelos internos de aprendizaje y estadística.
- **`get_factor`** calcula el impacto de un ciclo de uso sobre la degradación.
- El modelo puede integrarse fácilmente en simulaciones más grandes o análisis de valorización.

Consulta el código fuente y los comentarios para más detalles sobre los parámetros y la lógica interna del modelo.