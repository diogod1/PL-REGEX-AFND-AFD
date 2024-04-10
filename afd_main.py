import json, sys

exec_interp_autom: bool = False
exec_cria_graph: bool = False

if len(sys.argv) == 1:
    print("Inserir comando!\n")
    exit(-1)
else:
    #Verifica se o ficheiro é um json
    if not sys.argv[1].endswith('json'):
        print("Insira um ficheiro *.json")
        exit(-1)
    
    #Definir/abrir o caminho do ficheiro   
    afpath = sys.argv[1]
    with open(afpath, "r", encoding="utf-8") as f:
        af = json.load(f)  

    #Função para Autómatos Finitos Deterministas
    if(sys.argv[2].lower() == "-rec"):  
        #verifica se tem expressão
        if len(sys.argv) != 4: 
          print("Inserir palavra a analisar\n")
        else: 
            #executa a função
            exec_interp_autom = True
    #Função para criar um grafo
    elif sys.argv[2].lower() == "-graphviz":
        #executa a função
        exec_cria_graph = True

# -----
# definição do Autómato Finito 
#    AF=(V,Q,delta,q0,F) tal que:
V = set(af["V"])
Q = set(af["Q"])
delta =	af["delta"]	
q0 = af["q0"]
F = set(af["F"]) 

#Interpretação do Autómato Finito
def interp_autom( palavra: str ) -> str:
    estado_atual: str = q0 #estado inicial
    caminho = []
    tam = len(palavra)
    i = 0
    while( i < tam ):
        simbolo = palavra[i] #simbolo atual
        caminho.append(f"{estado_atual}-{simbolo}")
        #Verifica se simbolo está no alfabeto
        if simbolo not in V:
            return f"‘{palavra}’ nao e reconhecida\n[símbolo ‘{palavra[i]}’ nao pertence ao alfabeto]"
        
        #Seguir o caminho
        if simbolo in delta[estado_atual]:
            estado_atual = delta[ estado_atual ][ simbolo ]
        else:
            return f"Palavra ‘{palavra}’ nao e reconhecida"
        
        i += 1
        
    #se na ultima iteração o estado atual for diferente do Final
    if estado_atual not in F:
        return f"Palavra {palavra} nao e reconhecida.\n [Caminho: {'>'.join(caminho)} {estado_atual}, {estado_atual} nao e final]\n"
    else:
        return f"Palavra {palavra} e reconhecida.\n [Caminho: {'>'.join(caminho)} {estado_atual}]\n"

def cria_graph()-> int:
    #Abrir ou/e criar um ficheio *.gv
    with open('graph.gv', 'w') as file:
        # Escrever no ficheiro
        file.write('digraph {\n')
        file.write(f"\tnode [shape = doublecircle]; {' '.join(F)};\n")
        file.write('\tnode [shape = point  ]; initial;\n')
        file.write('\tnode [shape = circle];\n')
        file.write(f'\tinitial->{q0}\n')
        for i in Q:
            simbolo = delta[i]
            for y in simbolo:
                path = delta[i][y]
                file.write(f"\t{i}->{path}[label = \"{y}\"];\n")
        file.write('}\n')

if exec_interp_autom == True:
    print(interp_autom(sys.argv[3]))
elif exec_cria_graph == True:
    cria_graph()
