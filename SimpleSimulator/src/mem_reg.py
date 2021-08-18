import helpers
import execute
global MEM
global REG
global PC
global NEWPC
global HALTED
global CURRCYCLE
global CYCLES
global MEMACCESSES

# Refer initialize for more
CYCLES = []         # cycle no starting from 0 (int)
MEMACCESSES = []    # address accessed in each cycle (int)
MEM = []   # len = 256 and len(MEM[i]) = 16 bit (string)
for i in range(0, 256):
    MEM.append("0000000000000000")
REG = [0,0,0,0,0,0,0,[0,0,0,0]]   # len = 8 and len(MEM[i]) = 16 bit (int)    [R0, R1, ..., R6, [V,L,G,E]]
PC = 0     # stores current PC (int)
CURRCYCLE = 0
NEWPC = 0  # stores next PC (int)
HALTED = False

def initialize():
    global PC
    global NEWPC
    global HALTED
    PC = 0
    NEWPC = 0
    HALTED = False
    for i in range(0, 256):
        MEM[i] = "0000000000000000"
    for i in range(0, 7):
        REG[i] = 0
    REG[7] = [0,0,0,0] 
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
    a = REG[:]
    for i in range(0, 7):
        a[i] = helpers.dec_to_bin(a[i], 16)

    flags = 8*a[7][0] + 4*a[7][1] + 2*a[7][2] + 1*a[7][3]
    a[7] = helpers.dec_to_bin(flags , 16)

    a.insert(0, helpers.dec_to_bin(PC, 8))

    a = " ".join(a)
    print(a)

def dump_memory():
    for i in range(0, 256):
        print(MEM[i])

def reset_flags():
    REG[7] = [0,0,0,0]

def run_instr(instr):
    global NEWPC
    global CURRCYCLE
    flagReset = False
    op_code = instr[0:5]
    op_type = execute.OPCODES[op_code][0]
    CYCLES.append(CURRCYCLE)
    MEMACCESSES.append(PC)
    if((op_type!="E" and op_code!="00011") or op_code=="01111"):
        flagReset = True
        reset_flags()   # if it is not a jlt, jgt, je or mov Flags instr then reset flag register
    if(op_type=="A"):
        NEWPC = PC+1
        if(op_code=="00000"):
            add_A(instr)
        elif(op_code=="00001"):
            sub_A(instr)
        elif(op_code=="00110"):
            mul_A(instr)
        elif(op_code=="01010"):
            xor_A(instr)
        elif(op_code=="01011"):
            or_A(instr)
        elif(op_code=="01100"):
            and_A(instr)
    elif(op_type=="B"):
        NEWPC = PC+1
        if(op_code=="00010"):
            mov_imm_B(instr)
        elif(op_code=="01000"):
            rs_B(instr)
        elif(op_code=="01001"):
            ls_B(instr)
    elif(op_type=="C"):
        NEWPC = PC+1
        if(op_code=="00011"):
            mov_reg_C(instr)
        elif(op_code=="00111"):
            div_C(instr)
        elif(op_code=="01101"):
            not_C(instr)
        elif(op_code=="01110"):
            cmp_C(instr)
    elif(op_type=="D"):
        NEWPC = PC+1
        if(op_code=="00100"):
            load_D(instr)
        elif(op_code=="00101"):
            store_D(instr)
    elif(op_type=="E"):
        if(op_code=="01111"):
            jmp_E(instr)
        elif(op_code=="10000"):
            jlt_E(instr)
        elif(op_code=="10001"):
            jgt_E(instr)
        elif(op_code=="10010"):
            je_E(instr)
    elif(op_type=="F"):
        if(op_code=="10011"):
            hlt_F(instr)
    if(flagReset==False):
        reset_flags()

def add_A(instr):
    # s = OPCODES["add"][0] + "00"
    # s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
    # res = REG[int(instruction[2][1:])] + REG[int(instruction[3][1:])]
    # if(res>=(1<<16)):
    #     REG[int(instruction[1][1:])] = res%(1<<16)
    #     REG[-1][0] = 1
    # else:
    #     REG[int(instruction[1][1:])] = res
    # ANS.append(s)
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    res=REG[execute.REG_Names[src1_reg][0]]+REG[execute.REG_Names[src2_reg][0]]
    if(res>=(1<<16)):
        REG[execute.REG_Names[dest_reg][0]] = res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[execute.REG_Names[dest_reg][0]] = res
    
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
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    res=REG[execute.REG_Names[src1_reg][0]]-REG[execute.REG_Names[src2_reg][0]]
    if(res<0):
        REG[execute.REG_Names[dest_reg][0]] = 0
        REG[-1][0] = 1
    else:
        REG[execute.REG_Names[dest_reg][0]] = res
 
