from instruction import Instruction

def get_user_input()->list[Instruction]:
    print("Enter instructions as: OP dst src1 src2")
    print("Example: ADD x1 x2 x3")
    print("Type 'done' or 'end' or 'quit' to finish.\n")
    
    program = []
    valid_operations = ("ADD","SUB") # Can we modified to include more
    
    while(True):
        user_input = input("> ").strip()
        if user_input.lower() in ("done", "end", "quit"):
            break
        
        commands = user_input.split()
        if len(commands) != 4:
            print("Invalid format. Use: ADD dst src1 src2")
            continue

        instruction = commands[0].upper()
        dst = commands[1]
        src1 = commands[2]
        src2 = commands[3]
        
        if(instruction not in valid_operations):
                print("Invalid input. Only ADD and SUB are allowed")
                continue
        
        instruction_obj = Instruction(instruction, (src1,src2), dst)
        program.append(instruction_obj)
    
    return program