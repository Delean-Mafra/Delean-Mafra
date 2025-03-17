print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

try:
    numero = int(input("Digite um numero: "))
    print(numero)
except ZeroDivisionError:
    print("Informe um valor diferente de zero(0)")
except ValueError:
    print("Digite um valor valido")
except:
    print("Digite um valor valido.")
finally:
    print("Final do codigo")