import matplotlib.pyplot as plt
from generic_qaoa.vqf_helper import factor_56153, factor_291311, create_clauses
from generic_qaoa.clause import CombinatoricsClause, MathematicalClause
from generic_qaoa.utils import get_pq_from_selected, plot_histogram
from generic_qaoa import GenericQaoa

if __name__ == '__main__':
    # example for MaxCut
    clauses = [CombinatoricsClause([0], [1]), CombinatoricsClause([1], [0]), CombinatoricsClause([2], [1]), CombinatoricsClause([1], [2]),
               CombinatoricsClause([2], [3]), CombinatoricsClause([3], [2]), CombinatoricsClause([3], [0]), CombinatoricsClause([0], [3])]

    qaoa = GenericQaoa(_p=2,
                       _clauses=clauses,
                       _qbits=range(4),
                       _grid_size=10,
                       _simulate=True)
    circ = qaoa.qaoa_circuit
    circ.draw()
    qaoa.run()
    print(qaoa.last_result.selected, qaoa.last_result.counts_histogram)
    # VQF
    # define m=p*q
    m = 69169
    # 1. define clauses
    if m == 56153:
        p_dict, q_dict, z_dict, clauses = factor_56153()
    elif m == 45313:
        p_dict, q_dict, z_dict, clauses = create_clauses(m,true_p_int=113, true_q_int=401, verbose=True)
    elif m == 69169:
        p_dict, q_dict, z_dict, clauses = create_clauses(m,true_p_int=263, true_q_int=263, verbose=True)
    elif m == 291311:
        p_dict, q_dict, z_dict, clauses = factor_291311()
    else:
        p_dict, q_dict, z_dict, clauses = create_clauses(m, verbose=True)

    free_symbols = set().union(*[clause.free_symbols for clause in clauses])
    qubit_index_to_symbol = {i: sym for i, sym in enumerate(free_symbols)}
    symbol_to_qubit_index = {sym: i for i, sym in qubit_index_to_symbol.items()}
    final_clauses = [MathematicalClause((clause * clause).expand(), symbol_to_qubit_index) for clause
                     in
                     clauses if clause != 0]
    vqf_qaoa = GenericQaoa(_p=3,
                           _clauses=final_clauses,
                           _qbits=range(len(free_symbols)),
                           _grid_size=8,
                           _simulate=True)

    circ = vqf_qaoa.qaoa_circuit
    vqf_qaoa.run()
    plot_histogram(vqf_qaoa.last_result.counts_histogram)
    plt.show()
    print(vqf_qaoa.last_result.selected)
    p, p_dict, q, q_dict = get_pq_from_selected(p_dict, q_dict, vqf_qaoa.last_result.selected, symbol_to_qubit_index)
    n = len(p_dict) + len(q_dict)
    print("p,q=", p, q)
    if p * q != m:
        print("Trying to fix with bit-flip.")
        for i in range(len(p_dict)):
            for j in range(len(q_dict)):
                new_p: int
                if p_dict[i] == 1:
                    new_p = p - 2 ** i
                else:
                    new_p = p + 2 ** i
                new_q: int
                if q_dict[j] == 1:
                    new_q = q - 2 ** j
                else:
                    new_q = q + 2 ** j
                if new_q == m or new_p == m:
                    break
                if new_p * q == m:
                    p = new_p
                elif p * new_q == m:
                    q = new_q
                if new_p * new_q == m:
                    p = new_p
                    q = new_q
                if p * q == m:
                    break
            if p * q == m:
                break

    # print(f"final results: {p}*{q}={p*q}?={m}")
    # #
    # # semiprimes = [11469, 11474, 11477, 11479, 11482, 11485, 11486, 11498, 11499, 11507, 11509, 11513, 11521, 11531,
    # #               11533, 11537, 11539, 11541, 11545, 11553, 11555, 11558, 11559, 11561, 11563, 11566, 11567, 11569,
    # #               11573, 11581, 11582, 11589, 11591, 11599, 11602, 11603, 11611, 11614, 11623, 11626, 11629, 11631,
    # #               11639, 11641, 11642, 11643, 11647, 11651, 11653, 11654, 11659, 11663, 11665, 11667, 11669, 11671,
    # #               11678, 11683, 11686, 11693, 11695, 11698, 11702, 11705, 11707, 11714, 11721, 11722, 11723, 11729,
    # #               11733, 11734, 11735, 11738, 11741, 11747, 11749, 11751, 11755, 11757, 11758, 11759, 11761, 11762,
    # #               11769, 11771, 11773, 11785, 11787, 11791, 11793, 11794, 11797, 11806, 11819, 11829, 11841, 11843,
    # #               11846, 11851, 11854, 11855, 11857, 11861, 11873, 11878, 11879, 11881, 11885, 11893, 11899, 11901,
    # #               11905, 11906, 11911, 11915, 11917, 11929, 11945, 11947, 11957, 11962, 11963, 11965, 11967, 11974,
    # #               11983, 11989, 11993, 11995, 12001, 12003, 12009, 12013, 12014, 12017, 12021, 12022, 12023, 12029,
    # #               12031, 12039, 12047, 12053, 12055, 12057, 12058, 12059, 12061, 12063, 12067, 12074, 12077, 12079,
    # #               12081, 12083, 12085, 12086, 12091, 12094, 12106, 12115, 12127, 12131, 12133, 12134, 12137, 12139,
    # #               12146, 12147, 12151, 12153, 12158, 12169, 12171, 12178, 12179, 12181, 12182, 12185, 12187, 12191,
    # #               12193, 12199, 12202, 12205, 12209, 12217, 12219, 12223, 12226, 12229, 12233, 12235, 12237, 12242,
    # #               12247, 12262, 12266, 12271, 12273, 12279, 12283, 12286, 12287, 12293, 12295, 12297, 12302, 12307,
    # #               12311, 12313, 12317, 12319, 12326, 12333, 12335, 12346, 12349, 12353, 12359, 12361, 12365, 12367,
    # #               12371, 12381, 12385, 12387, 12389, 12394, 12398, 12399, 12403, 12406, 12407, 12417, 12419, 12422,
    # #               12431, 12434, 12439, 12442, 12443, 12449, 12458, 12459, 12461, 12469, 12471, 12477, 12481, 12494,
    # #               12499, 12509, 12514, 12515, 12521, 12523, 12526, 12531, 12533, 12538, 12542, 12554, 12557, 12559,
    # #               12563, 12571, 12574, 12581, 12587, 12598, 12599, 12602, 12603, 12605, 12607, 12622, 12623, 12629,
    # #               12631, 12633, 12634, 12643, 12646, 12651, 12655, 12657, 12658, 12661, 12667, 12674, 12677, 12679,
    # #               12683, 12686, 12687, 12693, 12695, 12701, 12706, 12707, 12709, 12715, 12718, 12722, 12723, 12729,
    # #               12731, 12734, 12737, 12745, 12746, 12751, 12755, 12758, 12759, 12761, 12767, 12769, 12773, 12777,
    # #               12778, 12779, 12783, 12785, 12787, 12793, 12794, 12797, 12811, 12813, 12817, 12819, 12827, 12833,
    # #               12839, 12842, 12847, 12849, 12851, 12854, 12863, 12867, 12869, 12871, 12877, 12881, 12883, 12891,
    # #               12895, 12898, 12902, 12913, 12929, 12931, 12937, 12938, 12946, 12949, 12955, 12961, 12962, 12965,
    # #               12977, 12981, 12982, 12989, 12991, 12997, 13011, 13017, 13019, 13021, 13027, 13031, 13042, 13045,
    # #               13047, 13051, 13057, 13058, 13061, 13067, 13069, 13071, 13073, 13081, 13085, 13087, 13089, 13094,
    # #               13097, 13102, 13105, 13106, 13111, 13117, 13119, 13123, 13126, 13129, 13133, 13138, 13139, 13141,
    # #               13142, 13153, 13154, 13157, 13162, 13165, 13169, 13173, 13191, 13193, 13198, 13199, 13201, 13207,
    # #               13211, 13213, 13214, 13223, 13227, 13231, 13235, 13238, 13247, 13253, 13261, 13263, 13269, 13271,
    # #               13273, 13274, 13283, 13285, 13289, 13295, 13301, 13303, 13306, 13307, 13315, 13318, 13319, 13322,
    # #               13323, 13333, 13341, 13343, 13346, 13349, 13353, 13355, 13358, 13361, 13369, 13371, 13373, 13378,
    # #               13379, 13382, 13385, 13387, 13389, 13391, 13393, 13402, 13403, 13406, 13415, 13418, 13423, 13427,
    # #               13429, 13435, 13438, 13439, 13443, 13445, 13449, 13453, 13459, 13465, 13466, 13471, 13474, 13479,
    # #               13483, 13493, 13495, 13501, 13507, 13511, 13517, 13519, 13521, 13522, 13526, 13529, 13531, 13535,
    # #               13539, 13541, 13543, 13549, 13551, 13555, 13557, 13558, 13561, 13562, 13565, 13569, 13571, 13579,
    # #               13582, 13586, 13589, 13595, 13603, 13606, 13607, 13609, 13621, 13631, 13637, 13639, 13641, 13643,
    # #               13645, 13646, 13647, 13654, 13655, 13657, 13658, 13661, 13663, 13666, 13667, 13682, 13683, 13701,
    # #               13703, 13705, 13714, 13726, 13733, 13738, 13739, 13742, 13745, 13747, 13749, 13753, 13765, 13766,
    # #               13771, 13773, 13777, 13787, 13791, 13793, 13798, 13801, 13809, 13811, 13813, 13814, 13817, 13819,
    # #               13822, 13823, 13834, 13835, 13837, 13843, 13847, 13849, 13853, 13861, 13863, 13885, 13891, 13894,
    # #               13897, 13898, 13909, 13911, 13917, 13918, 13919, 13922, 13927, 13929, 13934, 13939, 13942, 13943,
    # #               13945, 13947, 13951, 13953, 13954, 13955, 13957, 13961, 13966, 13969, 13971, 13973, 13979, 13982,
    # #               13985, 13987, 13989, 13991, 13993, 13994, 14002, 14005, 14015, 14017, 14019, 14021, 14023, 14026,
    # #               14037, 14038, 14039, 14041, 14047, 14054, 14059, 14069, 14073, 14077, 14078, 14086, 14089, 14093,
    # #               14095, 14099, 14101, 14109, 14111, 14113, 14114, 14117, 14119, 14123, 14129, 14131, 14137, 14138,
    # #               14141, 14158, 14163, 14165, 14167, 14169, 14171, 14179, 14183, 14185, 14187, 14189, 14191, 14199,
    # #               14201, 14203, 14206, 14209, 14213, 14215, 14218, 14219, 14227, 14233, 14237, 14239, 14242, 14253,
    # #               14254, 14255, 14257, 14258, 14261, 14263, 14267, 14269, 14273, 14277, 14279, 14285, 14291, 14299,
    # #               14302, 14305, 14309, 14311, 14317, 14318, 14333, 14339, 14349, 14351, 14353, 14354, 14359, 14361,
    # #               14363, 14367, 14371, 14374, 14377, 14379, 14381, 14383, 14386, 14393, 14395, 14397, 14403, 14414,
    # #               14417, 14422, 14426, 14429, 14435, 14438, 14439, 14441, 14451, 14453, 14458, 14459, 14471, 14473,
    # #               14474, 14477, 14483, 14485, 14486, 14491, 14493, 14494, 14501, 14506, 14507, 14509, 14513, 14515,
    # #               14521, 14527, 14531, 14545, 14566, 14567, 14569, 14579, 14581, 14583, 14585, 14587, 14594, 14597,
    # #               14599, 14603, 14609, 14611, 14613, 14614, 14617, 14618, 14623, 14631, 14635, 14642, 14647, 14659,
    # #               14662, 14666, 14667, 14671, 14677, 14681, 14687, 14689, 14693, 14695, 14698, 14701, 14702, 14709,
    # #               14711, 14719, 14727, 14738, 14743, 14757, 14761, 14765, 14777, 14785, 14786, 14789, 14791, 14793,
    # #               14799, 14803, 14809, 14811, 14815, 14822, 14829, 14834, 14837, 14845, 14849, 14853, 14855, 14857,
    # #               14863, 14866, 14871, 14873, 14881, 14893, 14899, 14901, 14902, 14903, 14907, 14909, 14914, 14917,
    # #               14918, 14919, 14921, 14933, 14941, 14953, 14954, 14959, 14961, 14962, 14963, 14971, 14974, 14977,
    # #               14978, 14979, 14981, 14987, 14989, 14995, 14997, 14998, 14999, 15001, 15005, 15007, 15009, 15011,
    # #               15014, 15019, 15023, 15027, 15033, 15034, 15037, 15046, 15047, 15049, 15055, 15058, 15063, 15069,
    # #               15071, 15074, 15079, 15082, 15089, 15094, 15095, 15097, 15098, 15103, 15109, 15115, 15117, 15118,
    # #               15119, 15122, 15127, 15133, 15143, 15146, 15151, 15153, 15154, 15157, 15163, 15166, 15167, 15177,
    # #               15178, 15179, 15182, 15185, 15191, 15203, 15205, 15206, 15209, 15214, 15221, 15223, 15229, 15231,
    # #               15242, 15243, 15245, 15247, 15251, 15253, 15261, 15278, 15286, 15293, 15297, 15298, 15303, 15305,
    # #               15311, 15321, 15335, 15338, 15339, 15343, 15346, 15347, 15353, 15357, 15362, 15371, 15374, 15382,
    # #               15389, 15395, 15397, 15398, 15403, 15406, 15409, 15415, 15419, 15421, 15431, 15434, 15437, 15441,
    # #               15445, 15446, 15449, 15454, 15459, 15469, 15479, 15481, 15482, 15487, 15491, 15499, 15501, 15503,
    # #               15506, 15509, 15513, 15514, 15517, 15518, 15529, 15537, 15539, 15545, 15547, 15553, 15557, 15563,
    # #               15567, 15571, 15577, 15578, 15586, 15591]
    # # _min ,_min_sp= np.inf, None
    # # for sp in semiprimes:
    # #     try:
    # #         p_dict, q_dict, z_dict, clauses = create_clauses(sp)
    # #         free_p_keys=list(filter(lambda x: not isinstance([x], int), p_dict))
    # #         free_q_keys=list(filter(lambda x: not isinstance([x], int), q_dict))
    # #         free_z_keys=list(filter(lambda x: not isinstance([x], int), z_dict))
    # #         if _min > len(free_z_keys)+len(free_q_keys)+len(free_p_keys):
    # #             _min=len(free_z_keys)+len(free_q_keys)+len(free_p_keys)
    # #             _min_sp=sp
    # #     except Exception as e:
    # #         pass
    # # print(sp)