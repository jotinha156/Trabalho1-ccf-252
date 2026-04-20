# Codigo de:
    # Joao Pedro De Oliveira Rodrigues - 4425
    # Pablo da Silva Santana - 5900

import sys

# REGISTRADORES DICIONARIO
REGISTRADORES = {f'x{i}': format(i, '05b') for i in range(32)} # Cria os registradores (Binarios de 5 bits) de forma automatica


# INSTRUÇÕES DICIONARIO
INSTRUCOES = {
    'add':  {'tipo': 'R',  'funct7': '0000000', 'funct3': '000', 'opcode': '0110011'},
    'or':   {'tipo': 'R',  'funct7': '0000000', 'funct3': '110', 'opcode': '0110011'},
    'sll':  {'tipo': 'R',  'funct7': '0000000', 'funct3': '001', 'opcode': '0110011'},

    'lh':   {'tipo': 'I',  'funct3': '001', 'opcode': '0000011'},
    'andi': {'tipo': 'I',  'funct3': '111', 'opcode': '0010011'},

    'sh':   {'tipo': 'S',  'funct3': '001', 'opcode': '0100011'},

    'bne':  {'tipo': 'SB', 'funct3': '001', 'opcode': '1100011'}
}


# FUNCOES EXTRAS - funcoes auxiliares para a logica do programa
def conversor_registrador(reg): # Retorna o valor binario do registrador procurado
    if reg not in REGISTRADORES:
        raise ValueError(f"Registrador inválido: {reg}")
    return REGISTRADORES[reg]

def conversor_imediato(numero): # Recebe um numero inteiro (entre -2048 e 2047) e o devolve em seu formato binario
    numero = int(numero)
    if numero < -2048 or numero > 2047:
        raise ValueError("Imediato fora do intervalo")

    if numero < 0:
        numero = (1 << 12) + numero

    return format(numero, '012b')

def conversor_imediato_branch(offset): # Prepara o imediato para fazer um branch (bne)
    offset = int(offset)

    if offset < -4096 or offset > 4094:
        raise ValueError("Offset fora do alcance")

    offset = offset >> 1  # remove bit 0

    if offset < 0:
        offset = (1 << 12) + offset

    return format(offset, '012b')


# FUNCOES LEITORAS - funcoes que fazem a leitura do arquivo entrada
def calculador_rotulos(arquivo): # Retorna um dicionario de todos os rotulos de um arquivo + as suas posicoes

    rotulos = {} # Cria um dicionario vazio para armazenar todos os rotulos do arquivo
    pos = 0     # O dicionario guarda o rotulo e a posicao da sua instrucao Ex: 'L1' -> 8, 'L2' -> 24, etc

    # pos é contado de 4 em 4 para corresponder ao offset das instrucoes bne

    with open(arquivo) as f:
        for linha in f:
            linha = linha.strip() # Remove espacos e quebra linhas
            if not linha: # Pula caso linha vazia
                continue

            if ':' in linha: # Caso exista um rotulo na linha
                nome, resto = linha.split(':', 1)  # Separa o rotulo do restante da instrucao
                rotulos[nome.strip()] = pos         # Guarda o rotulo e sua posicao no dicionario

                if resto.strip(): # Verifica se tem instrucao pos nomeacao do rotulo. Ex: L1: ; ou L1: or x2, x1, x1
                    pos += 4      # Caso sim, avanca para a proxima instrucao


            else: # Linha normal (sem rotulo), avanca para a proxima instrucao
                pos += 4

    return rotulos # Retorna o dicionario de rotulos resultante

