import sublime, sublime_plugin, os,shlex, subprocess, tempfile
import merge_utils

def formatWholeFile(view, edit):
    region = sublime.Region(0, view.size())
    code = view.substr(region)
    newCode = format(code)
    view.replace(edit, sublime.Region(0, view.size()), newCode)

def format(code):
    #temp = tempfile.NamedTemporaryFile()
    temp = open('ffa.js','w') 
    temp.write(code)
    temp.seek(0)
    tempName = os.path.abspath(temp.name)
    temp.close()
    # if can't find node, should add ln like this:
    #   which node
    #   $ sudo ln -s [which node] /usr/bin/node
    fecs = '/usr/local/lib/node_modules/fecs/bin/fecs'

    cmd = '%s format %s --output=.' % (fecs,tempName)
    print cmd
    print os.popen(cmd).read()
    temp = file(tempName)
    newCode = temp.read()
    print newCode
    temp.close()
    os.remove(tempName)
    return newCode

class FormatByFecsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        if (len(sels) == 1 and len(sels[0]) == 0):
            # format whole file
            formatWholeFile(self.view, edit)
        else:
            # format selection
            for sel in sels:
                if (len(sel) > 0):
                    print self.view.substr(sel)

