score=0
occurqijd=0
min_score = -10000
double_min=4.9e-324
tfqijd=0
score_crter=0
score_bm25=0
// 这5个参数很重要，调参主要就是调这几个
b = 0.35 
k1 = 1.2
k3 = 8.0
rate = 0.045
sigma = 20

field = "all"
docs_num = _index[field].docCount()
field_length = doc['all.length' ].value
avg_field_length = _index[field].sumttf() / docs_num
K = k1 * ((1 - b) + b * field_length/ avg_field_length)
qtf = []
// terms 为通过params传进来的参数
// 查询词的重复情况
for (term in terms) {
    within = 0;
	for (term_next in terms) {
		if (term == term_next) {
            within = within + 1;
		}   
	}   
    qtf.add(within)
}
terms_size = terms.size()
for(qi=0;qi<terms_size; qi++){
    term=terms[qi]
    term_info=_index[field].get(term, _FREQUENCIES | _POSITIONS | _CACHE)
    // 词在文档中的频率
    tfqid = term_info.tf()
	if (tfqid == 0){
        continue
	}
    // 词在文档中的位置列表，为int类型
    term_info_list = []
	for (pos in term_info){
        term_info_list.add(pos.position)
	}
	for (qj=qi+1; qj<terms_size; qj++){
        term_next = terms[qj]
        term_next_info = _index[field].get(term_next, _FREQUENCIES | _POSITIONS | _CACHE)
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
        // 统计文档中，两个词的位置相关性
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
		}
	}
    // for BM25                                            
    df = _index[field][term].df()         
    TF = (k1 + 1) * tfqid / (K + tfqid)           
    IDF = log2((docs_num - df + 0.5) / (df + 0.5))  
    QTF = (k3 + 1) * qtf[qi] / (k3 + qtf[qi])    
    score_bm25 += TF * IDF * QTF

};
// 此处未归一化，应该用zmin-zmax进行归一化
score = score_bm25 * (1 -rate) + score_crter * rate
return score;
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
