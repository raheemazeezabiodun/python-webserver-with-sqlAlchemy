def render_template(filename):
    open_file = open(filename, 'r')
    output = ""
    for x in open_file:
        output += x
    return output
