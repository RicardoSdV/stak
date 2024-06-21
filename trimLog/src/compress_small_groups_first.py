from typing import List

from src.compression_format_list import CompressionFormatList


def compress(post_pass_cfl: CompressionFormatList) -> CompressionFormatList:
    represents = post_pass_cfl.rep

    for group_size in range(1, len(post_pass_cfl) // 2):

        pre_pass_cfl = post_pass_cfl
        post_pass_cfl = CompressionFormatList(cnt=pre_pass_cfl.cnt, rep=pre_pass_cfl.rep)

        this_group_start_i = 0
        this_group_end_i = group_size - 1

        next_group_start_i = group_size
        next_group_end_i = 2 * group_size - 1

        this_group: List[str] = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
        next_group: List[str] = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

        groups_cnt = 1

        while this_group:

            if this_group == next_group:
                groups_cnt += 1

                next_group_start_i += group_size
                next_group_end_i += group_size

            else:
                if groups_cnt == 1:
                    post_pass_cfl.append(this_group[0])

                    this_group_start_i += 1
                    this_group_end_i += 1

                    next_group_start_i += 1
                    next_group_end_i += 1

                else:  # There has been one or more repetitions of this_group

                    compressed_group = CompressionFormatList(this_group, cnt=groups_cnt, rep=represents)
                    post_pass_cfl.append(compressed_group)

                    this_group_start_i = next_group_start_i
                    this_group_end_i = next_group_end_i

                    next_group_start_i += group_size
                    next_group_end_i += group_size

                    groups_cnt = 1

            this_group = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
            next_group = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

    return post_pass_cfl
