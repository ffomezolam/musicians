""" opts.py
-----------
Helpers for setting and getting options
"""

from typing import Optional

def setopts(dest: dict, src: Optional[dict|str] = None, val: Optional[str] = None):
    """
    Set instance options

    Parameters
    ----------
    dest: dict
        The options dictionary to be altered (e.g. the defaults)
    src: [dict|str]
        Dict of options to set or, with second parameter, the key of an option to set
    val: [str]
        With string argument to opts, the value to set to the key
    """

    if dest and src:
        if type(src) == dict:
            for k, v in src.items():
                if k in dest: dest[k] = v
        elif val:
            k, v = src, val
            if k in dest: dest[k] = v

    return dest

def getopts(opts: dict, opt: Optional[str] = None):
    """
    Get instance options

    Parameters
    ----------
    opts dict
        The options dictionary
    opt: [str]
        If specified, get the value associated with this option key.
        Otherwise, return full dict of options.
    """

    if not opt: return opts

    return opts.get(opt, None)

class OptsMixin():
    """
    Mixin class for allowing opt setting and getting
    """

    def __init__(self, default_opts: dict = {}):
        self._opts = default_opts.copy() # make a fresh copy of defaults

    def setopts(self, opts: Optional[dict|str] = {}, val: Optional[str] = None):
        """
        Set instance options

        Parameters
        ----------
        opts: [dict|str]
            dict of options to set or, with second parameter, the key of an option to set
        val: [str]
            with string argument to opts, the value to set to the key
        """

        self._opts = setopts(self._opts, opts, val)

        return self

    def getopts(self, opt: Optional[str] = None):
        """
        Get instance options

        Parameters
        ----------
        opt: [str]
            If specified, get the value associated with this option key.
            Otherwise, return full dict of options.
        """

        return getopts(self._opts, opt)
