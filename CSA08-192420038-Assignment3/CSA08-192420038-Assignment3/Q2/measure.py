"""Q2 - memory and time: list vs tuple of 1,000,000 values; dictionary grid vs list-of-lists grid."""
import sys, time, timeit

N = 1_000_000
data = list(range(N))
lst, tup = data, tuple(data)
print(f"sys.getsizeof(list of {N:,}) = {sys.getsizeof(lst):,} bytes")
print(f"sys.getsizeof(tuple of {N:,}) = {sys.getsizeof(tup):,} bytes   (difference {sys.getsizeof(lst)-sys.getsizeof(tup):,} bytes)")
print("(both only count the pointer array; the int objects are shared)")
e = list(range(0)); print("empty list", sys.getsizeof([]), "bytes, empty tuple", sys.getsizeof(()), "bytes")

t_list = timeit.timeit(lambda: list(range(N)), number=5) / 5
t_tup = timeit.timeit(lambda: tuple(range(N)), number=5) / 5
print(f"\ncreate list of {N:,}: {t_list*1000:7.2f} ms    create tuple: {t_tup*1000:7.2f} ms")
t_il = timeit.timeit(lambda: lst[500000], number=2_000_000)
t_it = timeit.timeit(lambda: tup[500000], number=2_000_000)
print(f"index list x 2,000,000: {t_il:.3f} s    index tuple x 2,000,000: {t_it:.3f} s")

# small constant tuples are created at compile time
a = timeit.timeit("(1, 2, 3, 4)", number=2_000_000); b = timeit.timeit("[1, 2, 3, 4]", number=2_000_000)
print(f"literal (1,2,3,4) x 2,000,000: {a:.3f} s    literal [1,2,3,4]: {b:.3f} s")

# ----- alternative: dictionary grid with only non-empty zones -----
print("\nZone grid: list of lists vs dict keyed by (row, col) holding only non-empty zones")
print(f"{'rows x cols':>12} {'non-empty':>10} {'list grid bytes':>16} {'dict grid bytes':>16} {'t list access ns':>17} {'t dict access ns':>17}")
for rows, cols, k in [(10, 10, 5), (100, 100, 50), (1000, 1000, 500)]:
    grid = [[0] * cols for _ in range(rows)]
    d = {}
    for i in range(k):
        r, c = (i * 7) % rows, (i * 13) % cols
        grid[r][c] += 1
        d[(r, c)] = d.get((r, c), 0) + 1
    size_list = sys.getsizeof(grid) + sum(sys.getsizeof(r) for r in grid)
    size_dict = sys.getsizeof(d)
    n = 1_000_000
    tl = timeit.timeit(lambda: grid[5][5], number=n) / n * 1e9
    td = timeit.timeit(lambda: d.get((5, 5), 0), number=n) / n * 1e9
    print(f"{rows:>5}x{cols:<6} {k:>10} {size_list:>16,} {size_dict:>16,} {tl:>17.1f} {td:>17.1f}")
