######################################################################
# Copyright (c) 2011 by Pascal Wittmann <mail@pascal-wittmann.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

try:
    import weechat as w
    WEECHAT_RC_OK = w.WEECHAT_RC_OK
    import_ok = True
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: http://www.weechat.org/"
    import_ok = False

SCRIPT_NAME    = "correction-completion"
SCRIPT_AUTHOR  = "Pascal Wittmann <mail@pascal-wittmann.de>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Provides a completion for s/typo/correct"
SCRIPT_COMMAND = "correction-completion"

def completion(data, completion_item, buffer, completion):
    list = []
    infolist = w.infolist_get('buffer_lines', buffer, '');
    while w.infolist_next(infolist):
        list.append(stripcolor(w.infolist_string(infolist, 'message')))
    text = (' '.join(list)).split(' ')

    pos = w.buffer_get_integer(buffer, 'input_pos')
    input = w.buffer_get_string(buffer, 'input')

    if pos > 0 and ("s/" in input):
        n = input.rfind("s/", 0, pos)
        substr = input[n+2:pos]
        replace = find((lambda word : word.startswith(substr)), text)
        if replace == "":
          replace = substr
        n = len(substr)
        input = '%s%s%s' %(input[:pos-n], replace, input[pos:])
        w.buffer_set(buffer, 'input', input)
        w.buffer_set(buffer, 'input_pos', str(pos - n + len(replace)))
    return WEECHAT_RC_OK

def stripcolor(string):
    return w.string_remove_color(string, '')

def find(p, list):
    for item in list:
      if p(item):
        return item
    return ""

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    template = 'correction_completion'
    w.hook_completion(template, "Completes after 's/' with words from buffer",
            'completion', '')
    w.hook_command(SCRIPT_COMMAND, SCRIPT_DESC, "",
                    """Setup: Add the template %%(%(completion)s) to the default completion template"""
                    %dict(completion=template),
                    '', '', '')
