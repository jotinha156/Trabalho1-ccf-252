def registradorconversor(x2):
    testando = {
            'x0': '00000', 'x1': '00001', 'x2': '00010', 'x3': '00011',
            'x4': '00100', 'x5': '00101', 'x6': '00110', 'x7': '00111',
            'x8': '01000', 'x9': '01001', 'x10': '01010', 'x11': '01011',
            'x12': '01100', 'x13': '01101', 'x14': '01110', 'x15': '01111',
            'x16': '10000', 'x17': '10001', 'x18': '10010', 'x19': '10011',
            'x20': '10100', 'x21': '10101', 'x22': '10110', 'x23': '10111',
            'x24': '11000', 'x25': '11001', 'x26': '11010', 'x27': '11011',
            'x28': '11100', 'x29': '11101', 'x30': '11110', 'x31': '11111'
            }
    return testando[x2]

    
     
     
     
     #funct7 | rs2 | rs1 | funct3 | rd | opcode
    #  0       1     2      3     4       5
def Registradormontador(instrucao,rd,rs1,rs2):
     if(instrucao == 'add'):
         lista_completa[5] = '0110011'
         lista_completa[3] = '000'
         lista_completa[0] = '0000000'
         lista_completa[4] = registradorconversor(rd)
         lista_completa[2] = registradorconversor(rs1)
         lista_completa[1] = registradorconversor(rs2)
     if(instrucao == 'or'):
         lista_completa[5] = '0110011'
         lista_completa[3] = '000'
         lista_completa[0] = '0000000'
         lista_completa[4] = registradorconversor(rd)
         lista_completa[2] = registradorconversor(rs1)
         lista_completa[1] = registradorconversor(rs2)
     if(instrucao == 'sll'):
         lista_completa[5] = '0110011'
         lista_completa[3] = '000'
         lista_completa[0] = '0000000'
         lista_completa[4] = registradorconversor(rd)
         lista_completa[2] = registradorconversor(rs1)
         lista_completa[1] = registradorconversor(rs2)
         
     
         
    
     
        
      


     numeroconvertido = lista_completa[0] + lista_completa[1] + lista_completa[2] + lista_completa[3] + lista_completa[4] + lista_completa[5]
     return numeroconvertido


#adicionando de forma fake

with open('asb.txt','r') as archive:
    conteudo=archive.read()
    print(conteudo)


with open('asb.txt','r') as arquivo:
    conteudo1=arquivo.read()
    conteudo1=conteudo1.replace(',', ' ')
    print(conteudo1)


 
i=0
with open('asb.txt','r') as arquivo2:
    for linha in arquivo2:
        i=i+1
        print(i)
        linha=linha.strip()
        linha = linha.replace(',',' ')
        linha=linha.replace(' ','')
        print(linha)
   
   # strip remove espaços
   #replace troca um trecho por outro
   #split divide a string em partes


lista_completa = [""] * 6  #criar lista vazia com 6 posições

with open('asb.txt','r') as arquivo3:
    for linha in arquivo3:
        partes=linha.strip()
        print("1 passo")
        print(partes)
        print(" 2 passo \n")
        partes=partes.replace(',',' ')
        print(partes)
        print(" 3 passo \n")
        partes= partes.split()
        print(partes)

        instruction = partes[0] #add
        instruction1 = partes[1] #variavel rd registrador que armazena valor
        instruction2 = partes[2] #  variavel rs1
        instruction3 = partes[3] #variavel rs2
        print("DEBUG partes:", partes)
        print("DEBUG rd:", instruction1)
        print("DEBUG rs1:", instruction2)
        print("DEBUG rs2:", instruction3)

        resultadobinario= Registradormontador(instruction,instruction1,instruction2,instruction3)
        print(" a instrucao convertida para binario e ",resultadobinario)
    
teste = {'add': '0000000'}


#trataremos os numeros como string



