from multiprocessing import Pool
import numpy as np

# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.


def process_stone_chunk(stone_chunk: np.ndarray, iterations: int) -> np.ndarray:
    for _ in range(iterations):
        new_stones = []
        for stone in stone_chunk:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                num_digits = len(str(stone))
                divisor = 10 ** (num_digits // 2)
                new_stone1 = stone // divisor
                new_stone2 = stone % divisor
                new_stones.extend([new_stone1, new_stone2])
            else:
                new_stones.append(stone * 2024)
        stone_chunk = np.array(new_stones)
    return stone_chunk


def chunkify(lst, n):
    avg = len(lst) / float(n)
    out = []
    last = 0.0

    while last < len(lst):
        out.append(lst[int(last) : int(last + avg)])
        last += avg

    return out


if __name__ == "__main__":
    stones = "4610211 4 0 59 3907 201586 929 33750"
    # stones = "125 17"
    stones = np.array(list(map(int, stones.split(" "))))

    num_processes = 6  # Use the number of CPU cores
    iterations = 75

    chunks = chunkify(stones, num_processes)
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(
            process_stone_chunk, [(np.array(chunk), iterations) for chunk in chunks]
        )
    stones = np.concatenate(results)

    print(len(stones))
