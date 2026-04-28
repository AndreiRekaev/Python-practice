def get_entrance_and_floor(flat_no, flats_on_floor, floors):
    floors_before = (flat_no - 1) // flats_on_floor
    entrance = floors_before // floors + 1
    floor = floors_before % floors + 1
    return entrance, floor

def check(K1, M, K2, P2, N2, flats_on_floor):
    ent2, floor2 = get_entrance_and_floor(K2, flats_on_floor, M)
    if ent2 == P2 and floor2 == N2:
        return get_entrance_and_floor(K1, flats_on_floor, M)
    return -1, -1



def solve(K1, M, K2, P2, N2):

    ent = -1
    floor = -1
    good_flag = False

    for flats_on_floor in range(1, 10**6 + 1):
        n_ent, n_floor = check(K1, M, K2, P2, N2, flats_on_floor)
        if n_ent != -1:
            good_flag = True
            if ent == -1:
                ent, floor = n_ent, n_floor
            elif ent != n_ent and ent != 0:
                ent = 0
            elif floor != n_floor and floor != 0:
                floor = 0

    if good_flag:
        print(ent, floor)
    else:
        print(-1, -1)


K1, M, K2, P2, N2 = map(int, input().split())
solve(K1, M, K2, P2, N2)