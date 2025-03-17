def atravessar_rua():
    while True:
        print("\nEscolha uma ação:")
        print("1. Olhar para a esquerda")
        print("2. Olhar para a direita")
        print("3. Confirmar se está vindo carro")
        print("4. Atravessar a rua")
        
        acao1 = input("Escolha a primeira ação (1-4): ")

        if acao1 == '1':
            print("Você olhou para a esquerda.")
            acao2 = input("Escolha a próxima ação (2-4): ")
            if acao2 == '2':
                print("Você olhou para a direita.")
                acao3 = input("Escolha a próxima ação (3-4): ")
                if acao3 == '3':
                    carro_vindo = input("Está vindo carro? (sim/não): ")
                    if carro_vindo == 'sim':
                        print("Você deve esperar.")
                        reiniciar = input("Deseja reiniciar o processo? (sim/não): ")
                        if reiniciar == 'sim':
                            continue
                        else:
                            print("Você foi atropelado!")
                            break
                    else:
                        print("Você pode atravessar a rua.")
                        print("Rua atravessada com sucesso!")
                        break
                else:
                    print("Você foi atropelado!")
                    break
            else:
                print("Você foi atropelado!")
                break
        else:
            print("Você foi atropelado!")
            break

atravessar_rua()