def interpretador_linha(linha, rotulos, pos): # Define como devesse ler uma linha e quais as suas variaveis
    linha = linha.strip() # Reemove espacos e \n
    if not linha: # Ignora linhas vazias
        return None

    if ':' in linha: # Detecta rotulos
        linha = linha.split(':', 1)[1].strip() # Remove o rotulo e fica apenas com a instrucao
        if not linha: # Caso pos o rotulo nao tenha instrucao. Ex: L1: 'nada'
            return None

    linha = linha.replace(',', ' ') # Prepara a linhas add x1, x2, x3 -> add x1 x2 x3
    partes = linha.split() # Divide a linha em uma lista ['add', 'x1', 'x2', 'x3']

    instr = partes[0]

    rd = rs1 = rs2 = imed = '0' # Padroniza os valores para evitar erros caso algum nao seja usado


    # Os if/elif abaixo servem para ler de forma diferente uma linha a depender de sua instrucao
    # Tipo R: add, or, sll
    if instr in ['add', 'or', 'sll']:
        rd  = partes[1]
        rs1 = partes[2]
        rs2 = partes[3]

    # Tipo I: andi
    elif instr == 'andi':
        rd   = partes[1]
        rs1  = partes[2]
        imed = partes[3]

    # Tipo I (load): lh
    elif instr == 'lh':
        rd = partes[1]
        offset, reg = partes[2].split('(')
        rs1 = reg.replace(')', '')
        imed = offset

    # Tipo S: sh
    elif instr == 'sh':
        rs2 = partes[1]
        offset, reg = partes[2].split('(')
        rs1 = reg.replace(')', '')
        imed = offset

    # Tipo SB: bne
    elif instr == 'bne':
        rs1 = partes[1]
        rs2 = partes[2]
        rotulo_destino = partes[3]

        if rotulo_destino in rotulos:
            imed = rotulos[rotulo_destino] - pos
                # Exemplo:
                    # L1 = 8 e pos 24
                    # imed = 8 - 24 = -16 de offset
        else:
            imed = rotulo_destino

    else:
        raise ValueError(f"Instrução desconhecida: {instr}")

    return instr, rd, rs1, rs2, imed


# MONTADOR - Logica principal do programa
def montador(instrucao, rd, rs1, rs2, imediato):
    dados = INSTRUCOES.get(instrucao)
    if not dados:
        raise ValueError(f"Instrução não suportada: {instrucao}")
    
    tipo = dados['tipo']

    if tipo == 'R':
        return ( # Retorna a Instrucao em seu formato binario final
            dados['funct7'] + 
            conversor_registrador(rs2) + 
            conversor_registrador(rs1) + 
            dados['funct3'] + 
            conversor_registrador(rd) + 
            dados['opcode']
        )

    elif tipo == 'I':
        n_imediato = conversor_imediato(imediato) # Transforma o imediato em binario

        return ( # Retorna a Instrucao em seu formato binario final
            n_imediato + 
            conversor_registrador(rs1) + 
            dados['funct3'] + 
            conversor_registrador(rd)+
            dados['opcode']
        )
        
    elif tipo == 'S':
        n_imediato = conversor_imediato(imediato) # Transforma o imediato em binario

        imediato_11_5 = n_imediato[:7] # Bits do imediato da posição 5 até a 11
        imediato_4_0  = n_imediato[7:] # Bits do imediato da posição 0 até a 4

        return ( # Retorna a Instrucao em seu formato binario final
            imediato_11_5 +
            conversor_registrador(rs2) +
            conversor_registrador(rs1) +
            dados['funct3'] +
            imediato_4_0 +
            dados['opcode']
        )

    elif tipo == 'SB':
        n_imediato = conversor_imediato_branch(imediato) # Transforma o imediato em binario (12 bits para o bne)
        
        imediato_12   = n_imediato[0]
        imediato_11   = n_imediato[1]
        imediato_10_5 = n_imediato[2:8]
        imediato_4_1  = n_imediato[8:12]

        return ( # Retorna a Instrucao em seu formato binario final
            imediato_12 +
            imediato_10_5 +
            conversor_registrador(rs2) +
            conversor_registrador(rs1) +
            dados['funct3'] +
            imediato_4_1 +
            imediato_11 +
            dados['opcode']
        )


# MAIN - funcao main do programa
def main():
    if len(sys.argv) < 2:
        print("Uso: py montador.py entrada.asm [-o saida.txt] \n" \
                "Ou" \
                "py montador.py entrada.asm")
        return

    entrada = sys.argv[1]
    saida = None

    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        saida = sys.argv[idx + 1]

    rotulos = calculador_rotulos(entrada) # Pega-se os rotulos primeiro antes de realmente ler o arquivo

    resultado = [] # Lista das instrucoes finais em binario
    pos = 0 # Posicao atual na leitura do arquivo

    with open(entrada) as f:
        for linha in f: # Interpreta linha a linha do arquivo e monta a sua intrucao no formato binario
            linha_preparada = interpretador_linha(linha, rotulos, pos)
            if linha_preparada:
                instr, rd, rs1, rs2, imed = linha_preparada
                binario = montador(instr, rd, rs1, rs2, imed)
                resultado.append(binario)
                pos += 4

    if saida:
        with open(saida, 'w') as f:
            f.write('\n'.join(resultado)) # Evita linha vazia no final do arquivo
    else:
        print('\n'.join(resultado))

# Comeca o Programa
if __name__ == "__main__":
    main()