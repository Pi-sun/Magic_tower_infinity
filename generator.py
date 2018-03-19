# Magic Tower map generator - v0.02T

import random

def return_boundary(positions):
    'return the boundary of the area indicated by given positions'
    boundary =[]
    for position in positions:
        if [position[0],position[1]+1] not in positions and [position[0],position[1]+1] not in boundary:
            boundary.append([position[0],position[1]+1])
        if [position[0],position[1]-1] not in positions and [position[0],position[1]-1] not in boundary:
            boundary.append([position[0],position[1]-1])
        if [position[0]+1,position[1]] not in positions and [position[0]+1,position[1]] not in boundary:
            boundary.append([position[0]+1,position[1]])
        if [position[0]-1,position[1]] not in positions and [position[0]-1,position[1]] not in boundary:
            boundary.append([position[0]-1,position[1]])
    return boundary

class Board:
    'a class which describes a board in the game'
    def __init__(self,size):
        self.main_route=[]
        self.side_route=[]
        self.door=[]
        self.side_start=None
        self.side_end=None
        self.award_area=[]
        self.size=size
        self.special=[]
        self.special_door=[]
        self.content=list()
        for i in range(size):
            self.content.append([0]*size)
        return None

    def check_item(self,position):
        'return the object at the given position on the board'
        if position[0]>=0 and position[0]>=0 and position[0]<self.size and position[1]<self.size:
            return self.content[position[0]][position[1]]
        else:
            return 0

    def area_assign(self,index,positions):
        if index==0:
            self.main_route=positions
        if index==1:
            self.side_route=positions
        if index>1:
            self.award_area.append(positions)
        return None

    def assign(self,position,thing):
        self.content[position[0]][position[1]]=thing
        return None

    def special_assign(self,index,position):
        'assign starting position (index 0), ending position(index 1), starting position of side route (index 3), ending position of side route(index 2),door (index 4)'
        if index==0:
            self.start_position=position
        if index==1:
            self.end_position=position
        if index==3:
            self.side_start=position
        if index==2:
            self.side_end=position
        if index==4:
            self.door.append(position)
        return None
        

    def length(self):
        return self.size

    def nearby_check(self,position,thing):
        result=0
        num_near=0
        if not self.valid_position(position):
            result=-1
        else:
            for item in return_boundary([position]):
                if self.check_item(item)== thing:
                    num_near+=1
            result=num_near
        return result

    def valid_position(self,position):
        'check whether a position is valid in the board'
        if position[0]>=0 and position[1]>=0 and position[0]<self.size and position[1]<self.size:
            return True
        else:
            return False

    def can_walk(self,position):
        'check whether a position in the board'
        if not self.valid_position(position):
            return False
        else:
            'To be continued'

            return True

    def present(self):
        for line in self.content:
            print(line)
        print('\n')
        return None

