def valid_var_name(name, var_dict, reg_dict, opcodes):
    # A variable name consists of alphanumeric characters and underscores
    # returns 1 if valid
    # else in alphanumeric invalid then 2 
    # else in instr then 3 
    # else in registers then 4
    # else in redefinition then 5
    pass

def valid_label_name(name, label_dict, reg_dict, opcodes):
    # A label name consists of alphanumeric characters and underscores
    # returns 1 if valid
    # else in alphanumeric invalid then 2 
    # else in instr then 3 
    # else in registers then 4
    # else in redefinition then 5
    pass

def dec_to_binary(n):
    binary = ""
    ct=1
    while(n>0 and ct<=8):
        binary=str(n & 1)+binary
        n=n>>1
        ct+=1
    
    s='0'*max(0,8-len(binary))+binary
    return s