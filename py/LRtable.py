import csv


#Transforms LR table, Goto table and Follow table into the dictionary

''' Be careful When changing the contents '''

csv_action = open("Action_table.csv", "r", encoding="utf-8-sig")
csv_goto = open("Goto_table.csv", "r", encoding="utf-8-sig")
csv_follow = open("Follow_table.csv", "r", encoding="utf-8-sig")

Action=dict()
Goto=dict()
Follow=dict()

f = csv.DictReader(csv_action)
g= csv.DictReader(csv_goto)
e= csv.DictReader(csv_follow)

for row in f:
    State=int(row["State"])
    row.pop("State")
    Action[State]=row

for row in g:
    State=int(row["State"])
    row.pop("State")
    Goto[State]=row

for row in e:
    Follow[row['1']] = row['2'].rstrip('}').lstrip('{').split(',')