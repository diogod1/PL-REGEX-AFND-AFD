import json

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

def state_set_to_string(state_set):
    """Converte um conjunto de estados em uma string ordenada e única."""
    return ",".join(sorted(state_set))

def convert_afnd_to_afd(V, Q, delta, q0, F):
    initial_state_str = state_set_to_string({q0})
    states = {initial_state_str}
    transitions = {}
    unmarked_states = [initial_state_str]
    final_states = set()

    while unmarked_states:
        current_state_str = unmarked_states.pop()
        if current_state_str:
            current_state_set = set(current_state_str.split(','))
        else:
            current_state_set = set()

        for input_symbol in V:
            next_state_set = set()
            for substate in current_state_set:
                next_states = delta.get(substate, {}).get(input_symbol, [])
                next_state_set.update(next_states)
            
            next_state_str = state_set_to_string(next_state_set)
            if next_state_str and next_state_str not in states:
                states.add(next_state_str)
                unmarked_states.append(next_state_str)

            transitions[f"{current_state_str},{input_symbol}"] = next_state_str if next_state_set else ""

            if next_state_set and next_state_set.intersection(F):
                final_states.add(next_state_str)

    afd = {
        'states': list(states),
        'initial_state': initial_state_str,
        'final_states': list(final_states),
        'symbols': list(V),
        'transitions': transitions,
    }
    return afd

def afd_to_json_string(afd):
    parts = ['{']

    parts.append('"states": [')
    parts.append(', '.join(f'"{state}"' for state in afd['states'] if state))
    parts.append('],')

    parts.append(f'"initial_state": "{afd["initial_state"]}",')

    parts.append('"final_states": [')
    parts.append(', '.join(f'"{state}"' for state in afd['final_states']))
    parts.append('],')

    parts.append('"symbols": [')
    parts.append(', '.join(f'"{symbol}"' for symbol in afd['symbols']))
    parts.append('],')

    parts.append('"transitions": {')
    transition_parts = []
    for transition_key, nextState in afd['transitions'].items():
        state, symbol = transition_key.split(',')
        transition_parts.append(f'"{state},{symbol}": "{nextState}"')
    parts.append(', '.join(transition_parts))
    parts.append('}')

    parts.append('}')
    return ''.join(parts)

# Conversão de AFND para AFD e representação em string JSON
afd = convert_afnd_to_afd(V, Q, delta, q0, F)
afd_json_string = afd_to_json_string(afd)
print(afd_json_string)
