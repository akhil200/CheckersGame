##########################
# 2015B4A7PS0631P
##########################
import sys
import copy
import random
sys.setrecursionlimit(1000)
class myState(object):
    """docstring for myState"""
    def __init__(self, matrix = [[-1,-1,0,-1,0,-1,0,-1,0,-1,-1],
                                 [-1,0 ,-1,0,-1,0,-1,0,-1,0,-1],
                                 [0,-1,0,-1,0,-1,0,-1,0,-1,0],
                                 [-1,0,-1,0,-1,0,-1,0,-1,0,-1],
                                 [-1,-1,0,-1,0,-1,0,-1,0,-1,-1]], player = 2, utility = 0):
        self.matrix = matrix 
        self.player = player
       #self.utility = utility 

    def __eq__(self, other):
        return self.matrix == other.matrix and self.player == other.player

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.matrix)

    def __hash__(self):
        return hash(tuple([tuple(x) for x in self.matrix]))

    def count_coins(self, player_num):
        count = 0
        if player_num == 1:
            for i in range(0,5):
                for j in range(0,11):
                    if self.matrix[i][j] == 1: 
                        count += 1
        else:
            for i in range(0,5):
                for j in range(0,11):
                    if self.matrix[i][j] == 2: 
                        count += 1
        return count
   
    def initial_state_generator(self):
        foo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        dict={0:[0,2],1:[0,4],2:[0,6],3:[0,8],4:[1,1],5:[1,3],6:[1,5],7:[1,7],8:[1,9],9:[2,0],10:[2,2],11:[2,4],12:[2,6],
              13:[2,8],14:[2,10],15:[3,1],16:[3,3],17:[3,5],18:[3,7],19:[3,9],20:[4,2],21:[4,4],22:[4,6],23:[4,8]}
        for i in range(0,10):
            r1=random.choice(foo)
            i=dict[r1][0]
            j=dict[r1][1]
            self.matrix[i][j]=1
            foo.remove(r1)
            r2=random.choice(foo)
            i=dict[r2][0]
            j=dict[r2][1]
            self.matrix[i][j]=2
            foo.remove(r2)
        return self            
    
    def safetomove(self,i,j):
        if(i>=0 and i<=4 and j>=0 and j<=10):
            if(self.matrix[i][j]!=-1 and self.matrix[i][j]==0):
                return True
        return False
    def opposite(self,i,j,k):
        if(k==1):
            if(self.matrix[i][j]==2):
                return True
            return False
        if(k==2):
            if(self.matrix[i][j]==1):
                return True
            return False
    def findpos(self,i):
        pos=[]
        for l in range(0,5):
            for m in range(0,11):
                if(self.matrix[l][m]==i):
                    pos.append((l,m))
        return pos
    def action(state):
        dx1=[-1,-1,0,1,1,0]
        dy1=[-1,1,2,1,-1,-2]
        dx2=[-2,-2,0,2,2,0]
        dy2=[-2,2,4,2,-2,-4]
        action_list=[]
        posone=state.findpos(1)
        for i,j in posone:
            for l in range(0,6):
                    if(state.safetomove(i+dx1[l],j+dy1[l])):
                        action_list.append((i,j,i+dx1[l],j+dy1[l],1))     
            for l in range(0,6):
                    if(state.safetomove(i+dx2[l],j+dy2[l]) and state.opposite(i+dx1[l],j+dy1[l],1)):
                        action_list.append((i,j,i+dx2[l],j+dy2[l],2))              
        postwo=state.findpos(2)
        for i,j in postwo:
            for l in range(0,6):
                    if(state.safetomove(i+dx1[l],j+dy1[l])):
                        action_list.append((i,j,i+dx1[l],j+dy1[l],1))     
            for l in range(0,6):
                    if(state.safetomove(i+dx2[l],j+dy2[l]) and state.opposite(i+dx1[l],j+dy1[l],2)):
                        action_list.append((i,j,i+dx2[l],j+dy2[l],2))              
        return action_list
    
    def computemiddle(self,action):
        dx1=[-1,-1,0,1,1,0]
        dy1=[-1,1,2,1,-1,-2]
        dx2=[-2,-2,0,2,2,0]
        dy2=[-2,2,4,2,-2,-4]
        for l in range(0,6):
            if(action[0]+dx2[l]==action[2] and action[1]+dy2[l]==action[3]):
                return action[0]+dx1[l],action[1]+dy1[l]
    def change_player(self):
        if self.player == 1:
            return 2
        else:
            return 1            
    def next_state(self,action):
        temp=copy.deepcopy(self.matrix)
        action=tuple(action)
        temp[action[2]][action[3]]=temp[action[0]][action[1]]
        temp[action[0]][action[1]]=0
        if(action[4]==2):
            i,j=self.computemiddle(action)
            temp[i][j]=0
        new_state=myState(matrix=temp,player=self.change_player())
        return new_state            
