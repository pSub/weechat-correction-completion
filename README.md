correction_completion plugin for weechat
========================================

Usage:
------
If you want to correct yourself, you often do this using the
expression 's/typo/correct'. This plugin allows you to complete the
first part (the typo) by pressing <Tab>. The words from the actual
buffer are used to complet this part. If the word can be perfectly
matched the next word in alphabetical order is shown.

Setup:
------
Add the template %(correction_completion) to the default completion template
