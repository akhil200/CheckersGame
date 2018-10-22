##########################
# Akhil Agrawal
# 2015B4A7PS0631P
##########################
import tkinter as tk
import MinMax as mm
import Alpha_Beta as ab
import copy
import time
class GUI:
	def start(self):
		self.root.mainloop()
	def __init__(self):
		self.root = tk.Tk(className="Checkers")
		self.root.geometry('1000x1000')
		begin = mm.myState().initial_state_generator()
		self.state = begin
		self.textbox = tk.Text(self.root, width = 25,height=100,bg='yellow')
		self.canvas=tk.Canvas(self.root,width=75*10,height=450,bg='black')
		self.canvas2=tk.Canvas(self.root,width=75*10,height=100*2,bg='red')
		#b=tk.Button(self.root,text="Next turn",bg='gray',fg='white',font=('Arial',25,'bold'))
		self.t = tk.Text(self.root, width = 25,height=1,bg='blue',font=('Arial',14,'bold'))
		self.t1=tk.Text(self.root, width = 6,height=1,bg='blue',font=('Arial',20,'bold'))
		self.e=tk.Entry(self.root,width=25,font=('Arial',15,'bold'))
		self.b1=tk.Button(self.root,text="MinMax",bg='gray',fg='white',font=('Arial',25,'bold'),command=self.PlayGameMinMax)
		self.b2=tk.Button(self.root,text="Alpha-Beta",bg='gray',fg='white',font=('Arial',25,'bold'),command=self.PlayGameMinMax)
		# Packing
		self.textbox.place(x=0,y=0)  
		self.canvas.place(x=25*8,y=0)
		self.canvas2.place(x=25*8,y=600)
		self.t1.place(x=450,y=460)
		self.t.place(x=183,y=525)
		self.e.place(x=183,y=550)
		self.t.insert(tk.END,"Enter initial and final position")
		self.b1.place(x=225,y=600)
		self.b2.place(x=425,y=600)
		#b.place(x=25*8,y=440)
		#populate analysis
		for i in range(0,13):
			text="R"+str(i+1)+":"
			l=tk.Label(self.textbox,text=text,font = ('Arial',15,"bold"),bg='yellow')
			l.pack()
	
	
	def displayinitialstateoncanvasMinMax(self,canvas,state,e,t1):
		mat=copy.deepcopy(state.matrix)
		for i in range(0,5):
			for j in range (0,11):
				if(mat[i][j]!=-1):
					tk.Label(canvas, text=str(mat[i][j]), borderwidth=5, padx=5 , pady=5,font=('Arial',45,'bold')).grid(row=i, column=j)
					canvas.pack()
		t1.insert('1.0',"Turn:0")
		t1.pack()
			#start playing game
		canvas.after(5000,self.startgameMinMax,state,canvas,e,t1)
	def startgameMinMax(self,state,canvas,e,t1):
		#print("Safe")
		turn_count=0
		while True:
			state.player = 2
			bot_action, num_nodes, garbage = mm.minimax_decision(state)
			state = state.next_state(bot_action)
			#print(state)
			turn_count+=1
			print("Player1")
			t1.insert('1.0',"Turn:"+str(turn_count))
			self.displayoncanvas(state,canvas,turn_count)
			t1.pack()
			if(turn_count>15):
				break
			if(mm.terminal_test(state)==True):
				print("Bot wins")
				break
			time.sleep(15)
			s=e.get()
			tup=[int(s[0]),int(s[2]),int(s[4]),int(s[6]),int(s[8])]
			tup=tuple(tup)    
			#print(tup)
			print("Player2")
			state.player = 1 
			#human_action is feftet of initial and final position and length of jump
			#assume human don't play faulty move
			state = state.next_state(tup)
			#print(state)
			turn_count+=1
			self.displayoncanvas(state,canvas,turn_count)
			t1.insert('1.0',"Turn:"+str(turn_count))
			t1.pack()
			if(mm.terminal_test(state)==True):
				print("Player 1 wins")
				break
			time.sleep(10)
		return
	def displayoncanvas(self,state,canvas,turn_count):
		canvas.delete("all")
		mat=copy.deepcopy(state.matrix)
		for i in range(0,5):
			for j in range (0,11):
				if(mat[i][j]!=-1):
					tk.Label(canvas, text=str(mat[i][j]), borderwidth=5, padx=5
						  , pady=5,font=('Arial',45,'bold')).grid(row=i, column=j)          
		canvas.pack()  
	def PlayGameMinMax(self):
		GUI=self
		self.displayinitialstateoncanvasMinMax(GUI.canvas,GUI.state,GUI.e,GUI.t1)
	def displayinitialstateoncanvasAlphaBeta(self,canvas,state,e,t1):
			mat=copy.deepcopy(state.matrix)
			for i in range(0,5):
				for j in range (0,11):
					if(mat[i][j]!=-1):
						tk.Label(canvas, text=str(mat[i][j]), borderwidth=5, padx=5
							  , pady=5,font=('Arial',45,'bold')).grid(row=i, column=j)          
			canvas.pack()
			t1.insert('1.0',"Turn:0")
			t1.pack()
			#start playing game
			canvas.after(10000,self.startgameAlphaBeta,state,canvas,e,t1)    
	def startgameAlphaBeta(self,state,canvas,e,t1):
			#print("Safe")
			turn_count=0
			while True:
				state.player=2
				bot_action = ab.alpha_beta_search(state)
				state = state.next_state(bot_action)
				#print(state)
				turn_count+=1
				t1.insert('1.0',"Turn:"+str(turn_count))
				self.displayoncanvas(state,canvas,turn_count)
				t1.pack()
				if(turn_count>15):
					break
				if(ab.terminal_test(state)==True):
					print("Bot wins")
					break
				time.sleep(5)
				s=e.get()
				tup=[int(s[0]),int(s[2]),int(s[4]),int(s[6]),int(s[8])]
				tup=tuple(tup)    
				#print(tup)
				print("Player2")
				state.player = 1
				state = state.next_state(tup)
				print(state)
				turn_count+=1
				self.displayoncanvas(state,canvas,turn_count)
				t1.insert('1.0',"Turn:"+str(turn_count))
				t1.pack()
				if(ab.terminal_test(state)==True):
					print("Player 1 wins")
					break
				time.sleep(5)
			return         
	def PlayGameAlphaBeta(self):
		#print("string")
		self.displayinitialstateoncanvasAlphaBeta(self.canvas,self.state,self.e,self.t1)      

appstart=GUI()
appstart.start()
