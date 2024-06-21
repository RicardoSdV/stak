"""
Run this file to run the log trimmer.

log_dir_path -> Paste the absolute path to the dir where the logs to be trimmed can be found
                all .log files in this dir will be found recursively and trimmed.

force_retrim -> When force_retrim is False log files that don't have a trimmed version are trimmed,
                log file is considered trimmed when its name starts with 't_'. But if
                force_retrim is True, then all logs than don't start with 't_' will be trimmed.


"""
from src.run import run

""" =================== SETTINGS ================== """

force_retrim = True
log_dir_path = r'/logs_dir_example'

""" =============================================== """


run(
    force_retrim=force_retrim,
    log_dir_path=log_dir_path,
)
