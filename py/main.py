import LRtable

before_depth = 0

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def print_tree(self, depth=0): # parsing tree 출력
        global before_depth
        if (depth == 0): connect = ''
        elif(before_depth == depth): connect = '  '
        else: connect = '└─'
        print('   ' * depth + connect + self.value) # 트리의 깊이 만큼 탭
        for child in self.children:
            child.print_tree(depth + 1)
        before_depth = depth

    def get_tree_string(self, depth=0): # output.txt에 저장할 형식
        global before_depth
        if (depth == 0): connect = ''
        elif(before_depth == depth): connect = '  '
        else: connect = '└─'
        for child in self.children:
            result += child.get_tree_string(depth + 1)
        before_depth = depth
        return result

stack=[0] #states stack
stack_str=[] #The left-hand of Indicator(already checked)
indicator=-1

# For reducing, needs to have the nonterminal to be reduced and the length of reduced tokens
reduce_len=[1,2,1,0,2,2,2,2,3,1,1,1,1,2,3,0,2,3,0,3,1,1,9,3,0,4,0,2,0,1,2,8,7,3,1,4,0,3]
reduced_nonterminal=['S','CODE','CODE','CODE','CODE\'','VDECL','VDECL\'','VDECL\'','ASSIGN','RHS','RHS','RHS','RHS','EXPR','EXPR\'','EXPR\'','TERM','TERM\'','TERM\'','FACTOR','FACTOR','FACTOR','FDECL','ARG','ARG','MOREARGS','MOREARGS','BLOCK','BLOCK','STMT','STMT','STMT','STMT','COND','COND','ELSE','ELSE','RETURN']
current_reduced_nonterminal=[]

# input.txt에서 불러오게 선언
with open("input.txt", "r") as file:
    input_tokens = file.read().strip().split()
input_tokens.append("$")

# 트리 구성위한 변수 선언
parsing_tree = None
nodes_stack = []

#SLR Parser
while (1):
    currentstate=stack[-1]

    if current_reduced_nonterminal:
        #Goto Case
        val=None

        #If Goto table is not viewable, Error.
        try:
            val=LRtable.Goto[currentstate][current_reduced_nonterminal.pop()]
            nextstate=int(val)
        except:
            print("Goto Failed")
            print(*stack_str, end='')
            print(" | ", end='')
            print(*input_tokens[indicator+1:])
            break
        stack.append(nextstate)
    else:
        #Shift & Goto or Reduce case
        val=None
        # If Action table is not viewable, Error.
        try:
            val=LRtable.Action[currentstate][input_tokens[indicator+1]]
            val[0] # val을 참조했을 때 공백인지 확인
        except:
            print("Shift & Goto Failed")
            print(*stack_str, end='')
            print(" | ", end='')
            print(*input_tokens[indicator+1:])
            break
        
        if val=="acc":
            #Successed Case
            print("Successed!")
            parsing_tree = nodes_stack[0] if nodes_stack else None # parsing tree 제대로 구성됐는지 파악
            break
        if val[0]=='s':
            #Shift & Goto Case
            nextstate=int(val[1:])
            indicator+=1
            stack.append(nextstate)
            stack_str.append(input_tokens[indicator])
            nodes_stack.append(TreeNode(input_tokens[indicator])) # 자식 노드 구성위해 shift, goto시 스택에 저장
        else:
            #Reduce Case
            nextstate=int(val[1:])
            #Checks follow condition
            if not (input_tokens[indicator+1] in LRtable.Follow[reduced_nonterminal[nextstate]]):
                print("Reduced Failed")
                print(*stack_str, end='')
                print(" | ", end='')
                print(*input_tokens[indicator+1:])
                break
            
            children = [] # 서브트리 생성

            # Reducing for the length of reduced tokens

            for _ in range(reduce_len[nextstate]):
                stack.pop()
                stack_str.pop()
                children.append(nodes_stack.pop())

            children.reverse() # 정확한 자식노드 구성을 위해 리버스
            parent = TreeNode(reduced_nonterminal[nextstate])
            for child in children:
                parent.add_child(child)

            # After reducing, needs to execute Goto.

            current_reduced_nonterminal.append(reduced_nonterminal[nextstate])
            stack_str.append(reduced_nonterminal[nextstate])   
            # 서브트리 생성 완료
            nodes_stack.append(parent) 

    #Printing current processing
    print("Stack: ",end='')
    print(*stack)
    print("LHS of indicator: ",end='')
    print(*stack_str)
    print()

print()

# parsing tree output파일에 저장
try:
    with open("output.txt", "w") as f:
        f.write(parsing_tree.get_tree_string())
except:
    print("Parsing tree save error")

# parsing tree 출력
try:
    print("Parsing Tree")
    parsing_tree.print_tree()
except:
    print("Parsing tree print error")

print("The \"output.txt\" is updated")