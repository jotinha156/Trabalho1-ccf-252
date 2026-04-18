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
def converter_imediato_branch(offset):
    offset = int(offset)


    if offset < -4096 or offset > 4094:
        raise ValueError("Offset fora do alcance do branch")
     
    return format(offset , '013b')


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
          n_imediato = converter_imediato_branch(imediato)
            imediato12 = n_imediato[0]     # numero imediato[0]  = bit 12
            imediato11 = n_imediato[1]
            imediato10_5 = n_imediato[2:8] # vai do bit 10 do imediato até o 5
            imediato4_1 = n_imediato[8:12]
            instrucaoFinal = (
                imediato12 +
                imediato10_5 +
                RegistradorConversor(rs2) +
                RegistradorConversor(rs1) +
                dados['funct3'] +
                imediato4_1 +
                imediato11 +
                dados['opcode']
            )

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
    posicao = 0  # cada instrução ocupa 4 bytes

    with open(nome_arquivo, 'r') as arquivo2:
        for linha in arquivo2:
            linha = linha.strip()
            print(linha)

            if linha == '':
                continue

            if ':' in linha:   # procura se tem : no arquivo
                partes = linha.split(':', 1)
                print(partes)

                nome_rotulo = partes[0].strip()
                print(nome_rotulo)

                rotulo[nome_rotulo] = posicao  # adiciona ao dicionário

                resto = partes[1].strip()

                if resto == '':
                    continue   # linha só com rótulo, não incrementa posicao
                else:
                    posicao = posicao + 4

            else:
                posicao = posicao + 4

    return rotulo 
            



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


def terceira_passagem(teste):
    rotulo = calculo_offset('asb.txt')
    with open('testealeatorio2.txt','r') as arquivo4:
        posicao1 = 0
        for linha in arquivo4:
            linha = linha.strip()
            
            if linha == '':
                continue
            if ':' in linha:
                partes_da_linha = linha.split(':',1)
                linha = partes_da_linha[1]
                if linha == '':
                    continue
            linha = linha.replace(',',' ')
            partes = linha.split()
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
                instruction_rs2 = partes[1]

                offset, reg = partes[2].split('(')
                reg = reg.replace(')', '')

                instruction_rs1 = reg
                instruction_imed = offset

            # Tipo SB: bne
            elif instruction_func == 'bne':
                instruction_rs1 = partes[1]
                instruction_rs2 = partes[2]
                nome_rotulo = partes[3]

                endereco_rotulo = rotulo[nome_rotulo]
                offset = endereco_rotulo - posicao1
                instruction_imed = offset

            else:
                print("Instrução não suportada:", instruction_func)
                continue

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

            posicao1 = posicao1 + 4

