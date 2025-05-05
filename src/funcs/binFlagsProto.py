flags = (
    'flag0',
    'flag1',
    'flag2',
    'flag3',
    'flag4',
    'flag5',
    'flag6',
    'flag7',
    'flag8',
    'flag9',
    'flag10',
)
# All flags -> 11 1111 1111 -> 1023
# No flags -> 0 -> 0
# Flag 2 only -> 100 -> 4



# Encode a set of flags into an integer bitmask
def encode_flags(flag_list):
    return sum(1 << flags.index(flag) for flag in flag_list)

# Decode an integer bitmask back into flag names
def decode_flags(bitmask):
    return [flags[i] for i in range(len(flags)) if bitmask & (1 << i)]

# Add a flag to the bitmask
def add_flag(bitmask, flag):
    return bitmask | (1 << flags.index(flag))

# Remove a flag from the bitmask
def remove_flag(bitmask, flag):
    return bitmask & ~(1 << flags.index(flag))

# # Examples
# bitmask = encode_flags(['flag2', 'flag4', 'flag7'])  # 132
# print(bin(bitmask))  # 0b10000100
#
# decoded = decode_flags(bitmask)
# print(decoded)  # ['flag2', 'flag4', 'flag7']
#
# bitmask = add_flag(bitmask, 'flag1')
# print(bin(bitmask))  # Now includes 'flag1'
#
# bitmask = remove_flag(bitmask, 'flag2')
# print(bin(bitmask))  # 'flag2' is removed


r1, r2, r3, r4 = 1<<0, 1<<1, 1<<2, 1<<3

def _set(reasons, bitVal, value):
    reasons = reasons | bitVal if value else reasons & ~bitVal
    print 'reasons', bin(reasons)
    return reasons

reasons = 0

reasons = _set(reasons, r1, 1)
reasons = _set(reasons, r1, 0)

reasons = _set(reasons, r1, 1)
reasons = _set(reasons, r2, 1)
reasons = _set(reasons, r3, 1)
reasons = _set(reasons, r4, 1)

reasons = _set(reasons, r1, 0)
reasons = _set(reasons, r2, 0)
reasons = _set(reasons, r3, 0)
reasons = _set(reasons, r4, 0)
