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

    # Intrucoes Tipo R
    'add': {'tipo': 'R', 'funct7': '0000000', 'funct3': '000', 'opcode': '0110011'},
    'or':  {'tipo': 'R', 'funct7': '0000000', 'funct3': '110', 'opcode': '0110011'},
    'sll': {'tipo': 'R', 'funct7': '0000000', 'funct3': '001', 'opcode': '0110011'},

    # Intrucoes Tipo I
    'lh':   {'tipo': 'I', 'funct3': '001', 'opcode': '0000011'},
    'andi': {'tipo': 'I', 'funct3': '111', 'opcode': '0010011'},

    # Intrucoes Tipo S
    'sh': {'tipo': 'S', 'funct3': '001', 'opcode': '0100011'},

    # Intrucoes Tipo SB
    'bne': {'tipo': 'SB', 'funct3': '001', 'opcode': '1100011'}
}


# Retorna o valor binario do registrador procurado
def RegistradorConversor(reg):
    if reg not in REGISTRADORES:
        raise ValueError(f"Registrador inválido: {reg}")
    return REGISTRADORES[reg]


# Recebe as variaveis da instrução e as retorna em binario em uma unica instrução de 32 bits
def RegistradorMontador(instrucao, rd, rs1, rs2, imediato):
    dados = INSTRUCOES.get(instrucao)

    match dados['tipo']:
        case 'R':
            instrucaoFinal = (
                dados['funct7'] + 
                RegistradorConversor(rs2) + 
                RegistradorConversor(rs1) + 
                dados['funct3'] + 
                RegistradorConversor(rd) + 
                dados['opcode']
            )

        case 'I':
            n_imediato = converter_numerobinario(imediato) 

            instrucaoFinal = (
                n_imediato + 
                RegistradorConversor(rs1) + 
                dados['funct3'] + 
                RegistradorConversor(rd)+
                dados['opcode']
            )
           
        case 'S':
            n_imediato = converter_numerobinario(imediato)

            imediato_11_5 = n_imediato[:7]
            imediato_4_0 = n_imediato[7:]

            instrucaoFinal = (
                imediato_11_5 +
                RegistradorConversor(rs2) +
                RegistradorConversor(rs1) +
                dados['funct3'] +
                imediato_4_0 +
                dados['opcode']
            )

        case 'SB':
            print("Ainda não")

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
            
def calculo_offset(nome_arquivo):
    rotulo = {}
    posicao = 0 # em cada linha vai ser somado 4bytes e a  variavel vai ajudar no calculo de deslocamento
    with open(nome_arquivo,'r') as arquivo2:
        for linha in arquivo2:
            linha=linha.strip()
            print(linha)
            if ':' in linha:     #procura se tem : no arquivo
                partes=linha.split(':')
                print(partes)
                nome_rotulo = partes[0].strip()
                print(nome_rotulo)
                rotulo[nome_rotulo] = posicao #adiciona um item ao dicionario
                resto = partes[1].strip()
                if resto == '':
                    continue  #se a linha  so tiver : o programa vai incrementar
                else:
                    posicao=posicao + 4   
          else:
            posição = posição + 4
  return rotulo      
def segunda_passagem(nome_arquivo,rotulo):
    posicao1 = 0 #variavel para ajudar no calculo do offset
    with open(nome_arquivo,'r') as arquivo3:
        for linha4 in arquivo3:

            linha4 = linha4.strip() #strip usado para remover espaço em branco
            if linha4 == '': #ignora linha vazia
                continue 
            if ':' in linha4:
                partes_da_linha = linha4.split(':',1) #divide a linha em 2 partes
                linha4 = partes_da_linha[1].strip()
                if linha4 == '':
                    continue
            linha4 = linha4.replace(',',' ')
            partes = linha4.split()
            
            instruction_func = partes[0]
            if instruction_func == 'bne':
                rs1 = parte[1]
                rs2 = parte[2]
                nome_rotulo = parte[3]
                endereco_rotulo = rotulo[nome_rotulo]
                offset = endereco_rotulo - posicao1
            posicao1 = posicao1 + 4 


# Abre  e le o arquivo de instrucoes
with open('asb.txt','r') as arquivo:
    for linha in arquivo:
        partes = linha.strip()
        partes = partes.replace(',', ' ')
        partes = partes.split()

        instruction_func = partes[0]

        # Inicialização
        instruction_rd = '0'
        instruction_rs1 = '0'
        instruction_rs2 = '0'
        instruction_imed = '0'

        # Tipo R: add, or, sll
        if instruction_func in ['add', 'or', 'sll']:
            instruction_rd  = partes[1]
            instruction_rs1 = partes[2]
            instruction_rs2 = partes[3]

        # Tipo I: andi
        elif instruction_func == 'andi':
            instruction_rd  = partes[1]
            instruction_rs1 = partes[2]
            instruction_imed = partes[3]

        # Tipo I (load): lh
        elif instruction_func == 'lh':
            instruction_rd = partes[1]

            offset, reg = partes[2].split('(')
            reg = reg.replace(')', '')

            instruction_rs1 = reg
            instruction_imed = offset

        # Tipo S: sh
        elif instruction_func == 'sh':
            instruction_rs2 = partes[1]  # valor a armazenar

            offset, reg = partes[2].split('(')
            reg = reg.replace(')', '')

            instruction_rs1 = reg
            instruction_imed = offset

        # Tipo SB: bne
        elif instruction_func == 'bne':
            print("Ainda Nada")

        else:
            print("Instrução não suportada:", instruction_func)
            continue

        # DEBUG
        print("\nDEBUG partes:", partes)
        print("DEBUG function:", instruction_func)
        print("DEBUG rd:", instruction_rd)
        print("DEBUG rs1:", instruction_rs1)
        print("DEBUG rs2:", instruction_rs2)
        print("DEBUG imediato:", instruction_imed)

        resultadobinario = RegistradorMontador(
            instruction_func,
            instruction_rd,
            instruction_rs1,
            instruction_rs2,
            instruction_imed
        )

        print("A instrucao convertida para binario e", resultadobinario)
