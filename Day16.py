import math

class LongPkt():
    def __init__(self, tag):
        self.full_bits = ''
        self.pkt_tag = tag
        self.sub_pkts = []
        self.ver = 0
        self.type_id = 0
        self.literal_val = 0
        self.sub_type = 'NONE'

    def parse(self, queue, idx, level):
        # parse into pkt starting from queue[idx]
        level_tag = ' '*level*4
        my_pt = idx
        parse_done = False
        print(f"{level_tag}Start parsing from queue idx={my_pt}, level = {level}")
        print(f"{level_tag}{[queue[idx:idx+64]]}")
        while my_pt < len(queue) and not parse_done:
            self.ver = int(queue[my_pt:my_pt+3], 2)
            print(f"{level_tag}got ver={self.ver}")
            my_pt += 3
            self.type_id = int(queue[my_pt:my_pt+3], 2)
            my_pt += 3
            if self.type_id == 4:
                print(f"{level_tag}Got literal (type {self.type_id})")
                # literals
                while True:
                    lv = int(queue[my_pt:my_pt+5], 2)
                    my_pt += 5
                    if lv >= 16: # bit[4]=1
                        self.literal_val = self.literal_val*16+(lv - 16)
                        print(f"{level_tag}Continue doing literal, lv = {lv} ({queue[my_pt-5:my_pt]}) outcome sofar = {self.literal_val}, my_pt={my_pt}")
                    else:
                        self.literal_val = self.literal_val * 16 + lv
                        # From this point to the next 4bit boundary should be all 0s
                        print(f"{level_tag}Finished doing literal, lv = {lv} ({queue[my_pt-5:my_pt]}) outcome final = {self.literal_val}, my_pt={my_pt}, level={level}")
                        if level==0:
                            if my_pt % 4:
                                my_pt += 4 - (my_pt % 4)
                                print(f"lining up, outcome = {self.literal_val}, my_pt={my_pt}")
                        else:
                            parse_done = True
                        break
            else:
                print(f"{level_tag}Got operator {self.type_id}")
                length_type = int(queue[my_pt:my_pt+1], 2)
                my_pt += 1
                if length_type == 0:
                    length_subpkts = int(queue[my_pt:my_pt+15], 2)
                    self.sub_type = str.format('LENGTH-{}', length_subpkts)
                    my_pt += 15
                    print(f"{level_tag}subpkt length = {length_subpkts}")
                    subpkts_start_idx = my_pt
                    print(f"{level_tag}Start processing all sub packets, my_pt={my_pt}, level = {level}")
                    sub_pkt_cnt = 0
                    while True:
                        new_pkt = LongPkt(self.pkt_tag + '_subcnt' + str(sub_pkt_cnt))
                        self.sub_pkts.append(new_pkt)
                        sub_pkt_cnt += 1
                        my_pt = new_pkt.parse(binary_q, my_pt, level + 1)
                        print(f"{level_tag}length-based Finished parsing a sub-pkt, ptr is now at {my_pt}")
                        if my_pt - subpkts_start_idx == length_subpkts:
                            print(f"{level_tag}Got enough length for subpkts find a total of {sub_pkt_cnt} subpkts, break...")
                            parse_done = True
                            break
                        else:
                            print(f"{level_tag}my_pt={my_pt}, start_idx = {subpkts_start_idx}, not at length={length_subpkts} yet, continue...")
                else:
                    num_subpkts = int(queue[my_pt:my_pt + 11], 2)
                    self.sub_type = str.format('NUM-{}', num_subpkts)
                    my_pt += 11
                    print(f"{level_tag}subpkt Num = {num_subpkts}")
                    for i in range(num_subpkts):
                        print(f"{level_tag}processing sub packets {i+1} of {num_subpkts}, my_pt={my_pt}")
                        new_pkt = LongPkt(self.pkt_tag+'_subnum'+str(i))
                        self.sub_pkts.append(new_pkt)
                        my_pt = new_pkt.parse(binary_q, my_pt, level + 1)
                        print(f"{level_tag}num-based Finished parsing a sub-pkt, ptr is now at {my_pt}")
                    print(f"{level_tag}num-based Finished processing all sub packets, my_pt={my_pt}")
                    parse_done = True
                print(f"{level_tag}Finished processing all sub packets, my_pt={my_pt}")
                if level == 0:
                    parse_done = True
        print(f"{level_tag}Finished parsing, my_pt = {my_pt}, queue length = {len(queue)}")
        self.full_bits = queue[idx:my_pt]
        return my_pt

    def get_ver_sum(self):
        ver_sum = self.ver
        for p in self.sub_pkts:
            ver_sum += p.get_ver_sum()
        return ver_sum

    def print_pkt(self, indent_lvl):
        print(" "* indent_lvl, end='')
        print(f"- Pkt: full_bits={self.full_bits} (length={len(self.full_bits)})")
        print(" " * indent_lvl, end='')
        print(f"- Pkt: version={self.ver}, type_id = {self.type_id}",end='')
        if self.type_id == 4:
            print(f', literal value = {self.literal_val}')
        else:
            print(f',subpkt generated from {self.sub_type}, Number of sub packets = {len(self.sub_pkts)}:')
            for p in self.sub_pkts:
                p.print_pkt(indent_lvl+4)

    def get_val(self):
        ret_val = 0
        if self.type_id == 4:
            ret_val = self.literal_val
        else:
            sub_vals = []
            for p in self.sub_pkts:
                sub_vals.append(p.get_val())
            if self.type_id == 0:
                ret_val = sum(sub_vals)
            elif self.type_id == 1:
                ret_val = math.prod(sub_vals)
            elif self.type_id == 2:
                ret_val = min(sub_vals)
            elif self.type_id == 3:
                ret_val = max(sub_vals)
            elif self.type_id == 5:
                ret_val = 1 if sub_vals[0] > sub_vals[1] else 0
            elif self.type_id == 6:
                ret_val = 1 if sub_vals[0] < sub_vals[1] else 0
            elif self.type_id == 7:
                ret_val = 1 if sub_vals[0] == sub_vals[1] else 0
        return ret_val




