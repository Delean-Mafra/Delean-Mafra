import random

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def generate_cnpj():                                                       
    def calculate_special_digit(l):                                             
        digit = 0                                                               

                                                                                
        for i, v in enumerate(l):                                               
            digit += v * (i % 8 + 2)                                            
                                                                                
        digit = 11 - digit % 11                                                 
                                                                                
        return digit if digit < 10 else 0                                       
                                                                                
    cnpj =  [1, 0, 0, 0] + [random.randint(0, 9) for x in range(8)]             
                                                                                
    for _ in range(2):                                                          
        cnpj = [calculate_special_digit(cnpj)] + cnpj                           
                                                                                
    return '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(cnpj[::-1])


cnpj = str(generate_cnpj().replace('.', '').replace('/', '').replace('-', ''))

print(cnpj)