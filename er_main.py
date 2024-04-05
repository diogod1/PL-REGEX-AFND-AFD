import json

def ler_expressao_regular(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            expressao_regular = json.load(arquivo)
            print(f"Arquivo '{nome_arquivo}' encontrado.")
        return expressao_regular
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"O arquivo '{nome_arquivo}' não contém um JSON válido.")
        return None

def construir_afnd(er):
    if 'simb' in er:  # É um símbolo do alfabeto
        estado_inicial = 'q0'
        estado_final = 'q1'
        alfabeto = {er['simb']}
        transicoes = {'q0': {er['simb']: {'q1'}}}
        return {'estados': {'q0', 'q1'}, 'alfabeto': alfabeto, 'estado_inicial': 'q0', 'estados_finais': {'q1'}, 'transicoes': transicoes}

    elif 'op' in er:
        if er['op'] == 'alt' or er['op'] == 'seq':  # Operador de alternativa ou concatenação
            afnd1 = construir_afnd(er['args'][0])
            afnd2 = construir_afnd(er['args'][1])
            if afnd1 is None or afnd2 is None:  # Verifica se alguma das expressões é inválida
                return None
            novo_estado_inicial = 'q0'
            novo_estado_final = 'q' + str(len(afnd1['estados']) + len(afnd2['estados']))
            alfabeto = afnd1['alfabeto'] | afnd2['alfabeto']

            transicoes = {'q0': {}}
            transicoes['q0'].update(afnd1['transicoes'].get(afnd1['estado_inicial'], {}))
            transicoes['q0'].update(afnd2['transicoes'].get(afnd2['estado_inicial'], {}))
            transicoes['q0']['epsilon'] = {afnd1['estado_inicial'], afnd2['estado_inicial']}

            for estado in afnd1['estados'] | afnd2['estados']:
                transicoes[estado] = afnd1['transicoes'].get(estado, {}).copy()
                transicoes[estado].update(afnd2['transicoes'].get(estado, {}).copy())
                if estado in afnd1['estados_finais'] or estado in afnd2['estados_finais']:
                    transicoes[estado]['epsilon'] = transicoes.get(estado, {}).get('epsilon', set()) | {novo_estado_final}

            return {'estados': afnd1['estados'] | afnd2['estados'] | {novo_estado_inicial, novo_estado_final}, 'alfabeto': alfabeto, 'estado_inicial': novo_estado_inicial, 'estados_finais': {novo_estado_final}, 'transicoes': transicoes}

        elif er['op'] == 'kle':  # Operador de fecho de Kleene
            afnd = construir_afnd(er['args'][0])
            if afnd is None:  # Verifica se a expressão é inválida
                return None
            novo_estado_inicial = 'q0'
            novo_estado_final = 'q' + str(len(afnd['estados']) + 1)
            alfabeto = afnd['alfabeto']

            transicoes = {'q0': {}}
            transicoes['q0'].update(afnd['transicoes'].get(afnd['estado_inicial'], {}))
            transicoes['q0']['epsilon'] = {afnd['estado_inicial'], novo_estado_final}

            for estado in afnd['estados'] | {novo_estado_final}:
                transicoes[estado] = afnd['transicoes'].get(estado, {}).copy()
                if estado in afnd['estados_finais']:
                    transicoes[estado]['epsilon'] = transicoes.get(estado, {}).get('epsilon', set()) | {afnd['estado_inicial'], novo_estado_final}

            return {'estados': afnd['estados'] | {novo_estado_inicial, novo_estado_final}, 'alfabeto': alfabeto, 'estado_inicial': novo_estado_inicial, 'estados_finais': {novo_estado_final}, 'transicoes': transicoes}

def escrever_afnd_em_arquivo(afnd, nome_arquivo):
    afnd_dict = {
        "estados": list(afnd['estados']),
        "alfabeto": list(afnd['alfabeto']),
        "estado_inicial": afnd['estado_inicial'],
        "estados_finais": list(afnd['estados_finais']),
        "transicoes": afnd['transicoes']
    }
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(afnd_dict, arquivo, indent=4)

def main(): 
    expressao_regular = ler_expressao_regular('exemplo02.er.json')
    if expressao_regular:
        afnd = construir_afnd(expressao_regular)
        if afnd:
            escrever_afnd_em_arquivo(afnd, 'afnd.json')
            print("AFND gerado com sucesso em 'afnd.json'.")
        else:
            print("Expressão regular inválida ou não suportada para a construção do AFND.")
    else:
        print("Não foi possível ler a expressão regular do arquivo.")

main()