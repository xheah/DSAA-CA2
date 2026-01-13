"""
Turning a string into tokens
Convert a raw expression like (Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))
into a list like 
["(", "Alpha", "+", "(", "Delta", "+", "(", "Pi", "*", "(", "Beta", "*", "(", "Gamma", "/", "Sigma", ")", ")", ")", ")", ")"]

Supports operators: +, -, *, /, ++, **, //
"""
from string import ascii_letters


def tokenize(expr: str) -> list[str]:
    """
    Tokenize a DASK expression string into a list of tokens.
    
    Args:
        expr: The expression string to tokenize
        
    Returns:
        A list of tokens (variables, operators, parentheses, etc.)
    """
    tokens = []
    var = ''
    i = 0
    
    while i < len(expr):
        ch = expr[i]
        
        if ch in ascii_letters:
            # Accumulate letters into a variable name
            var += ch
        else:
            # When we hit a non-letter, add any accumulated variable first
            if len(var) > 0:
                tokens.append(var)
                var = ''
            
            # Check for multi-character operators: ++, **, //
            if i + 1 < len(expr):
                two_char = ch + expr[i + 1]
                if two_char in ['++', '**', '//']:
                    tokens.append(two_char)
                    i += 1  # Skip the next character since we've consumed it
                else:
                    tokens.append(ch)
            else:
                # Last character, just add it
                tokens.append(ch)
        
        i += 1
    
    # Add any remaining variable at the end
    if len(var) > 0:
        tokens.append(var)
    
    return tokens
