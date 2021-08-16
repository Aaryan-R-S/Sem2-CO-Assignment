import helpers
import execute
global MEM
global REG
global PC
global NEWPC
global HALTED

# Refer initialize for more
MEM = []   # len = 256 and len(MEM[i]) = 16 bit (string)
REG = []   # len = 8 and len(MEM[i]) = 16 bit (int)    [R0, R1, ..., R6, [V,L,G,E]]
PC = 0     # stores current PC (int)
NEWPC = 0  # stores next PC (int)
HALTED = False

def initialize():
    PC = 0
    NEWPC = 0
    HALTED = False
    for i in range(0, 256):
        MEM[i] = "0000000000000000"
    for i in range(0, 7):
        REG[i] = 0
    REG[7] = [0,0,0,0]  # V,L,G,E
    j = 0 
    while(True):
        try:
            MEM[j] = input().strip()
            j+=1
        except EOFError:
            break

def getInstruction():
    return MEM[PC]

def dump():
    a = REG
    for i in range(0, 7):
        a[i] = helpers.dec_to_bin(a[i], 16)

    flags = 8*a[7][3] + 4*a[7][2] + 2*a[7][1] + 1*a[7][0]
    a[7] = helpers.dec_to_bin(flags , 16)

    a.insert(0, helpers.dec_to_bin(PC, 8))

    a = " ".join(a)
    print(a)

def dump_memory():
    for i in range(0, 256):
        print(MEM[i])

def run_instr(instr):
    opcode = instr[0:5]
    op_type = execute.OPCODES[opcode][0]
    if(op_type=="A"):
        if(opcode=="00000"):
            add_A(instr)
        elif(opcode=="00001"):
            sub_A(instr)
        elif(opcode=="00110"):
            mul_A(instr)
        elif(opcode=="01010"):
            xor_A(instr)
        elif(opcode=="01011"):
            or_A(instr)
        elif(opcode=="01100"):
            and_A(instr)
    elif(op_type=="B"):
        if(opcode=="00010"):
            mov_imm_B(instr)
        elif(opcode=="01000"):
            rs_B(instr)
        elif(opcode=="01001"):
            ls_B(instr)
    elif(op_type=="C"):
        if(opcode=="00011"):
            mov_reg_C(instr)
        elif(opcode=="00111"):
            div_C(instr)
        elif(opcode=="01101"):
            not_C(instr)
        elif(opcode=="01110"):
            cmp_C(instr)
    elif(op_type=="D"):
        if(opcode=="00100"):
            load_D(instr)
        elif(opcode=="00101"):
            store_D(instr)
    elif(op_type=="E"):
        if(opcode=="01111"):
            jmp_E(instr)
        elif(opcode=="10000"):
            jlt_E(instr)
        elif(opcode=="10001"):
            jgt_E(instr)
        elif(opcode=="10010"):
            je_E(instr)
    elif(op_type=="F"):
        if(opcode=="10011"):
            hlt_F(instr)

def add_A(instr):
    # s = OPCODES["add"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # res = REG[int(instr[2][1:])] + REG[int(instr[3][1:])]
    # if(res>=(1<<16)):
    #     REG[int(instr[1][1:])] = res%(1<<16)
    #     REG[-1][0] = 1
    # else:
    #     REG[int(instr[1][1:])] = res
    # ANS.append(s)
    pass
    
def sub_A(instr):
    # s = OPCODES["sub"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # res = REG[int(instr[2][1:])] - REG[int(instr[3][1:])]
    # if(res<0):
    #     REG[int(instr[1][1:])] = 0
    #     REG[-1][0] = 1
    # else:
    #     REG[int(instr[1][1:])] = res
    # ANS.append(s)
    pass
    
def mov_imm_B(instr):
    # s = "00010" + REG_Names[instr[1]]     
    # s += helpers.dec_to_binary(int(instr[2][1:]))
    # REG[int(instr[1][1:])] = int(instr[2][1:])
    # ANS.append(s)
    pass
    
