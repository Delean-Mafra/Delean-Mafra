def calcular_media(nota1, nota2, nota3, nota4):
    return (nota1 + nota2*2 + nota3*3 + nota4*4) / 10
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Entrada das notas
nota_trabalho = float(input("Nota do trabalho de laboratório: "))
nota_semestral = float(input("Nota da avaliação semestral: "))
nota_exame = float(input("Nota do exame final: "))
nota_projeto = float(input("Nota do projeto final: "))

# Cálculo da média final
media_final = calcular_media(nota_trabalho, nota_semestral, nota_exame, nota_projeto)

# Verificação da média para aprovação
if media_final >= 6.0:
    print(f"A média final é {media_final:.2f}. Aluno Aprovado!")
else:
    print(f"A média final é {media_final:.2f}. Aluno Reprovado!")
