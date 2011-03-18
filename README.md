correction_completion plugin for weechat
========================================

### Usage:
If you want to correct yourself, you often do this using the
expression 's/typo/correct'. This plugin allows you to complete the
first part (the typo) by pressing <Tab>. The words from the actual
buffer are used to complet this part. If the word can be perfectly
matched the next word in alphabetical order is shown.


The second part (the correction) can also be completed. Just press
<Tab> and the best correction for the typo is fetched from aspell.
If you press <Tab> again, it shows the next suggestion. The lanuage
used for suggestions can be set over

  plugins.var.python.correction_completion.lang

The aspell language pack must be installed for this language.

### Setup:
Add the template %(correction_completion) to the default completion template
