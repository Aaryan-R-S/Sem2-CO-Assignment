def var_error(line, test_no, myVar=None):
    # 1 = not proper instruction length
    # 2 = alphanumeric invalid 
    # 3 = in instr  
    # 4 = in registers 
    # 5 = redefinition 
    # 6 = all vars must be initialized at beginning
    pass

def label_error(line, test_no, myLabel=None):
    # 2 = alphanumeric invalid 
    # 3 = in instr  
    # 4 = in registers 
    # 5 = redefinition 
    pass

def mem_over_flow():
    # more instr + var initializtion then 256
    pass

def hlt_error(line, test_no):
    # 1 = hlt is not last inst
    # 2 = hlt is present more than once
    pass

def op_error(line, test_no, op=None):
    # 1 = not a instr
    pass

def improper_len_instr(line, test_no, type_instr):
    # test_no = instr_name 
    # type_instr = instr type
    pass
