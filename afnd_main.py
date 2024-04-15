import sys  # Importar módulo sys
import json # Importar módulo json
 
arquivo = ""
 
# Ler um arquivo JSON
def read_afnd(file_json):
    with open(file_json, 'r') as file:  # Abre o arquivo .json
        afnd = json.load(file) # Carrega o arquivo
    return afnd


def convert_afnd_to_afd(afnd):
    V = afnd['V']
    Q = afnd['Q']
    delta = afnd['delta']
    q0 = afnd['q0']
    F = afnd['F']
    
    simbolos = V 
    estadoInicial = q0 
    estados = [] 
    caminhos = {} 
    estadosFinais = [] 

    def process_eplison_close(estado_set):
        fecho = [estado_set]
        fila = [estado_set]

        while fila:
            estado = fila.pop()
            if '' in delta[estado]:
                for prox_estado in delta[estado]['']:
                    if prox_estado not in fecho:
                        fecho.append(prox_estado)
                        fila.append(prox_estado)

        return fecho

    estadosIniciais = process_eplison_close(estadoInicial)
    fila = ['_'.join(sorted(estadosIniciais))]
    estados.append('_'.join(sorted(estadosIniciais)))

    while len(fila) != 0:
        estadoAtual = fila.pop() 
        estadosAtuais = estadoAtual.split('_')

        if any(f in estadosAtuais for f in F):
            if estadoAtual not in estadosFinais:
                estadosFinais.append(estadoAtual)

        for simbolo in simbolos:
            novosEstados = set()
            for estado in estadosAtuais:
                if simbolo in delta[estado]:
                    for proximoEstado in delta[estado][simbolo]:
                        novosEstados.update(process_eplison_close(proximoEstado))

            if len(novosEstados) == 0:
                continue

            novoEstado = '_'.join(sorted(novosEstados))

            if estadoAtual not in caminhos:
                caminhos[estadoAtual] = {}

            caminhos[estadoAtual][simbolo] = novoEstado

            if novoEstado not in estados:
                estados.append(novoEstado)
                fila.append(novoEstado)

    afd = {
        "V": list(simbolos),
        "Q": estados,
        "delta": caminhos,
        "q0": '_'.join(sorted(estadosIniciais)), 
        "F": estadosFinais
    }

    return afd

# Gerar o código Graphviz da AFD
def generate_graph(afd):
    lines = ['digraph {']
    lines.append('    node [shape = doublecircle]; ' + ' '.join(afd['F']) + ';')
    lines.append('    node [shape = point]; qi;')
    lines.append('    node [shape = circle];')
 
    # Estado inicial apontando para o primeiro estado
    lines.append('    qi -> ' + afd['q0'] + ';')
 
    # Adiciona as transições
    for start_state, transitions in afd['delta'].items(): # Para cada estado de início
        for input_val, end_states in transitions.items(): # Pode haver mais de uma transição para um mesmo símbolo
            for end_state in end_states: # Pode haver mais de um estado final
                lines.append(f'    {start_state} -> {end_state} [label="{input_val}"];')
 
    lines.append('}')
    dot_representation = '\n'.join(lines)
 
    # Salva o dot_representation em um arquivo
    with open("graphviz.gv", "w") as file:
        file.write(dot_representation)
    # print(dot_representation)


def save_file(afnd, nome_ficheiro):

    #adicionar .json no fim
    if not nome_ficheiro.endswith('.json'):
        nome_ficheiro += ".json"

    with open(nome_ficheiro, 'w') as ficheiro:
        json.dump(afnd, ficheiro, indent=4)

    return

# Assume que o primeiro argumento é o arquivo JSON
arquivo = sys.argv[1]
afnd = read_afnd(arquivo)
afd = convert_afnd_to_afd(afnd)
 
# Verifica se o argumento graphviz foi passado
if '-graphviz' in sys.argv:
    generate_graph(afnd)
 
# Verifica se o argumento output foi passado
elif '-output' in sys.argv:
    indice_output = sys.argv.index('-output') #Procura a posição do argumento
    if indice_output + 1 < len(sys.argv):
        arquivo = sys.argv[indice_output + 1]
        save_file(afd, arquivo)
    else:
        print("Especifique o arquivo de saída com o argumento '-output'.")
else:
    print("Comando não reconhecido.")
