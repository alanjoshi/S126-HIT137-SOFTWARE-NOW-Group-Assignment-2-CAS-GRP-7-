# HIT137 Assignment 2 - Question 2
# Mathematical Expression Evaluator using Recursive Descent Parsing
#Group 7
# Member 1: Swojan Singh Maharjan - s401770

# Member 2: Alan Joshi John - s394323
# Member 3: Sandip Kharel - s401293
# Member 4: Haonan ding - s394323
# Date: April 2026

from pathlib import Path
import re


def tokenize(expression):
    """
    Convert expression string into list of tokens.
    Each token is a tuple: (type, value)
    Token types: NUM, OP, LPAREN, RPAREN, END
    
    Returns list of tokens or None if invalid character found.
    """
    tokens = []
    i = 0
    n = len(expression)
    
    while i < n:
        ch = expression[i]
        
        # Skip whitespace characters
        if ch == ' ':
            i += 1
            continue
        
        # Handle numbers (integers and decimals)
        if ch.isdigit() or ch == '.':
            num = ""
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(("NUM", float(num)))
            continue
        
        # Handle operators
        if ch in '+-*/':
            tokens.append(("OP", ch))
            i += 1
            continue
        
        # Handle left parenthesis
        if ch == '(':
            tokens.append(("LPAREN", '('))
            i += 1
            continue
        
        # Handle right parenthesis
        if ch == ')':
            tokens.append(("RPAREN", ')'))
            i += 1
            continue
        
        # Invalid character found
        return None
    
    # Add end marker to signal end of input
    tokens.append(("END", None))
    return tokens


def parse_factor(tokens, pos):
    """
    Parse a factor - highest precedence level.
    Handles:
    - Numbers (e.g., 5, 3.14)
    - Parenthesized expressions (e.g., (3+4))
    - Unary minus (e.g., -5, -(3+4))
    
    Returns: (tree, new_position)
    """
    if pos >= len(tokens):
        return None, pos
    
    token_type, token_value = tokens[pos]
    
    # Case 1: Number literal
    if token_type == "NUM":
        return token_value, pos + 1
    
    # Case 2: Parenthesized expression
    if token_type == "LPAREN":
        # Recursively parse what's inside the parentheses
        expr, new_pos = parse_expression(tokens, pos + 1)
        # Expect a closing parenthesis
        if new_pos < len(tokens) and tokens[new_pos][0] == "RPAREN":
            return expr, new_pos + 1
        return None, pos
    
    # Case 3: Unary minus (negation)
    if token_type == "OP" and token_value == '-':
        # Parse what comes after the minus sign
        operand, new_pos = parse_factor(tokens, pos + 1)
        if operand is not None:
            return ('neg', operand), new_pos
        return None, pos
    
    return None, pos


def parse_term(tokens, pos):
    """
    Parse a term - middle precedence level.
    Handles multiplication (*) and division (/)
    
    Returns: (tree, new_position)
    """
    # Parse the first factor
    left, new_pos = parse_factor(tokens, pos)
    if left is None:
        return None, pos
    
    # Keep combining while we see * or /
    while new_pos < len(tokens):
        token_type, token_value = tokens[new_pos]
        if token_type == "OP" and token_value in ('*', '/'):
            op = token_value
            # Parse the next factor
            right, next_pos = parse_factor(tokens, new_pos + 1)
            if right is None:
                return None, pos
            # Combine into binary operation tree
            left = (op, left, right)
            new_pos = next_pos
        else:
            break
    
    return left, new_pos


def parse_expression(tokens, pos):
    """
    Parse an expression - lowest precedence level.
    Handles addition (+) and subtraction (-)
    
    Returns: (tree, new_position)
    """
    # Parse the first term
    left, new_pos = parse_term(tokens, pos)
    if left is None:
        return None, pos
    
    # Keep combining while we see + or -
    while new_pos < len(tokens):
        token_type, token_value = tokens[new_pos]
        if token_type == "OP" and token_value in ('+', '-'):
            op = token_value
            # Parse the next term
            right, next_pos = parse_term(tokens, new_pos + 1)
            if right is None:
                return None, pos
            # Combine into binary operation tree
            left = (op, left, right)
            new_pos = next_pos
        else:
            break
    
    return left, new_pos


