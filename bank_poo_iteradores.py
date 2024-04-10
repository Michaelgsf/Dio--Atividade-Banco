#Esté script é foi desenvolvido para um atividade para um bootcamp da DIO
#Este é um script de Banco usando poo, uma atualização do código de banco "bank_otimizado.py" com as funções
#de depositar, sarcar, ver o extrato de ações realizadas, criar novas contas ou usuários, listar e filtrar contas.
# fazendo uso de iteradores, decoradores, geradores e datetime para retonar a data e hora das operações

from abc import ABC, abstractproperty
from datetime import datetime
import textwrap

#Definindo classes:

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indices = 0
        
    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_por_dia()) >= 10:
            print("Você atingiu o limite de transações permitidas por dia!")
            return 
                
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
            
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero 
    
    @property
    def agencia(self):
        return self._agencia 
    
    @property
    def historico(self):
        return self._historico 
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
           
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
            
        else:
            print("Operação falhou! O valor informado é inválido.")
            
        return False

    def depositar(self, valor):
        if valor > 0: 
            self._saldo += valor
            print("Deposito realizado com sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            
        return False
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
            
        elif excedeu_saque:
            print("Operação falhou! Número máximo de saques excedido.")   
            
        else:
            return super().sacar(valor) 
        
        return False
    
    def __str__(self):
        return f"""\
                Agencia:\t{self.agencia}
                C/C:\t{self.numero}
                Titular\t{self._cliente.nome}
                """
                                
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    def gerar_relatorios(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
    
    def transacoes_por_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_trasacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_trasacao:
                transacoes.append(transacao)
        return transacoes
    
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @property
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_sucedida = conta.sacar(self.valor)
        
        if transacao_sucedida:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_sucedida = conta.depositar(self.valor)
        
        if transacao_sucedida:
            conta.historico.adicionar_transacao(self)

class ContadorDeContas:
    def __init__(self, contas):
        self.contas = contas
        self._contador = 0
        
    def __init__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self._contador]
            return f"""
            Agencia:\t{conta.agencia}
            C/C:\t{conta.numero}
            Titular\t{conta.cliente.nome}
            Saldo: R$ {conta.saldo:.2f}
            """ 
        except IndexError:
            raise StopIteration
        finally:
            self._contador += 1
            
#Definindo funções         
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

def log_transacao(funcao):
    def wrapper(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        print(f'{datetime.now()}: {funcao.__name__.upper()}')
        return resultado
    return wrapper

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado no sistema!")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
@log_transacao 
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado no sistema!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)   
    
@log_transacao    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado no sistema!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("====================== Extrato ======================")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in conta.historico.gerar_relatorios():
            extrato += f'\n{transacao["data"]}\n{transacao["tipo"]}:\nR${transacao["valor"]:.2f}'
                
    print(extrato)
    print(f'Saldo: R$ {conta.saldo:.2f}\n')
    print("====================== Fim do Extrato ======================")
    
@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigra estado): ")
        
        novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        clientes.append(novo_cliente)        
        print("=== Usuário criado com sucesso! ===")
        return novo_cliente 
    else:
        print("Já existe um usuário com o CPF informado!")
        return None
    
def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    return cliente.contas[0]

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)  # Adiciona a conta ao cliente específico
        print("\n === Conta criada com sucesso! ===")
    else:
        print("Usuário não encontrado!")
        return

def listar_contas(contas):
    if contas == []:
        return print("Não há contas cadastradas!")
    else:
        for conta in contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
            print("=" * 100)
        return
    
def main():
    clientes = []
    contas = []
    
    while True:
        
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
                    
        elif opcao == "s":
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)
            
        elif opcao == 'nu':
            criar_cliente(clientes)
                  
        elif opcao == "nc":
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == 'q':
            print("Saindo!")
            print("Obrigado por escolher nossos serviços.")
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desajado.")
                    
main()