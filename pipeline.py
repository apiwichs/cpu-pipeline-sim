def pipeline(program):
    """
    This acts as a shift register
    program is a list of Instructions object
    None is garbage values 
    """
    print("===== Pipeline Simualation =====")
    cycle = 0
    stall_count = 0
    stall_flag = False
    retired = 0
    program_counter = 0
    num_of_instructions = len(program)
    data = []

    shift_reg = [None, None, None, None, None]
    
    is_empty = True
    
    while((program_counter < num_of_instructions) or (not is_empty)):
        stall_flag = False              # Reset flag
        cycle += 1
        
        curr_reg0 = shift_reg[0]
        curr_reg1 = shift_reg[1]
        curr_reg2 = shift_reg[2]
        curr_reg3 = shift_reg[3]
        curr_reg4 = shift_reg[4]
        
        stall_flag = detect_data_hazard(shift_reg)
        
        if(stall_flag):
            stall_count += 1
            ##if new instruction is dependent on previous incomplete writes
            shift_reg[0] = curr_reg0
            shift_reg[1] = curr_reg1
            shift_reg[2] = None
            shift_reg[3] = curr_reg2
            shift_reg[4] = curr_reg3
        else:
            ## new instruction is independent from previous incomplete writes
            if(program_counter < num_of_instructions):
                # Shift data across the registers
                shift_reg[0] = program[program_counter]
                program_counter += 1
            
            else:
                shift_reg[0] = None
            shift_reg[1] = curr_reg0
            shift_reg[2] = curr_reg1
            shift_reg[3] = curr_reg2
            shift_reg[4] = curr_reg3
        
        is_empty = True                 # Reset flag
        
        ## Check if the pipeline has been fully executed
        for reg in shift_reg:
            if(reg is not None):
                is_empty = False
        
        ## Count retired instructions
        if(curr_reg4 is not None):
                retired += 1
        ## Get str of Instruction object in each shift_reg AFTER clock cycle
        reg0_str = current_state(shift_reg[0])
        reg1_str = current_state(shift_reg[1])
        reg2_str = current_state(shift_reg[2])
        reg3_str = current_state(shift_reg[3])
        reg4_str = current_state(shift_reg[4])
        
        ## Data from this cycle
        current_cycle_data = {"cycle": cycle,
                "stall": stall_flag,
                "pc": program_counter,
                "IF": reg0_str,
                "ID": reg1_str,
                "EX": reg2_str,
                "MEM": reg3_str,
                "WB": reg4_str}
        
        data.append(current_cycle_data)
       
        print(
        f"Cycle {cycle:02d} | "
        f"IF: {reg0_str} | "
        f"ID: {reg1_str} | "
        f"EX: {reg2_str} | "
        f"MEM: {reg3_str} | "
        f"WB: {reg4_str}")  

    print("\n===== Pipeline Performance Summary =====")
    print(f"Total cycles   : {cycle}")
    print(f"Total stalls   : {stall_count}")
    print(f"Instructions retired : {retired}")

    if retired != 0:
        CPI = cycle / retired
        print(f"Cycles Per Instruction (CPI) : {CPI:.2f}")
        #print(f"CPI            : {CPI:.2f}")

    else:
        print("Cycles Per Instruction (CPI) : N/A (no instructions retired)")
    
    return data      
                
def detect_data_hazard(shift_reg)->bool:
    id = shift_reg[1]
    exe  = shift_reg[2]
    mem = shift_reg[3]
    wb = shift_reg[4]
    
    if(id == None):
        return False
    
    id_src_regs = (id.src_regs)
    incomplete_writes = set()

    if(exe is not None and exe.dst_reg is not None):
        exe_dst = exe.dst_reg
        incomplete_writes.add(exe_dst)
    
    if(mem is not None and mem.dst_reg is not None):
        mem_dst = mem.dst_reg
        incomplete_writes.add(mem_dst)
    
    ### WB writes the register file this cycle, so we don’t treat WB as an incomplete write
    """
    if(wb is not None and wb.dst_reg is not None):
        wb_dst = wb.dst_reg
        incomplete_writes.add(wb_dst)
    """
        
    for dependent in id_src_regs: ##Check if instruction needs data from other incomplete instructions
        if(dependent in incomplete_writes):
            return True
        
    return False
    
def current_state(instruction_object):
    if(instruction_object is not None):
        return str(instruction_object)
    else:
        return "---------------"