def tree_to_string(tree):
    """
    Convert parse tree to required string format.
    
    Examples:
    - Number: 5 -> "5"
    - Binary: ('+', 3, 5) -> "(+ 3 5)"
    - Unary: ('neg', 5) -> "(neg 5)"
    """
    if tree is None:
        return "ERROR"
    
    # Handle numbers
    if isinstance(tree, (int, float)):
        if tree == int(tree):
            return str(int(tree))  # Remove .0 for whole numbers
        return str(tree)
    
    # Handle binary operations (+, -, *, /)
    if isinstance(tree, tuple) and len(tree) == 3:
        op, left, right = tree
        return "(" + op + " " + tree_to_string(left) + " " + tree_to_string(right) + ")"
    
    # Handle unary negation
    if isinstance(tree, tuple) and len(tree) == 2 and tree[0] == 'neg':
        return "(neg " + tree_to_string(tree[1]) + ")"
    
    return "ERROR"


def evaluate_tree(tree):
    """
    Recursively evaluate the parse tree.
    Returns numeric result or None for errors (like division by zero).
    """
    if tree is None:
        return None
    
    # Base case: number literal
    if isinstance(tree, (int, float)):
        return tree
    
    # Binary operation
    if isinstance(tree, tuple) and len(tree) == 3:
        op, left, right = tree
        left_val = evaluate_tree(left)
        right_val = evaluate_tree(right)
        
        if left_val is None or right_val is None:
            return None
        
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            # Check for division by zero
            if right_val == 0:
                return None
            return left_val / right_val
    
    # Unary negation
    if isinstance(tree, tuple) and len(tree) == 2 and tree[0] == 'neg':
        val = evaluate_tree(tree[1])
        if val is None:
            return None
        return -val
    
    return None


def tokens_to_string(tokens):
    """
    Convert token list to required output format.
    
    Example: [("NUM",3), ("OP","+"), ("NUM",5), ("END",None)]
    becomes: "[NUM:3] [OP:+] [NUM:5] [END]"
    """
    if tokens is None:
        return "ERROR"
    
    result = []
    for token_type, token_value in tokens:
        if token_type == "NUM":
            val = token_value
            if val == int(val):
                result.append("[NUM:" + str(int(val)) + "]")
            else:
                result.append("[NUM:" + str(val) + "]")
        elif token_type == "OP":
            result.append("[OP:" + token_value + "]")
        elif token_type == "LPAREN":
            result.append("[LPAREN:(]")
        elif token_type == "RPAREN":
            result.append("[RPAREN:)]")
        elif token_type == "END":
            result.append("[END]")
    
    return " ".join(result)


def evaluate_expression(expression):
    """
    Evaluate a single mathematical expression.
    Returns dictionary with input, tree, tokens, and result.
    """
    expr = expression.strip()
    
    # Check for invalid characters (like @, #, $, etc.)
    # Allowed: 0-9, +, -, *, /, (, ), ., and whitespace
    invalid = re.findall(r'[^0-9+\-*/()\s.]', expr)
    if invalid:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
    
    # Step 1: Tokenize
    tokens = tokenize(expr)
    if tokens is None:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
    
    # Step 2: Parse (build abstract syntax tree)
    tree, pos = parse_expression(tokens, 0)
    if tree is None or pos != len(tokens) - 1:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": tokens_to_string(tokens),
            "result": "ERROR"
        }
    
    # Step 3: Evaluate
    result = evaluate_tree(tree)
    
    # Step 4: Format result
    if result is None:
        result_str = "ERROR"
    elif result == int(result):
        result_str = str(int(result))  # Remove decimal for whole numbers
    else:
        # Round to 4 decimal places and remove trailing zeros
        result_str = "{:.4f}".format(result).rstrip('0').rstrip('.')
    
    return {
        "input": expr,
        "tree": tree_to_string(tree),
        "tokens": tokens_to_string(tokens),
        "result": result_str
    }


def evaluate_file(input_path):
    """
    Main function required by the assignment.
    
    Reads expressions from input file (one per line),
    evaluates each expression,
    writes results to output.txt in the same directory,
    returns list of result dictionaries.
    """
    input_file = Path(input_path)
    output_file = input_file.parent / "output.txt"
    
    # Read all expressions from input file
    expressions = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                expressions.append(line)
    
    # Evaluate each expression
    results = []
    for expr in expressions:
        results.append(evaluate_expression(expr))
    
    # Write output file in required format
    with open(output_file, 'w') as f:
        for i, res in enumerate(results):
            f.write("Input: " + res["input"] + "\n")
            f.write("Tree: " + res["tree"] + "\n")
            f.write("Tokens: " + res["tokens"] + "\n")
            f.write("Result: " + res["result"] + "\n")
            # Add blank line between expressions (not after last one)
            if i < len(results) - 1:
                f.write("\n")
    
    return results


# Run the program when script is executed directly
if __name__ == "__main__":
    results = evaluate_file("sample_input_2.txt")
    for res in results:
        print("Input:", res["input"])
        print("Tree:", res["tree"])
        print("Tokens:", res["tokens"])
        print("Result:", res["result"])
        print()
    print("Done! Check output.txt")