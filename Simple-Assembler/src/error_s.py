def var_error(line, test_no, myVar=None):
    # 1 = not proper instruction length
    # 2 = alphanumeric invalid 
    # 3 = in instr  
    # 4 = in registers 
    # 5 = redefinition 
    # 6 = all vars must be initialized at beginning
    if(test_no==1):
        print("[ERROR] Invalid format for variable initialization at the line no. "+str(line)+" \nVariable must be initialized in the format: var x")
    elif(test_no==2):
        print("[ERROR] "+myVar+" is invalid variable name at the line no. "+str(line)+" \nVariable name consists of alphanumeric characters and underscores only.")
    elif(test_no==3):
        print("[ERROR] "+myVar+" is invalid variable name at the line no. "+str(line)+" \nVariable name must not be an instruction.")
    elif(test_no==4):
        print("[ERROR] "+myVar+" is invalid variable name at the line no. "+str(line)+" \nVariable name must not be a register.")
    elif(test_no==5):
        print("[ERROR] "+myVar+" is redefined at the line no. "+str(line)+" \nVariable name must be initialized once.")
    elif(test_no==6):
        print("[ERROR] Invalid initialization of variable at the line no. "+str(line)+" \nAll variables must be initialized at the beginning of program.")

def label_error(line, test_no, myLabel=None):
    # 2 = alphanumeric invalid 
    # 3 = in instr  
    # 4 = in registers 
    # 5 = redefinition 
    # 6 = var
    # 7 = followed by instr
    if(test_no==2):
        print("[ERROR] "+myLabel+" is invalid label name at the line no. "+str(line)+" \nLabel name consists of alphanumeric characters and underscores only.")
    elif(test_no==3):
        print("[ERROR] "+myLabel+" is invalid label name at the line no. "+str(line)+" \nLabel name must not be an instruction.")
    elif(test_no==4):
        print("[ERROR] "+myLabel+" is invalid label name at the line no. "+str(line)+" \nLabel name must not be a register.")
    elif(test_no==5):
        print("[ERROR] "+myLabel+" is redefined at the line no. "+str(line)+" \nLabel name must be defined once.")
    elif(test_no==6):
        print("[ERROR] "+myLabel+" is invalid label name at the line no. "+str(line)+" \nLabel name must not be a variable.")
    elif(test_no==7):
        print("[ERROR] "+myLabel+" is invalid label initialization at the line no. "+str(line)+" \nA Label must be follwed by an instruction.")

def mem_over_flow():
    print("[ERROR] Memory Overflow. \nTotal number of instructions and variables must not exceed memory length i.e. 256")
    
def hlt_error(line, test_no):
    # 1 = hlt is not last inst
    # 2 = hlt is present more than once
    if(test_no==1):
        print("[ERROR] Program doesn't have any halt instruction at the end. \nInsert a hlt instruction at the end of the program.")   
    elif(test_no==2):
        print("[ERROR] Program has more than one halt instruction at the line no."+str(line)+" \nUse only one hlt instruction which is to be at the end of the program.")   

def op_error(line, test_no, op):
    # 1 = not a instr
    if(test_no==1):
        print("[ERROR] "+op+" is not a instruction at the line no. "+str(line))

def improper_len_instr(line, test_no, type_instr):
    # test_no = instr_name 
    # type_instr = instr type
    print("[ERROR] "+test_no+" is a type-"+type_instr+" instruction at the line no. "+str(line))

def invalid_reg(line, name):
    # an invalid reg name
    print("[ERROR] "+name+" is not a register at the line no. "+str(line))

def invalid_imm(line, imm):
    # an invalid imm
    print("[ERROR] "+str(imm)+" is not a valid immediate value at the line no. "+str(line)+" \nImmediate value must be an integer between 0 and 255 (both including).")

def invalid_mem_addr(line, mem_addr, test_no):
    # an invalid var(0)/label(1)
    if(test_no==0):
        print("[ERROR] "+mem_addr+" is not a valid variable name at the line no. "+str(line)+" \nVariable name must be initialized first before using it.")
    else:
        print("[ERROR] "+mem_addr+" is not a valid label name at the line no. "+str(line)+" \nLabel name must be defined first before using it.")

def flags_invalid(line):
    print("[ERROR] Invalid use of FLAGS register at the line no. "+str(line))