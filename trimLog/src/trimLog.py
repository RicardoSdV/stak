"""
Deprecated: Only here to use commented out code as inspiration





"""
from time import time

from path_ops import compress, CompressionFormatList, pretty_fmt_cfl_lines

start_time = time()

from pathlib import Path


""" =================== SETTINGS ================== """

force_retrim = True
log_dir_path = Path(r'/logs_dir_example')

""" =============================================== """

log_paths = log_dir_path.glob('**/*.log')

for log_path in log_paths:

    """ ======================= INIT STUFF ======================= """

    if log_path.name.startswith('t_'): continue
    trimmed_log_path = log_path.with_name('t_' + log_path.name)
    if trimmed_log_path.exists() and not force_retrim: continue

    with open(log_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < 1: continue

    """ =========================================================== """


    """ ==================================== Compress lines ===================================== """
    if not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    cfl_lines = compress(CompressionFormatList(lines, rep='lines'))

    """ ========================================================================================= """

    """ =================================== Compress frames in lines ================================ """

    # fmt_cmp_lines_for_frame_cmp(cmp_lines)

    """ ============================================================================================= """


    """ =================== Compressing with multiple passes when a group of lines repeats ========================= """

    #
    # indent = '    '
    # max_group_size = 100
    # post_pass_lines = lines
    #
    # for group_size in range(max_group_size, 0, -1):
    #
    #     pre_pass_lines = post_pass_lines
    #     post_pass_lines = []
    #
    #     this_group_start_i = 0
    #     this_group_end_i = group_size - 1
    #
    #     next_group_start_i = group_size
    #     next_group_end_i = 2 * group_size - 1
    #
    #     this_group = pre_pass_lines[this_group_start_i: this_group_end_i + 1]
    #     next_group = pre_pass_lines[next_group_start_i: next_group_end_i + 1]
    #
    #     groups_cnt = 1
    #
    #     while this_group:
    #
    #         if this_group == next_group:
    #             groups_cnt += 1
    #
    #             next_group_start_i += group_size
    #             next_group_end_i += group_size
    #
    #         else:
    #             if groups_cnt == 1:
    #                 post_pass_lines.append(this_group[0])
    #
    #                 this_group_start_i += 1
    #                 this_group_end_i += 1
    #
    #                 next_group_start_i += 1
    #                 next_group_end_i += 1
    #
    #             else:
    #
    #                 prev_indent = re.match(r'^ *', this_group[0]).group(0)
    #                 post_pass_lines.append(f'{prev_indent}{groups_cnt}x\n')
    #                 for line in this_group:
    #                     post_pass_lines.append(f'{indent}{line}')
    #
    #                 this_group_start_i = next_group_start_i
    #                 this_group_end_i = next_group_end_i
    #
    #                 next_group_start_i += group_size
    #                 next_group_end_i += group_size
    #
    #                 groups_cnt = 1
    #
    #
    #         this_group = pre_pass_lines[this_group_start_i: this_group_end_i + 1]
    #         next_group = pre_pass_lines[next_group_start_i: next_group_end_i + 1]
    #
    # lines = post_pass_lines

    """=============================================================================================================="""

    """ ============= Compressing with multiple passes when a group of frames in the call stack repeats ============ """
    #
    # max_group_size = 3
    # post_pass_lines = lines
    #
    # for line in lines:
    #
    #     if ' <- ' not in line:
    #         post_pass_lines.append(line)
    #         continue
    #
    #     post_pass_frames = line.strip().split(' <- ')
    #
    #     for group_size in range(max_group_size, 0, -1):
    #
    #         pre_pass_frames = post_pass_frames
    #         post_pass_frames = []
    #
    #         this_group_start_i = 0
    #         this_group_end_i = group_size - 1
    #
    #         next_group_start_i = group_size
    #         next_group_end_i = 2 * group_size - 1
    #
    #         this_group = pre_pass_frames[this_group_start_i: this_group_end_i + 1]
    #         next_group = pre_pass_frames[next_group_start_i: next_group_end_i + 1]
    #
    #         groups_cnt = 1
    #
    #         while this_group:
    #             if this_group == next_group:
    #                 groups_cnt += 1
    #
    #                 next_group_start_i += group_size
    #                 next_group_end_i += group_size
    #             else:
    #                 if groups_cnt == 1:
    #                     post_pass_frames.append(this_group[0])
    #
    #                     this_group_start_i += 1
    #                     this_group_end_i += 1
    #
    #                     next_group_start_i += 1
    #                     next_group_end_i += 1
    #
    #                 else:
    #
    #                     prev_indent = re.match(r'^ *', this_group[0]).group(0)
    #                     post_pass_frames.append(f'{prev_indent}{groups_cnt}x\n')
    #                     for frame in this_group:
    #                         post_pass_frames.append(f'{prev_indent}{frame}')
    #
    #                     this_group_start_i = next_group_start_i
    #                     this_group_end_i = next_group_end_i
    #
    #                     next_group_start_i += group_size
    #                     next_group_end_i += group_size
    #
    #                     groups_cnt = 1
    #
    #             this_group = pre_pass_frames[this_group_start_i: this_group_end_i + 1]
    #             next_group = pre_pass_frames[next_group_start_i: next_group_end_i + 1]
    #
    #     post_pass_lines.append(post_pass_frames)
    #
    # lines = post_pass_lines




    # post_pass_lines = []
    # for line in lines:
    #     if ' <- ' not in line: post_pass_lines.append(line); continue
    #     num_start, x_next, space_next = False, False, False; chars = []; line = line.strip()
    #     for char in line:
    #         if char in nums and not x_next and not space_next: num_start = True
    #         elif num_start and char == 'x' and not x_next and not space_next: x_next = True
    #         elif x_next and char == ' ' and not space_next: space_next = True
    #         else: break
    #         chars.append(char)
    #
    #     repeats_marker = ''.join(chars) if num_start and x_next and space_next else ''
    #     line = line[len(repeats_marker):]; frames = line.split(' <- '); post_pass_frames = frames
    #
    #     for group_size in range(1, max_group_size + 1):
    #         pre_pass_frames = post_pass_frames; post_pass_frames = []
    #         prev_group = pre_pass_frames[0: group_size]; cnt = 1
    #         for i in range(group_size, len(pre_pass_frames) + group_size, group_size):
    #             group = pre_pass_frames[i: i + group_size]
    #             if group == prev_group: cnt += 1
    #             else:
    #                 if cnt > 1: post_pass_frames.append(f'{cnt}x[{" <- ".join(prev_group)}]')
    #                 else: post_pass_frames.extend(prev_group)
    #                 cnt = 1; prev_group = group
    #     post_pass_lines.append(f'{repeats_marker}{" <- ".join(post_pass_frames)}\n')
    # lines = post_pass_lines

    """ ============================================================================================================ """

    """ ======================= Save lines to new file ======================= """

    pretty_lines = pretty_fmt_cfl_lines(cfl_lines)

    with open(trimmed_log_path, 'w') as f:
        f.writelines(pretty_lines)

    """ ======================================================================= """


print('Done trimming, took:', time() - start_time)
