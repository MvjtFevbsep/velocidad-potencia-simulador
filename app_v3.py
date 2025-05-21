import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURACION DE PAGINA
st.set_page_config(page_title="Simulador Vehicular V3", layout="centered")
st.title("Simulador de Velocidad, Potencia y Torque")

# PANEL LATERAL - INPUTS DINAMICOS
st.sidebar.header("Configuración del entorno")

air_density = st.sidebar.number_input("Densidad del aire (kg/m³)", value=1.225, step=0.01)
Cd = st.sidebar.number_input("Coeficiente aerodinámico (Cd)", value=0.29, step=0.01)
A = st.sidebar.number_input("Area frontal (m²)", value=2.2, step=0.1)
Cr = st.sidebar.number_input("Coef. resistencia rodadura", value=0.015, step=0.001)

efficiency = st.sidebar.slider("Eficiencia mecánica (%)", min_value=10, max_value=100, value=85)

st.sidebar.header("Parámetros del vehículo")
power_hp = st.sidebar.number_input("Potencia disponible (HP)", value=272)
rpm = st.sidebar.number_input("RPM máximas del motor", value=5500)
vehicle_weight = st.sidebar.number_input("Peso del vehículo (kg)", value=1550)
passengers = st.sidebar.number_input("Número de pasajeros", value=1)
passenger_weight = st.sidebar.number_input("Peso por persona (kg)", value=75)
extra_cargo = st.sidebar.number_input("Carga adicional (kg)", value=0)

final_drive_ratio = st.sidebar.number_input("Relación de transmisión final", value=3.23, step=0.01)
tire_radius = st.sidebar.number_input("Radio del neumático (m)", value=0.34, step=0.01)

# CALCULOS BASICOS
power_watts = power_hp * 745.7
mass_total = vehicle_weight + passengers * passenger_weight + extra_cargo

# FUNCIONES

def potencia_necesaria(vel_kph):
    v = vel_kph / 3.6
    drag_force = 0.5 * air_density * Cd * A * v**2
    rolling_resistance = Cr * mass_total * 9.81
    total_force = drag_force + rolling_resistance
    required_power = total_force * v / (efficiency / 100)
    return required_power / 745.7

def velocidad_maxima():
    # Inverso: encuentra velocidad donde potencia requerida ~= disponible
    for v in range(10, 500):
        if potencia_necesaria(v) > power_hp:
            return v - 1
    return 500

def torque_salida():
    torque_engine = (power_watts * 60) / (2 * np.pi * rpm)
    torque_wheel = torque_engine * final_drive_ratio * (efficiency / 100)
    return torque_engine, torque_wheel

# CALCULOS FINALES
v_max = velocidad_maxima()
torque_engine, torque_wheel = torque_salida()

# RESULTADOS
st.subheader("Resultados:")
st.write(f"**Peso total del vehículo:** {mass_total:.1f} kg")
st.write(f"**Velocidad máxima estimada:** {v_max} km/h")
st.write(f"**Torque en motor:** {torque_engine:.1f} Nm")
st.write(f"**Torque estimado en ruedas:** {torque_wheel:.1f} Nm")

# GRAFICA
vel_range = np.linspace(10, 350, 300)
required_powers = [potencia_necesaria(v) for v in vel_range]

fig, ax = plt.subplots()
ax.plot(vel_range, required_powers, label='Potencia requerida (HP)')
ax.axhline(power_hp, color='r', linestyle='--', label='Potencia disponible')
ax.set_xlabel("Velocidad (km/h)")
ax.set_ylabel("Potencia (HP)")
ax.set_title("Curva de potencia requerida vs velocidad")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.caption("Versión 3.0 - Modelo de simulación vehicular ampliado")