def terminal_test(state):
        human_coins=state.count_coins(1)
        bot_coins=state.count_coins(2)
        if(human_coins == 0 or bot_coins == 0):
            return True
        return False
def utility_value(state):
       return state.count_coins(2)-state.count_coins(1)  
        
def successor_function(state):
    action_list=state.action()
    if len(action_list)==0:
        return []
    statelist=[]
    for action in action_list:
        statelist.append(state.next_state(action))
    return statelist           

def minimax_decision(state):
    action_list = state.action()
    num_nodes = 0
    depth_of_stack = 0
    util_values = {}
    explored = {}
    for action in action_list:
        temp = state.next_state(action)
        if temp is not None:
            num_nodes += 1
            util_values[action], temp_num_nodes, temp_depth_of_stack = min_value(temp, explored, depth_of_stack)
            if depth_of_stack < temp_depth_of_stack:
                depth_of_stack = temp_depth_of_stack
               
            num_nodes += temp_num_nodes   
        if (depth_of_stack>8):
            break             
    print("Bot computation complete")
    max_val =-100
    action = -1
    for i in util_values:
       if(max_val<util_values[i]):
           max_val=util_values[i]
           action=i
    return action, num_nodes, depth_of_stack

def min_value(state, explored, depth_of_stack):
    if(terminal_test(state)==True):
        return utility_value(state), 0, depth_of_stack
    num_nodes = 0
    depth_of_stack += 1
    #print("min_val:"+str(depth_of_stack))
    if (depth_of_stack>7):
        return utility_value(state),num_nodes, depth_of_stack
    v = 10
    action_list = state.action()
    util_values = []
    for action in action_list:
        temp = state.next_state(action)
        if temp is not None and temp not in explored:
            # print(temp)
            num_nodes += 1
            maxi, temp_num_nodes, garbage = max_value(temp, explored, depth_of_stack)
            num_nodes += temp_num_nodes
            util_values.append(maxi)
            explored[temp] = maxi
        elif temp is not None:
            num_nodes += 1
            util_values.append(explored[temp])
    min_val = min(util_values)
    if v < min_val:
        return v, num_nodes, depth_of_stack
    else:
        return min_val, num_nodes, depth_of_stack

def max_value(state, explored, depth_of_stack):
    if(terminal_test(state)==True):
        return utility_value(state), 0, depth_of_stack
    num_nodes = 0
    depth_of_stack += 1
    #print("max_val:"+str(depth_of_stack))
    if (depth_of_stack>7):
        return utility_value(state),num_nodes, depth_of_stack
    v = -15
    action_list = state.action()
    util_values = []
    for action in action_list:
        temp = state.next_state(action)
        if temp is not None and temp not in explored:
            num_nodes += 1
            mini, temp_num_nodes, garbage = min_value(temp, explored, depth_of_stack)
            num_nodes += temp_num_nodes
            util_values.append(mini)
            explored[temp] = mini
        elif temp is not None:
            num_nodes += 1
            util_values.append(explored[temp])
    if(len(util_values)!=0):
        max_val = max(util_values)
        if v > max_val:
            return v, num_nodes, depth_of_stack
        else:
            return max_val, num_nodes, depth_of_stack        
'''
def start_game_minimax():
    begin = myState().initial_state_generator()
    state = begin
    print(state)
    while True:
        state.player = 2
        bot_action, num_nodes, garbage = minimax_decision(state)
        state = state.next_state(bot_action)
        print(state)
        if(terminal_test(state)==True):
            print("Bot wins")
            break
        state.player = 1 
        #not to be changed till this point
        #human_action = raw_input()
        #human_action = int(human_action)
        human_action=input('Enter action:')
        inList = [int(n) for n in human_action.split(' ')]   # check for parens too?
        human_action = tuple(inList)
        #human_action is feftet of initial and final position and length of jump
        #assume human don't play faulty move
        state = state.next_state(human_action)
        print(state)
        if(terminal_test(state)==True):
            print("Player 1 wins")
            break 
 '''           
# def main():
#     begin = myState()
#     print(begin.minimax_decision())
'''        
if __name__ == "__main__":
    start_game_minimax()
    # main()
'''
'''
 #elementary testing
def main():
    print("Welcome")
    begin=myState()
    initial=begin.initial_state_generator()
    print(begin.matrix)
    action_list=begin.action()
   # print(action_list)
    print("testing next state")
    for action in action_list:
        state=initial.next_state(action)
        print("first players coin:"+str(state.count_coins(1))+
              "second players coin:"+str(state.count_coins(2)))
        new_state=state.next_state(action)
        print("first players coin:"+str(new_state.count_coins(1))+
              "second players coin:"+str(new_state.count_coins(2)))
        print(state.matrix)
    statelist=successor_function(initial)
    print(statelist)
main()    
'''