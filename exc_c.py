import sys  # Importar módulo sys
import json # Importar módulo json

output = False
arquivo = ""

# Ler um arquivo JSON
def read_afnd(file_json):
    with open(file_json, 'r') as file:  # Abre o arquivo .json 
        afd = json.load(file) # Carrega o arquivo 
    return afd
 
# Converter afnd em afd
def convert_afd(afd):
    # Extrai os elementos do afd
    V = afd['V']
    Q = afd['Q']
    delta = afd['delta']
    q0 = afd['q0']
    F = afd['F']
   
    # Inicializa as estruturas
    new_Initial = q0
    new_V = [new_Initial]
    new_Delta = {}
    new_F = []
    fila = [new_Initial]  
   
    # Conversão de afnd para afd (Algoritmo)
    while fila:
        state = fila.pop(0)  # Remove o primeiro estado da fila
        for simbolo in Q:
            new_V = set()
            state_V = state.split(',')  # Divide os estados atuais por vírgula
 
            # Para cada estado atual, verifica todas as transições possíveis para o símbolo atual
            for estado in state_V:
                if estado in delta and simbolo in delta[estado]:
                    new_V.update(delta[estado][simbolo])
 
            new_V_str = ','.join(sorted(new_V))  # Cria uma string representando os novos estados
            if new_V_str and new_V_str not in new_V: # Se o novo estado não estiver na lista de novos estados
                new_V.append(new_V_str)
                fila.append(new_V_str)
 
            if state not in new_Delta: # Se o estado atual não estiver na nova delta
                new_Delta[state] = {}
            new_Delta[state][simbolo] = new_V_str
 
            # Verifica se o novo estado gerado contém algum estado final do afd original
            if any(estado_final in new_V_str.split(',') for estado_final in F):
                if new_V_str not in new_F:
                    new_F.append(new_V_str)
    
    #Criar um afd novo
    afd = {
        "V": new_V,
        "Q": Q,
        "delta": new_Delta,
        "q0": new_Initial,
        "F": new_F
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
    print(dot_representation)
 
# Carrega o AFND do arquivo JSON
# if len(sys.argv) < 2:
#     print("?")
#     sys.exit(1)

# Salvar um afd em um arquivo JSON
def save_file(afd, outputf):
    # Criar uma cópia do AFD para não modificar o original
    afd_copy = afd.copy()

    print(afd)
    print(afd_copy)
    
    # Converter conjuntos para listas
    afd_copy["V"] = list(afd_copy["V"])
    afd_copy["Q"] = list(afd_copy["Q"])
    for state, transitions in afd_copy["delta"].items():
        for input_val, end_states in transitions.items():
            afd_copy["delta"][state][input_val] = list(end_states)
    afd_copy["F"] = list(afd_copy["F"])
    
    # Salvar o AFD serializado em JSON
    with open(outputf, 'w') as file:
        json.dump(afd_copy, file, indent=4)
 
# Assume que o primeiro argumento é o arquivo JSON
arquivo = sys.argv[1]
afnd = read_afnd(arquivo)
afd = convert_afd(afnd)

# Verifica se o argumento graphviz foi passado
if '-graphviz' in sys.argv:
    generate_graph(afnd)
 
# Verifica se o argumento output foi passado
elif '-output' in sys.argv:
    indice_output = sys.argv.index('-output') #Procura a posição do argumento
    if indice_output + 1 < len(sys.argv):
        arquivo = sys.argv[indice_output + 1]
        save_file(afnd, arquivo)
    else:
        print("Especifique o arquivo de saída com o argumento '-output'.")
else:
    print("Comando não reconhecido.")