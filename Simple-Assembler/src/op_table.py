global REG
global OPCODES
global TEMP
global MEM_LINE
# global CURR_MEM_LINE
global CURR_LINE
global VAR_S
global LABEL_S
# global MEM_LD_ST
global ANS

ANS = [] # 16-bit instruction

# Stores data for address greater than MEM_LINE (= instr+var ) less than 256 else print error (if in var range then put in var_s instead)
# MEM_LD_ST = []
VAR_S = {}  # "var_name": [addr(int in decimal starting from 0), val(int in decimal initially None)]
LABEL_S = {}     # "label_name": [addr(int in decimal starting from 0)]

# CURR_MEM_LINE = 0
MEM_LINE = 0  # Mem occupied by instructions + variables 
CURR_LINE = 0

# (all are in string)
TEMP = [None,None,None,None,None,None]    # [opcode, reg1, reg2, reg3, imm_val, mem_adr] 
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
# (all are in int)
REG = [None,None,None,None,None,None,None,[0,0,0,0]]     # [R0, R1, ..., R6, [V,L,G,E]]
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
        if(len(instruction)>2 and instruction[2] in REG_Names): 
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
    # reset temp
    # reset FLAGS if not E instruction

def instruction_A(instruction):
    if(len(instruction)!=4):
        # ERROR
        pass
    reg1 = instruction[1] 
    reg2 = instruction[2] 
    reg3 = instruction[3] 
    TEMP[1] = reg1
    TEMP[2] = reg2
    TEMP[3] = reg3
    # validate registers
    if(TEMP[0]=="00000"): add_A(instruction)
    elif(TEMP[0]=="00001"): sub_A(instruction)
    elif(TEMP[0]=="00110"): mul_A(instruction)
    elif(TEMP[0]=="01010"): xor_A(instruction)
    elif(TEMP[0]=="01011"): or_A(instruction)
    elif(TEMP[0]=="01100"): and_A(instruction)
    else:
        pass
    
def instruction_B(instruction):
    if(len(instruction)!=3):
        # ERROR
        pass
    reg1 = instruction[1] 
    imm_val = instruction[2] 
    TEMP[1] = reg1
    TEMP[4] = imm_val
    # validate registers
    if(TEMP[0]=="00010"): mov_imm_B(instruction)
    elif(TEMP[0]=="01000"): rs_B(instruction)
    elif(TEMP[0]=="01001"): ls_B(instruction)
    else:
        pass

def instruction_C(instruction):
    if(len(instruction)!=3):
        # ERROR
        pass
    reg1 = instruction[1] 
    reg2 = instruction[2] 
    TEMP[1] = reg1
    TEMP[2] = reg2 
    # validate registers
    if(TEMP[0]=="00011"): mov_reg_C(instruction)
    elif(TEMP[0]=="00111"): div_C(instruction)
    elif(TEMP[0]=="01101"): not_C(instruction)
    elif(TEMP[0]=="01110"): cmp_C(instruction)
    else:
        pass
    
def instruction_D(instruction):
    if(len(instruction)!=3):
        # ERROR
        pass
    reg1 = instruction[1] 
    mem_addr = instruction[2] 
    TEMP[1] = reg1
    TEMP[5] = mem_addr
    # validate registers
    if(TEMP[0]=="00100"): load_D(instruction)
    elif(TEMP[0]=="00101"): store_D(instruction)
    else:
        pass

def instruction_E(instruction):
    if(len(instruction)!=2):
        # ERROR
        pass
    mem_addr = instruction[1] 
    TEMP[5] = mem_addr
    # validate registers
    if(TEMP[0]=="01111"): jmp_E(instruction)
    elif(TEMP[0]=="10000"): jlt_E(instruction)
    elif(TEMP[0]=="10001"): jgt_E(instruction)
    elif(TEMP[0]=="10010"): je_E(instruction)
    else:
        pass
    
def instruction_F(instruction):
    if(len(instruction)!=1):
        # ERROR
        pass
    if(TEMP[0]=="10011"): hlt_F(instruction)

def add_A(instruction):
    pass
def sub_A(instruction):
    pass
def mov_imm_B(instruction):
    pass
def mov_reg_C(instruction):
    s="0001100000"
    s = s + REG_Names(instruction[1]) + REG_Names(instruction[2])
    ANS.append(s)
def load_D(instruction):
    s = "00100"
    s = s + REG_Names(instruction[1]) + VAR_S(instruction[2])[0]
    ANS.append(s)
def store_D(instruction):
    s = "00101"
    s = s + REG_Names(instruction[1]) + VAR_S(instruction[2])[0]
    ANS.append(s)
def mul_A(instruction):
    pass
def div_C(instruction):
    s="0011100000"
    s = s + REG_Names(instruction[1]) + REG_Names(instruction[2])
    REG[0] = REG[instruction[1][-1]] // REG[instruction[2][-1]]
    REG[1] = REG[instruction[1][-1]] % REG[instruction[2][-1]]
    ANS.append(s)
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
    s = "0110100000"
    s = s + REG_Names(instruction[1]) + REG_Names(instruction[2])
    a = str(bin(~REG[instruction[1][-1]]))
    a = a[3:]
    REG[instruction[2][-1]] = int(a,2)
    ANS.append(s)
def cmp_C(instruction):
    s = "0111000000"
    s = s + REG_Names(instruction[1]) + REG_Names(instruction[2])
    a = REG[instruction[1][-1]]
    b = REG[instruction[2][-1]]
    if(a>b):
        REG[7][1] = 1
    elif(a==b):
        REG[7][3] = 1
    else:
        REG[7][2] = 1
    ANS.append(s)
def jmp_E(instruction):
    s = "0111100000"
    s = s + LABEL_S(instruction[1])
    ANS.append(s)
def jlt_E(instruction):
    if(REG[7][1]==1):
        s = "1000000000"
        s = s + LABEL_S(instruction[1])
        ANS.append(s)
def jgt_E(instruction):
    if(REG[7][2]==1):
        s = "1000100000"
        s = s + LABEL_S(instruction[1])
        ANS.append(s)
def je_E(instruction):
    if(REG[7][3]==1):
        s = "10010000000"
        s = s + LABEL_S(instruction[1])
        ANS.append(s)
def hlt_F(instruction):
    s = "1001100000000000"