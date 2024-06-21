from typing import List

from src.compression_format_list import CompressionFormatList, CompressionRecursive

INDENT_STR = '    '



def trav_lines_pretty_stack_in_place(lines_cfl: CompressionRecursive) -> None:
    for i, el in enumerate(lines_cfl):
        if isinstance(el, CompressionFormatList):
            if el.rep == 'line':
                lines_cfl[i] = prettyfy_line(el).rstrip(' <- ') + '\n'
            elif el.rep == 'lines':
                trav_lines_pretty_stack_in_place(el)
            else:
                raise TypeError("At the moment of writing this error there was only "
                                "two types of CompressionFormatList: 'line' & 'lines'")
        else:
            raise TypeError('In trav_lines_mod_cs_lines_in_place for loop there should only be CompressionFormatLists')


def prettyfy_line(line_cfl: CompressionRecursive) -> str:
    result = ''

    if line_cfl.cnt > 1:
        result += f'{line_cfl.cnt}x['

    for el in line_cfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'line'
            result += prettyfy_line(el)
        elif isinstance(el, str):
            result += (el + ' <- ')
        else:
            raise TypeError('Wrong type in compressed stack: type(el)', type(el))

    if line_cfl.cnt > 1:
        result = result.rstrip(' <- ')
        result += (']' + ' <- ')

    return result


def prettyfy_lines(lines_cfl: CompressionRecursive, depth: int = 0) -> List[str]:
    indent = depth * INDENT_STR
    result = []

    if lines_cfl.cnt > 1:
        result.append(f'{(depth-1) * INDENT_STR}{lines_cfl.cnt}x\n')

    for el in lines_cfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'lines'
            result.extend(prettyfy_lines(el, depth + 1))
        elif isinstance(el, str):
            result.append(f'{indent}{el}')
        else:
            raise TypeError('Wrong type in compressed list: type(el)', type(el))
    return result