def mov_reg_C(instr):
    # s="0001100000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # if(instr[2]=="FLAGS"):
    #     REG[int(instr[1][-1])] = 1*REG[7][3] + 2*REG[7][2] + 4*REG[7][1] + 8*REG[7][0]
    # else:
    #     REG[int(instr[1][-1])] = REG[int(instr[2][-1])]
    # ANS.append(s)
    pass
    
def load_D(instr):
    # s = "00100"
    # s = s + REG_Names[instr[1]] + helpers.addr_to_bin(VAR_S[instr[2]][0])
    # REG[int(instr[1][-1])] = VAR_S[instr[2]][1]
    # ANS.append(s)
    pass
    
def store_D(instr):
    # s = "00101"
    # s = s + REG_Names[instr[1]] + helpers.addr_to_bin(VAR_S[instr[2]][0])
    # VAR_S[instr[2]][1] = REG[int(instr[1][-1])]
    # ANS.append(s)
    pass
    
def mul_A(instr):
    # s = OPCODES["mul"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # res = REG[int(instr[2][1:])] * REG[int(instr[3][1:])]
    # if(res>=(1<<16)):
    #     REG[int(instr[1][1:])] = res%(1<<16)
    #     REG[-1][0] = 1
    # else:
    #     REG[int(instr[1][1:])] = res
    # ANS.append(s)
    pass
    
def div_C(instr):
    # s="0011100000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # REG[0] = REG[int(instr[1][-1])] // REG[int(instr[2][-1])]
    # REG[1] = REG[int(instr[1][-1])] % REG[int(instr[2][-1])]
    # ANS.append(s)
    pass
    
def rs_B(instr):
    # s = "01000" + REG_Names[instr[1]]
    # s += helpers.dec_to_binary(int(instr[2][1:]))

    # REG[int(instr[1][1:])] = REG[int(instr[1][1:])]>>int(instr[2][1:])
    # ANS.append(s)
    pass
    
def ls_B(instr):
    # s = "01001" + REG_Names[instr[1]]
    # s += helpers.dec_to_binary(int(instr[2][1:]))

    # res = REG[int(instr[1][1:])]<<min(16,int(instr[2][1:]))
    # if(res>=(1<<16)):
    #     REG[int(instr[1][1:])] = res%(1<<16)
    # else:
    #     REG[int(instr[1][1:])] = res
    # ANS.append(s)
    pass

def xor_A(instr):
    # s = OPCODES["xor"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] ^ REG[int(instr[3][1:])]
    # ANS.append(s)
    pass
    
def or_A(instr):
    # s = OPCODES["or"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] | REG[int(instr[3][1:])]
    # ANS.append(s)
    pass
    
def and_A(instr):
    # s = OPCODES["and"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] & REG[int(instr[3][1:])]
    # ANS.append(s)
    pass
    
def not_C(instr):
    # s = "0110100000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # c = helpers.addr_to_bin(REG[int(instr[2][-1])]) 
    # c_c = ""
    # for i in range(len(c)):
    #     if(c[i]=='0'):
    #         c_c+='1'
    #     else:
    #         c_c+='0'
    # REG[int(instr[1][-1])] = int(c_c, 2)
    # ANS.append(s)
    pass

def cmp_C(instr):
    # s = "0111000000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # a = REG[int(instr[1][-1])]
    # b = REG[int(instr[2][-1])]
    # if(a>b):
    #     REG[7][2] = 1
    # elif(a==b):
    #     REG[7][3] = 1
    # else:
    #     REG[7][1] = 1
    # ANS.append(s)
    pass

def jmp_E(instr):
    # s = "01111000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    pass
    
def jlt_E(instr):
    # s = "10000000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    pass
        
def jgt_E(instr):
    # s = "10001000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    pass
        
def je_E(instr):
    # s = "10010000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    pass
        
def hlt_F(instr):
    # s = "1001100000000000"
    # ANS.append(s)
    pass

