# gf2p3_software_team16

This is a repo for Team 16 GF2 Software Project. This project contains software used to simulate logic circuits. See the EBNF Syntax below for definition file syntax, and use python logsim.py {path to definition .txt file} to get started. See separate user guide.

## Install requirements

pip install -r requirements.txt

## Commands to generate new .pot, .po and .mo files

Simply replace {directory} with the desired directory and {Iso language code} with the desired code, such as en_GB or es_ES.
The babel.cfg file can be found in the languages folder.

pybabel extract -F {path to babel.cfg}babel.cfg -o messages.pot gui.py
pybabel init -i messages.pot -d {directory} -l {Iso langauge code}
pybabel compile -f -d {directory}

## EBNF SYNTAX

### # Here we define what is new_devices

new_device = "DEVICE", ":", device_name, ",", device_type, ",", device_property, ";",;

device_name = letter, {letter | positive_non_zero_integer};
device_type = "CLOCK" | "SWITCH" | "NAND" | "DTYPE" | "XOR" | "AND" |
              "OR" | "NOR" | "NOT";
device_property = [define_inputs | define_switch_state | define_clock_period];

define_inputs = "INPUTS(",{positive_non_zero_integer, ","},
                positive_non_zero_integer, ")";
define_switch_state = "STATE(", {switch_state, ","}, switch_state, ")";
switch_state = "0" | "1";
define_clock_period = "PERIOD(", {positive_non_zero_integer, ","},
                      positive_non_zero_integer, ")";

### # Here we define connections

connectionlist = "CONNECT", ":", connection, {",",connection},";";

connection = ip_device, '=', op_device
output = device_name, "." ["Q" | "QBAR"];
input = device_name, "." ("I", positive_non_zero_integer);

### # Definition of monitors

monitors = "MONITOR", ":" , {output, ","}, output;

### # Additional definitions

non_zero_digit = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
digit = "0" | digit_excluding_zero;

lowercase_letter = "a"| "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"| "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z";

uppercase_letter = "A"| "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"| "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z";

space_tab = " " | "\t";

letter = lowercase_letter | uppercase_letter;
alphanumeric = digit | lowercase_letter | uppercase_letter;
comment = "#", {alphanumeric | space_tab} , '#'

sign = "+” | ”-”;
integer = ([sign], non_zero_digit, {digit}) | "0";
positive_non_zero_integer = non_zero_digit, {digit};

### # Examples of EBNF Grammar

DEVICE: G1, NAND, 2;
DEVICE: G2, NAND, 2;
CONNECT: G2.I1 = SW1, G1.I2 = G2, G2.I1 = G1, G2.I2 = SW2;
MONITOR: G1, G2;
