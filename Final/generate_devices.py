import random


txt = "["
for i in range(12):
    txt = txt + ("""["G""")
    txt = txt + (str(i + 1))
    txt = txt + ('''", "''')
    txt = txt + (str(i))
    txt = txt + ('''", "''')
    txt = txt + (str(random.randint(0, 5)))
    txt = txt + (""""], """)
print(txt[:-2] + "]")
