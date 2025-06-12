from models.battery import BatteryModel
from functions import synthetic_profile, total_cycle, profile_repeat, valorización
import matplotlib.pyplot as plt
import numpy as np

## CONFIGURACIÓN DE LA SIMULACIÓN ##

# parametros batería degradada
Q_max_degradated = 4.753  # Carga nominal (Ah) de la batería degradada
initial_SOH_degrated = 0.80  # Initial State of Health of the battery
life_cycles_degradated = 500  # Ciclos de vida de la batería degradada
degradation_percentage_degradated = 0.8  # Porcentaje de degradación de la batería degradada

# parametros de batería ideal
Q_max_ideal = 3.070  # Carga nominal (Ah) de la batería ideal
initial_SOH_ideal = 1  # Initial State of Health of the battery
life_cycles_ideal = 500  # Ciclos de vida de la batería ideal
degradation_percentage_ideal = 0.73  # Porcentaje de degradación de la batería ideal

# definición del perfil de uso
# aquí se puede importar un perfil dado o definir uno sintético
# (en este caso, se usa un perfil sintético)
aplication_cap = 2.5 # hay que definir la capacidad minima exigida por la aplicación
amb_temp = 25 # se define la temperatura ambiente de la aplicación en grados Celsius
cap_profile = synthetic_profile(dt=1, dis_curr=-0.5, charg_curr=0.5, 
                                lower_capacity=-aplication_cap, upper_capacity=aplication_cap, N=1)




# Definimos los modelos de baterías a comparar
degradated_batt = BatteryModel(Q_max_degradated,life_cycles_degradated, degradation_percentage_degradated) 
ideal_batt = BatteryModel(Q_max_ideal,life_cycles_ideal, degradation_percentage_ideal)

# Definimos la repetición del perfil de uso
aplication_profile = profile_repeat(cap_profile, N=10000)

# Definimos los parámetros de la batería degradada
deg_terminal_SOH = aplication_cap/degradated_batt.parameters["Qmax"]  # Terminal State of Health of the battery
deg_terminal_SOH = max(deg_terminal_SOH, 0.6)  # Ensure terminal SOH is not below 60%

# Definimos los parámetros de la batería ideal
ideal_terminal_SOH = aplication_cap/ideal_batt.parameters["Qmax"]  # Terminal State of Health of the battery
ideal_terminal_SOH = max(ideal_terminal_SOH, 0.6)  # Ensure terminal SOH is not below 60%

# Obtenemos el número total de ciclos equivalentes para la batería degradada
total_cycles_degradated, _, _ = total_cycle(
    degradated_batt, initial_SOH_degrated, deg_terminal_SOH, cap_profile, amb_temp, initial_SOC=100
)
# Obtenemos el número total de ciclos equivalentes para la batería ideal
total_cycles_ideal, _, _ = total_cycle(
    ideal_batt, initial_SOH_ideal, ideal_terminal_SOH, cap_profile, amb_temp, initial_SOC=100
)

# print the total cycles for each battery
print(f"La batería degradada puede ejecutar: {total_cycles_degradated:.2f} ciclos equivalentes de la aplicación")
print(f"La batería ideal puede ejecutar: {total_cycles_ideal:.2f} ciclos equivalentes de la aplicación")

# ejemplo de valorización de la batería degradada
valor_ideal = 5.2  # Ideal value of the battery in monetary units

# Calculamos el valor de la batería degradada
valor_deg_id = valorización(initial_SOH_degrated, degradated_batt.parameters["Qmax"], aplication_cap, valor_ideal, 
                            total_cycles_degradated, total_cycles_ideal)
print(f"Valor económico de la batería ideal es: {valor_ideal:.2f} monetary units")
print(f"Valor económico de la batería degradada es: {valor_deg_id:.2f} monetary units")

# cálculo de costo por ciclo equivalente de la batería degradada
costo_por_ciclo_degradated = valor_deg_id / total_cycles_degradated
print(f"Costo por ciclo de la batería degradada (usando precio de batería ideal): {costo_por_ciclo_degradated:.5f} monetary units")

costo_por_ciclo_ideal = valor_ideal / total_cycles_ideal
print(f"Costo por ciclo de la batería ideal: {costo_por_ciclo_ideal:.5f} monetary units")

