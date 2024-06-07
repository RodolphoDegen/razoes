import matplotlib.pyplot as plt
import numpy as np
import modulo_hapke as pyast
from ajustes_Itokawa_v1 import *
import os
import pandas as pd

#####################  Teste
fMet='Altaameem_opc.dat'
fFe='fe_optical_constants.txt'

dname=''
fname = '/home/usuario/Documents/modulos_ROD/plots/razoes/teste2_2.txt'
fdat=os.path.join(dname,fname)

# Carregar os dados do CSV
df = pd.read_csv('/home/usuario/Documents/modulos_ROD/plots/razoes/teste.txt')

aS = (df['aS_phi001']+df['aS_phi500'])/2
aS_mean = np.mean(aS)

volfe = (df['volfe_phi001']+df['volfe_phi500'])/2
volfe_mean = np.mean(volfe)

# Selecionar o canal específico e os ângulos de fase
canal_especifico = 'canal30'
angulos_fase = df['phase']
reflectancia = df[canal_especifico]

### Valores iniciais
x0={'aS':aS_mean,
    'aL':2000,
    'theta':np.radians(25),
    'phi':0.25,
    'volfe':volfe_mean}

# Precisamos ler os espectros da Hayabusa
nObs, specID, g, gR, i, muI, e, muE, nK, R, wvC = leHayabusa(fdat)

# Precisamos agora das constantes óticas interpoladas para os comprimentos de onda dos espectros
n, k, fen, fek = leConstantesOticas(fMet, fFe, wvC)

# Calculamos agora as constantes óticas modificadas pelo nano Ferro.
nmix, kmix = np.zeros(nK), np.zeros(nK)
for ii in range(nK):
    nmix[ii], kmix[ii] = past.maxwell_garnett(n, k[ii], fen[ii], fek[ii], x0['volfe'])

# Lista para armazenar as reflectâncias calculadas para cada valor de gR de 0 a 40
reflectancias_por_gR = []

# Calcular a reflectância para cada valor de gR de 0 a 40
for jj in range(len(muI)):
    reflectancias = []
    for gR in range(41):
        # Calcular a reflectância com base nos parâmetros
        Rc = np.pi * past._Hapke_IMSA_phys_nu4(muI[jj],
                                               muE[jj],
                                               gR,
                                               wvC,
                                               nmix,
                                               kmix,
                                               x0['aS'],
                                               x0['aL'],
                                               x0['phi'],
                                               x0['theta'])
        # Adicionar o valor de reflectância à lista para este ponto
        reflectancias.append(Rc)
    
    # Adicionar a lista de reflectâncias para este ponto à lista principal
    reflectancias_por_gR.append(reflectancias)

# Converter a lista de listas em um array numpy para facilitar o plot
reflectancias_por_gR = np.array(reflectancias_por_gR)

# Plotar a reflectância em função do valor de gR
plt.figure(figsize=(10, 6))
for i in range(len(df)):
    plt.plot(range(41), reflectancias_por_gR[i], label=f'Linha {i+1}')
plt.xlabel('Valor de gR')
plt.ylabel('Reflectância')
plt.title('Reflectância por Valor de gR')
plt.legend()
plt.grid(True)
plt.show()

