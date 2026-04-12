# Dicionario para os Registradores
REGISTRADORES = {
            'x0': '00000', 'x1': '00001', 'x2': '00010', 'x3': '00011',
            'x4': '00100', 'x5': '00101', 'x6': '00110', 'x7': '00111',
            'x8': '01000', 'x9': '01001', 'x10': '01010', 'x11': '01011',
            'x12': '01100', 'x13': '01101', 'x14': '01110', 'x15': '01111',
            'x16': '10000', 'x17': '10001', 'x18': '10010', 'x19': '10011',
            'x20': '10100', 'x21': '10101', 'x22': '10110', 'x23': '10111',
            'x24': '11000', 'x25': '11001', 'x26': '11010', 'x27': '11011',
            'x28': '11100', 'x29': '11101', 'x30': '11110', 'x31': '11111'
}

# Dicionario para as Instrucoes
INSTRUCOES = {

    #Intrucoes Tipo R
    'add': {'tipo': 'R', 'funct7': '0000000', 'funct3': '000', 'opcode': '0110011'},
    'or':  {'tipo': 'R', 'funct7': '0000000', 'funct3': '110', 'opcode': '0110011'},
    'sll': {'tipo': 'R', 'funct7': '0000000', 'funct3': '001', 'opcode': '0110011'},

    #Intrucoes Tipo I
    'lh':   {'tipo': 'I', 'funct3': '001', 'opcode': '0000011'},
    'addi': {'tipo': 'I', 'funct3': '000', 'opcode': '0010011'}
}


# Retorna o valor binario do registrador procurado
def RegistradorConversor(reg):
    if reg not in REGISTRADORES:
        raise ValueError(f"Registrador inválido: {reg}")
    return REGISTRADORES[reg]


# Recebe as variaveis da instrução e as retorna em binario em uma unica instrução de 32 bits
def RegistradorMontador(instrucao, rd, rs1, rs2):
    dados = INSTRUCOES.get(instrucao)

    match dados['tipo']:
        case 'R':
            instrucaoFinal = { dados['funct7'] + RegistradorConversor(rs2) + RegistradorConversor(rs1) + 
                                dados['funct3'] + RegistradorConversor(rd) + dados['opcode'] }

        case 'I':
            n_imediato = converter_numerobinario(rs2) 
            instrucaoFinal = { n_imediato + RegistradorConversor(rs1) + dados['funct3'] + RegistradorConversor(rd)+
                                dados['opcode']}
           
        case _:
            raise ValueError("Instrução não suportada")
        
    if not dados:
        raise ValueError("Instrução não suportada")


    #Restorna o numero agora convertido
    return (
        instrucaoFinal
    )


# Recebe um numero inteiro (entre -2048 e 2047) e o devolve em seu formato binario
def converter_numerobinario(numero):
    numero = int(numero)
    if numero < -2048 or numero > 2047:
        print("numero invalido")
        return 0 
    
    binario = ""
    if(numero < 0):
        numero = (1 << 12) + numero
        binario=format(numero,'012b')
        return binario

    while(numero > 0 ):
         r = numero % 2

         binario = str(r) + binario
         numero = numero // 2

    while len(binario) < 12:
        binario="0" + binario

    return str(binario) 


# Abre  e le o arquivo de instrucoes
with open('asb.txt','r') as arquivo:
    for linha in arquivo:
        partes=linha.strip() #Remove os espaços vazios

        partes=partes.replace(',',' ') #Remove as virgulas

        partes= partes.split() #Separa a string em diferentes variaveis (func, rd, rs1, rs2)

        instruction_func = partes[0] # funcao
        instruction_rd = partes[1]   # variavel rd
        instruction_rs1 = partes[2]  # variavel rs1
        instruction_rs2 = partes[3]  # variavel rs2 ou imediato

        print("\n\n")

        print("DEBUG partes:", partes, "\n")

        print("DEBUG function:", instruction_func)
        print("DEBUG rd:", instruction_rd)
        print("DEBUG rs1:", instruction_rs1)
        print("DEBUG rs2:", instruction_rs2)

        resultadobinario= RegistradorMontador(instruction_func, instruction_rd, instruction_rs1, instruction_rs2)
        print("A instrucao convertida para binario e ",resultadobinario)
