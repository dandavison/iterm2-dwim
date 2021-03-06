``iterm2-dwim`` is a click handler for iTerm2. The aim is that you
command-click on any file path, relative or absolute, and it opens the
file in your editor. If there was a line number, your editor goes to
that line. So, compiler/linter output, tracebacks, git output, etc.

Currently Emacs, PyCharm, VS Code and Sublime are supported. To choose which
editor to use, see ``settings.py``.

The following path-like patterns are supported. For the ones with line
numbers, the file will be opened at that line.

+---------------------------------------------------------------+--------------------------------+----------+
| Pattern                                                       | Type                           | Status   |
+===============================================================+================================+==========+
| ``/absolute/path/to/file``                                    | Absolute path                  | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+
| ``relative/path/to/file``                                     | Relative path                  | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+
| ``relative/path/to/file:336:1:``                              | Compiler / Linter etc output   | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+
| ``a/relative/path/to/file``                                   | In git diff output             | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+
| ``"/absolute/path/to/file.py", line 336, in some_function``   | Python stack traces            | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+
| ``> /path/to/file.py(336)some_function()``                    | Python ipdb output             | ✅       |
+---------------------------------------------------------------+--------------------------------+----------+

Installation
~~~~~~~~~~~~

1. Clone this repo and run ``python setup.py develop``.

2. In ``settings.py``, set the absolute path to the command-line utility
   that opens files in youe text editor / IDE. For PyCharm this is
   called ``charm``, for Sublime this is called ``subl`` and for Emacs
   this is called ``emacsclient``.

3. Find the absolute path to the ``iterm2-dwim`` executable, by running
   the command ``which iterm2-dwim``. For example, on my system, this is
   ``/usr/local/bin/iterm2-dwim``.

4. Open iTerm2 settings, click on "Profiles", select your profile, click
   on the "Advanced" tab for that profile, and do two things:

5. In the "Smart Selection" section, click "Edit", click "+" to add a new rule, and enter the
   following values in the 3 rule fields:

   - Notes: ``Compiler/Linter output``
   - Regular Expression: ``(\~?/?([[:letter:][:number:]._-]+/+)+[[:letter:][:number:]._-]+/?)(:.+)``
   - Precision: ``Very High``

   Now click "Edit Actions", click "+" to add an action, choose "Run
   Command" and enter ``/absolute/path/to/iterm2-dwim \1 \3`` as the
   "Parameter".

6. In the "Semantic History" section, choose "Run command" and enter
   ``/absolute/path/to/iterm2-dwim \1 \4``.

7. Make sure you didn't literally enter ``/absolute/path/to/`` anywhere!
   The path should be the path from step (3), given by ``which iterm2-dwim``.

8. (Optional, but relative paths won't be resolved without it):
   configure your shell prompt so that the current directory is written
   to a file named ``/tmp/cwd`` every time the prompt is displayed. For
   example, put this line in your ``~/.bashrc``:

   .. code:: sh

       export PROMPT_COMMAND='echo $PWD > /tmp/cwd'

9. ⌘-click on things!

Your iTerm2 settings should look something like this:

Optional configuration
^^^^^^^^^^^^^^^^^^^^^^

1. To get error message alerts, run ``brew install terminal-notifier``
   and check it's working with ``terminal-notifier -message hello``.

**For Emacs users:**

1. Make sure that you are starting the emacs server
in your emacs config file:

   .. code:: emacs-lisp

       (require 'server)
       (unless (server-running-p) (server-start))

Debugging
~~~~~~~~~

This is under development and you will encounter problems initially.
Probably, you'll command click on something and nothing will happen.

You can't use ``ipdb`` to debug it: the python process is started by
iTerm2 and is not attached to your terminal's standard input/output.
Similarly, note that the python process inherits its environment from
the iTerm2 process and thus does not have access to environment
modifications made in your shell config file.

It writes a log: run ``tail -f /tmp/iterm2-dwim.log``.

If nothing happens and nothing is written to the log, another trick is
just to run it from the command line and see the traceback:

::

    $ iterm2-dwim /some/file.py 'the text that comes after the file path'
