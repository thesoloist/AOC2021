def transpose(l1):
    l2 = [[row[i] for row in l1] for i in range(len(l1[0]))]
    return l2

def print_state(state):
    for l in state:
        print(''.join(l))

def move(state, move_char):
    stable = True
    for l_idx, line in enumerate(state):
        new_state = line.copy()
        for idx in range(len(line)):
            if idx+1 == len(line):
                if (line[idx], line[0]) == (move_char, '.'):
                    new_state[0], new_state[idx] = move_char, '.'
                    stable = False
            else:
                if (line[idx], line[idx+1]) == (move_char, '.'):
                    new_state[idx], new_state[idx + 1] = '.', move_char
                    stable = False
        state[l_idx] = new_state
    return stable

fn = open('inputs/day25.txt', 'r')
flines = fn.read().splitlines()
fn.close()

state = []
for l in flines:
    state_line = []
    for c in l:
        state_line.append(c)
    state.append(state_line)

print_state(state)
move_stable = False
step_cnt = 0
while move_stable==False:
    move_stable = True
    step_cnt += 1
    print(f"Starting step {step_cnt}")
    move_stable = move_stable & move(state, '>')
    # transpose
    # print(f"After horiz move, state looks like:")
    # print_state(state)
    state_t = []
    state_t = transpose(state)
    move_stable = move_stable & move(state_t, 'v')
    # transpose again
    state = transpose(state_t)
    # print(f"After step {step_cnt}, state looks like:")
    # print_state(state)

print(f"Stablized after {step_cnt} steps")
print_state(state)