
# Online IDE - Code Editor, Compiler, Interpreter

print('Welcome to Online IDE!! Happy Coding :)')
day14_pair_dict = {
   'OO' : 'N',
   'VK' : 'B',
   'KS' : 'N',
   'PK' : 'H',
   'FB' : 'H',
   'BF' : 'S',
   'BB' : 'V',
   'KO' : 'N',
   'SP' : 'K',
   'HK' : 'O',
   'PV' : 'K',
   'BP' : 'O',
   'VO' : 'V',
   'OP' : 'C',
   'BS' : 'V',
   'OK' : 'V',
   'KN' : 'H',
   'KC' : 'N',
   'PP' : 'F',
   'NB' : 'V',
   'CH' : 'V',
   'HO' : 'K',
   'PN' : 'H',
   'SS' : 'O',
   'CK' : 'P',
   'VV' : 'K',
   'FN' : 'O',
   'BH' : 'B',
   'SC' : 'B',
   'HH' : 'P',
   'FO' : 'O',
   'CC' : 'H',
   'OS' : 'H',
   'FP' : 'S',
   'HC' : 'F',
   'BO' : 'F',
   'CF' : 'S',
   'NC' : 'S',
   'HS' : 'V',
   'KF' : 'O',
   'ON' : 'C',
   'CN' : 'K',
   'VF' : 'F',
   'NO' : 'K',
   'CP' : 'N',
   'HF' : 'K',
   'CV' : 'N',
   'HN' : 'K',
   'VH' : 'B',
   'KK' : 'P',
   'CS' : 'O',
   'VS' : 'P',
   'NH' : 'F',
   'CB' : 'S',
   'BV' : 'P',
   'FK' : 'F',
   'NV' : 'O',
   'OV' : 'K',
   'SB' : 'N',
   'NF' : 'O',
   'VN' : 'S',
   'OH' : 'O',
   'PS' : 'N',
   'HB' : 'H',
   'SV' : 'V',
   'CO' : 'H',
   'SO' : 'P',
   'FV' : 'N',
   'PF' : 'O',
   'NN' : 'S',
   'KB' : 'P',
   'NP' : 'F',
   'OC' : 'S',
   'FS' : 'P',
   'FH' : 'P',
   'VP' : 'K',
   'BN' : 'O',
   'NS' : 'H',
   'VB' : 'V',
   'PO' : 'K',
   'KP' : 'N',
   'SN' : 'O',
   'BC' : 'H',
   'SF' : 'V',
   'PC' : 'O',
   'NK' : 'F',
   'BK' : 'V',
   'KH' : 'S',
   'SH' : 'S',
   'SK' : 'H',
   'OB' : 'V',
   'PH' : 'N',
   'PB' : 'C',
   'HV' : 'N',
   'HP' : 'V',
   'FF' : 'B',
   'OF' : 'P',
   'VC' : 'S',
   'KV' : 'C',
   'FC' : 'F'}
# day14_pair_dict = {'CH' : 'B',
# 'HH' : 'N',
# 'CB' : 'H',
# 'NH' : 'C',
# 'HB' : 'C',
# 'HC' : 'B',
# 'HN' : 'C',
# 'NN' : 'C',
# 'BH' : 'H',
# 'NC' : 'B',
# 'NB' : 'B',
# 'BN' : 'B',
# 'BB' : 'N',
# 'BC' : 'B',
# 'CC' : 'N',
# 'CN' : 'C'}

day14_input = 'HHKONSOSONSVOFCSCNBC'
# day14_input = 'NNCB'

run_days = 40
polymer_dict = {}

def ins_update_dict(l, c, r, day):
    if day == run_days:
        return
    newc_l = day14_pair_dict[l+c]
    newc_r = day14_pair_dict[c+r]
    if newc_l in polymer_dict.keys():
        polymer_dict[newc_l] += 1
    else:
        polymer_dict[newc_l] = 1
    if newc_r in polymer_dict.keys():
        polymer_dict[newc_r] += 1
    else:
        polymer_dict[newc_r] = 1
    # print(f"Insert called: day={day}, left={l}, center={c}, right={r} -> newc_l = {newc_l}, newc_r = {newc_r}")
    ins_update_dict(l, newc_l, c, day+1)
    ins_update_dict(c, newc_r, r, day+1)

for p_idx in range(len(day14_input)):
    if day14_input[p_idx] in polymer_dict:
        polymer_dict[day14_input[p_idx]] += 1
    else:
        polymer_dict[day14_input[p_idx]] = 1
    if p_idx < len(day14_input)-1:
        pair = day14_input[p_idx] + day14_input[p_idx+1]
        insert_c = day14_pair_dict[pair]
        print(f"Got pair {pair} -> inserting {insert_c}")
        if insert_c in polymer_dict:
            polymer_dict[insert_c] += 1
        else:
            polymer_dict[insert_c] = 1
        ins_update_dict(day14_input[p_idx], insert_c, day14_input[p_idx+1], 1)
    
max_cnt, max_itm = 0, ''
min_cnt, min_itm = max(polymer_dict.values()), ''

print(polymer_dict)

for k in polymer_dict.keys():
    if polymer_dict[k] > max_cnt:
        max_cnt = polymer_dict[k]
        max_itm = k
    elif polymer_dict[k] < min_cnt:
        min_cnt = polymer_dict[k]
        min_itm = k
print(f"Max itm/cnt = {max_itm}/{max_cnt}, Min itm/cnt={min_itm}/{min_cnt} - diff = {max_cnt - min_cnt}")
