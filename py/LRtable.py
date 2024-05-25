import csv

# 확인을 위해 현재 작업 디렉터리를 출력

# Implement LR table as a dictionary
# state 0~85
state = 0

terminals=['vtype','id','semi','assign','literal','character','boolstr','addsub','multdiv','lparen','rparen','num','lbrace','rbrace','comma','if','while','comp','else','return','$']
nonterminals=['CODE','CODE\'','VDECL','VDECL\'','ASSIGN','RHS','EXPR','EXPR\'','TERM','TERM\'','FACTOR','FDECL','ARG','MOREARGS','BLCOK','STMT','IFSTMT','WHILESTMT','COND','COND\'','ELSE','RETURN']

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

