import dateutil.parser as dparser

dt_1 = '2021-02-08T13:08:53-05:00'
dt_2 = '2021-02-08T13:08:53-00:00'

print(dparser.parse(dt_1, fuzzy=True))
print(dparser.parse(dt_2, fuzzy=True))