def mov_imm_B(instr):
    # s = "00010" + REG_Names[instr[1]]     
    # s += helpers.dec_to_binary(int(instr[2][1:]))
    # REG[int(instr[1][1:])] = int(instr[2][1:])
    # ANS.append(s)
    dest_reg=instr[5:8]
    imm=instr[8:16]
    REG[execute.REG_Names[dest_reg][0]] = helpers.bin_to_dec(imm)
    
def mov_reg_C(instr):
    # s="0001100000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # if(instr[2]=="FLAGS"):
    #     REG[int(instr[1][-1])] = 1*REG[7][3] + 2*REG[7][2] + 4*REG[7][1] + 8*REG[7][0]
    # else:
    #     REG[int(instr[1][-1])] = REG[int(instr[2][-1])]
    # ANS.append(s)
    reg1 = instr[10:13]
    reg2 = instr[13:16]
    if execute.REG_Names[reg2][0] == 7 :
        REG[execute.REG_Names[reg1][0]] = 1*REG[7][3] + 2*REG[7][2] + 4*REG[7][1] + 8*REG[7][0]
    else:
        REG[execute.REG_Names[reg1][0]] = REG[execute.REG_Names[reg2][0]]
    
def load_D(instr):
    # s = "00100"
    # s = s + REG_Names[instr[1]] + helpers.addr_to_bin(VAR_S[instr[2]][0])
    # REG[int(instr[1][-1])] = VAR_S[instr[2]][1]
    # ANS.append(s)
    dest_reg=instr[5:8]
    addr=instr[8:16]
    REG[execute.REG_Names[dest_reg][0]] = helpers.bin_to_dec(MEM[helpers.bin_to_dec(addr)])
    CYCLES.append(CURRCYCLE)
    MEMACCESSES.append(helpers.bin_to_dec(addr))
    # reg1 = int(instr[5:8],2)
    # addr = int(instr[8:],2)
    # a = int(MEM[addr],2)
    # REG[reg1] = a
    
def store_D(instr):
    # s = "00101"
    # s = s + REG_Names[instr[1]] + helpers.addr_to_bin(VAR_S[instr[2]][0])
    # VAR_S[instr[2]][1] = REG[int(instr[1][-1])]
    # ANS.append(s)
    dest_reg=instr[5:8]
    addr=instr[8:16]
    MEM[helpers.bin_to_dec(addr)] = helpers.dec_to_bin(REG[execute.REG_Names[dest_reg][0]], 16)
    CYCLES.append(CURRCYCLE)
    MEMACCESSES.append(helpers.bin_to_dec(addr))
    # reg1 = REG[int(instr[5:8],2)]
    # addr = int(instr[8:],2)
    # MEM[addr] = helpers.dec_to_bin(reg1,16)
    
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
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    res=REG[execute.REG_Names[src1_reg][0]]*REG[execute.REG_Names[src2_reg][0]]
    if(res>=(1<<16)):
        REG[execute.REG_Names[dest_reg][0]] = res%(1<<16)
        REG[-1][0] = 1
    else:
        REG[execute.REG_Names[dest_reg][0]] = res
    
def div_C(instr):
    # s="0011100000"
    # s = s + REG_Names[instr[1]] + REG_Names[instr[2]]
    # REG[0] = REG[int(instr[1][-1])] // REG[int(instr[2][-1])]
    # REG[1] = REG[int(instr[1][-1])] % REG[int(instr[2][-1])]
    # ANS.append(s)
    reg1 = instr[10:13]
    reg2 = instr[13:16]
    REG[0] = REG[execute.REG_Names[reg1][0]] // REG[execute.REG_Names[reg2][0]]
    REG[1] = REG[execute.REG_Names[reg1][0]] % REG[execute.REG_Names[reg2][0]]
    
