#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by nirm03
# Copyright (c) 2013 nirm03
#
# License: MIT
#

"""This module exports the Clang plugin class."""

import shlex
from SublimeLinter.lint import Linter, persist
import sublime
import os

class Clang(Linter):

    """Provides an interface to clang."""

    syntax = ('c', 'c improved', 'c++')
    executable = 'clang'

    # We are missing out on some errors by ignoring multiline messages.
    regex = (
        r'^<stdin>:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>(error|fatal error))|(?P<warning>warning)): '
        r'(?P<message>.+)'
    )

    defaults = {
        'include_dirs': [],
        'extra_flags': ""
    }

    base_cmd = (
        'clang -cc1 -fsyntax-only '
        '-fno-caret-diagnostics -fcxx-exceptions -Wall '
    )

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra flags and include paths
        based on the 'include_dirs' and 'extra_flags' settings.

        """

        result = self.base_cmd

        if persist.get_syntax(self.view) == 'c++':
            result += ' -x c++ '

        settings = self.get_view_settings()
        result += settings.get('extra_flags', '')

        include_dirs = settings.get('include_dirs', [])

        # make include paths relative to project file (if it exitst)
        proj_file = sublime.active_window().project_file_name()
        if proj_file:
            src_path = os.path.dirname(self.filename)
            proj_path = os.path.dirname(proj_file)
            rel_path = os.path.relpath(proj_path, src_path)
            include_dirs = [os.path.join(rel_path, i) for i in include_dirs]

        if include_dirs:
            result += ' '.join([' -I ' + shlex.quote(include) for include in include_dirs])

        return result
