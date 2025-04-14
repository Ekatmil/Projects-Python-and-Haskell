def move(Map,h,w):
	for i in range(0,int(h),1):
		for j in range(0,int(w),1):
			if (Map[i][j] == '>'):
				if ((Map[i+1][j]=='X' and Map[i][j + 1] == '.')or(Map[i+1][j+1]=='X' and Map[i][j + 1] == '.')):
					Map[i][j] = '.'
					Map[i][j + 1] ='>'
					return
				if (Map[i + 1][j] == '.'):
					Map[i][j] = 'v'
					return
				if (Map[i][j + 1] == 'X'):
					Map[i][j] = '^'
					return
			if (Map[i][j] == '^'):
				if ((Map[i][j + 1] == 'X' and Map[i - 1][j]=='.')or(Map[i-1][j+1]=='X' and Map[i-1][j]=='.')):
					Map[i][j] = '.'
					Map[i - 1][j] = '^'
					return
				if (Map[i][j + 1] == '.'):
					Map[i][j] = '>'
					return
				if (Map[i-1][j]=='X'):
					Map[i][j] = '<'
					return
			if (Map[i][j]=='<'):
				if ((Map[i-1][j]=='X' and Map[i][j-1]=='.')or(Map[i-1][j-1]=='X' and Map[i][j-1]=='.')):
					Map[i][j] = '.'
					Map[i][j - 1] = '<'
					return
				if (Map[i-1][j]=='.'):
					Map[i][j] = '^'
					return
				if (Map[i][j-1]=='X'):
					Map[i][j] = 'v'
					return
			if (Map[i][j]== 'v'):
				if ((Map[i][j-1]=='X' and Map[i+1][j]=='.')or(Map[i+1][j-1]=='X' and Map[i+1][j]=='.')):
					Map[i][j] = '.'
					Map[i + 1][j] = 'v'
					return
				if (Map[i][j-1]=='.'):
					Map[i][j] = '<'
					return
				if (Map[i+1][j]=='X'):
					Map[i][j] = '>'
					return
def drawMap(Map,h, w):
	for i in range(0,int(h),1):
		for j in range(0,int(w),1):
			print(Map[i][j], end = '')
		print("")
k = open('maze.txt','r')
w = k.readline() 
h = k.readline()
game = [ ]
for i in range (0,int(h),1):
	game.append(list(k.readline())) 
for q in range(1,21,1):
	move(game,h,w)
	drawMap(game,h,w)
	print("")

