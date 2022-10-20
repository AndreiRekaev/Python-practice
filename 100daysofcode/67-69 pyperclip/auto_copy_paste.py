import time
import sys
import os
import pyperclip

sys.path.append(os.path.abspath("SO_site-packages"))

recent_value = ""

D = time.strftime("%D")
r = time.strftime("%r")

while True:
    tmp_value = pyperclip.paste()
    if tmp_value != recent_value:
        recent_value = tmp_value
        print("Value changed: %s" % str(recent_value)[:20])
        with open('out_clipboard.txt', '+a') as output:
            try:
                output.write("---------------"+D+" "+r+"---------------\n")
                output.write("%s\n\n" % str(tmp_value))
                output.write("---------------------------------------------\n\n\n")
            except:
                output.write("---------------" + D + " " + r + "---------------\n")
                output.write("%s\n\n" % str(tmp_value.encode('UTF-8')))
                output.write("---------------------------------------------\n\n\n")
    time.sleep(0.1)
