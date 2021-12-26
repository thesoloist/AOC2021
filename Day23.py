import math,time
import Graph

day23_input = [
    '#############',
    '#...........#',
    '###B#C#C#B###',
    '  #D#D#A#A#  ',
    '  #########  ']


homes_dict = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3}
homes_rev_dict = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D'}

state_energy_dict = {}
class AmphiState:
    def __init__(self, RoomDepth=2):
        self.hall = []
        for i in range(11):
            self.hall.append('.')
        self.Rooms = [['.'*RoomDepth] for i in range(4)] #first char is top position
        self.illegal_hall = [2,4,6,8]

    def get_hashkey(self):
        key = ''.join(self.hall) + '_'
        for r in self.Rooms:
            for c in r:
                key += c
        return key

    def IsComplete(self):
        for idx,r in enumerate(self.Rooms):
            for c in r:
                if c != homes_rev_dict[idx]:
                    return False
        return True

    def IsRoomOpen(self, room_idx):
        for c in self.Rooms[room_idx]:
            if c != '.' and c != homes_rev_dict[room_idx]:
                return False
        return True

    def print_state(self):
        print(f'#############')
        print(f"#{''.join(self.hall)}#")
        print(f"###{self.Rooms[0][0]}#{self.Rooms[1][0]}#{self.Rooms[2][0]}#{self.Rooms[3][0]}###")
        for i in range(1,len(self.Rooms[0])):
            print(f"  #{self.Rooms[0][i]}#{self.Rooms[1][i]}#{self.Rooms[2][i]}#{self.Rooms[3][i]}#  ")
        print(f'  #########  ')
    def check_room(self, room_id, room):
        # returns the least depth where a move can be made. -1 means no move can be made from this room
        # empty/completed/half-completed room
        for idx, c in enumerate(room):
            if c == '.':
                continue
            elif c==homes_rev_dict[room_id]:
                # see if it's at top of a set home. If not, it can be moved
                for bot in room[idx+1:]:
                    if c != bot:
                        return idx
                return -1
            else:
                return idx
        return -1
    def get_room_level(self, room_idx):
        ret = 0
        for c in self.Rooms[room_idx]:
            if c != '.':
                break
            ret += 1
        return ret
    def gen_moves(self, tag, hash_states, hash_graph):
        # returns an array of states that one legal move from this state can get to
        # first, check if someone can leave room
        # print(f"Calling gen_moves at level {tag}")
        shortest_energy = math.inf
        next_states = []
        if(self.get_hashkey() not in hash_graph.keys()):
            hash_states.append(self.get_hashkey())
            hash_graph[self.get_hashkey()] = {}
        for idx, rm in enumerate(self.Rooms):
            room_move_id = self.check_room(idx, rm)
            if room_move_id == -1:
                continue
            else:
                # find all legal moves
                # to the left: stop at the first non-empty location.(can't crosswalk in hall). illegal location ignored too
                legal_halls = []
                # print(f"Moving room[{idx}][{room_move_id}]='{rm[room_move_id]}'")
                for l in range((self.illegal_hall[idx]-1), -1, -1):
                    if l in self.illegal_hall:
                        continue
                    if self.hall[l] != '.':
                        break
                    legal_halls.append(l)
                # to the right
                for r in range((self.illegal_hall[idx]+1), 11):
                    if r in self.illegal_hall:
                        continue
                    if self.hall[r] != '.':
                        break
                    legal_halls.append(r)
                # found a legal move. add energy for that, and save to next_states[]
                for l in legal_halls:
                    # print(f"Moving to hall location {l}", end='')
                    move_cnt = (room_move_id + 1 + abs(self.illegal_hall[idx] - l))
                    # print(f", need {move_cnt} steps, move_id={room_move_id}, r={r}, r[room_move_id] = {rm[room_move_id]}", end='')
                    move_energy = move_cnt * (10 ** homes_dict[rm[room_move_id]])
                    # print(f", using energy {move_energy}")
                    nextState = AmphiState()
                    nextState.hall = self.hall.copy()
                    nextState.hall[l] = rm[room_move_id]
                    nextState.Rooms = [row[:] for row in self.Rooms]
                    nextState.Rooms[idx][room_move_id] = '.'

                    if nextState.get_hashkey() not in hash_graph.keys():
                        hash_states.append(nextState.get_hashkey())
                        hash_graph[nextState.get_hashkey()] = {}
                        next_states.append(nextState)
                    hash_graph[self.get_hashkey()][nextState.get_hashkey()] = move_energy

                # to destination room:
                # needs destination room open, and no obstruction between them
                if self.IsRoomOpen(homes_dict[rm[room_move_id]]):
                    path_clear = True
                    start, end = 0, 0
                    if self.illegal_hall[idx] > self.illegal_hall[homes_dict[rm[room_move_id]]]:
                        start, end = self.illegal_hall[homes_dict[rm[room_move_id]]] + 1, self.illegal_hall[idx]
                    else:
                        start, end = self.illegal_hall[idx] + 1, self.illegal_hall[homes_dict[rm[room_move_id]]]
                    # print(f"Checking path from {start} to {end}")
                    for c in range(start, end):
                        if self.hall[c] != '.':
                            # print(f"hall[{c}] = {self.hall[c]}, NOT CLEAR")
                            path_clear = False
                            break
                        else:
                            None
                            # print(f"hall[{c}] = {self.hall[c]}, CLEAR")
                    if path_clear:
                        # print(f"Found a direct room-to-room connection: room {idx}(hall {self.illegal_hall[idx]}), {room_move_id} to hall {self.illegal_hall[homes_dict[rm[room_move_id]]]}, {self.get_room_level(homes_dict[rm[room_move_id]])-1}")
                        move_steps = room_move_id + 1 + abs(self.illegal_hall[idx] - self.illegal_hall[homes_dict[rm[room_move_id]]]) + self.get_room_level(homes_dict[rm[room_move_id]])
                        move_energy = move_steps * (10**homes_dict[rm[room_move_id]])
                        # print(f"Found a direct room-to-room connection: steps = {move_steps}, energy = {move_energy}")
                        nextState = AmphiState()
                        nextState.hall = self.hall.copy()
                        nextState.Rooms = [row[:] for row in self.Rooms]
                        nextState.Rooms[idx][room_move_id] = '.'
                        nextState.Rooms[homes_dict[rm[room_move_id]]][self.get_room_level(homes_dict[rm[room_move_id]])-1] = rm[room_move_id]
                        # nextState.print_state()
                        if nextState.get_hashkey() not in hash_graph.keys():
                            hash_states.append(nextState.get_hashkey())
                            hash_graph[nextState.get_hashkey()] = {}
                            next_states.append(nextState)
                        hash_graph[self.get_hashkey()][nextState.get_hashkey()] = move_energy

        # then, check if someone in hall can get in a room
        # print(f"After checking move-out, next_states size = {len(next_states)}")
        for idx, h in enumerate(self.hall):
            if h == '.':
                continue
            # see if its room is open
            if self.IsRoomOpen(homes_dict[h]) == False:
                continue
            # room is open, but can we get there?
            path_clear = True
            start, end = 0, 0
            if idx > self.illegal_hall[homes_dict[h]]:
                start, end = self.illegal_hall[homes_dict[h]]+1, idx
            else:
                start, end = idx+1, self.illegal_hall[homes_dict[h]]
            # print(f"Checking path from {start} to {end}")
            for c in range(start, end):
                if self.hall[c] != '.':
                    # print(f"hall[{c}] = {self.hall[c]}, NOT CLEAR")
                    path_clear = False
                    break
                else:
                    None
                    # print(f"hall[{c}] = {self.hall[c]}, CLEAR")
            if path_clear:
                # Make the move
                move_to_door = abs(idx - self.illegal_hall[homes_dict[h]])
                door_to_floor = 0
                for c in self.Rooms[homes_dict[h]]:
                    if c != '.':
                        break
                    door_to_floor += 1
                move_energy = (move_to_door + door_to_floor) * (10**homes_dict[h])
                # print(f"Moving {h} from Hall[{idx}] to its room, moves = {move_to_door} + {door_to_floor} moves -> {move_energy} energy spent")
                nextState = AmphiState()
                nextState.hall = self.hall.copy()
                nextState.hall[idx] = '.'
                nextState.Rooms = [row[:] for row in self.Rooms]
                nextState.Rooms[homes_dict[h]][door_to_floor-1] = h
                #nextState.print_state()
                if nextState.get_hashkey() not in hash_graph.keys():
                    hash_states.append(nextState.get_hashkey())
                    hash_graph[nextState.get_hashkey()] = {}
                    if (nextState.IsComplete()):
                        None
                        # print(f"DING DING DING - we have a completed state")
                    else:
                        next_states.append(nextState)
                hash_graph[self.get_hashkey()][nextState.get_hashkey()] = move_energy


        # Now, for each of the nextState, call its gen_moves(). we'll get there somehow...
        # print(f"After checking move-in, next_states size = {len(next_states)}")
        for idx, state in enumerate(next_states):
            if tag==0:
                print(f"Testing {idx+1} of {len(next_states)} next_state:")
                state.print_state()
                print(f"hash_states size so far = {len(hash_states)}, hash_graph keysize so far = {len(hash_graph.keys())}")
            state_energy = state.gen_moves(tag+1, hash_states, hash_graph)
            # print(f"got min energy from the state = {state_energy}")


