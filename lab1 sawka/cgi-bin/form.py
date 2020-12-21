#!/usr/bin/env python3
import os
import http.cookies
import cgi

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
count = cookie.get("count")
form = cgi.FieldStorage()
text1 = form.getfirst("name", "empty")
text2 = form.getfirst("secondname", "empty")



if form.getvalue('maths'):
   math_flag = "ON"
else:
   math_flag = "OFF"
if form.getvalue('physics'):
   physics_flag = "ON"
else:
   physics_flag = "OFF"

if form.getvalue('radio'):
	radio = form.getvalue('radio')
else:
	radio = "Not set"

if count is None:
  print("Set-Cookie: count+=1")
  print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Processing of data forms</title>
        </head>
        <body>""")

print("<h1>Processing of data forms!</h1>")
print("<p>name: {}</p>".format(text1))
print("<p>secondname: {}</p>".format(text2))
print("<p>Physics: {}</p>".format(math_flag))
print("<p>Maths: {}</p>".format(physics_flag))
print("<p>Point: {}</p>".format(radio))
print("<p>Cookies: {}</p>".format(5))

print("""</body> </html>""")
