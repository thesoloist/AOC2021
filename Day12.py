day12_input = [
    'ey-dv',
    'AL-ms',
    'ey-lx',
    'zw-YT',
    'hm-zw',
    'start-YT',
    'start-ms',
    'dv-YT',
    'hm-ms',
    'end-ey',
    'AL-ey',
    'end-hm',
    'rh-hm',
    'dv-ms',
    'AL-dv',
    'ey-SP',
    'hm-lx',
    'dv-start',
    'end-lx',
    'zw-AL',
    'hm-AL',
    'lx-zw',
    'ey-zw',
    'zw-dv',
    'YT-ms']

day12_map_dict = {}


def parse_input(inp):
    for path in inp:
        (start,finish) = path.split('-')
        # print(f"Path goes from {start} to {finish}")
        if start in day12_map_dict.keys():
            day12_map_dict[start].append(finish)
        else:
            day12_map_dict[start] = [finish]
        if finish in day12_map_dict.keys():
            day12_map_dict[finish].append(start)
        else:
            day12_map_dict[finish] = [start]


def go_next(cur_path, cur_pt, allow_small_twice):
    this_path = cur_path
    # print(f"Current path {cur_path}, Exploring next step from point '{cur_pt}'")
    for next_pt in day12_map_dict[cur_pt]:
        print(f"cur_path = {this_path}, cur_pt = {cur_pt}, Trying next point {next_pt}")
        if next_pt == 'end':
            print(f"Found a path to end! path is {cur_path + ['end']}")
            day12_1_paths.append(cur_path + ['end'])
        elif (next_pt in this_path) and next_pt.lower() == next_pt:
            print(f"Checking if {next_pt} can be visited twice")
            can_visit_twice = allow_small_twice
            if next_pt == 'start' or next_pt == 'end':
                can_visit_twice = False
            else:
                for k in day12_map_dict.keys():
                    if k.lower() == k and this_path.count(k) > 1:
                        can_visit_twice = False
            if can_visit_twice:
                print(f"Visiting cave {next_pt} for the second time")
                this_path.append(next_pt)
                go_next(this_path, next_pt, False)
            else:
                print(f"Cannot visit cave {next_pt} for the second time")
        else:
            this_path.append(next_pt)
            go_next(this_path, next_pt, allow_small_twice)
    print(f"Tried all next points for point {cur_pt}, popping...")
    cur_path.pop(-1)


parse_input(day12_input)
#for k in day12_map_dict.keys():
#    print(f"{k}: {day12_map_dict[k]}")
day12_1_paths = []
for start_pt in day12_map_dict['start']:
    path = ['start', start_pt]
    go_next(path, start_pt, allow_small_twice=True)

print(f"Found {len(day12_1_paths)} paths to leave")

