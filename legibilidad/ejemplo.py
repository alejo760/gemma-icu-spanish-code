\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importar las funciones necesarias de la biblioteca legibilidad
from legibilidad import fernandez_huerta, szigriszt_pazos, gutierrez, mu, crawford, interpretaL, interpretaP, inflesz, gutierrez_interpret, mu_interpret

# Texto de ejemplo para analizar
texto_ejemplo = """
Este es un texto de ejemplo para probar las funciones de legibilidad.
Contiene varias frases con diferentes longitudes y palabras de distinta complejidad.
El objetivo es calcular los diferentes índices de legibilidad disponibles en la biblioteca.
Se incluyen números como 123 y 45.67 para verificar la conversión a palabras.
¿Será fácil de leer este texto? ¡Veámoslo!
"""

# Calcular los diferentes índices de legibilidad
fh_score = fernandez_huerta(texto_ejemplo)
sp_score = szigriszt_pazos(texto_ejemplo)
g_score = gutierrez(texto_ejemplo)
mu_score = mu(texto_ejemplo)
c_score = crawford(texto_ejemplo)

# Imprimir los resultados
print("--- Resultados de Legibilidad ---")
print(f"Índice Fernández Huerta: {fh_score} ({interpretaL(fh_score)})")
print(f"Índice Szigriszt-Pazos (INFLESZ): {sp_score} ({inflesz(sp_score)})")
print(f"Índice Gutiérrez de Polini: {g_score} ({gutierrez_interpret(g_score)})")
print(f"Índice Mu Legibility: {mu_score} ({mu_interpret(mu_score)})")
print(f"Fórmula Crawford (años escolaridad): {c_score}")

print("\n--- Interpretaciones Adicionales ---")
print(f"Interpretación Szigriszt-Pazos (original): {interpretaP(sp_score)}")