day16_input = '420D4900B8F31EFE7BD9DA455401AB80021504A2745E1007A21C1C862801F54AD0765BE833D8B9F4CE8564B9BE6C5CC011E00D5C001098F11A232080391521E4799FC5BB3EE1A8C010A00AE256F4963B33391DEE57DA748F5DCC011D00461A4FDC823C900659387DA00A49F5226A54EC378615002A47B364921C201236803349B856119B34C76BD8FB50B6C266EACE400424883880513B62687F38A13BCBEF127782A600B7002A923D4F959A0C94F740A969D0B4C016D00540010B8B70E226080331961C411950F3004F001579BA884DD45A59B40005D8362011C7198C4D0A4B8F73F3348AE40183CC7C86C017997F9BC6A35C220001BD367D08080287914B984D9A46932699675006A702E4E3BCF9EA5EE32600ACBEADC1CD00466446644A6FBC82F9002B734331D261F08020192459B24937D9664200B427963801A094A41CE529075200D5F4013988529EF82CEFED3699F469C8717E6675466007FE67BE815C9E84E2F300257224B256139A9E73637700B6334C63719E71D689B5F91F7BFF9F6EE33D5D72BE210013BCC01882111E31980391423FC4920042E39C7282E4028480021111E1BC6310066374638B200085C2C8DB05540119D229323700924BE0F3F1B527D89E4DB14AD253BFC30C01391F815002A539BA9C4BADB80152692A012CDCF20F35FDF635A9CCC71F261A080356B00565674FBE4ACE9F7C95EC19080371A009025B59BE05E5B59BE04E69322310020724FD3832401D14B4A34D1FE80233578CD224B9181F4C729E97508C017E005F2569D1D92D894BFE76FAC4C5FDDBA990097B2FBF704B40111006A1FC43898200E419859079C00C7003900B8D1002100A49700340090A40216CC00F1002900688201775400A3002C8040B50035802CC60087CC00E1002A4F35815900903285B401AA880391E61144C0004363445583A200CC2C939D3D1A41C66EC40'
#day16_input = '04005AC33890'

binary_q = ''
input_ptr = 0

for c in day16_input:
    binary_q += "{0:04b}".format(int(c, 16))

print(f"Got binary q={binary_q}")

top_pkt = LongPkt("toplevel")
top_pkt.parse(binary_q, 0, 0)

# top_pkt.print_pkt(0)

version_sum = 0
version_sum += top_pkt.get_ver_sum()
print(f"sum of versions = {version_sum}")
pkt_total_val = top_pkt.get_val()
print(f"total value = {pkt_total_val}")
