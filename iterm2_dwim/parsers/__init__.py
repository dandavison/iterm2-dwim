import os

from iterm2_dwim.logger import log
from iterm2_dwim.parsers.parsers import PARSERS
from iterm2_dwim.parsers.parsers import ParseError


def get_path_and_line(path_text, extra_text):
    for parse_fn in PARSERS:
        log(parse_fn.__name__)
        try:
            path, line = parse_fn(path_text, extra_text)
        except ParseError as ex:
            continue
        else:
            if os.path.exists(path):
                return path, line

    assert os.path.exists(path_text), 'No such file: %s' % path_text

    return path_text, 1
