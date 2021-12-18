day17_input_x = (201,230)
day17_input_y = (-99,-65)

# for tallest / farthest point
def get_max_dist(spd):
    return (spd/2) * (spd+1)

def get_y_dist(spd, step):
    return step/2 * (2*spd-step+1)

def get_x_dist(spd, step):
    dist = 0
    for i in range(step):
        if spd > i:
            dist += spd - i
    return dist

def is_hit(x,y):
    if x >= day17_input_x[0] and x <= day17_input_x[1] and y >= day17_input_y[0] and y <= day17_input_y[1]:
        return True
    else:
        return False

x_spd = 20
y_spd = 1

max_height = 0
while y_spd < 500: # trial and error gets here
    step = 2
    while True:
        if get_y_dist(y_spd, step) < day17_input_y[0] and get_y_dist(y_spd, step-1) > day17_input_y[1]:
            #print(f"y_spd={y_spd} can cause lap-over at step {step} - max height = {get_max_dist(y_spd)}")
            break
        elif get_y_dist(y_spd, step) < day17_input_y[0] and get_y_dist(y_spd, step-1) < day17_input_y[0]:
            #print(f"y_spd={y_spd} gone too far at step {step} - max height = {get_max_dist(y_spd)}")
            break
        elif get_y_dist(y_spd, step) >= day17_input_y[0] and get_y_dist(y_spd, step) <= day17_input_y[1]:
            #print(f"y_spd={y_spd} can land at step {step} - max height = {get_max_dist(y_spd)}")
            if get_max_dist(y_spd) > max_height:
                max_height = get_max_dist(y_spd)
        step += 1
    y_spd += 1

print(f"day 17-1 max height reached = {max_height}")

hit_speeds = []
for x_spd in range(20,day17_input_x[1]+1):
    for y_spd in range(day17_input_y[0], 100): # 100 comes from prev test
        step = 1
        print(f"Testing x/y spd = {x_spd}/{y_spd} - ",end='')
        while True:
            if get_y_dist(y_spd, step) < day17_input_y[0] or get_x_dist(x_spd,step) > day17_input_x[1]:
                # overshot, next...
                print("overshot")
                break
            else:
                x_loc = get_x_dist(x_spd, step)
                y_loc = get_y_dist(y_spd, step)
                if is_hit(x_loc, y_loc):
                    print(f"Found a hit speed! x/y={x_spd}/{y_spd}, at step {step}")
                    hit_speeds.append((x_spd, y_spd, step))
                    break
                step += 1

print(len(hit_speeds))