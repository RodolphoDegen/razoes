import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do CSV
df = pd.read_csv('/home/usuario/Documents/modulos_ROD/plots/razoes/teste.txt')

# Selecionar o canal específico e os ângulos de fase
canal_especifico = 'canal30'
angulos_fase = df['phase']
reflectancia = df[canal_especifico]

# Criar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(angulos_fase, reflectancia, marker='o', linestyle='', markersize=6)
plt.xlabel('Ângulo de Fase (graus)')
plt.ylabel('Reflectância')
plt.title(f'Reflectância do {canal_especifico} pelo Ângulo de Fase')
plt.grid(True)
plt.show()
