import matplotlib.pyplot as plt
import numpy as np

# Definindo o domínio para f(x) = 2x
x = np.linspace(-3, 3, 400)
f_x = 2 * x
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Definindo a função constante g(x) = 2
g_x = np.full_like(x, 2)

# Plotando f(x) = 2x
plt.plot(x, f_x, label='f(x) = 2x', color='green')

# Plotando g(x) = 2
plt.plot(x, g_x, label='g(x) = 2', color='red')

# Configurando os rótulos dos eixos e o título
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráficos de f(x) = 2x e g(x) = 2')
plt.legend()

# Adicionando uma grade para melhor visualização
plt.grid(True)

# Exibindo o gráfico
plt.show()
