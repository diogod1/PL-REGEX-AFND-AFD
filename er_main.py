import json, sys

exec_convert_er_afnd: bool = False
simb,operator,args,epsilon = "simb", "op","args","epsilon"
opkle, optrans, opseq, opalt = "kle","trans","seq","alt"
alfabeto,estados,caminhos = [],[],{}


if len(sys.argv) == 1:
    print("Inserir comando!\n")
    exit(-1)
else:
    #Verifica se o ficheiro é um json
    if not sys.argv[1].endswith('.json'):
        print("Insira um ficheiro *.json")
        exit(-1)
    
    #Definir/abrir o caminho do ficheiro   
    afpath = sys.argv[1]
    with open(afpath, "r", encoding="utf-8") as f:
        af = json.load(f)  
    
    #Função conversão de er -> afnd
    if(sys.argv[2].lower() == "-output"):  
        #verifica se tem expressão
        if len(sys.argv) != 4: 
          print("Insira nome do ficheiro de saida\n")
          exit(-1)
        else: 
            #executa a função
            exec_convert_er_afnd = True
            nome_ficheiro:str = sys.argv[3]

def salvar_ficheiro(afnd, nome_ficheiro):

    #adicionar .json no fim
    if not nome_ficheiro.endswith('.json'):
        nome_ficheiro += ".json"

    with open(nome_ficheiro, 'w') as ficheiro:
        json.dump(afnd, ficheiro, indent=4)


    return

def insere_simbolo(simbolo):
    #adiciona simbolo ao alfabeto
    if simbolo not in alfabeto:
        alfabeto.append(simbolo)

    #estados novos
    estado_ini = f'q{len(estados)}'
    estados.append(estado_ini)
    estado_fim = f'q{len(estados)}'
    estados.append(estado_fim)
 
    #adicona caminho
    caminhos[estado_ini] = {simbolo: [estado_fim]}
 
    #retorna estados
    return estado_ini, estado_fim

def insere_altern(args):
    #estados novos
    estado_ini = f'q{len(estados)}'
    estados.append(estado_ini)
    estado_fim = f'q{len(estados)}'
    estados.append(estado_fim)
 
    for item in args:
        #analisa argumento
        estado_ini_2, estado_fim_2 = analisa_regex(item)
 
        #adiciona caminho inicio para o inicio 2
        caminhos.setdefault(estado_ini, {}).setdefault('', []).append(estado_ini_2)
 
        #adiciona caminho fim para o fim 2
        caminhos.setdefault(estado_fim_2, {}).setdefault('', []).append(estado_fim)

    #retorna estados
    return estado_ini, estado_fim

def insere_seqnc(args):
    estado_prev = None
    estado_incio = None
 
    for item in args:
        # Converter cada arg
        estado_incio_2, estado_fim_2 = analisa_regex(item)
 
        #não ser o primeiro arg
        if estado_prev:
            #cria caminho do estado anterior para o atual
            caminhos.setdefault(estado_prev, {}).setdefault('', []).append(estado_incio_2)
        else:
            #primeiro arg
            estado_incio = estado_incio_2
 
        #ultimo estado
        estado_prev = estado_fim_2

    #retorna estados
    return estado_incio, estado_prev

def insere_kle(args):
    #estados novos
    estado_ini = f'q{len(estados)}'
    estados.append(estado_ini)
    estado_fim = f'q{len(estados)}'
    estados.append(estado_fim)
 
    #adiciona caminho epsilon
    caminhos.setdefault(estado_ini, {}).setdefault('', []).append(estado_fim)
 
    for item in args:
        # Processar o arg que tem
        estado_ini_2, estado_fim_2 = analisa_regex(item)
 
        #caminho para o arg inicio do kle
        caminhos.setdefault(estado_ini, {}).setdefault('', []).append(estado_ini_2)
 
        #caminho do final para o incial
        caminhos.setdefault(estado_fim_2, {}).setdefault('', []).append(estado_ini_2)
 
        #caminho do fim2 para o fim
        caminhos.setdefault(estado_fim_2, {}).setdefault('', []).append(estado_fim)
 
    # Retornar o inicio e fim do Kle
    return estado_ini, estado_fim

def insere_trans(args):
    #estados novos
    estado_ini = f'q{len(estados)}'
    estados.append(estado_ini)
    estado_fim = f'q{len(estados)}'
    estados.append(estado_fim)
 
    for item in args:
        #processa args
        estado_ini_2, estado_fim_2 = analisa_regex(item)
 
        #caminho incio para o incio 2
        caminhos.setdefault(estado_ini, {}).setdefault('', []).append(estado_ini_2)

        #caminho fim2 para o inicio2 do arg
        caminhos.setdefault(estado_fim_2, {}).setdefault('', []).append(estado_ini_2) 
 
        #caminho do arg para o estado final principal
        caminhos.setdefault(estado_fim_2, {}).setdefault('', []).append(estado_fim)
 
    #retorna estados
    return estado_ini, estado_fim

def insere_epsilon():
    #estados novos
    estado_ini = f'q{len(estados)}'
    estados.append(estado_ini)
    estado_fim = f'q{len(estados)}'
    estados.append(estado_fim)
 
    #caminho inicio -> final
    caminhos[estado_ini] = {'': [estado_fim]}
 
    #retorna estados
    return estado_ini, estado_fim

def analisa_regex(regex):

    if simb in regex: #simbolo
        return insere_simbolo(regex[simb])
    elif opalt == regex[operator]: #alternancia
        return insere_altern(regex[args])
    elif opseq == regex[operator]: #sequencia
        return insere_seqnc(regex[args])
    elif opkle == regex[operator]: #kle
        return insere_kle(regex[args])
    elif optrans == regex[operator]: #transitivo
        return insere_trans(regex[args])
    elif epsilon in regex: #€
        return insere_epsilon()
    

def converte_er_anfd()-> any:

    incio, fim = analisa_regex(af)

    afnd = {
        "V": alfabeto,
        "Q": estados,
        "delta": caminhos,
        "q0": incio,
        "F": [fim]
    }

    return afnd

if exec_convert_er_afnd == True:
    afnd = converte_er_anfd()
    salvar_ficheiro(afnd,nome_ficheiro)
