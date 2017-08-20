correction_completion plugin for weechat
========================================

### Usage:
If you want to correct yourself, you often do this using the
expression 's/typo/correct'. This plugin allows you to complete the
first part (the typo) by pressing *Tab*. The words from the actual
buffer are used to complet this part. If the word can be perfectly
matched the next word in alphabetical order is shown.

The second part (the correction) can also be completed. Just press
*Tab* after the slash and the best correction for the typo is fetched from aspell.
If you press *Tab* again, it shows the next suggestion.
The language used for suggestions can be set with the option

      plugins.var.python.correction_completion.lang

The aspell language pack must be installed for this language.

### Setup:
Add the template %(correction_completion) to the default completion template.
The best way to set the template is to use the [iset-plugin](http://weechat.org/scripts/source/stable/iset.pl/),
because you can see there the current value before changing it. Of course you can also use the
standard /set-command e.g.

      /set weechat.completion.default_template "%(nicks)|%(irc_channels)|%(correction_completion)"
