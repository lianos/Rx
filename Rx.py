import sublime
import sublime_plugin
import os
import subprocess
import string
import re

## This file started its life as Rtools.py
## https://github.com/karthikram/Rtools/blob/master/Rtools.py

rx_settings = sublime.load_settings('Rx.sublime-settings')
r_scope_regex = rx_settings.get('r_scope_regex')
r_scope_regex = re.compile(r_scope_regex)
rapp = rx_settings.get('Rapp')

class SendToRsessionCommand(sublime_plugin.TextCommand):
    @staticmethod
    def cleanString(str):
        str = string.replace(str, '\\', '\\\\')
        str = string.replace(str, '"', '\\"')
        return str

    def is_r_scope(self, region):
        # Check if the cursor / selection is in an R source scope
        # Using region.begin() instead of region.b for the case when
        # you are in a highlighted region/block. The curor can be at
        # the 0 column of a new line which you don't want to execute
        # but this will be out of R scope, eg. imagine the block is
        # highlighted and the cursor is at ^, this might be out of
        # source.r scope::
        #
        #    ```{r}
        #    a <- 1:10
        #    b <- 1:10
        #    plot(a,b)
        #    ^```
        scope = self.view.scope_name(region.begin())
        return r_scope_regex.search(scope) is not None

    def run(self, edit):
        # Split the selection into new lines allows us to highlight a chunk
        # of lines that might not all fall into a source.r scope, but still
        # evaluate the ones that do.
        original_region = self.view.sel()[0]            # info to restore orig
        is_single_select = len(self.view.sel()) == 1    # block selection
        self.view.run_command('split_selection_into_lines')
        regions = [x for x in self.view.sel()]

        if not any([self.is_r_scope(x) for x in regions]):
            # No selections in block are scoped as R cdoe, move along
            self.advanceCursor(regions[-1])
            return

        # Collate the R code across selection(s)
        selection = ""
        for region in regions:
            if not self.is_r_scope(region):
                continue
            if region.empty():
                selection += self.view.substr(self.view.line(region)) + "\n"
                self.advanceCursor(region)
            else:
                selection += self.view.substr(region) + "\n"

        selection = (selection[::-1].replace('\n'[::-1], '', 1))[::-1]
        if selection == "":
            # An empty R block somehow slipped through.
            return

        # split selection into lines
        selection = self.cleanString(selection).split("\n")
        # define osascript arguments
        args = ['osascript']
        # add code lines to list of arguments
        for part in selection:
            args.extend(['-e', 'tell app "%s" to cmd "' % rapp + part + '"\n'])
        # execute code
        subprocess.Popen(args)

        if is_single_select and not original_region.empty():
            # Reverses side effect from our `split_selection_into_lines` trick
            # when a selection was passed into this function
            self.view.sel().clear()
            self.view.sel().add(original_region)

    def advanceCursor(self, region):
        (row, col) = self.view.rowcol(region.begin())
        # Make sure not to go past end of next line
        nextline = self.view.line(self.view.text_point(row + 1, 0))
        if nextline.size() < col:
            loc = self.view.text_point(row + 1, nextline.size())
        else:
            loc = self.view.text_point(row + 1, col)
        # Remove the old region and add the new one
        self.view.sel().subtract(region)
        self.view.sel().add(sublime.Region(loc, loc))

class JumpToRsessionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        args = ['osascript', '-e', 'tell app "R64" to activate\n']
        subprocess.Popen(args)

class RoxyDocsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pass

# class RDocsCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         sel = self.view.sel()[0]
#
#         params_reg = self.view.find('(?<=\().*(?=\))', sel.begin())
#         params_txt = self.view.substr(params_reg)
#         params = params_txt.split(',')
#
#         snippet = "#'<brief desc>\n#'\n#'<full description>\n"
#
#         for p in params:
#             snippet += "#' @param %s <what param does>\n" % p
#
#         snippet += "#' @export\n#' @keywords\n#' @seealso\n#' @return\n#' @alias\n#' @examples \dontrun{\n#'\n#'}\n"
#
#         self.view.insert(edit, sel.begin(), snippet)



