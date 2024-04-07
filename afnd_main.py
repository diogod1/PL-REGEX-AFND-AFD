import json, sys
# Dados do AFND fornecidos
af = {
    "V": ["a", "b"],
    "Q": ["q0", "q1", "q2"],
    "delta": {
        "q0": {"a": ["q1"], "b": ["q0", "q1"]},
        "q1": {"a": ["q2"], "b": []},
        "q2": {"a": ["q2"], "b": ["q1"]}
    },
    "q0": "q0",
    "F": ["q2"]
}

# Variáveis globais derivadas dos dados do JSON
V = set(af["V"])
Q = set(af["Q"])
delta = af["delta"]
q0 = af["q0"]
F = set(af["F"])

def state_to_string(state):
    """Converte um conjunto de estados em uma string ordenada e única."""
    return ",".join(sorted(state))

def convert_afnd_to_afd(V, Q, delta, q0, F):
    initial_state_str = state_to_string([q0])
    states = {initial_state_str}
    transitions = {}
    unmarked_states = [initial_state_str]
    final_states = set()

    while unmarked_states:
        current_state_str = unmarked_states.pop()
        current_state = set(current_state_str.split(","))

        for input_symbol in V:
            next_state = set()
            for substate in current_state:
                if input_symbol in delta.get(substate, {}):
                    next_state.update(delta[substate][input_symbol])
            next_state_str = state_to_string(next_state)

            if next_state_str not in states:
                states.add(next_state_str)
                unmarked_states.append(next_state_str)

            transitions[(current_state_str, input_symbol)] = next_state_str

            if next_state.intersection(F):
                final_states.add(next_state_str)

    afd = {
        "states": list(states),
        "initial_state": initial_state_str,
        "final_states": list(final_states),
        "symbols": list(V),
        "transitions": {k: v for k, v in transitions.items()},
    }
    return afd

def afd_to_json_string(afd):
    """Converte o dicionário AFD em uma string JSON manualmente."""
    parts = []  # Para armazenar partes da string JSON
    parts.append('{')

    # Adiciona os estados
    parts.append('"states": [')
    parts.append(', '.join(f'"{state}"' for state in afd['states']))
    parts.append('],')

    # Adiciona o estado inicial
    parts.append(f'"initial_state": "{afd["initial_state"]}",')

    # Adiciona os estados finais
    parts.append('"final_states": [')
    parts.append(', '.join(f'"{state}"' for state in afd['final_states']))
    parts.append('],')

    # Adiciona os símbolos
    parts.append('"symbols": [')
    parts.append(', '.join(f'"{symbol}"' for symbol in afd['symbols']))
    parts.append('],')

    # Adiciona as transições
    parts.append('"transitions": {')
    transition_parts = []
    for (state, symbol), nextState in afd['transitions'].items():
        transition_parts.append(f'"{state},{symbol}": "{nextState}"')
    parts.append(', '.join(transition_parts))
    parts.append('}')

    parts.append('}')
    return ''.join(parts)

afd = convert_afnd_to_afd(V, Q, delta, q0, F)
afd_json_string = afd_to_json_string(afd)
print(afd_json_string)

