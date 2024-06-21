"""
CompressionFormatList inherits from list with two extra attrs:
    - cnt: Which holds the number of repetitions of itself it represents
    - rep: A string represents the type of data the list holds for easy formatting after compression

compress() algo receives an uncompressed CompressionFormatList and recursively compresses it, producing a nested
CompressionFormatList in such way:

Pass 0: [A, A, A, A, B, A, A, B, C] is a CompressionFormatList of strs
Pass 1: [A, A, A, A, B, A, A, B, C] group_size is 4, bc len = 9 & 9 // 2 = 4 so nothing happens bc no groups found
Pass 2: [A, A, [A, A, B], C] group_size -= 1 so is 3, one group is found it is compressed
Pass 3: [A, A, [[A] B], C] the group found in the previous stage compressed recursively
Pass 4: [A, A, [[A] B], C] Recursion finished, we're back, group size is 2, no groups found
Pass 4: [[A], [[A], B], C] Finally group size 1 another group found

The cnts:
    result.cnt = 1
    result[0].cnt = 2
    result[1].cnt = 2
    result[1][0].cnt = 2
    result[2].cnt = AttributeError: 'str' object has no attribute 'cnt'


Known problems:

    - It will always prefer longer patterns over short ones, for example:
    A, A, A, A, A, A
    Will be compressed into:
    2, 3A
    Which does make sense because its two groups of three As, but it's not a readable way of compressing logs.

    Solution:
        - Do a second pass and try to remove such wierd patters which is partially achieved by remove_redundant, but
        only partially

"""
from typing import Union, TypeAlias

from src.compression_format_list import CompressionFormatList


def compress(cfl: CompressionFormatList) -> CompressionFormatList:
    post_pass_cfl = cfl
    max_group_size = len(cfl) // 2
    for group_size in range(max_group_size, 0, -1):

        pre_pass_cfl = post_pass_cfl
        post_pass_cfl = CompressionFormatList(cnt=pre_pass_cfl.cnt, rep=cfl.rep)

        this_group_start_i, this_group_end_i = 0, group_size - 1
        next_group_start_i, next_group_end_i = group_size, 2 * group_size - 1

        this_group = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
        next_group = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

        groups_cnt = 1
        while this_group:

            if this_group == next_group:
                groups_cnt += 1
                next_group_start_i += group_size
                next_group_end_i += group_size

            elif groups_cnt == 1:
                post_pass_cfl.append(this_group[0])
                this_group_start_i += 1
                this_group_end_i += 1
                next_group_start_i += 1
                next_group_end_i += 1

            else:  # There are two or more of this_group

                # Recursively compress the found group
                cfl_group = CompressionFormatList(this_group, cnt=groups_cnt, rep=cfl.rep)
                compressed_group = compress(cfl_group)
                post_pass_cfl.append(compressed_group)

                # next_group is the first set of strings which is not inside the compressed
                # group, therefore it becomes this_group and the process restarts.
                this_group_start_i, this_group_end_i = next_group_start_i, next_group_end_i
                next_group_start_i += group_size
                next_group_end_i += group_size
                groups_cnt = 1

            this_group = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
            next_group = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

    return post_pass_cfl




def remove_redundant(cfl: CompressionFormatList, result: CompressionFormatList) -> CompressionFormatList:
    """ Does not actually work as expected, cant remember why"""

    for el in cfl:
        if isinstance(el, CompressionFormatList):
            el = remove_redundant(el, CompressionFormatList(cnt=el.cnt, rep=el.rep))

            len_cfl = len(el)
            if len_cfl == 1:
                inner_el = el[0]
                if isinstance(inner_el, CompressionFormatList):
                    # Here we have found a CompressionFormatList (el) which contains only one other of its kind
                    # (inner_el) therefore, these two cfls can be further compressed into one.
                    # This is done by substituting the outer list for the inner cfl, with an updated cnt.
                    inner_el.cnt *= el.cnt
                    result.append(inner_el)

                elif isinstance(inner_el, str):
                    result.append(el)
                else:
                    raise TypeError('A CompressionRecursive should only contain strings and CompressionFormatLists')

            elif len_cfl > 1:  # No possibility of deredundification
                result.append(el)
            else:
                ValueError('Inappropriate length of a CompressionFormatList:', len_cfl)

        elif isinstance(el, str):
            result.append(el)
        else:
            raise TypeError('A CompressionRecursive should only contain strings and CompressionFormatLists')

    return result































# end