def rs_B(instr):
    # s = "01000" + REG_Names[instr[1]]
    # s += helpers.dec_to_binary(int(instr[2][1:]))
    # REG[int(instr[1][1:])] = REG[int(instr[1][1:])]>>int(instr[2][1:])
    # ANS.append(s)
    dest_reg=instr[5:8]
    imm=instr[8:16]
    REG[execute.REG_Names[dest_reg][0]]=REG[execute.REG_Names[dest_reg][0]]>>helpers.bin_to_dec(imm)
    
def ls_B(instr):
    # s = "01001" + REG_Names[instr[1]]
    # s += helpers.dec_to_binary(int(instr[2][1:]))
    # res = REG[int(instr[1][1:])]<<min(16,int(instr[2][1:]))
    # if(res>=(1<<16)):
    #     REG[int(instr[1][1:])] = res%(1<<16)
    # else:
    #     REG[int(instr[1][1:])] = res
    # ANS.append(s)
    dest_reg=instr[5:8]
    imm=instr[8:16]
    res=REG[execute.REG_Names[dest_reg][0]]<<min(16,helpers.bin_to_dec(imm))
    if(res>=(1<<16)):
        REG[execute.REG_Names[dest_reg][0]] = res%(1<<16)
    else:
        REG[execute.REG_Names[dest_reg][0]] = res

def xor_A(instr):
    # s = OPCODES["xor"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] ^ REG[int(instr[3][1:])]
    # ANS.append(s)
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    REG[execute.REG_Names[dest_reg][0]] = REG[execute.REG_Names[src1_reg][0]] ^ REG[execute.REG_Names[src2_reg][0]]
    
def or_A(instr):
    # s = OPCODES["or"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] | REG[int(instr[3][1:])]
    # ANS.append(s)
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    REG[execute.REG_Names[dest_reg][0]] = REG[execute.REG_Names[src1_reg][0]] | REG[execute.REG_Names[src2_reg][0]]
    
def and_A(instr):
    # s = OPCODES["and"][0] + "00"
    # s += REG_Names[instr[1]] + REG_Names[instr[2]] + REG_Names[instr[3]]
    # REG[int(instr[1][1:])] =  REG[int(instr[2][1:])] & REG[int(instr[3][1:])]
    # ANS.append(s)
    dest_reg=instr[7:10]
    src1_reg=instr[10:13]
    src2_reg=instr[13:16]
    REG[execute.REG_Names[dest_reg][0]] = REG[execute.REG_Names[src1_reg][0]] & REG[execute.REG_Names[src2_reg][0]]

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
    reg1 = instr[10:13]
    reg2 = instr[13:16]
    c = helpers.dec_to_bin(REG[execute.REG_Names[reg2][0]], 16) 
    c_c = ""
    for i in range(len(c)):
        if(c[i]=='0'):
            c_c+='1'
        else:
            c_c+='0'
    REG[execute.REG_Names[reg1][0]] = helpers.bin_to_dec(c_c)

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
    reg1 = instr[10:13]
    reg2 = instr[13:16]
    a = REG[execute.REG_Names[reg1][0]]
    b = REG[execute.REG_Names[reg2][0]]
    if(a>b):
        REG[7][2] = 1
    elif(a==b):
        REG[7][3] = 1
    else:
        REG[7][1] = 1

def jmp_E(instr):
    global NEWPC
    # s = "01111000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    addr = helpers.bin_to_dec(instr[8:16])
    NEWPC = addr
    
def jlt_E(instr):
    global NEWPC
    # s = "10000000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    addr = helpers.bin_to_dec(instr[8:16])
    if(REG[7][1]==1):
        NEWPC = addr
    else:
        NEWPC = PC + 1
        
def jgt_E(instr):
    global NEWPC
    # s = "10001000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    addr = helpers.bin_to_dec(instr[8:16])
    if(REG[7][2]==1):
        NEWPC = addr
    else:
        NEWPC = PC + 1
        
def je_E(instr):
    global NEWPC
    # s = "10010000"
    # s = s + helpers.addr_to_bin(LABEL_S[instr[1]][0])
    # ANS.append(s)
    addr = helpers.bin_to_dec(instr[8:16])
    if(REG[7][3]==1):
        NEWPC = addr
    else:
        NEWPC = PC + 1
        
def hlt_F(instr):
    global HALTED
    # s = "1001100000000000"
    # ANS.append(s)
    HALTED = True
