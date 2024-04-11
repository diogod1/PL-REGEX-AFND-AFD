import json, sys

exec_converter_er_afnd: bool = False



def cria_novo_estado(estados):
    estado = f'q{len(estados)}'
    estados.append(f'q{len(estados)}')
    return estado

def insere_trans(args, estados, simbolos, transicoes):
    inicio = cria_novo_estado(estados)
    fim = cria_novo_estado(estados)

    for arg in args:
        subInicio, subFim = analisa_regex(arg, estados, simbolos, transicoes)

        transicoes.setdefault(inicio, {}).setdefault('', []).append(subInicio)
        transicoes.setdefault(subFim, {}).setdefault('', []).append(subInicio)
        transicoes.setdefault(subFim, {}).setdefault('', []).append(fim)

    return inicio, fim

def insere_kle(args, estados, simbolos, transicoes):

    inicio = cria_novo_estado(estados)
    fim = cria_novo_estado(estados)

    transicoes.setdefault(inicio, {}).setdefault('', []).append(fim)

    for arg in args:
        subInicio, subFim = analisa_regex(arg, estados, simbolos, transicoes)

        transicoes.setdefault(inicio, {}).setdefault('', []).append(subInicio)
        transicoes.setdefault(subFim, {}).setdefault('', []).append(subInicio)
        transicoes.setdefault(subFim, {}).setdefault('', []).append(fim)

    return inicio, fim

def insere_seq(args, estados, alfabeto, caminhos):
    fimAnterior = None
    estado_inicio = None

    for arg in args:
        estado_inicio2, estado_fim2 = analisa_regex(arg, estados, alfabeto, caminhos)

        if fimAnterior: 
            caminhos.setdefault(fimAnterior, {}).setdefault('', []).append(estado_inicio2)
        else:
            estado_inicio = estado_inicio2

        fimAnterior = estado_fim2

    return estado_inicio, fimAnterior

def insere_altern(args, estados, alfabeto, caminhos):
    estado_inicio = cria_novo_estado(estados)
    estado_fim = cria_novo_estado(estados)

    for arg in args:
        estado_inicio2, estado_fim2 = analisa_regex(arg, estados, alfabeto, caminhos)
        alfabeto.setdefault(estado_inicio, {}).setdefault('', []).append(estado_inicio2) 
        alfabeto.setdefault(estado_fim2, {}).setdefault('', []).append(estado_fim) 

    return estado_inicio, estado_fim

def insere_epsilon(estados, caminhos):
    estado_inicio = cria_novo_estado(estados)
    estado_fim = cria_novo_estado(estados)

    caminhos[estado_inicio] = {'': [estado_fim]}

    return estado_inicio, estado_fim

def insere_simbolo(simbolo, alfabeto, estados, caminhos):
    estado_inicio = cria_novo_estado(estados)
    estado_fim = cria_novo_estado(estados)

    caminhos[estado_inicio] = {simbolo: [estado_fim]}

    if simbolo not in alfabeto:
        alfabeto.append(simbolo)

    return estado_inicio, estado_fim

def analisa_regex(regex, estados, alfabeto, caminhos):

    operador = regex['op']
    if 'simb' in regex: 
        insere_simbolo(regex['simb'], alfabeto, estados, caminhos)
    elif 'epsilon' in regex:  
        insere_epsilon(estados, caminhos)
    elif operador == 'alt':  # operador -> alt
        insere_altern(regex['args'], estados, alfabeto, caminhos)
    elif operador == 'seq':  # operador -> seq
        insere_seq(regex['args'], estados, alfabeto, caminhos)
    elif operador == 'kle':  # operador -> kle
        insere_kle(regex['args'], estados, alfabeto, caminhos)
    elif operador == 'trans': # operador -> trans
        insere_trans(regex['args'], estados, alfabeto, caminhos)

    return

def converter_er_afnd(output_path: str) -> any:

    alfabeto = []
    estados = []
    caminhos = {}
 
    #Definir/abrir o caminho do ficheiro  
    afpath = "exemplo01.json"
    with open(afpath, "r", encoding="utf-8") as f:
        af = json.load(f)

    # Iniciar processo de conversão
    inicio, fim = analisa_regex(af, estados, alfabeto, caminhos)

    # Verificar se o fim não está nas transições, se não tiver adicionar
    if fim not in caminhos:
        caminhos[fim] = {'': []}

    afnd = {
        "V": alfabeto,
        "Q": estados,
        "delta": caminhos,
        "q0": inicio,
        "F": [fim]
    }

    return afnd

afnd = converter_er_afnd("")
print(afnd)