REG_Names = {
    "000":[0, "R0"],
    "001":[1, "R1"],
    "010":[2, "R2"],
    "011":[3, "R3"],
    "100":[4, "R4"],
    "101":[5, "R5"],
    "110":[6, "R6"],
    "111":[7, "FLAGS"]
}

OPCODES = {
    "00000":["A", "add"],
    "00001":["A", "sub"],
    "00010":["B", "mov"],
    "00011":["C", "mov"],
    "00100":["D", "ld"],
    "00101":["D", "st"],
    "00110":["A", "mul"],
    "00111":["C", "div"],
    "01000":["B", "rs"],
    "01001":["B", "ls"],
    "01010":["A", "xor"],
    "01011":["A", "or"],
    "01100":["A", "and"],
    "01101":["C", "not"],
    "01110":["C", "cmp"],
    "01111":["E", "jmp"],
    "10000":["E", "jlt"],
    "10001":["E", "jgt"],
    "10010":["E", "je"],
    "10011":["F", "hlt"],
}

