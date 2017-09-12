score=0
b = 0.35 
k1 = 1.2
k3 = 8.0
rate = 0.045
sigma = 20
occurqijd=0
min_score = -10000
double_min=4.9e-324
tfqijd=0

field = "all"
docs_num = _index[field].docCount()
field_length = doc['all.length' ].value
avg_field_length = _index[field].sumttf() / docs_num
K = k1 * ((1 - b) + b * field_length/ avg_field_length)
qtf = []
for (term in terms) {
    within = 0;
    for (term_next in terms) {
        if (term == term_next) {
            within = within + 1;
        }   
    }   
    qtf.add(within)
}
println qtf 
terms_size = terms.size()
score_crter=0
for(qi=0;qi<terms_size; qi++){
    term=terms[qi]
    term_info=_index[field].get(term, _POSITIONS | _CACHE)
    tfqid = term_info.tf()
    if (tfqid == 0){
        continue
    }
    term_info_list = []
    for (pos in term_info){
      term_info_list.add(pos.position)
    }
    println term;
    println term_info_list;
    for (qj=qi+1; qj<terms_size; qj++){
        term_next = terms[qj]
        println term_next
        term_next_info = _index[field].get(term_next, _POSITIONS | _CACHE)
        ndqij = 0 
        tfqjd = term_next_info.tf()
        if (tfqjd == 0)
            continue
        term_next_info_list = []
        for (pos in term_next_info){
          term_next_info_list.add(pos.position)
        }
        withinqij = min(qtf[qi], qtf[qj])
        qtf_kernel = my_kernel(intersect(1), sigma) * withinqij
        for (pos_term in term_info_list) {
            position_k = pos_term
            for (pos_term_next in term_next_info_list) {
                position_k2 = pos_term_next
                kernel_termp = my_kernel(intersect(1) * abs(position_k - position_k2), sigma)
                if (kernel_termp >= double_min) {
                    tfqijd += kernel_termp
                    occurqijd += 1
                }
            }
        if (occurqijd != 0){
          ndqij += tfqijd / occurqijd
        }
        TFqijd = (k1 + 1) * tfqijd / (K + tfqijd)
        IDFqijd = log2((docs_num - ndqij + 0.5)/ (ndqij + 0.5))
        QTF = (k3 + 1) * qtf_kernel / (k3 + qtf_kernel)
        score_crter += TFqijd * IDFqijd * QTF
        println score_crter
        }
    }
};

return score_crter;

def my_kernel(distfromcenter, sigma){
    if (distfromcenter > sigma){
        return 0.0
    }
    else{
        return 1.0 - distfromcenter / sigma
    }
}

def intersect(distbetween){
    return distbetween / 2.0
}

def log2(num){
    return log(num) / log(2)
}
