def setup(app):
    app.connect('autodoc-process-docstring', filter)

def filter(app, what, name, obj, options, lines):
    if what == 'module':
        lines.insert(1, '    ' + lines[0])
        lines[0] = '**' + name + '**'
