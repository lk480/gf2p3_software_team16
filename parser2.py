# Tokenize input
def tokenize(data):
    tokens = []
    current_token = ""
    inside_comment = False

    for char in data:
        if char == "#":
            inside_comment = True
        elif char == "\n":
            inside_comment = False
        elif inside_comment:
            continue

        if char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in [":", ",", ";", "=", ".", "(", ")", "[", "]"]:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    return tokens

# Parsing rules
def parse_overall_circuit(tokens):
    if parse_new_devices(tokens) and parse_connections(tokens):
        print("Parsed overall_circuit")
    else:
        print("Failed to parse overall_circuit")

def parse_new_devices(tokens):
    if parse_new_device(tokens) and parse_new_devices(tokens):
        return True
    else:
        return False

def parse_new_device(tokens):
    if expect("NEW_DEVICE", tokens) and expect(":", tokens) and expect("DEVICE_NAME", tokens) \
            and expect(",", tokens) and expect("DEVICE_TYPE", tokens) and parse_device_property(tokens) \
            and expect(";", tokens):
        print("Parsed new_device")
        return True
    else:
        return False

def parse_device_property(tokens):
    if parse_define_inputs(tokens) or parse_define_switch_state(tokens) or parse_define_clock_period(tokens):
        return True
    else:
        return False

def parse_define_inputs(tokens):
    if expect("INPUTS", tokens) and expect("(", tokens) and expect("INTEGER", tokens) \
            and expect(",", tokens) and expect("INTEGER", tokens) and expect(")", tokens):
        print("Parsed define_inputs")
        return True
    else:
        return False

def parse_define_switch_state(tokens):
    if expect("STATE", tokens) and expect("(", tokens) and expect("INTEGER", tokens) \
            and expect(",", tokens) and expect("INTEGER", tokens) and expect(")", tokens):
        print("Parsed define_switch_state")
        return True
    else:
        return False

def parse_define_clock_period(tokens):
    if expect("PERIOD", tokens) and expect("(", tokens) and expect("INTEGER", tokens) \
            and expect(",", tokens) and expect("INTEGER", tokens) and expect(")", tokens):
        print("Parsed define_clock_period")
        return True
    else:
        return False

def parse_connections(tokens):
    if expect("CONNECT", tokens) and expect(":", tokens) and parse_connectionlist(tokens):
        print("Parsed connections")
        return True
    else:
        return False

def parse_connectionlist(tokens):
    if parse_connection(tokens) and (expect(",", tokens) and parse_connectionlist(tokens)) or expect(";", tokens):
        print("Parsed connectionlist")
        return True
    else:
        return False

def parse_connection(tokens):
    if expect("DEVICE_NAME", tokens) and expect(".", tokens) and expect("I", tokens) \
            and expect("INTEGER", tokens) and expect("=", tokens) and expect("DEVICE_NAME", tokens):
        print("Parsed connection")
        return True
    else:
        return False

def expect(expected_token_type, tokens):
    if tokens and tokens[0] == expected_token_type:
        tokens.pop(0)
        return True
    else:
        print(f"Expected {expected_token_type}, but found {tokens[0]}")
        return False

# Input string
input_string = """
NEW_DEVICE: G1, NAND, 2;
NEW_DEVICE: G2, NAND, 2;
CONNECT: G2.I1 = SW1, G1.I2 = G2, G2.I1 = G1, G2.I2 = SW2;
"""

# Tokenize and parse the input
tokens = tokenize(input_string)
parse_overall_circuit(tokens)
