global REG
global OPCODES
global TEMP
global MEM

MEM = [0 for i in range(0,256)]

TEMP = ["","","","","",""]    # [opcode, reg1, reg2, reg3, imm_val, mem_adr]
REG_Names = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R4":"101",
    "R6":"110",
    "FLAGS":"111"
}
REG = ["","","","","","","",[0,0,0,0]]     # [R0, R1, ..., R6, [V,L,G,E]]
OPCODES = {
    "add": ["00000", "A"],
    "sub": ["00001", "A"],
    "mov": ["00010", "B"],
    "mov": ["00011", "C"],
    "ld": ["00100", "D"],
    "st": ["00101", "D"],
    "mul": ["00110", "A"],
    "div": ["00111", "C"],
    "rs": ["01000", "B"],
    "ls": ["01001", "B"],
    "xor": ["01010", "A"],
    "or": ["01011", "A"],
    "and": ["01100", "A"],
    "not": ["01101", "C"],
    "cmp": ["01110", "C"],
    "jmp": ["01111", "E"],
    "jlt": ["10000", "E"],
    "jgt": ["10001", "E"],
    "je": ["10010", "E"],
    "hlt": ["10011", "F"],
}

def instruction_type(instruction):
    op = instruction[0]
    if op in OPCODES:
        op_code = OPCODES[op][0]
        op_type = OPCODES[op][1]
        TEMP[0] = op_code
    else:
        # ERROR 
        pass
    if(op=="mov"):
        if(instruction[2] in REG_Names): 
            TEMP[0] = "00011"
            op_type = "C"
        else:
            TEMP[0] = "00010"
            op_type = "B"
    if(op_type=="A"): instruction_A(instruction)
    elif(op_type=="B"): instruction_B(instruction)
    elif(op_type=="C"): instruction_C(instruction)
    elif(op_type=="D"): instruction_D(instruction)
    elif(op_type=="E"): instruction_E(instruction)
    elif(op_type=="F"): instruction_F(instruction)
    else:
        pass

def instruction_A(instruction):
    reg1 = instruction[7:10] 
    reg2 = instruction[10:13] 
    reg3 = instruction[13:16] 
    TEMP[1] = reg1
    TEMP[2] = reg2
    TEMP[3] = reg3
    if(TEMP[0]=="00000"): add_A(instruction)
    elif(TEMP[0]=="00001"): sub_A(instruction)
    elif(TEMP[0]=="00110"): mul_A(instruction)
    elif(TEMP[0]=="01010"): xor_A(instruction)
    elif(TEMP[0]=="01011"): or_A(instruction)
    elif(TEMP[0]=="01100"): and_A(instruction)
    else:
        pass
    
def instruction_B(instruction):
    reg1 = instruction[5:8] 
    imm_val = instruction[8:16] 
    TEMP[1] = reg1
    TEMP[4] = imm_val
    if(TEMP[0]=="00010"): mov_imm_B(instruction)
    elif(TEMP[0]=="01000"): rs_B(instruction)
    elif(TEMP[0]=="01001"): ls_B(instruction)
    else:
        pass

def instruction_C(instruction):
    reg1 = instruction[10:13] 
    reg2 = instruction[13:16] 
    TEMP[1] = reg1
    TEMP[2] = reg2
    if(TEMP[0]=="00011"): mov_reg_C(instruction)
    elif(TEMP[0]=="00111"): div_C(instruction)
    elif(TEMP[0]=="01101"): not_C(instruction)
    elif(TEMP[0]=="01110"): cmp_C(instruction)
    else:
        pass
    
def instruction_D(instruction):
    reg1 = instruction[5:8] 
    mem_addr = instruction[8:16] 
    TEMP[1] = reg1
    TEMP[5] = mem_addr
    if(TEMP[0]=="00100"): load_D(instruction)
    elif(TEMP[0]=="00101"): store_D(instruction)
    else:
        pass

def instruction_E(instruction):
    mem_addr = instruction[8:16] 
    TEMP[5] = mem_addr
    if(TEMP[0]=="01111"): jmp_E(instruction)
    elif(TEMP[0]=="10000"): jlt_E(instruction)
    elif(TEMP[0]=="10001"): jgt_E(instruction)
    elif(TEMP[0]=="10010"): je_E(instruction)
    else:
        pass
    
def instruction_F(instruction):
    if(TEMP[0]=="10011"): hlt_F(instruction)

def add_A(instruction):
    pass
def sub_A(instruction):
    pass
def mov_imm_B(instruction):
    pass
def mov_reg_C(instruction):
    pass
def load_D(instruction):
    pass
def store_D(instruction):
    pass
def mul_A(instruction):
    pass
def div_C(instruction):
    pass
def rs_B(instruction):
    pass
def ls_B(instruction):
    pass
def xor_A(instruction):
    pass
def or_A(instruction):
    pass
def and_A(instruction):
    pass
def not_C(instruction):
    pass
def cmp_C(instruction):
    pass
def jmp_E(instruction):
    pass
def jlt_E(instruction):
    pass
def jgt_E(instruction):
    pass
def je_E(instruction):
    pass
def hlt_F(instruction):
    pass