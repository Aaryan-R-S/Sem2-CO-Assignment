import sys
import re
import op_table

global INP

INP = []
op_table.ANS = []

while(True):
    try:
        curr_instr = input().strip()
        curr_instr = str(re.sub(' +', ' ', curr_instr))
        INP.append(curr_instr)
    except EOFError:
        break

op_table.CURR_LINE = 1
op_table.TEST_NO = None

# VAR STORING
while(op_table.CURR_LINE <= len(INP)):
    if(INP[op_table.CURR_LINE-1].split(" ")[0]=="var"):
        if(len(INP[op_table.CURR_LINE-1].split(" ")) != 2):
            op_table.TEST_NO = 1
            op_table.error_s.var_error(op_table.CURR_LINE, op_table.TEST_NO)
            sys.exit()
        else:
            myVar = INP[op_table.CURR_LINE-1].split(" ")[1]
            # check_valid_var_name() along with not in instr or reg or redefinition
            verdict = op_table.helpers(myVar, op_table.VAR_S, op_table.REG_Names, op_table.OPCODES)
            if(verdict!=1):
                op_table.TEST_NO = verdict
                op_table.error_s.var_error(op_table.CURR_LINE, op_table.TEST_NO, myVar)
                sys.exit()
            op_table.VAR_S[myVar] = [None, 0]
            op_table.CURR_LINE += 1
    elif(INP[op_table.CURR_LINE-1]==""):
        op_table.CURR_LINE += 1
    else:
        break
    
op_table.MEM_LINE = 0
    
# Label Storing with address
while(op_table.CURR_LINE <= len(INP)):
    if(INP[op_table.CURR_LINE-1].split(" ")[0][-1:]==":"):
        # check_valid_label_name() along with not in instruction or reg or redefinition
        myLabel = INP[op_table.CURR_LINE-1].split(" ")[0][:-1]
        verdict = op_table.helpers.valid_label_name(myLabel, op_table.VAR_S, op_table.LABEL_S, op_table.REG_Names, op_table.OPCODES)
        if(verdict != 1):
            op_table.TEST_NO = verdict
            op_table.error_s.label_error(op_table.CURR_LINE, op_table.TEST_NO, myLabel)
            sys.exit()
        op_table.LABEL_S[myLabel] = [op_table.MEM_LINE]
        op_table.MEM_LINE += 1
    elif(INP[op_table.CURR_LINE-1].split(" ")[0]=="var"):
        op_table.TEST_NO = 6
        op_table.error_s.var_error(op_table.CURR_LINE, op_table.TEST_NO)
        sys.exit()
    elif(INP[op_table.CURR_LINE-1]!=""):
        op_table.MEM_LINE += 1
    op_table.CURR_LINE += 1

# Assign address to variables
for v in op_table.VAR_S:
    op_table.VAR_S[v][0] = op_table.MEM_LINE
    op_table.MEM_LINE += 1

# Check Memory Overflow
if(op_table.MEM_LINE>=256):
    op_table.error_s.mem_over_flow()
    sys.exit()

# Check last instruction is hlt or not and how many hlt instructions
hlt_count = 0
while(op_table.CURR_LINE>=1):
    if(INP[op_table.CURR_LINE-1]!=""):
        if(INP[op_table.CURR_LINE-1].split(" ")[0]=="hlt"):
            hlt_count += 1 
        if(hlt_count==0 and INP[op_table.CURR_LINE-1].split(" ")[0]!="hlt"):
            op_table.TEST_NO = 1
            op_table.error_s.hlt_error(op_table.CURR_LINE, op_table.TEST_NO)
            sys.exit()
    if(hlt_count>1):
        op_table.TEST_NO = 2
        op_table.error_s.hlt_error(op_table.CURR_LINE, op_table.TEST_NO)
        sys.exit()
    op_table.CURR_LINE -= 1
    
op_table.CURR_LINE = 1

# Start executing the assembly code
while(op_table.CURR_LINE<=len(INP)):
    if(INP[op_table.CURR_LINE-1]==""):
        op_table.CURR_LINE += 1
        continue
    myInstr = INP[op_table.CURR_LINE-1].split(" ")
    if(myInstr[0]=="var"):
        op_table.CURR_LINE += 1
        continue
    if(myInstr[0][-1:]==":"):
        myInstr = myInstr[1:]
    op_table.instruction_type(myInstr)
    op_table.CURR_LINE += 1

for i in op_table.ANS:
    print(i)