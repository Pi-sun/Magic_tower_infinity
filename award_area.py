import generator

def award_area_optimize(new_board):
    'award return the award area index of a give position, award index return the layer of given position, award listing return the immediate previous area of an area and the immediate door leading to this area'
    new_board.award=list()
    new_board.award_index=list()
    new_board.award_listing=[None]*len(new_board.award_area)
    new_board.key_main=[]
    new_board.key_side=[]
    index=0
    for i in range(new_board.size):
        new_board.award_index.append([None]*new_board.size)
    for i in new_board.main_route:
        new_board.award_index[i[0]][i[1]]=-1
    for i in new_board.side_route:
        new_board.award_index[i[0]][i[1]]=-1
    for i in range(new_board.size):
        new_board.award.append([-9]*new_board.size)
    for i in new_board.main_route:
        new_board.award[i[0]][i[1]]=-1
    for i in new_board.side_route:
        new_board.award[i[0]][i[1]]=-1
    for i in new_board.award_area:
        for j in i:
            new_board.award[j[0]][j[1]]=index
        index+=1
    'all walkable square on the board indexed -1 for main nad side route, 0,1,2,3,4 for award areas'
    new_board.present()
    clean_board(new_board)
    for i in new_board.main_route:
        new_board.assign(i,1)
        if len(generator.area_detect(new_board))>1:
            new_board.key_main.append(i)
        new_board.assign(i,0)
    for i in new_board.side_route:
        new_board.assign(i,1)
        if len(generator.area_detect(new_board))>1:
            new_board.key_side.append(i)
        new_board.assign(i,0)
    remain_door=[]
    for i in new_board.door:
        remain_door.append(i)
    index=0
    while True:
        print(remain_door,index)
        temp_set=[]
        temp_door=[]
        success=False
        for i in remain_door:
            success=False
            temp_set=[]
            for j in generator.return_boundary([i]):
                if new_board.valid_position(j):
                    print(j,new_board.award_index[j[0]][j[1]],int(index-1))
                    if new_board.award_index[j[0]][j[1]]==index-1:
                        success=True
                        root=new_board.award[j[0]][j[1]]
                    elif new_board.award[j[0]][j[1]]!=-9:
                        temp_set.append(new_board.award[j[0]][j[1]])
            if success:
                temp_door.append(i)
            if success:
                for j in temp_set:
                    new_board.award_listing[j]=[root,i]
                    for k in new_board.award_area[j]:
                        new_board.award_index[k[0]][k[1]]=int(index)
                new_board.award_index[i[0]][i[1]]=int(index)
        for i in temp_door:
            remain_door.remove(i)
        index+=0.5
        new_board.present()
        new_board.award_present()
        if len(remain_door)==0:
            break
    restore_board(new_board)
            
    
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
        board.assign(i,0)
    board.assign(board.start_position,0)
    board.assign(board.end_position,0)
    return None

def restore_board(board):
    for i in board.door:
        board.assign(i,3)
    for i in board.main_route:
        board.assign(i,1)
    for i in board.side_route:
        board.assign(i,1)
    for i in board.door:
        board.assign(i,3)
    board.assign(board.start_position,-1)
    board.assign(board.end_position,-2)
    return None
    
if __name__ == "__main__":
    a=generator.map_generate(11,[1,7])
    a.prettyPrint()
    print()
    award_area_optimize(a)
    a.present()
    a.award_present()
