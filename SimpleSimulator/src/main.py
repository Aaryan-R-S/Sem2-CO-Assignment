import mem_reg
from matplotlib import pyplot as plt

mem_reg.initialize()

while(not mem_reg.HALTED):
    Instruction = mem_reg.getInstruction()
    mem_reg.run_instr(Instruction) 
    mem_reg.dump()
    mem_reg.PC = mem_reg.NEWPC
    mem_reg.CURRCYCLE += 1

mem_reg.dump_memory()

plt.scatter(mem_reg.CYCLES, mem_reg.MEMACCESSES)
plt.xlabel('Cycle Number (an integer starting from 0)')
plt.ylabel('Memory-address Accessed (an integer from 0 to 255)')
plt.title('Bonus Part')
plt.legend(['(x,y) = (cycle number, memory-address accessed)'])
plt.savefig('bonus.png', dpi=300, bbox_inches='tight')
plt.close()