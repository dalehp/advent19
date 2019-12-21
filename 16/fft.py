from itertools import cycle, islice
from typing import Dict, Iterable, List, Optional

def coefficients(pos: int) -> Iterable[int]:
    coef_pattern = cycle((0, 1, 0, -1))
    skip_first = True
    
    for x in coef_pattern:
        for i in range(pos + 1):
            if skip_first:
                skip_first = False
                continue
            yield x

def fft(signal: List[int]) -> List[int]:
    output: List[int] = []
    for i in range(len(signal)):
        res = sum(x * y for x, y in zip(signal, coefficients(i)))
        output.append(abs(res) % 10)
    return output

def fft_quick(signal_list: List[int]) -> List[int]:
    # Approimation valid for positions at least halfway through signal
    output: List[int] = []
    for pos in range(len(signal_list) - 1, -1, -1):
        added = output[-1] if output else 0
        output.append((signal_list[pos] + added) % 10)
    output.reverse()
    return output

def get_signal(signal: List[int], pos: int) -> int:
    return signal[pos % len(signal)]


if __name__ == "__main__":
    with open("input.txt") as f:
        signal = [int(x) for x in f.read().strip()]

    offset = int(''.join(str(s) for s in signal[:7]))
    len_signal = len(signal) * 10000
    
    signal_list = [get_signal(signal, pos) for pos in range(offset, len_signal)]

    for i in range(100):
        signal_list = fft_quick(signal_list)
    print(signal_list[:8])
    print(''.join(str(s) for s in signal_list[:8]))