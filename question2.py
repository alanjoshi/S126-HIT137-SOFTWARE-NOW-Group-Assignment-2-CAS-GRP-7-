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


class Token:
    """Stores token type and value from the expression"""
    def __init__(self, type_, value):
        self.type = type_     # NUM, OP, LPAREN, RPAREN, END
        self.value = value


def tokenize(expression):
    """
    Breaks the expression into tokens.
    Returns list of tokens or None if invalid character found.
    """
    tokens = []
    i = 0
    n = len(expression)
    
    while i < n:
        ch = expression[i]
        
        # Skip spaces
        if ch == ' ':
            i = i + 1
            continue
        
        # Handle numbers (integers and decimals)
        if ch.isdigit() or ch == '.':
            num = ""
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num = num + expression[i]
                i = i + 1
            tokens.append(Token("NUM", float(num)))
            continue
        
        # Handle operators
        if ch in '+-*/':
            tokens.append(Token("OP", ch))
            i = i + 1
            continue
        
        # Handle left parenthesis
        if ch == '(':
            tokens.append(Token("LPAREN", '('))
            i = i + 1
            continue
        
        # Handle right parenthesis
        if ch == ')':
            tokens.append(Token("RPAREN", ')'))
            i = i + 1
            continue
        
        # Invalid character found
        return None
    
    # Add end marker
    tokens.append(Token("END", None))
    return tokens


def parse_factor(tokens, pos):
    """
    Parses a factor - handles numbers, parentheses, and unary minus.
    Returns (tree, new_position)
    """
    if pos >= len(tokens):
        return None, pos
    
    token = tokens[pos]
    
    # Number literal
    if token.type == "NUM":
        return token.value, pos + 1
    
    # Parenthesized expression
    if token.type == "LPAREN":
        expr, new_pos = parse_expression(tokens, pos + 1)
        if new_pos < len(tokens) and tokens[new_pos].type == "RPAREN":
            return expr, new_pos + 1
        return None, pos
    
    # Unary negation
    if token.type == "OP" and token.value == '-':
        operand, new_pos = parse_factor(tokens, pos + 1)
        if operand is not None:
            return ('neg', operand), new_pos
        return None, pos
    
    return None, pos


def parse_term(tokens, pos):
    """
    Parses a term - handles multiplication and division.
    Returns (tree, new_position)
    """
    left, new_pos = parse_factor(tokens, pos)
    if left is None:
        return None, pos
    
    while new_pos < len(tokens):
        token = tokens[new_pos]
        if token.type == "OP" and token.value in ('*', '/'):
            op = token.value
            right, next_pos = parse_factor(tokens, new_pos + 1)
            if right is None:
                return None, pos
            left = (op, left, right)
            new_pos = next_pos
        else:
            break
    
    return left, new_pos


def parse_expression(tokens, pos):
    """
    Parses an expression - handles addition and subtraction.
    Returns (tree, new_position)
    """
    left, new_pos = parse_term(tokens, pos)
    if left is None:
        return None, pos
    
    while new_pos < len(tokens):
        token = tokens[new_pos]
        if token.type == "OP" and token.value in ('+', '-'):
            op = token.value
            right, next_pos = parse_term(tokens, new_pos + 1)
            if right is None:
                return None, pos
            left = (op, left, right)
            new_pos = next_pos
        else:
            break
    
    return left, new_pos


def tree_to_string(tree):
    """
    Converts the parse tree to required string format.
    Example: (+ 3 5) or (neg (+ 3 4))
    """
    if tree is None:
        return "ERROR"
    
    # Number literal
    if isinstance(tree, (int, float)):
        if tree == int(tree):
            return str(int(tree))
        return str(tree)
    
    # Binary operation
    if isinstance(tree, tuple) and len(tree) == 3:
        op, left, right = tree
        return "(" + op + " " + tree_to_string(left) + " " + tree_to_string(right) + ")"
    
    # Unary negation
    if isinstance(tree, tuple) and len(tree) == 2 and tree[0] == 'neg':
        return "(neg " + tree_to_string(tree[1]) + ")"
    
    return "ERROR"


def evaluate_tree(tree):
    """
    Evaluates the parse tree recursively.
    Returns numeric result or None for errors (division by zero).
    """
    if tree is None:
        return None
    
    # Number literal
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
    Converts token list to required format.
    Example: [NUM:3] [OP:+] [NUM:5] [END]
    """
    if tokens is None:
        return "ERROR"
    
    result = []
    for t in tokens:
        if t.type == "NUM":
            val = t.value
            if val == int(val):
                result.append("[NUM:" + str(int(val)) + "]")
            else:
                result.append("[NUM:" + str(val) + "]")
        elif t.type == "OP":
            result.append("[OP:" + t.value + "]")
        elif t.type == "LPAREN":
            result.append("[LPAREN:(]")
        elif t.type == "RPAREN":
            result.append("[RPAREN:)]")
        elif t.type == "END":
            result.append("[END]")
    
    return " ".join(result)


def evaluate_expression(expression):
    """
    Evaluates a single mathematical expression.
    Returns dictionary with input, tree, tokens, and result.
    """
    expr = expression.strip()
    
    # Check for invalid characters (like @, #, etc.)
    invalid = re.findall(r'[^0-9+\-*/()\s.]', expr)
    if invalid:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
    
    # Tokenize
    tokens = tokenize(expr)
    if tokens is None:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
    
    # Parse
    tree, pos = parse_expression(tokens, 0)
    if tree is None or pos != len(tokens) - 1:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": tokens_to_string(tokens),
            "result": "ERROR"
        }
    
    # Evaluate
    result = evaluate_tree(tree)
    
    # Format result according to spec
    if result is None:
        result_str = "ERROR"
    elif result == int(result):
        result_str = str(int(result))
    else:
        result_str = "{:.4f}".format(result).rstrip('0').rstrip('.')
    
    return {
        "input": expr,
        "tree": tree_to_string(tree),
        "tokens": tokens_to_string(tokens),
        "result": result_str
    }


def evaluate_file(input_path):
    """
    Reads expressions from input file, writes output.txt.
    Returns list of result dictionaries for each expression.
    This is the main function required by the assignment.
    """
    input_file = Path(input_path)
    output_file = input_file.parent / "output.txt"
    
    # Read all expressions from input file
    expressions = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
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
            if i < len(results) - 1:
                f.write("\n")
    
    return results


# Run the program
if __name__ == "__main__":
    results = evaluate_file("sample_input_2.txt")
    for res in results:
        print("Input:", res["input"])
        print("Tree:", res["tree"])
        print("Tokens:", res["tokens"])
        print("Result:", res["result"])
        print()
    print("Done! Check output.txt")