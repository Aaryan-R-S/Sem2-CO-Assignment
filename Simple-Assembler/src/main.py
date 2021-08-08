import op_table

global ANS
ANS = []

def check_last_hlt():
    if(len(ANS)==0 or ANS[len(ANS)-1][0:5]!="10011"):
        return False
    return True

while(True):
    try:
        curr_instr = input()
    except EOFError:
        if(check_last_hlt()):
            for i in ANS:
                print(i)
        else:
            # ERROR
            pass
        break
        
    if(curr_instr==""):
        continue
    
    curr_instr = curr_instr.split(" ")