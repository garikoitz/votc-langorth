# Devuelve un list con la misma longitud de a diciendo cuantas ocurrencias ha
# encontrado en b. OJo, solo devuelve el index del primero que encuentra. Si hay
# mas de una ocurrencias las ignora


def ismember(a, b):
    bind = {}
    for i, elt in enumerate(b):
        if elt not in bind:
            bind[elt] = i
    return [bind.get(itm, None) for itm in a]
