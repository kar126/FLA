def remove_epsilon_productions(grammar):
    def nullable(nonterminal, epsilon_producing, nullable_symbols):
        # A nonterminal is nullable if it directly produces ε or all its symbols are nullable
        if nonterminal in epsilon_producing:
            return True
        return all(symbol in nullable_symbols for symbol in grammar[nonterminal])

    def generate_new_productions(grammar, epsilon_producing):
        new_grammar = {}
        nullable_symbols = set()

        # Step 1: Identify epsilon-producing nonterminals
        for nonterminal, productions in grammar.items():
            if 'ε' in productions:
                epsilon_producing.add(nonterminal)
                nullable_symbols.add(nonterminal)

        # Step 2: Find all nullable symbols
        while True:
            added_nullable = False
            for nonterminal in grammar:
                if nonterminal not in nullable_symbols and nullable(nonterminal, epsilon_producing, nullable_symbols):
                    nullable_symbols.add(nonterminal)
                    added_nullable = True
            if not added_nullable:
                break

        # Step 3: Generate new productions without ε
        for nonterminal, productions in grammar.items():
            new_productions = set()
            for production in productions:
                if not any(symbol in epsilon_producing and symbol not in nullable_symbols for symbol in production):
                    new_productions.add(production.replace('ε', ''))

            new_grammar[nonterminal] = new_productions

        return new_grammar

    epsilon_producing = set()
    new_grammar = generate_new_productions(grammar, epsilon_producing)

    return new_grammar

# Example grammar represented as a dictionary
grammar = {
    'S': {'AaAb', 'ε'},
    'A': {'B', 'ε'},
    'B': {'c'}
}

# Remove ε productions
new_grammar = remove_epsilon_productions(grammar)

# Display the modified grammar
for nonterminal, productions in new_grammar.items():
    for production in productions:
        print(f"{nonterminal} -> {production}")
