def valid_var_name(name, var_dict, reg_dict, opcodes):
    # A variable name consists of alphanumeric characters and underscores
    # returns 1 if valid
    # else in alphanumeric invalid then 2 
    # else in instr then 3 
    # else in registers then 4
    # else in redefinition then 5
    if(not(name.replace('_', '').isalnum() or name=="_")):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in var_dict.keys()):
        return 5
    return 1    

def valid_label_name(name, var_dict, label_dict, reg_dict, opcodes):
    # A label name consists of alphanumeric characters and underscores
    # returns 1 if valid
    # else in alphanumeric invalid then 2 
    # else in instr then 3 
    # else in registers then 4
    # else in redefinition then 5
    # else in var then 6
    if(not(name.replace('_', '').isalnum() or name=="_")):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in label_dict.keys()):
        return 5
    if(name in var_dict.keys()):
        return 6
    return 1

def dec_to_binary(n):
    binary = ""
    ct=1
    while(n>0 and ct<=8):
        binary=str(n & 1)+binary
        n=n>>1
        ct+=1
    
    s='0'*max(0,8-len(binary))+binary
    return s

def addr_to_bin(x):
    t = bin(x)
    t = t[2:]
    t = t[-8:]
    if(len(t)!=8):
        t = '0'*(8-len(t))+t
    return t

def val_reg(list_reg, type_instr, reg_names, var_label_dict=None):
    # type_instr A then 3 reg; return the reg index(1-based indexing) which is invalid else 0 if all valid
    # type_instr B then 1 reg and 1 imm; return the 1 if reg is invalid or 2 if imm is invalid else 0 if all valid
    # type_instr C then 2 reg; return the reg index(1-based indexing) which is invalid else 0 if all valid
    # type_instr D then 1 reg 1 var; return the 1 if reg is invalid or 2 if var is invalid else 0 if all valid
    # type_instr E then 1 label; return the 1 if label is invalid else 0 if valid
    # return 10 in invalid use of flags register
    if(type_instr=="A"):
        for i in range(len(list_reg)):
            if(list_reg[i] not in reg_names):
                return i+1
            if(list_reg[i] == "FLAGS"):
                return 10
        return 0
    if(type_instr=="B"):
        if(list_reg[0] not in reg_names):
            return 1
        if(list_reg[0] == "FLAGS"):
            return 10
        if(int(list_reg[1][1:])>255 or int(list_reg[1][1:])<0):
            return 2
        return 0
    if(type_instr=="C"):
        for i in range(len(list_reg)):
            if(list_reg[i] not in reg_names):
                return i+1
        return 0
    if(type_instr=="D"):
        if(list_reg[0] not in reg_names):
            return 1
        if(list_reg[0] == "FLAGS"):
            return 10
        if(list_reg[1] not in var_label_dict.keys()):
            return 2
        return 0
    if(type_instr=="E"):
        if(list_reg[0] not in var_label_dict.keys()):
            return 1
        return 0
    return 0