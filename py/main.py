import LRtable

input_tokens=[]
stack=[0] #states stack
stack_str=[] #The lefthand of Indicator
indicator=-1 
reduce_len=[1,2,1,0,2,2,2,2,3,1,1,1,1,2,3,0,2,3,0,3,1,1,9,3,0,4,0,2,0,1,2,1,1,8,7,3,1,1,4,0,3]
reduced_nonterminal=['S','CODE','CODE','CODE','CODE\'','VDECL','VDECL\'','VDECL\'','ASSIGN','RHS','RHS','RHS','RHS','EXPR','EXPR\'','EXPR\'','TERM','TERM\'','TERM\'','FACTOR','FACTOR','FACTOR','FDECL','ARG','ARG','MOREARGS','MOREARGS','BLOCK','BLOCK','STMT','STMT','STMT','STMT','IFSTMT','WHILESTMT','COND','COND\'','COND','ELSE','ELSE','RETURN']
current_reduced_nonterminal=[]

input_tokens=input().strip().split()
input_tokens.append("$")


while (1):
    currnetstate=stack[-1]
    if current_reduced_nonterminal:
        #Goto Case
        val=None
        try:
            val=LRtable.Goto[currnetstate][current_reduced_nonterminal.pop()]
        except:
            print("Goto Failed")
            print(*stack_str, end='')
            print(" | ", end='')
            print(*input_tokens[indicator+1:])
            break

        nextstate=int(val)
        stack.append(nextstate)
    else:
        #Shift & Goto or Reduce
        val=None
        try:
            val=LRtable.Action[currnetstate][input_tokens[indicator+1]]
        except:
            print("Shift & Goto Failed")
            print(*stack_str, end='')
            print(" | ", end='')
            print(*input_tokens[indicator+1:])
            break
        
        if val=="acc":
            #Successed Case
            print("Successed!")
            break
        if val[0]=='s':
            #Shift & Goto Case
            nextstate=int(val[1:])
            indicator+=1
            stack.append(nextstate)
            stack_str.append(input_tokens[indicator])
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

            for _ in range(reduce_len[nextstate]):
                stack.pop()
                stack_str.pop()
            current_reduced_nonterminal.append(reduced_nonterminal[nextstate])
            stack_str.append(reduced_nonterminal[nextstate])    

    print(stack,stack_str)

