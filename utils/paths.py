from pathlib import Path
import inspect


def get_py_path(verbose=False):
    # return Path(globals()['_dh'][0]) if globals().get('_dh') else Path(__file__)
    env = inspect.currentframe().f_back.f_locals
    if ((not env.get('_dh')) and (not env.get('__file__'))):
        env = inspect.currentframe().f_back.f_back.f_locals
    if env.get('_dh'):
        if verbose:
            print('==ipython shell==')
        if env.get('__file__'):
            return Path(env["_dh"][0], env["__file__"]).resolve().parent

        if verbose:
            print('<File.py>: NOT FOUND!')
            print('Next time run with:\n  ipython -i -- <File.py>')
            print('using cwd()')
        return Path(env["_dh"][0])
    if verbose:
        print(f'env = {env}')
    return Path(env["__file__"]).resolve().parent
