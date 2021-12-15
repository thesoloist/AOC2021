import time
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
#day14_pair_dict = {'CH' : 'B',
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
#day14_input = 'NNCB'

def init_result_dict():
    out_dict = {}
    for p in day14_pair_dict.values():
        if p in out_dict.keys():
            None
        else:
            out_dict[p] = 0
    return out_dict

def ins_update_dict(l, c, r, day, total_days, result_dict):
    if day == total_days:
        return
    newc_l = day14_pair_dict[l+c]
    newc_r = day14_pair_dict[c+r]
    result_dict[newc_l] += 1
    result_dict[newc_r] += 1

    #print(f"Insert called: day={day} / {total_days} total days, left={l}, center={c}, right={r} -> newc_l = {newc_l}, newc_r = {newc_r}")
    ins_update_dict(l, newc_l, c, day+1, total_days, result_dict)
    ins_update_dict(c, newc_r, r, day+1, total_days, result_dict)

def ins_update_dict_cached(l, r, day, cached_days, total_days, cached_dict, result_dict):
    if day == total_days:
        return
    else:
        if day == total_days - cached_days:
            #print(f"CACHED - Using cached value: day={day}, pair = {l, r}")
            for p in result_dict.keys():
                result_dict[p] += cached_dict[l+r][p]
        else:
            newc = day14_pair_dict[l + r]
            result_dict[newc] += 1

            #print(f"CACHED - Insert called: day={day}, left={l}, center={newc}, right={r}")
            ins_update_dict_cached(l, newc, day + 1, cached_days, total_days, cached_dict, result_dict)
            ins_update_dict_cached(newc, r, day + 1, cached_days, total_days, cached_dict, result_dict)

def build_cache(pair,days):
    # print(f"Building cache for pair {pair}, cache for {days} days")
    out_result_dict = init_result_dict()
    # out_result_dict[pair[0]] += 1
    # out_result_dict[pair[1]] += 1
    out_result_dict[day14_pair_dict[pair]] += 1

    ins_update_dict(pair[0], day14_pair_dict[pair], pair[1], 1, days, out_result_dict)
    return out_result_dict



start_time = time.time()

run_days = 40
polymer_dict = {}
# initialize output dict
polymer_dict = init_result_dict()

using_cache = True
cache_days = 20
cache_dict = {}

if using_cache is True and cache_days > 0:
    for p in day14_pair_dict.keys():
        cache_dict[p] = build_cache(p, cache_days)
    print(f"cache dict: {cache_dict}")

for p_idx in range(len(day14_input)):
    polymer_dict[day14_input[p_idx]] += 1

    if p_idx < len(day14_input)-1:
        pair = day14_input[p_idx] + day14_input[p_idx+1]
        insert_c = day14_pair_dict[pair]
        print(f"time {time.time() - start_time} - Got pair {pair} -> inserting {insert_c}")
        if using_cache is False:
            polymer_dict[insert_c] += 1
            ins_update_dict(day14_input[p_idx], insert_c, day14_input[p_idx+1], 1, run_days, polymer_dict)
        else:
            ins_update_dict_cached(day14_input[p_idx], day14_input[p_idx+1], 0, cache_days, run_days, cache_dict, polymer_dict)

print(f"Finished in {time.time() - start_time} seconds")

max_cnt, max_itm = 0, ''
min_cnt, min_itm = max(polymer_dict.values()), ''

print(f"result dict: {polymer_dict}")

for k in polymer_dict.keys():
    if polymer_dict[k] > max_cnt:
        max_cnt = polymer_dict[k]
        max_itm = k
    elif polymer_dict[k] < min_cnt:
        min_cnt = polymer_dict[k]
        min_itm = k
print(f"Max itm/cnt = {max_itm}/{max_cnt}, Min itm/cnt={min_itm}/{min_cnt} - diff = {max_cnt - min_cnt}")