def main_route_generate(size,start_posi,new_one):

    'generate the mainroute in game, -1 for starting position, -2 to ending position, 1 for main route, 2 for walls'
    
    pre_direction=-10
    route=[start_posi]
    node=start_posi
    trial =0
    if_side=False
    while True:
        success=True
        temp_route=[]
        direction=random.randint(1,4)
        distance=random.randint(2,size)
        if direction!=pre_direction and direction!=pre_direction+2 and direction!=pre_direction-2:
            if direction==1:
                for step in range(distance):
                    new_point=[node[0]+step+1,node[1]]
                    if new_one.nearby_check(new_point,0)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            if direction==2:
                for step in range(distance):
                    new_point=[node[0],node[1]+step+1]
                    if new_one.nearby_check(new_point,0)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            if direction==3:
                for step in range(distance):
                    new_point=[node[0]-step-1,node[1]]
                    if new_one.nearby_check(new_point,0)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            if direction==4:
                for step in range(distance):
                    new_point=[node[0],node[1]-step-1]
                    if new_one.nearby_check(new_point,0)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break

        'tril is to stop the program from trying to find the next route while while it is impossible'
        if success:
            trial=0
            route.extend(temp_route)
            new_one.assign(node,1)
            finisher=random.randint(1,3)
            for i in temp_route:
                new_one.assign(i,1)
            node=route[-1]
            new_one.assign(node,0)
            if finisher==1:
                break
        else:
            trial+=1

        if trial>20:
            new_one.assign(node,1)
            break

    new_one.assign(start_posi,-1)
    new_one.special_assign(0,start_posi)
    new_one.assign(node,-2)
    new_one.special_assign(1,node)
    new_one.area_assign(0,route)
    'main route generated'

    'side route generated began'
    if len(route)>6:
        side_start=random.randint(0,int(0.6*len(route)))
        starting=route[side_start]
        side_route=[starting]
        pre_direction=-10
        node=starting
        new_one.assign(starting,0)
        trial=0
        while True:
            success='y'
            temp_route1=[]
            direction=random.randint(1,4)
            distance=random.randint(2,size)
            if direction!=pre_direction and direction!=pre_direction+2 and direction!=pre_direction-2:
                if direction==1:
                    for step in range(distance):
                        new_point=[node[0]+step+1,node[1]]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,3)==0:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                if direction==2:
                    for step in range(distance):
                        new_point=[node[0],node[1]+step+1]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,3)==0:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                if direction==3:
                    for step in range(distance):
                        new_point=[node[0]-step-1,node[1]]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,3)==0:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                if direction==4:
                    for step in range(distance):
                        new_point=[node[0],node[1]-step-1]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,3)==0:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break

                if success=='y':
                    trial=0
                    side_route.extend(temp_route1)
                    new_one.assign(node,3)
                    for i in temp_route1:
                        new_one.assign(i,3)
                    node=side_route[-1]
                    new_one.assign(node,0)
                elif success=='t' and (len(side_route)+len(temp_route1))>2:
                    side_route.extend(temp_route1)
                    new_one.assign(node,3)
                    for i in side_route:
                        new_one.assign(i,1)
                    if_side=True
                    break
                elif success=='t':
                    for i in side_route:
                        new_one.assign(i,0)
                    if_side=False
                    new_one.assign(starting,1)
                    if_end=random.randint(0,1)
                    if if_end==1:
                        break
                    else:
                        side_route=[starting]
                        node=starting
                        new_one.assign(starting,0)
                        trial=0
                else:
                    trial+=1

                if trial>20:
                    for i in side_route:
                        new_one.assign(i,0)
                    new_one.assign(starting,1)
                    if_side=False
                    if_end=random.randint(0,1)
                    if if_end==1:
                        break
                    else:
                        side_route=[starting]
                        node=starting
                        new_one.assign(starting,0)
                        trial=0

    if if_side:
        new_one.area_assign(1,side_route)
        new_one.special_assign(2,side_route[0])
        new_one.special_assign(3,side_route[-1])
    new_one.assign(start_posi,-1)



    
    'wall generation starts the next line'

    if not if_side:
        for wall_posi in return_boundary(route):
            if new_one.nearby_check(wall_posi,2)==0 or new_one.nearby_check(wall_posi,2)==1:
                new_one.assign(wall_posi,2)
        for wall_posi in return_boundary(route):
            if new_one.nearby_check(wall_posi,2)==2 and new_one.check_item(wall_posi)==0:
                new_one.assign(wall_posi,2)  
    else:
        all_route=route+side_route
        for wall_posi in return_boundary(all_route):
            if new_one.nearby_check(wall_posi,2)==0 or new_one.nearby_check(wall_posi,2)==1:
                new_one.assign(wall_posi,2)
        for wall_posi in return_boundary(all_route):
            if new_one.nearby_check(wall_posi,2)==2 and new_one.check_item(wall_posi)==0:
                new_one.assign(wall_posi,2)
                

    return new_one

def area_detect(new_board):
    all_area=[]
    area_list=[]
    for row_index in range(new_board.length()):
        for column_index in range(new_board.length()):
            if new_board.check_item([row_index,column_index])==0 and [row_index,column_index] not in area_list:
                area=[[row_index,column_index]]
                pre_area=area
                while True:
                    trial=0
                    temp_area=return_boundary(pre_area)
                    pre_area=[]
                    for i in temp_area:
                        if new_board.check_item(i)==0 and new_board.valid_position(i) and (i not in area):
                            area.append(i)
                            pre_area.append(i)
                            trial+=1
                    if trial==0:
                        break
                area_list.extend(area)
                all_area.append(area)
    return all_area

def create_subarea(area,starting_position,size):
    trial=0
    while True:
        area1=[starting_position]
        pre_area=[starting_position]
        while True:
            this_size=0
            temp_area=[]
            for tile in return_boundary(pre_area):
                if tile in area:
                    area1.append(tile)
                    this_size+=1
                    temp_area.append(tile)
            pre_area=temp_area
            if this_size>=len(pre_area)-1:
                break
        wall_area=[]
        for item in return_boundary(area1):
            if item in area:
                wall_area.append(item)
        trial_board=Board(100)
        for row_index in range(100):
            for column_index in range(100):
                if [row_index,column_index] not in area or [row_index,column_index] in wall_area:
                    trial_board.assign([row_index,column_index],1)
        if len(area_detect(trial_board))==2 and (len(area)-len(area1)-len(wall_area))>=3:
            break
        else:
            trial+=1
        if trial>10:
            area1=area
            wall_area=[]
            break
    return [area1,wall_area]
            
    
                
