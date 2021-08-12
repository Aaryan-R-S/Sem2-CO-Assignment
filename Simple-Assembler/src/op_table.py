import sys
import error_s
import helpers
global REG
global OPCODES
global TEMP
global MEM_LINE
# global CURR_MEM_LINE
global CURR_LINE
global VAR_S
global LABEL_S
global TEST_NO
# global MEM_LD_ST
global ANS

ANS = [] # 16-bit instruction

# Stores data for address greater than MEM_LINE (= instr+var ) less than 256 else print error (if in var range then put in var_s instead)
# MEM_LD_ST = []
VAR_S = {}  # "var_name": [addr(int in decimal starting from 0), val(int in decimal initially 0)]
LABEL_S = {}     # "label_name": [addr(int in decimal starting from 0)]

# CURR_MEM_LINE = 0
MEM_LINE = 0  # Mem occupied by instructions + variables 
CURR_LINE = 0

# Error related 
TEST_NO = 0

# (all are in string)
TEMP = [0,0,0,0,0,0]    # [opcode, reg1, reg2, reg3, imm_val, mem_adr] 
REG_Names = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}
# (all are in int)
REG = [0,0,0,0,0,0,0,[0,0,0,0]]     # [R0, R1, ..., R6, [V,L,G,E]]
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

def reset_temp():
    for i in range(len(TEMP)):
        TEMP[i] = 0
        
def reset_flags():
    for i in range(0,4):
        REG[7][i] = 0

def instruction_type(instruction):
    is_reset_flag = False
    reset_temp()
    op = instruction[0]
    if op in OPCODES:
        op_code = OPCODES[op][0]
        op_type = OPCODES[op][1]
        TEMP[0] = op_code
    else:
        TEST_NO = 1
        error_s.op_error(CURR_LINE, TEST_NO, op)
        sys.exit()
    if(op=="mov"):
        if(len(instruction)>2 and instruction[2] in REG_Names): 
            TEMP[0] = "00011"
            op_type = "C"
        else:
            TEMP[0] = "00010"
            op_type = "B"
    if((op_type!="E" and op_code!="00011") or op_code=="01111"):
        is_reset_flag = True
        reset_flags()   # if it is not a jlt, jgt, je or mov Flags instr then reset flag register
    if(op_type=="A"): instruction_A(instruction)
    elif(op_type=="B"): instruction_B(instruction)
    elif(op_type=="C"): instruction_C(instruction)
    elif(op_type=="D"): instruction_D(instruction)
    elif(op_type=="E"): instruction_E(instruction)
    elif(op_type=="F"): instruction_F(instruction)
    if(is_reset_flag==False):
        reset_flags()

def instruction_A(instruction):
    if(len(instruction)!=4):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "A")
        sys.exit()
    reg1 = instruction[1] 
    reg2 = instruction[2] 
    reg3 = instruction[3] 
    verdict = helpers.val_reg([reg1, reg2, reg3], "A", REG_Names)
    if(verdict!=0):
        if(verdict==10):
            error_s.flags_invalid(CURR_LINE)
        else:
            error_s.invalid_reg(CURR_LINE, instruction[verdict])
        sys.exit()
    TEMP[1] = reg1
    TEMP[2] = reg2
    TEMP[3] = reg3
    if(TEMP[0]=="00000"): add_A(instruction)
    elif(TEMP[0]=="00001"): sub_A(instruction)
    elif(TEMP[0]=="00110"): mul_A(instruction)
    elif(TEMP[0]=="01010"): xor_A(instruction)
    elif(TEMP[0]=="01011"): or_A(instruction)
    elif(TEMP[0]=="01100"): and_A(instruction)
    