Example_Start = AmphiState()
# Example_Start.Rooms=[['B','A'],['C','D'],['B','C'],['D','A']]
# Example_Start.Rooms=[['B','D'],['C','D'],['C','A'],['B','A']]
Example_Start.Rooms=[['B','D','D','D'],['C','C','B','D'],['C','B','A','A'],['B','A','C','A']]

Result_State = AmphiState()
#Result_State.Rooms=[['A','A'],['B','B'],['C','C'],['D','D']]
Result_State.Rooms=[['A','A','A','A'],['B','B','B','B'],['C','C','C','C'],['D','D','D','D']]

hash_states = []
hash_graph = {}

start_time = time.time()
print(start_time)

Example_Start.print_state()
Example_Start.gen_moves(0, hash_states, hash_graph)
print(f"size of states = {len(hash_states)}")

print(time.time() - start_time)

state_graph = Graph.Graph(hash_states, hash_graph)
result_prev_nodes, result_shortest_path = Graph.dijkstra_algo(state_graph, Example_Start.get_hashkey())

print(time.time() - start_time)

print(f"Lowest energy = {result_shortest_path[Result_State.get_hashkey()]}")
Graph.print_result(result_prev_nodes, result_shortest_path, Example_Start.get_hashkey(), Result_State.get_hashkey())


#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########
