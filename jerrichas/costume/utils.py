# Jerrichas by Jerricha@chat.cohtitan.com, Summer 2015!
# GPLv3


def clamp_scales(value):
    """
    :param value: value to be clamped
    :return: clamps value between -1.0 and 1.0
    """
    return max(min(value, 1.0), -1.0)


def is_clamped(value):
    """
    :param value: value to be checked for clampedness
    :return: true if value between -1.0 and 1.0
    """
    return -1 < value < 1


def signum(value):
    """
    :param value: value to be evaluated for sign
    :return: signum; 1 if value positive, -1 if value negative, 0 if value is 0
    """
    return value and (1, -1)[value < 0]


def int32(x):
    """
    :param x: an integer
    :return: cast x into a 32-bit signed integer
    """
    if x > 0xFFFFFFFF:
        raise OverflowError
    if x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
    if x < 2147483648:
        return -x
    else:
        return -2147483648
    return x


def encode_colour(colour_vals):
    """
    :param colour_vals: list of three decimal integers clamped between 0~255
    :return: a colour string in format "rrggbbaa", where aa is 'ff' and all alphabetical numbers are lower case,
            converted to a 32-bit signed int in little endian
    """
    assert (colour_vals.__len__() == 3)
    colour_vals = [int(colour) for colour in colour_vals]
    for colour in colour_vals:
        assert (0 <= colour <= 255)
    as_string = 'ff' + format(colour_vals[2], 'x') + format(colour_vals[1], 'x') + format(colour_vals[0], 'x')
    return int32(int(as_string, 16))


def floats_to_int(scales):
    """
    :param scales: list of floats clamped between 1.0 ~ -1.0
    :return: integer per ParagonChat db schema
    """
    assert (scales.__len__() == 3)
    scales = [float(scale) for scale in scales]
    if scales[0] == 0 and scales[1] == 0 and scales[2] == 0:
        return 0

    result = 0
    result += int(abs(scales[0] * 100)) | 0x80 \
        if signum(scales[0]) == -1 \
        else int(abs(scales[0] * 100)) | 0
    result += (int(abs(scales[1] * 100)) | 0x80) << 8 \
        if signum(scales[1]) == -1 \
        else (int(abs(scales[1] * 100)) | 0) << 8
    result += (int(abs(scales[2] * 100)) | 0x80) << 16 \
        if signum(scales[2]) == -1 \
        else (int(abs(scales[2] * 100)) | 0) << 16
    return result


def int_to_floats(value):
    """
    :param value: integer representing three floats clamped between 1.0 ~ -1.0
    :return: list of decomposed floats
    """
    results = [0.0, 0.0, 0.0]
    if value == 0:
        return results

    results[0] = (value & 0xFF) / 100.0 \
        if is_clamped((value & 0xFF) / 100) \
        else (value & 0x7F) / -100.0
    results[1] = ((value >> 8) & 0xFF) / 100.0 \
        if is_clamped(((value >> 8) & 0xFF) / 100) \
        else ((value >> 8) & 0x7F) / -100.0
    results[2] = ((value >> 16) & 0xFF) / 100.0 \
        if is_clamped(((value >> 16) & 0xFF) / 100) \
        else ((value >> 16) & 0x7F) / -100.0
    return results