def instruction_B(instruction):
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "B")
        sys.exit()
    reg1 = instruction[1] 
    imm_val = instruction[2] 
    verdict = helpers.val_reg([reg1, imm_val], "B", REG_Names)
    if(verdict!=0):
        if(verdict==1):
            error_s.invalid_reg(CURR_LINE, instruction[verdict])
        elif(verdict==2):
            error_s.invalid_imm(CURR_LINE, instruction[verdict])
        elif(verdict==10):
            error_s.flags_invalid(CURR_LINE)
        sys.exit()
    TEMP[1] = reg1
    TEMP[4] = imm_val
    if(TEMP[0]=="00010"): mov_imm_B(instruction)
    elif(TEMP[0]=="01000"): rs_B(instruction)
    elif(TEMP[0]=="01001"): ls_B(instruction)

def instruction_C(instruction):
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "C")
        sys.exit()
    reg1 = instruction[1] 
    reg2 = instruction[2] 
    verdict = helpers.val_reg([reg1, reg2], "C", REG_Names)
    if(verdict!=0):
        error_s.invalid_reg(CURR_LINE, instruction[verdict])
        sys.exit()
    TEMP[1] = reg1
    TEMP[2] = reg2 
    if(TEMP[0]=="00011"): mov_reg_C(instruction)
    elif(TEMP[0]=="00111"): div_C(instruction)
    elif(TEMP[0]=="01101"): not_C(instruction)
    elif(TEMP[0]=="01110"): cmp_C(instruction)
    
def instruction_D(instruction):
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "D")
        sys.exit()
    reg1 = instruction[1] 
    mem_addr = instruction[2] 
    verdict = helpers.val_reg([reg1, mem_addr], "D", REG_Names, VAR_S)
    if(verdict!=0):
        if(verdict==1):
            error_s.invalid_reg(CURR_LINE, instruction[verdict])
        elif(verdict==2):
            TEST_NO = 0
            error_s.invalid_mem_addr(CURR_LINE, instruction[verdict], TEST_NO)
        elif(verdict==10):
            error_s.flags_invalid(CURR_LINE)
        sys.exit()
    TEMP[1] = reg1
    TEMP[5] = mem_addr
    if(TEMP[0]=="00100"): load_D(instruction)
    elif(TEMP[0]=="00101"): store_D(instruction)

def instruction_E(instruction):
    if(len(instruction)!=2):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "E")
        sys.exit()
    mem_addr = instruction[1] 
    verdict = helpers.val_reg([mem_addr], "E", None, LABEL_S)
    if(verdict!=0):
        if(verdict==10):
            error_s.flags_invalid(CURR_LINE)
        else:
            TEST_NO = 1
            error_s.invalid_mem_addr(CURR_LINE, instruction[verdict], TEST_NO)
        sys.exit()
    TEMP[5] = mem_addr
    if(TEMP[0]=="01111"): jmp_E(instruction)
    elif(TEMP[0]=="10000"): jlt_E(instruction)
    elif(TEMP[0]=="10001"): jgt_E(instruction)
    elif(TEMP[0]=="10010"): je_E(instruction)
    
def instruction_F(instruction):
    if(len(instruction)!=1):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURR_LINE, TEST_NO, "F")
        sys.exit()
    if(TEMP[0]=="10011"): hlt_F(instruction)

def add_A(instruction):
    s="0000000"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    res =  REG[int(instruction[2][1:])] + REG[int(instruction[3][1:])]
    if(res>=(1<<16)):
        REG[int(instruction[1][1:])]= res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[int(instruction[1][1:])]= res
        REG[-1][0] = 0
    ANS.append(s)
    
def sub_A(instruction):
    s="0000100"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    res =  REG[int(instruction[2][1:])] - REG[int(instruction[3][1:])]
    if(res<0):
        REG[int(instruction[1][1:])]= 0
        REG[-1][0] = 1
    else:
        REG[int(instruction[1][1:])]= res
        REG[-1][0] = 0
    ANS.append(s)
    
def mov_imm_B(instruction):
    s="00010"+REG_Names[instruction[1]]     
    s+=helpers.dec_to_binary(int(instruction[2][1:]))
    REG[int(instruction[1][1:])]=int(instruction[2][1:])
    ANS.append(s)
    
