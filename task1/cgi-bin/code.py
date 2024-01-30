#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb

cgitb.enable()

print("Content-type: text/html\n")

form = cgi.FieldStorage()

def get_form_value(field_name):
    if field_name in form:
        return form[field_name].value
    else:
        return None

favorite_color = get_form_value("favorite_color")
music_genre = get_form_value("music_genre")
like_coffee = get_form_value("like_coffee")

print("<html>")
print("<head>")
print("<title>Result</title>")
print("</head>")
print("<body>")

print("<h2>Result:</h2>")
print("<p><strong>Favorite Color: </strong> {0}</p>".format(favorite_color))
print("<p><strong>Music Genre:</strong> {0}</p>".format(music_genre))

if like_coffee:
    print("<p><strong>You like coffee! :D</strong></p>")
else:
    print("<p><strong>You do not like coffee :(</strong></p>")

print("</body>")
print("</html>")
