"""
Turning a string into tokens
Convert a raw expression like (Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))
into a list like 
["(", "Alpha", "+", "(", "Delta", "+", "(", "Pi", "*", "(", "Beta", "*", "(", "Gamma", "/", "Sigma", ")", ")", ")", ")", ")"]

Supports operators: +, -, *, /, ++, **, //
Supports multi-digit numbers: 100, 123, etc.
"""
from string import ascii_letters, digits


def tokenize(expr: str) -> list[str]:
    """
    Tokenize a DASK expression string into a list of tokens.
    
    Args:
        expr: The expression string to tokenize
        
    Returns:
        A list of tokens (variables, operators, parentheses, numbers, etc.)
    """
    tokens = []
    var = ''
    num = ''
    i = 0
    
    while i < len(expr):
        ch = expr[i]
        
        if ch in ascii_letters:
            # Accumulate letters into a variable name
            # If we have accumulated a number, add it first
            if len(num) > 0:
                tokens.append(num)
                num = ''
            var += ch
        elif ch in digits:
            # Accumulate digits into a number
            # If we have accumulated a variable, add it first
            if len(var) > 0:
                tokens.append(var)
                var = ''
            num += ch
        elif ch == '.':
            # Handle decimal numbers
            next_is_digit = i + 1 < len(expr) and expr[i + 1] in digits
            if len(var) > 0:
                tokens.append(var)
                var = ''
            if len(num) == 0 and next_is_digit:
                num = '0.'
            elif len(num) > 0 and '.' not in num:
                num += '.'
            else:
                # Treat as a standalone token if it doesn't belong to a number
                if len(num) > 0:
                    tokens.append(num)
                    num = ''
                tokens.append(ch)
        else:
            # When we hit a non-letter, non-digit, add any accumulated variable or number first
            if len(var) > 0:
                tokens.append(var)
                var = ''
            if len(num) > 0:
                tokens.append(num)
                num = ''
            
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
    
    # Add any remaining variable or number at the end
    if len(var) > 0:
        tokens.append(var)
    if len(num) > 0:
        tokens.append(num)
    
    return tokens
