# -*- coding: utf-8 -*-
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
#
# Marked Parts are from Wojciech Muła <wojciech_mula@poczta.onet.pl>
# and are licensed under BSD and are avaliable at
# http://0x80.pl/proj/aspell-python/
########################################################################

import ctypes
import ctypes.util

try:
    import weechat as w
    WEECHAT_RC_OK = w.WEECHAT_RC_OK
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: http://www.weechat.org/"

SCRIPT_NAME    = "correction_completion"
SCRIPT_AUTHOR  = "Pascal Wittmann <mail@pascal-wittmann.de>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Provides a completion for 's/typo/correct'"
SCRIPT_COMMAND = "correction_completion"

# Default Options
settings = {
        'lang' : 'en',
}

def completion(data, completion_item, buffer, completion):
    # Current cursor position
    pos = w.buffer_get_integer(buffer, 'input_pos')

    # Current input string
    input = w.buffer_get_string(buffer, 'input')

    # Check for correct cursor position for completion
    if pos > 2 and input.find("s/") < pos:
        complete_typo(pos, input, buffer)
        return WEECHAT_RC_OK
    return WEECHAT_RC_OK

def complete_typo(pos, input, buffer):
    # Get the text of the current buffer
    list = []
    infolist = w.infolist_get('buffer_lines', buffer, '');
    while w.infolist_next(infolist):
        list.append(stripcolor(w.infolist_string(infolist, 'message')))

    # Generate a list of words
    text = (' '.join(list)).split(' ')

    # Remove duplicate elements
    text = unify(text)

    # Sort by alphabet and lenght
    text.sort(key=lambda item: (item, -len(item)))
    
    i = iter(text)
    
    # Get index of last occurence of "s/" befor cursor position
    n = input.rfind("s/", 0, pos)

    # Get substring and search the replacement
    substr = input[n+2:pos]
    replace = search((lambda word : word.startswith(substr)), i)
    
    # If no replacement found, display substring
    if replace == "":
      replace = substr
    
    # If substring perfectly matched take next replacement
    if replace == substr:
      try:
        replace = next(i)
      except StopIteration:
        pass

    # Put the replacement into the input
    n = len(substr)
    input = '%s%s%s' %(input[:pos-n], replace, input[pos:])
    w.buffer_set(buffer, 'input', input)
    w.buffer_set(buffer, 'input_pos', str(pos - n + len(replace)))

def stripcolor(string):
    return w.string_remove_color(string, '')

def search(p, i):
    while True:
      try:
        item = next(i)
        if p(item):
          return item
      except StopIteration:
        return ""

def unify(list):
    checked = []
    for e in list:
      if e not in checked:
        checked.append(e)
    return checked

# Parts are from Wojciech Muła
def suggest(word):
    if type(word) is str:
      suggestions = aspell.aspell_speller_suggest(
                      speller,
                      word.encode(),
                      len(word))
      elements = aspell.aspell_word_list_elements(suggestions)
      list = []
      while True:
          wordptr = aspell.aspell_string_enumeration_next(elements)
          if not wordptr:
              break;
          else:
              word = ctypes.c_char_p(wordptr)
              list.append(str(word.value))
      aspell.delete_aspell_string_enumeration(elements)
      return list
    else:
      raise TypeError("String expected")

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    aspell = ctypes.CDLL(ctypes.util.find_library('aspell'))
    config = aspell.new_aspell_config()

    for option, default in settings.iteritems():
        if not w.config_is_set_plugin(option):
          w.config_set_plugin(option, default)
        value = w.config_get_plugin(option)
        if not aspell.aspell_config_replace(
                        config, 
                        option.encode(), 
                        value.encode()):
          raise Exception("Failed to replace config entry")

    # Error checking is from Wojciech Muła
    possible_error = aspell.new_aspell_speller(config)
    aspell.delete_aspell_config(config)
    if aspell.aspell_error_number(possible_error) != 0:
      aspell.delete_aspell_can_have_error(possible_error)
      raise Exception("Couldn't create speller")
    speller = aspell.to_aspell_speller(possible_error)

    template = 'correction_completion'
    w.hook_completion(template, "Completes after 's/' with words from buffer",
            'completion', '')
    w.hook_command(SCRIPT_COMMAND, SCRIPT_DESC, "",
"""Usage:
If you want to correct yourself, you often do this using the
expression 's/typo/correct'. This plugin allows you to complete the
first part (the typo) by pressing <Tab>. The words from the actual
buffer are used to complet this part. If the word can be perfectly
matched the next word in alphabetical order is shown.

Setup:
Add the template %%(%(completion)s) to the default completion template"""
%dict(completion=template), '', '', '')
