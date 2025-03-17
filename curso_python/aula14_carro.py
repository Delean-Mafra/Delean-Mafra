print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")
 
class Carro:
    def __init__(self, marca, modelo, cor, combustivel):
        self.marca = marca
        self.cor = cor
        self.modelo = modelo
        self.combustivel = combustivel


        self.ligado = False
        self.velocidade = 0

    def ligar(self):
        if self.ligado:
            print("{self.modelo} já esta ligado")
        else:
            print("{self.modelo} ligado")
            self.ligado = True

    def desligado(self):
        if self.ligado:
            print("{self.modelo} desligado")
            self.ligado = False
        else:
            print("{self.modelo} já esta desligado")

    def acelerar(self):
        if self.ligado:
            self.velocidade +=1
            print(f"{self.modelo} {self.velocidade}km/h")
        else:
            print("Não é possivel acelerar, {self.modelo} desligado")

    def frear(self):
        if self.ligado:
            self.velocidade -=1
            print(f"{self.velocidade}km/h")
        else:
            print("Não é possivel freiar, {self.modelo} desligado")
