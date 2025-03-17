"""A função dada, f(x) = e^(x^3) + 2x, é composta por duas partes principais:




Uma exponencial: e^(x^3), onde o expoente é ele mesmo uma função.

Um termo linear: 2x.



Para derivar a parte exponencial, precisa usar a regra da cadeia. A regra da cadeia diz que a derivada de uma função composta f(g(x)) é dada por: (f(g(x)))' = f'(g(x)) * g'(x)



Função externa: f(u) = e^u

Função interna: g(x) = x^3



Calculando as derivadas:

f'(u) = e^u

g'(x) = 3x^2



Aplicando a regra da cadeia à parte exponencial:



(e^(x^3))' = f'(g(x)) * g'(x) = e^(x^3) * 3x^2



Derivando o termo linear:



A derivada de 2x em relação a x é simplesmente 2.



Combinando os resultados:



Agora, podemos combinar a derivada da parte exponencial com a derivada do termo linear:



f'(x) = (e^(x^3))' + (2x)' = 3x^2 * e^(x^3) + 2



Portanto, a derivada da função f(x) = e^(x^3) + 2x é:



f'(x) = 3x^2 * e^(x^3) + 2



O desenvolvimento da resposta é a seguinte:



Identificamos que a função é composta por uma exponencial e um termo linear.

Aplicamos a regra da cadeia à parte exponencial, decomondo-a em uma função externa e uma função interna.

Calculamos as derivadas das funções externa e interna.

Aplicamos a fórmula da regra da cadeia para encontrar a derivada da parte exponencial.

Derivamos o termo linear.

Combinamos os resultados para obter a derivada da função completa.



Conclusão:



A regra da cadeia é fundamental para derivar funções compostas. Ao decompor a função em partes mais simples e aplicar a regra corretamente, conseguimos calcular a derivada de forma eficiente."""

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


import sympy as sp

# Definindo a variável
x = sp.symbols('x')

# Definindo a função
f = sp.exp(x**3) + 2*x

# Calculando a derivada
f_prime = sp.diff(f, x)

# Exibindo o resultado
print(f_prime)
