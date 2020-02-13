from random import randint
literals = "ABCDDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*=':;,.+-"
def get_token():
    mixed_literals = ""
    lower_limit = 0
    upper_limit = len(literals)
    happend = set()
    while len(happend) < upper_limit:
        arbi_pos = randint(lower_limit,upper_limit-1)
        if arbi_pos not in happend:
            happend.add(arbi_pos)
            mixed_literals += literals[arbi_pos]
    
    token_literal_pos = []
    while len(token_literal_pos) < 23:
        temp_pos = randint(lower_limit,upper_limit-1)
        if temp_pos not in token_literal_pos:
            token_literal_pos.append(temp_pos)
    token = ""
    for i in token_literal_pos:
        token += mixed_literals[i]
    return token

print(get_token())