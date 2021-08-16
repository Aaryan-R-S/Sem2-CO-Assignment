import mem_reg

mem_reg.initialize()

while(not mem_reg.HALTED):
    Instruction = mem_reg.getInstruction()
    mem_reg.run_instr(Instruction) 
    mem_reg.dump()
    mem_reg.PC = mem_reg.NEWPC

mem_reg.dump_memory()