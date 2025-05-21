import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constantes
rho = 1.225  # densidad del aire (kg/m³)
Cd = 0.29    # coeficiente aerodinámico del ATS
A = 2.2      # área frontal m²
watts_to_hp = 1 / 745.7
hp_to_watts = 745.7

# Funciones
def potencia_necesaria_kph(vel_kph):
    v = vel_kph / 3.6
    P = 0.5 * rho * Cd * A * v**3
    return P * watts_to_hp

def velocidad_maxima_kph(hp):
    P = hp * hp_to_watts
    v = (2 * P / (rho * Cd * A))**(1/3)
    return v * 3.6

# UI
st.title("Simulador de Velocidad vs Caballos de Fuerza")
st.write("Aplicación basada en el comportamiento aerodinámico de tu Cadillac ATS 2.0T")

option = st.radio("¿Qué deseas calcular?", ["Potencia necesaria para una velocidad", "Velocidad máxima con X HP"])

if option == "Potencia necesaria para una velocidad":
    vel = st.slider("Velocidad (km/h)", 50, 350, 150)
    hp = potencia_necesaria_kph(vel)
    st.success(f"Potencia necesaria: {hp:.2f} HP")
else:
    potencia = st.slider("Potencia disponible (HP)", 50, 1000, 272)
    vel = velocidad_maxima_kph(potencia)
    st.success(f"Velocidad máxima teórica: {vel:.2f} km/h")

# Gráfica
vels = np.linspace(50, 350, 300)
hps = [potencia_necesaria_kph(v) for v in vels]

st.subheader("Curva Potencia vs Velocidad")
fig, ax = plt.subplots()
ax.plot(vels, hps, label="HP necesarios")
ax.set_xlabel("Velocidad (km/h)")
ax.set_ylabel("Potencia (HP)")
ax.grid(True)
ax.legend()
st.pyplot(fig)
