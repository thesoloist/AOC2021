day6_input = [1,3,4,1,1,1,1,1,1,1,1,2,2,1,4,2,4,1,1,1,1,1,5,4,1,1,2,1,1,1,1,4,1,1,1,4,4,1,1,1,1,1,1,1,2,4,1,3,1,1,2,1,2,1,1,4,1,1,1,4,3,1,3,1,5,1,1,3,4,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,1,1,5,2,5,5,3,2,1,5,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,5,1,1,1,1,5,1,1,1,1,1,4,1,1,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,3,1,2,4,1,5,5,1,1,5,3,4,4,4,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,5,3,1,4,1,1,2,2,1,2,2,5,1,1,1,2,1,1,1,1,3,4,5,1,2,1,1,1,1,1,5,2,1,1,1,1,1,1,5,1,1,1,1,1,1,1,5,1,4,1,5,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,5,4,5,1,1,1,1,1,1,1,5,1,1,3,1,1,1,3,1,4,2,1,5,1,3,5,5,2,1,3,1,1,1,1,1,3,1,3,1,1,2,4,3,1,4,2,2,1,1,1,1,1,1,1,5,2,1,1,1,2]

def day6(days):
    #Each state is for number of fishes that has X days left
    fish_state = [0]*9

    for d in day6_input:
        fish_state[d] += 1
    
    for day in range(days):
        end_state = fish_state
        print(f"start of day {day}: have {sum(end_state)} fish")
        # state-0's generate new state-8 fish
        new_fish_cnt = fish_state[0]
        # move every fish down a state
        for d in range(len(end_state)-1):
            end_state[d] = fish_state[d+1]
        # set state-8 fish
        end_state[8] = new_fish_cnt
        # add state-0's to state-6's
        end_state[6] += new_fish_cnt
        print(f"end of day {day}: have {new_fish_cnt} new fish, total fish count {sum(end_state)}")
        fish_state = end_state
    return sum(fish_state)
