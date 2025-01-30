a = {}
a["wa"] = 3
a["wo"] = 3
for i in a:
    i = a[i]
    print(i)
del a["wa"]
del a["wfawa"]
for i in a:
    i = a[i]
    print(i)