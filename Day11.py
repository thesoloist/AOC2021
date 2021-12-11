day11_input = [
    '2264552475',
    '7681287325',
    '3878781441',
    '6868471776',
    '7175255555',
    '7517441253',
    '3513418848',
    '4628736747',
    '1133155762',
    '8816621663'
]

day11_state = []


def parse_input(inp):
    outp = []
    for row in inp:
        row_int = []
        for c in row:
            row_int.append(int(c))
        outp.append(row_int)
    return outp


def process_flash(state_in):
    state_out = state_in.copy()
    flashpoint_tuples = []
    # build initial flashpoints (points == 9)
    for rid, row in enumerate(state_in):
        for cid, col in enumerate(row):
            if state_out[rid][cid] == 10:
                flashpoint_tuples.append((rid, cid))
    # process all flash points, adding new ones as they come
    # print(f"Start processing flash with {len(flashpoint_tuples)} initial flash points")
    while len(flashpoint_tuples):
        fp = flashpoint_tuples[0]
        # print(f"Point ({fp[1]},{fp[0]}) is flashing!")
        for rid in range(max(fp[0] - 1, 0), min(fp[0] + 1, len(state_out) - 1) + 1):
            for cid in range(max(fp[1] - 1, 0), min(fp[1] + 1, len(state_out[rid]) - 1) + 1):
                if state_out[rid][cid] < 10:
                    # print(f"Point ({cid},{rid}) is enhanced by adjacent point")
                    state_out[rid][cid] += 1
                    if state_out[rid][cid] == 10:
                        # print(f"Point ({cid},{rid}) is triggered by adjacent point to flash!")
                        flashpoint_tuples.append((rid, cid))
        flashpoint_tuples.pop(0)
        # print(f"After processing, {len(flashpoint_tuples)} flash points left")
    return state_out


day11_sim_days = 1000


def day11():
    day11_state = parse_input(day11_input)
    day11_1_flash_cnt = 0
    day = 1
    while True:
        print(f"Start of day {day}")
        # increase naturally
        for rid, row in enumerate(day11_state):
            for cid, col in enumerate(row):
                if day11_state[rid][cid] <= 9:
                    day11_state[rid][cid] += 1
        # Flash!
        day11_state = process_flash(day11_state)

        # Count flashes, clear all flashes
        day_flash_cnt = 0
        for rid, row in enumerate(day11_state):
            for cid, col in enumerate(row):
                if day11_state[rid][cid] == 10:
                    day_flash_cnt += 1
                    day11_state[rid][cid] = 0
        print(f"Flash count for day {day} = {day_flash_cnt}")
        day11_1_flash_cnt += day_flash_cnt
        print(f"Total flash count after day {day} = {day11_1_flash_cnt}")
        day += 1
        if day_flash_cnt == 100:
            break
