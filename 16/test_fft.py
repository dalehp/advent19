from fft import coefficients, coefficient_i, fft, fft_quick, get_signal

from itertools import islice

def test_coefficient_i():
    pos = 15
    expected = list(islice(coefficients(pos), 0, 100))
    actual = [coefficient_i(pos, i) for i in range(100)]
    assert actual == expected

def test_get_signal():
    signal = [0, 1, 2, 3, 4]
    assert get_signal(signal, 6) == 1

def test_fft_quick():
    signal = [1, 5, 6, 2, 4, 3]
    expected = [1, 0, 5, 9, 7, 3]
    assert fft_quick(signal) == expected