def mov_reg_C(instruction):
    s="0001100000"
    s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
    ANS.append(s)
    
def load_D(instruction):
    s = "00100"
    s = s + REG_Names[instruction[1]] + helpers.addr_to_bin(VAR_S[instruction[2]][0])
    ANS.append(s)
    
def store_D(instruction):
    s = "00101"
    s = s + REG_Names[instruction[1]] + helpers.addr_to_bin(VAR_S[instruction[2]][0])
    ANS.append(s)
    
def mul_A(instruction):
    s="0011000"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    res =  REG[int(instruction[2][1:])] * REG[int(instruction[3][1:])]
    if(res>=(1<<16)):
        REG[int(instruction[1][1:])]= res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[int(instruction[1][1:])]= res
        REG[-1][0] = 0
    ANS.append(s)
    
def div_C(instruction):
    s="0011100000"
    s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
    REG[0] = REG[int(instruction[1][-1])] // REG[int(instruction[2][-1])]
    REG[1] = REG[int(instruction[1][-1])] % REG[int(instruction[2][-1])]
    ANS.append(s)
    
def rs_B(instruction):
    s="01000"+REG_Names[instruction[1]]
    s+=helpers.dec_to_binary(int(instruction[2][1:]))

    REG[int(instruction[1][1:])]=REG[int(instruction[1][1:])]>>int(instruction[2][1:])
    ANS.append(s)
    
    res=REG[int(instruction[1][1:])]<<min(16,int(instruction[2][1:]))
    if(res>=(1<<16)):
        REG[int(instruction[1][1:])]= res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[int(instruction[1][1:])]= res
        REG[-1][0] = 0
    ANS.append(s)
    
def ls_B(instruction):
    s="01001"+REG_Names[instruction[1]]
    s+=helpers.dec_to_binary(int(instruction[2][1:]))

    res=REG[int(instruction[1][1:])]<<min(16,int(instruction[2][1:]))
    if(res>=(1<<16)):
        REG[int(instruction[1][1:])]= res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[int(instruction[1][1:])]= res
        REG[-1][0] = 0
    ANS.append(s)
        
def xor_A(instruction):
    s="0101000"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] ^ REG[int(instruction[3][1:])]
    ANS.append(s)
    
def or_A(instruction):
    s="0101100"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] | REG[int(instruction[3][1:])]
    ANS.append(s)
    
def and_A(instruction):
    s="0110000"
    s+=REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] & REG[int(instruction[3][1:])]
    ANS.append(s)
    
def not_C(instruction):
    s = "0110100000"
    s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
    c = helpers.addr_to_bin(REG[int(instruction[2][-1])]) 
    c_c = ""
    for i in range(len(c)):
        if(c[i]=='0'):
            c_c+='1'
        else:
            c_c+='0'
    REG[int(instruction[1][-1])] = int(c_c, 2)
    ANS.append(s)

def cmp_C(instruction):
    s = "0111000000"
    s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
    a = REG[int(instruction[1][-1])]
    b = REG[int(instruction[2][-1])]
    if(a>b):
        REG[7][1] = 1
    elif(a==b):
        REG[7][3] = 1
    else:
        REG[7][2] = 1
    ANS.append(s)
    
def jmp_E(instruction):
    s = "01111000"
    s = s + helpers.addr_to_bin(LABEL_S[instruction[1]][0])
    ANS.append(s)
    
def jlt_E(instruction):
    if(REG[7][1]==1):
        s = "10000000"
        s = s + helpers.addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
        
def jgt_E(instruction):
    if(REG[7][2]==1):
        s = "10001000"
        s = s + helpers.addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
        
def je_E(instruction):
    if(REG[7][3]==1):
        s = "100100000"
        s = s + helpers.addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
        
def hlt_F(instruction):
    s = "1001100000000000"
    ANS.append(s)

