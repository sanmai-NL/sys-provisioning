from contextlib import contextmanager
from locale import getpreferredencoding
from logging import basicConfig, DEBUG, debug, error, getLogger, INFO, info, \
    StreamHandler
from subprocess import CalledProcessError, PIPE, run
from time import sleep
from traceback import print_exc


def sh_cmd(*args, check: bool=True, shell: bool=True, stderr=PIPE, **kwargs):
    debug(args[0])
    return run(*args, check=check, shell=shell, stderr=stderr, **kwargs)


@contextmanager
def provision(debug: bool=True, log_file_path: str='/build.log'):
    try:
        try:
            basicConfig(
                level=DEBUG,
                format='%(asctime)-15s %(funcName)s %(levelname)s %(message)s',
                filename=log_file_path)
            console = StreamHandler()
            console.setLevel(INFO)
            getLogger().addHandler(console)

            info('Building container image ...')

            yield
        except CalledProcessError as exc:
            error('A subprocess errored. Standard error output: ' +
                  exc.stderr.decode(encoding=getpreferredencoding(False)))
            raise
    except:
        if debug:
            print_exc()
            error(
                'Exception occurred. Sleeping to help debugging inside container. ')
            sleep(100000)
        else:
            raise
