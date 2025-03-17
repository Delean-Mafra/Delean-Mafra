import numpy as np
import matplotlib.pyplot as plt

# Gerar dados de exemplo
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Plotar os dados
plt.plot(x, y)
plt.title('Padrão de Consumo de Energia')
plt.xlabel('Tempo')
plt.ylabel('Consumo')
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Gerar uma onda sonora
t = np.linspace(0, 1, 500)
freq = 5  # Frequência em Hz
y = np.sin(2 * np.pi * freq * t)

# Plotar a onda sonora
plt.plot(t, y)
plt.title('Onda Sonora')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.show()

