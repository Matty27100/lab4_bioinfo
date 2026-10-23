import random

MIN_OVERLAP = 10


def split_genome(genome, a, b):
    if not MIN_OVERLAP < a <= b <= len(genome):
        raise ValueError("Required: 10 < a <= b <= genome length")

    fragments = []
    start = 0

    while len(genome) - start > b:
        length = random.randint(a, b)
        fragments.append(genome[start:start + length])
        start += length - MIN_OVERLAP

    length = random.randint(max(a, len(genome) - start), b)
    fragments.append(genome[-length:])
    random.shuffle(fragments)
    return fragments


def overlap(left, right):
    for length in range(min(len(left), len(right)), MIN_OVERLAP - 1, -1):
        if left.endswith(right[:length]):
            return length
    return 0


def rebuild_genome(fragments):
    fragments = list(dict.fromkeys(fragments))
    fragments = [x for x in fragments if not any(x != y and x in y for y in fragments)]

    if not fragments:
        raise ValueError("The collection is empty")

    while len(fragments) > 1:
        best = (0, 0, 0)

        for i, left in enumerate(fragments):
            for j, right in enumerate(fragments):
                if i != j:
                    length = overlap(left, right)
                    if length > best[2]:
                        best = (i, j, length)

        i, j, length = best
        if length < MIN_OVERLAP:
            raise ValueError("The fragments cannot be joined")

        merged = fragments[i] + fragments[j][length:]
        fragments = [x for k, x in enumerate(fragments) if k not in (i, j)]
        fragments.append(merged)

    return fragments[0]


if __name__ == "__main__":
    genome = "ATGCGTACGATTCGAGCTAAGGCATTCGTACCGATGACCTTAGCGTATGCAAGTCCGTTACGGATACGTCTACCTGAGGACTTACGCTAGGATCCAGTTACGATGGTACATCCGAGATGCCTAGGCTTACGTCACGATAGTCGATCCGAATGCCTAGTCA"
    a, b = 30, 50
    fragments = split_genome(genome, a, b)

    print("Subsequences:", fragments)
    print("Rebuilt genome:", rebuild_genome(fragments))
