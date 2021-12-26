import re

day24_input = ['inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 10',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 2',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 14',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 13',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 14',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 13',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -13',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 9',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 10',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 15',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -13',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 3',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -7',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 6',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 11',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 5',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 10',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 16',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 1',
'add x 13',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 1',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -4',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 6',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -9',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 3',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -13',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 7',
'mul y x',
'add z y',
'inp w',
'mul x 0',
'add x z',
'mod x 26',
'div z 26',
'add x -9',
'eql x w',
'eql x 0',
'mul y 0',
'add y 25',
'mul y x',
'add y 1',
'mul z y',
'mul y 0',
'add y w',
'add y 9',
'mul y x',
'add z y']

def execute(op, inp1, inp2):
    out = 0
    if op == 'add':
        out = inp1 + inp2
    elif op == 'mul':
        out = inp1 * inp2
    elif op == 'div':
        out = int(inp1 / inp2)
    elif op == 'mod':
        out = inp1 % inp2
    elif op == 'eql':
        out = 1 if inp1==inp2 else 0
    else:
        None
    return out

def run_program(prog, input_num, input_mem):
    memory = input_mem
    input_str = str(input_num)
    input_str_ptr = 0
    inp_instr = r'inp (.)'
    op_var_instr = r'(...) ([wxyz]) ([wxyz])'
    op_lit_instr = r'(...) ([wxyz]) (-?\d+)'
    for inst in prog:
        result = re.match(inp_instr, inst)
        if result == None:
            result = re.match(op_var_instr, inst)
            if result == None:
                result = re.match(op_lit_instr, inst)
                if result == None:
                    None
                    # print(f"Invalid instruction {inst}")
                else:
                    # print(f"Literal instruction {inst}")
                    memory[result.group(2)] = execute(result.group(1), memory[result.group(2)], int(result.group(3)))
            else:
                # print(f"2-Op instruction {inst}")
                memory[result.group(2)] = execute(result.group(1), memory[result.group(2)], memory[result.group(3)])
        else:
            # print(f"Input instruction {inst}")
            memory[result.group(1)] = int(input_str[input_str_ptr])
            input_str_ptr += 1
        # print(f"after {inst}, memory is {memory}")
    return memory

program_chunks = []

cur_digit = 0
for inst in day24_input:
    inst_arr = inst.split(' ')
    if len(inst_arr) == 2:
        program_chunks.append([])
        cur_digit+=1
    program_chunks[cur_digit-1].append(inst)

for i in program_chunks:
    print(i)

digit_dicts = []
blank_memory = {'w': 0,
                'x': 0,
                'y': 0,
                'z': 0}

# Below is from WilliamLP's answer. takes a LOT of memory to finish(I hit memory issue on my 16GB machine), also took around an hour for part 2

REGS = {'w': 0, 'x': 1, 'y': 2, 'z': 3}

def execute(line, regs, input_arr):
    instr, reg, operand = line
    if instr == 'inp':
        regs[REGS[reg]] = int(input_arr.pop(0))
    else:
        if operand in REGS.keys():
            n = regs[REGS[operand]]
        else:
            n = int(operand)
        if instr == 'add':
            regs[REGS[reg]] += n
        elif instr == 'mul':
            regs[REGS[reg]] *= n
        elif instr == 'mod':
            regs[REGS[reg]] %= n
        elif instr == 'div':
            regs[REGS[reg]] //= n
        elif instr == 'eql':
            regs[REGS[reg]] = 1 if regs[REGS[reg]] == n else 0

MEMO2 = {}
def execute_all(chunks, pos, input, z):
    key = f'{pos} {input} {z}'
    if key in MEMO2:
        return MEMO2[key]
    regs = [0, 0, 0, z]
    input_arr = list(str(input))
    for line in chunks[pos]:
        execute(line, regs, input_arr)
    res = regs[REGS['z']]
    MEMO2[key] = res
    return res

MEMO = {}
MIN_Z = 999999
def find(chunks, pos, z):
    global MIN_Z

    key = f'{pos} {z}'
    if key in MEMO:
        return MEMO[key]
    found = None

    # PART 1
    # for i in (9,8,7,6,5,4,3,2,1):
    # PART 2
    for i in (1,2,3,4,5,6,7,8,9):
        #print(f"Trying digit {i} in position {pos}")
        exec_result = execute_all(chunks, pos, i, z)
        if(pos == 13):
            if abs(exec_result) < MIN_Z:
                print(f'Min z {exec_result}')
                MIN_Z = abs(exec_result)
            if exec_result == 0:
                found = [i]
                break
            else:
                found = None
        else:
            new_found = find(chunks, pos + 1, exec_result)
            if new_found:
                found = [i] + new_found
                break

    MEMO[key] = found
    return found

def main():
    code = []
    for line in day24_input:
        tokens = line.strip().split(' ')
        code.append((tokens[0], tokens[1], tokens[2] if len(tokens) > 2 else None))

    chunks = []
    rest = code
    while rest:
        chunks.append(rest[0:18])
        rest = rest[18:]

    res = find(chunks, 0, 0)
    print(f"Part 2 Answer: {''.join([str(ch) for ch in res])}")

main()