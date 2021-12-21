import re, random
day21_input = ['Player 1 starting position: 6',
'Player 2 starting position: 9']

player_pos = {}
player_score = {}
input_re = r'Player (\d) starting position: (\d)'
for p in day21_input:
    m = re.search(input_re, p)
    player_pos[int(m.group(1))] = int(m.group(2))
    player_score[int(m.group(1))] = 0
    
roll_cnt = 0
rolls = range(1,101)
gameover = False
print(player_pos)
while not gameover:
    for player in player_pos.keys():
        roll = 0
        roll += rolls[roll_cnt%100]
        roll_cnt += 1
        roll += rolls[roll_cnt%100]
        roll_cnt += 1
        roll += rolls[roll_cnt%100]
        roll_cnt += 1
        
        player_pos[player] += roll % 10
        if player_pos[player] > 10:
            player_pos[player] -= 10
        player_score[player] += player_pos[player]
        #print(f"Player {player} rolled, Total of 3 rolls = {roll}, moved to {player_pos[player]}, total score = {player_score[player]}")
        if player_score[player]>=1000:
            #print(f"Player {player} WINS")
            gameover = True
            break
        
print(f"roll_cnt = {roll_cnt}")
print(player_score)

#prep work for part 2
rolls_of_3x3 = []
for a in range(1,4):
    for b in range(1,4):
        for c in range(1,4):
            rolls_of_3x3.append(a+b+c)

# build a dict. key is ((p1_pos, p2_pos),(p1_score, p2_score),next move: 0 for p1, 1 for p2), value is (win_cnt_p1, win_cnt_p2).
state_to_wins_dict = {}

while len(state_to_wins_dict.keys()) < 10*10*21*21*2:
    print(f"Looping, decided {len(state_to_wins_dict.keys())} of {10*10*21*21*2} states")
    for p1_pos in range(1,11):
        for p2_pos in range(1,11):
            print(f"Trying to decide for pos - {p1_pos},{p2_pos}")
            # count from score=20 down to increase chance of dict hit
            for p1_score in range(20,-1,-1):
                for p2_score in range(20,-1,-1):
                    for player in range(2):
                        state = ((p1_pos,p2_pos),(p1_score,p2_score),player)
                        if(state in state_to_wins_dict.keys()):
                            continue
                        else:
                            # see if we can get a deterministic outcome for all 27 possible states in this move
                            wins = [0,0]
                            determined = [0 for i in range(len(rolls_of_3x3))]
                            for idx, roll in enumerate(rolls_of_3x3):
                                pos = state[0][state[2]] + roll
                                if pos > 10:
                                    pos -= 10
                                if state[1][state[2]] + pos >= 21:
                                    # wins outright
                                    wins[player]+=1
                                    determined[idx] = 1
                                else:
                                    # next state has a known outcome
                                    new_pos = list(state[0])
                                    new_pos[state[2]] = pos
                                    new_score = list(state[1])
                                    new_score[state[2]] = state[1][state[2]] + pos
                                    new_player = 1 if state[2] == 0 else 0
                                    next_state = (tuple(new_pos), tuple(new_score), new_player)
                                    if(next_state in state_to_wins_dict.keys()):
                                        #print(f"{state} - {idx}:{roll} Grabbing from dict, next_state = {next_state}, wins = {state_to_wins_dict[next_state][0]}:{state_to_wins_dict[next_state][1]}")
                                        determined[idx] = 1
                                        wins[0] += state_to_wins_dict[next_state][0]
                                        wins[1] += state_to_wins_dict[next_state][1]
                                    else: 
                                        break
                            if sum(determined) == len(rolls_of_3x3):
                                #we are deterministic
                                dict_key = state
                                state_to_wins_dict[dict_key] = tuple(wins)
                                #print(f"state {state} calculated - wins = {state_to_wins_dict[dict_key][0]} : {state_to_wins_dict[dict_key][1]}")

#print(state_to_wins_dict)
print(len(state_to_wins_dict.keys()))
print(state_to_wins_dict[(6,9),(0,0),0])


