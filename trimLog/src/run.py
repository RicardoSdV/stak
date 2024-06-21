"""
This is the develop run file, the one used to compress the logs in the log_dir_example during development

Ideas:
    - Sometimes one is printing the callstack of every callable in the callstack of the most stackfull. In such case it
    would be interesting to compress all that into one call stack, e.g. This makes sense in combination with STACK

    Untrimmed:
    callerOfCaller
    callerOfCalled <- callerOfCaller
    called <- callerOfCalled <- callerOfCaller

    Trimmed:
    called <- callerOfCalled <- callerOfCaller

    - Sometimes there's multiple methods of one class or functions from one file called sequentially in the callstack
    In this case they might be compressed by writing the class/file name only once followed by the callables names,
    with some sort of new syntax or old syntax

    - For those times were the timestamps might be useful there could be an option to take them out, compress, and then
    put them back in.

    - Don't compress white space nor empty lines

    - Find some new pretty printing structure, which occupies less space


Known Issues:
    - The both compression algos produce "artefacts" see: src/compress_big_groups_first.py & src/compress_small_groups_first.py

"""
from src.compress_small_groups_first import compress
from src.compression_format_list import CompressionRecursive, CompressionFormatList
from src.format import remove_datetime_and_log_type_prefixes_from_lines_in_place, format_lines_for_lines_compression, \
    format_line_for_callstack_comp
from src.path_ops import find_read_and_write_log_paths
from src.pretty import trav_lines_pretty_stack_in_place, prettyfy_lines


# TODO: Find a home for this func
def compress_stack_lines_by_trav_and_mod_in_place(cfl: CompressionRecursive) -> None:
    for i, el in enumerate(cfl):
        if isinstance(el, str):
            cfl[i] = compress(
                format_line_for_callstack_comp(el)
            )

        elif isinstance(el, CompressionFormatList) and el.rep == 'lines':
            compress_stack_lines_by_trav_and_mod_in_place(el)

        else:
            raise TypeError('Elements traversed in compress_stack_lines_by_trav_and_mod_in_place '
                            "should only be str or CompressionFormatList with cfl.rep == 'lines'")


def run(
        force_retrim: bool = True,
        log_dir_path: str = r'C:\prjs\trimLog_develop\logs_dir_example'
):
    log_paths = find_read_and_write_log_paths(force_retrim, log_dir_path)

    for read_path, write_path in log_paths:

        print('read_path, write_path', read_path, write_path)

        with open(read_path, 'r') as file:
            lines = file.readlines()
        if len(lines) < 1: continue

        remove_datetime_and_log_type_prefixes_from_lines_in_place(lines)

        lines_cfl = format_lines_for_lines_compression(lines)
        lines_cfl = compress(lines_cfl)

        compress_stack_lines_by_trav_and_mod_in_place(lines_cfl)
        trav_lines_pretty_stack_in_place(lines_cfl)

        pretty_lines = prettyfy_lines(lines_cfl)

        with open(write_path, 'w') as f:
            f.writelines(pretty_lines)


run()
