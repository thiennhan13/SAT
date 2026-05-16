def encode_ladder_amk_2_windows(x_start, shared_block, x_end, k, start_aux):
    clauses = []
    
    block_clauses, next_aux, shared_out_states = encode_amk_sc(shared_block, k, start_aux)
    clauses.extend(block_clauses)
    
    if len(shared_out_states) >= k:
        s_k = shared_out_states[k - 1]
        clauses.append([-x_start, -s_k])
        clauses.append([-x_end, -s_k])
        
    if len(shared_out_states) > k:
        s_k_plus_1 = shared_out_states[k]
        clauses.append([-s_k_plus_1])
        
    return clauses, next_aux

def encode_nrp_alsc_ladder(x_start, shared_block, x_end, w, k, start_aux):
    max_false_days = w - k
    
    neg_x_start = -x_start
    neg_shared_block = [-v for v in shared_block]
    neg_x_end = -x_end
    
    return encode_ladder_amk_2_windows(
        neg_x_start, 
        neg_shared_block, 
        neg_x_end, 
        max_false_days, 
        start_aux
    )