def divide_area(area):
    remaining_area=area
    final_area=[]
    wall_area=[]
    while True:
        if len(remaining_area)>12:
            for starting_point in range(len(remaining_area)):
                size=random.randint(3,12)
                if len((create_subarea(remaining_area,remaining_area[starting_point],size))[1])!=0:
                    temp_area=(create_subarea(remaining_area,remaining_area[starting_point],size))[0]
                    temp_wall=(create_subarea(remaining_area,remaining_area[starting_point],size))[1]
                    temp_remove=temp_area+temp_wall
                    final_area.append(temp_remove)
                    wall_area.extend(temp_wall)
                    for i in temp_remove:
                        remaining_area.remove(i)
                    success=True
                    break
                else:
                    success=False
            if not success:
                final_area.append(remaining_area)
                break
        else:
            final_area.append(remaining_area)
            break
    return [final_area,wall_area]
            

def award_area_generate(new_board):
    final_area=[]
    all_area = area_detect(new_board)
    for area in all_area:
        if len(area)<=7:
            final_area.append(area)
        else:
            temp_wall=(divide_area(area))[1]
            temp_area=(divide_area(area))[0]
            final_area.append(temp_area)
            new_board.area_assign(2,final_area)
            for i in temp_wall:
                new_board.assign(i,2)
    return new_board


def door_generate(new_board):
    'generate doors for the Board new_board'
    'Board -> Board'
    doors=[]
    walls=[]
    blank_board=Board(new_board.size)
    for row_index in range(new_board.length()):
        for column_index in range(new_board.length()):
            if new_board.check_item([row_index,column_index])==2:
                blank_board.assign([row_index,column_index],2)
                if [row_index,column_index] not in new_board.special:
                    walls.append([row_index,column_index])
    for i in walls:
        blank_board1=Board(blank_board.size)
        for row_index in range(blank_board.length()):
            for column_index in range(new_board.length()):
                if blank_board.check_item([row_index,column_index])==2:
                    blank_board1.assign([row_index,column_index],2)
        blank_board1.assign(i,0)
        if len(area_detect(blank_board1))<len(area_detect(blank_board)):
            doors.append(i)
            walls.remove(i)
            blank_board.assign(i,0)
            new_board.assign(i,0)
        if len(area_detect(blank_board))==1:
            break
    for i in doors:
        new_board.special_assign(4,i)
        new_board.assign(i,3)
    return new_board
def pre_generate(size,starting_position,size_area):
    
    dragon_width=size_area[0]
    dragon_length=size_area[1]
    if True:
        version_0=Board(size)
        while True:
            dragon_x=random.randint(0,size-dragon_width-1)
            dragon_y=random.randint(0,size-dragon_length)
            if (starting_position[0]<dragon_x or starting_position[0]>=dragon_x+dragon_length) and (starting_position[1]<dragon_y or starting_position[1]>=dragon_y+dragon_width):
                print('smile')
            else:
                break
        dragon=[]
        for x_cood in range(dragon_x,dragon_x+dragon_width):
            for y_cood in range(dragon_y,dragon_y+dragon_length):
                dragon.append([x_cood,y_cood])
        for i in dragon:
            version_0.assign(i,1)
        version_0.special=dragon
        version_0.special_door=[dragon_x+dragon_width,dragon_y+int((dragon_length-1)/2)]
        version_a=main_route_generate(size,starting_position,version_0)
        return version_a
    
def map_generate(size,starting_position,*special_requirement):
    'generate a random map with starting_position and size, special requirement include shop, dragon, no_return,guarded_area'
    version_0=Board(size)
    version_a=main_route_generate(size,starting_position,version_0)
    if 'dragon' in special_requirement:
        version_a=pre_generate(size,starting_position,[4,3])
    if 'guarded_area' in special_requirement:
        version_a=pre_generate(size,starting_position,[6,5])
    if 'shop' in special_requirement:
        version_a=pre_generate(size,starting_position,[1,3])
    if 'no_return' in special_requirement:
        version_a.assign(version_a.start_position,0)
        version_a.start_position=None
        
    version_c=door_generate(award_area_generate(version_a))
    if 'shop' in special_requirement or 'guard_area' in special_requirement:
        if version_c.check_item(version_c.special_door)==2:
            version_c.assign(version_c.special_door,0) 
    for i in version_c.special:
        version_c.assign(i,5)
    return version_c

if __name__ == "__main__":
	a=map_generate(10,[3,1])
	a.present()  
