#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import http.cookies
import os

cgitb.enable()

form = cgi.FieldStorage()

delete_cookies = form.getvalue("delete_cookies")
if delete_cookies:
    print("Set-Cookie: form_counter=0")
    form_counter_from_cookie = 0
else:
    cookies = http.cookies.SimpleCookie()
    if "HTTP_COOKIE" in os.environ:
        cookies.load(os.environ["HTTP_COOKIE"])

    form_counter_cookie = cookies.get("form_counter")
    if form_counter_cookie:
        form_counter = int(form_counter_cookie.value)
    else:
        form_counter = 0

    form_counter += 1

    cookies["form_counter"] = form_counter

    print("Set-Cookie: form_counter={}".format(form_counter))

    form_counter_from_cookie = form_counter

print("Content-type: text/html\n")

def get_form_value(field_name):
    if field_name in form:
        return form[field_name].value
    else:
        return None

print("<html>")
print("<head>")
print("<title>Result</title>")
print("</head>")
print("<body>")

print("<h2>Result:</h2>")
print("<p><strong>Favorite music genre:</strong> {0}</p>".format(get_form_value("music_genre")))
print("<p><strong>Do you like coffee?</strong> {0}</p>".format("Yes" if get_form_value("like_coffee") else "No"))
print("<p><strong>Favorite color:</strong> {0}</p>".format(get_form_value("favorite_color")))

print("<p><strong>Form count:</strong> {0}</p>".format(form_counter_from_cookie))

print('<form action="/cgi-bin/code.py" method="post">')
print('<input type="hidden" name="delete_cookies" value="true">')
print('<input type="submit" value="Delete cookies">')
print('</form>')

print("</body>")
print("</html>")
