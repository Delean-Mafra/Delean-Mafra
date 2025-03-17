import matplotlib.pyplot as plt

# Definindo os conjuntos
A = [1, 2, 3, 4]
B = [1, 2, 3, 4, 5, 6, 7, 8]
C = [2 * x for x in A]
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Plotando os pontos no gráfico
plt.plot(A, C, 'go-', label='f(x) = 2x')  # 'go-' significa linha sólida verde com marcadores de círculo

# Configurando os rótulos dos eixos e o título
plt.xlabel('Domínio (A)')
plt.ylabel('Imagem (I(f))')
plt.title('Gráfico de f(x) = 2x')
plt.legend()

# Adicionando uma grade para melhor visualização
plt.grid(True)

# Exibindo o gráfico
plt.show()
