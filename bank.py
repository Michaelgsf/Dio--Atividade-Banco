#Esté script é foi desenvolvido para um atividade para um bootcamp da DIO
#Este é um script de Banco, com as opções de depositar, sarcar e ver o extrato de ações realizadas.


menu = """
    Escolha a opção desejada
    
    [1] - Depositar
    [2] - Sacar
    [3] - Extrato
    [4] - Sair
    
Opção escolhida: """

saldo = 0
limit_withdraw_value = 500
n_withdraws = 0
limit_withdraws = 3
extrato = ""

while True:
    
    opcao = input(menu)
    
    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
    
        if valor > 0: 
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f}\n'
        
        else:
            print("Operação falhou! O valor informado é inválido.")
    
    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limit_withdraw_value
        excedeu_saques = n_withdraws >= limit_withdraws
        
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
                
        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R$ {valor:.2f}\n'
            n_withdraws += 1
            
        else:
            print("Operação falhou! O valor informado é inválido.")
            
    elif opcao == '3':
        print("\n========================== EXTRATO ==========================")
        print("Não há registro de movimentações." if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print("============================================================")
        
    elif opcao == '4':
        print("Saindo!")
        print("Obrigado por escolher nossos serviços.")
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desajado.")
            