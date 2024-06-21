import re
from typing import List

from src.compression_format_list import CompressionFormatList


def format_line_for_callstack_comp(line: str) -> CompressionFormatList:
    return CompressionFormatList(
        line.rstrip('\n').split(' <- '),
        rep='line'
    )


def remove_datetime_and_log_type_prefixes_from_lines_in_place(lines: List[str]) -> None:
    prefix_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3,4}): (DEBUG:|INFO:|WARNING:|ERROR:).*$"

    for i, line in enumerate(lines):
        match = re.match(prefix_pattern, line)
        if match:
            ymd, hour, minute, sec, msec, log_flag = match.groups()

            line = line.replace(
                '{}{}{}{}{}{}{}{}{}{}{}{}'.format(
                    ymd, ' ', hour, ':', minute, ':', sec, '.', msec, ': ', log_flag, ' '
                ), '')

            lines[i] = line


def format_lines_for_lines_compression(lines: List[str]) -> CompressionFormatList:
    if not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    return CompressionFormatList(lines, rep='lines')




