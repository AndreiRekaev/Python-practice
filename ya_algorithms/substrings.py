def solve():
    s = input().strip()

    max_cnt = 0
    max_letters = []
    for c in 'abcdefghijklmnopqrstuvwxyz':
        cnt = s.count(c)
        if cnt > max_cnt:
            max_cnt = cnt
            max_letters = [c]
        elif cnt == max_cnt:
            max_letters.append(c)

    ans = 1

    for letter in max_letters:
        positions = [i for i, ch in enumerate(s) if ch == letter]

        cur_len = 1
        while True:
            ok = True
            for pos in positions:
                if pos + cur_len >= len(s):
                    ok = False
                    break
                if s[pos + cur_len] != s[positions[0] + cur_len]:
                    ok = False
                    break
            if not ok:
                break
            cur_len += 1

        ans = max(ans, cur_len)

    print(ans)


if __name__ == "__main__":
    solve()