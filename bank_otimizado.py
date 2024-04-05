#Esté script é foi desenvolvido para um atividade para um bootcamp da DIO
#Este é um script de Banco otimizado, uma atualização do código de banco "bank.py" com as funções
#de depositar, sarcar, ver o extrato de ações realizadas, criar novas contas ou usuários, listar e filtrar contas.

import textwrap


def menu():
    menu = """
    Escolha a opção desejada
    
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [nc] - Nova conta
    [lc] - Listar contas
    [nu] - Novo usuário
    [q] - Sair
    
    Opção escolhida: """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato):
    if valor > 0: 
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
            
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        numero_saques += 1
        print("Saque realizado com sucesso!")
        
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato
    
def exibir_extrato(saldo, /, *, extrato):
    print("\n========================== EXTRATO ==========================")
    print("Não há registro de movimentações." if not extrato else extrato)
    print(f'\nSaldo: R$ {saldo:.2f}')
    print("============================================================")
    return None
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrat_usuario(cpf, usuarios)

    if usuario:
        print("\n Já existe um usuário com o CPF informado!")
        return None
    else:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigra estado): ")
        
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco":endereco})
        
        print("=== Usuário criado com sucesso! ===")
        return None
def filtrat_usuario(cpf,usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrat_usuario(cpf, usuarios)
    
    if usuario:
        print("\n === Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado!")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    agencia = "0001"
    saldo = 0
    limite = 500
    numero_saques = 0
    limite_saques = 3
    extrato = ""
    usuarios = []
    contas = []
    
    while True:
        
        opcao = menu()
        
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
        
            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            
            saldo, extrato = sacar(
                saldo = saldo, 
                valor = valor, 
                extrato = extrato, 
                limite = limite, 
                numero_saques = numero_saques, 
                limite_saques = limite_saques)
            
                
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == 'nu':
            criar_usuario(usuarios)
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == 'q':
            print("Saindo!")
            print("Obrigado por escolher nossos serviços.")
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desajado.")
            
            
main()