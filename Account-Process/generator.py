from compute import choose_next_node


def tx_seq(p_distribute, times):
    seqs = []
    for from_object in range(p_distribute.shape[0]):
        seq = []
        for i in range(times):
            to_object = choose_next_node(p_distribute, from_object)
            seq.append([from_object, to_object])
        seqs.append(seq)

    return seqs


if __name__ == "__main__":
    pass
