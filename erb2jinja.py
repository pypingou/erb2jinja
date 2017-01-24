#!/usr/bin/env python2

"""
This script takes one or more files as input and converts them to jinja2
templates.

Usage
python erb2jinja.py <file> [<file2>...]
"""


def main(filename):
    """ Main method doing the conversion from erb to jinja2. """


    space_dict = {
        "<%if": "<% if",
        "<%for": "<% for",
        "<%else":"<% else",
        "else%>":"else %>",
        "<%end":"<% end",
        "end%>":"end %>",
    }

    output = []
    with open(filename) as stream:
        IF = False
        FOR = False
        for row in stream.readlines():
            # Add spaces in case they are not there
            for key in space_dict:
                row = row.replace(key, space_dict[key])

            if "<%=" in row:
                row = row.replace("<%= @", "{{ ")
                row = row.replace("<%=", "{{")
                row = row.replace("%>", "}}")
            elif "<% if" in row:
                row = row.replace("<% if", "{% if ")
                row = row.replace("%>", "%}")
                IF = True
            elif "<% for " in row:
                row = row.replace("<% for", "{% for ")
                row = row.replace("%>", "%}")
                FOR = True
            elif "<% else %>" in row:
                row = row.replace("<% else %>", "{% else %}")
            elif "<% end %>" in row:
                if IF is True:
                    row = row.replace("<% end %>", "{% endif %}")
                    IF = False
                elif FOR is True:
                    row = row.replace("<% end %>", "{% endfor %}")
                    FOR = False
            output.append(row)

    print "".join(output)
    with open(filename + ".j2", "w") as stream:
        stream.write("".join(output))


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        print 'Usage: python erb2jinja.py <file> [<file2>...]'
        sys.exit(1)

    for filename in sys.argv[1:]:
        main(filename)
