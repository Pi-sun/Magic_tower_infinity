import generator

def award_area_optimize(new_board):
    new_board.award=list()
    new_board.award_listing=[None,None]*len(new_board.award_area)
    new_board.key_main=[]
    new_board.key_side=[]
    index=0
    for i in range(new_board.size):
        new_board.award.append([-9]*new_board.size)
    for i in new_board.main_route:
        new_board.award[i[0]][i[1]]=-1
    for i in new_board.side_route:
        new_board.award[i[0]][i[1]]=-1
    for i in new_board.award_area:
        for j in i:
            new_board.award[i[0]][i[1]]=index
        index+=1
    'all walkable square on the board indexed -1 for main nad side route, 0,1,2,3,4 for award areas'
    clean_board(new_board)
    for i in new_board.main_route:
        new_board.assign(i,1)
        if area_detect(new_board)>1:
            new_board.key_main.append(i)
        new_board.assign(i,0)
    for i in new_board.side_route:
        new_board.assign(i,1)
        if area_detect(new_board)>1:
            new_board.key_side.append(i)
        new_board.assign(i,0)
    rem_door=new_board.door
    
    return None

def check_connect(board,posi1,posi2):
    result=False
    area=generator.area_detect(board)
    for i in area:
        if posi1 in area and posi2 in area:
            result=True
    return result

def check_award_index(board,position):
    'return the ajacent tile with unique award index'
    result=[]
    nearby_index=[]
    nearby=[[position[0],position[1]+1],[position[0],position[1]-1],[position[0]-1,position[1]],[position[0]+1,position[1]]]
    for i in nearby:
        if (not board.valid_position) or board.check_item(i)!=0:
            nearby.remove(i)
        else:
            nearby_index.append(board.award[i[0]][i[1]])
    for i in nearby:
        if nearby_index.count(board.award[i[0]][i[1]])==1:
            result.append(i)
    return result
            
            

def clean_board(board):
    for i in board.door:
        board.assign(i,0)
    for i in board.main_route:
        board.assign(i,0)
    for i in board.side_route:
        board.assign(1,0)
    board.assign(board.start_position,0)
    board.assign(board.end_position,0)
    return None

def restore_board(board):
    for i in board.door:
        board.assign(i,3)
    for i in board.main_route:
        board.assign(i,1)
    for i in board.side_route:
        board.assign(1,1)
    board.assign(board.start_position,-1)
    board.assign(board.end_position,-2)
    return None
a=generator.map_generate(7,[1,1])
award_area_optimize(a)
