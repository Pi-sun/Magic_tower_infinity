import random, sys

def boss_floor_generate(start_position,size):
    half_size=size//2
    new_one=Board(size)
    new_one.start_position=start_position
    new_one.assign(start_position,-1)
    new_one.main_route=[start_position]
    if start_position[0]+1>0.5*size:
        wall_y=half_size-1
        boss=1
        specials = [[x,y] for x in range(0,half_size-1) for y in range(size)]
    else:
        wall_y=half_size
        boss=0
        specials = [[x,y] for x in range(half_size+1,size) for y in range(size)]
    new_one.special += specials
    for i in specials:
        new_one.assign(i,5)
    new_one.special_wall = [[wall_y,i] for i in range(size)]
    new_one.wall += new_one.special_wall
    for i in range(size):
        new_one.assign([wall_y,i],2)
    if start_position[1]<half_size:
        for i in range(start_position[1]+1,half_size+1):
            position=[start_position[0],i]
            new_one.assign(position,1)
            new_one.main_route.append(position)
    else:
        for i in range(half_size+1,start_position[1]+1):
            position=[start_position[0],i]
            new_one.assign(position,1)
            new_one.main_route.append(position)
    if start_position[0]<half_size:
        for i in range(start_position[0],half_size):
            position=[i,half_size]
            new_one.assign(position,1)
            new_one.main_route.append(position)
        new_one.assign([half_size,half_size],3)
        new_one.door.append([half_size,half_size])
    else:
        for i in range(half_size,start_position[0]+1):
            position=[i,half_size]
            new_one.assign(position,1)
            new_one.main_route.append(position)
        new_one.assign([half_size-1,half_size],3)
        new_one.door.append([half_size-1,half_size])
    for i in return_boundary_s(new_one.main_route):
        if new_one.valid_position(i) and new_one.content[i[0]][i[1]]!=3:
            new_one.assign(i,2)
            new_one.wall.append(i)
    if boss==1:
        new_one.end_position=[random.randint(0,half_size-2),half_size]
    elif boss==0:
        new_one.end_position=[random.randint(half_size+1,size-1),half_size]
    new_one_v2=door_generate(award_area_generate(new_one))
    new_one_v3=wall_optimize(new_one_v2)
    
    for i in new_one_v3.special:
        new_one_v3.assign(i,5)

    new_one_v3.assign(new_one_v3.end_position,-2)
    new_one_v3.assign(new_one_v3.start_position,-1)
    return new_one_v3
        
def return_boundary_s(positions):
    boundary=return_boundary(positions)
    for position in positions:
        if [position[0]+1,position[1]+1] not in positions and [position[0]+1,position[1]+1] not in boundary:
            boundary.append([position[0]+1,position[1]+1])
        if [position[0]+1,position[1]-1] not in positions and [position[0]+1,position[1]-1] not in boundary:
            boundary.append([position[0]+1,position[1]-1])
        if [position[0]-1,position[1]+1] not in positions and [position[0]-1,position[1]+1] not in boundary:
            boundary.append([position[0]-1,position[1]+1])
        if [position[0]-1,position[1]-1] not in positions and [position[0]-1,position[1]-1] not in boundary:
            boundary.append([position[0]-1,position[1]-1])
    return boundary
    
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
        self.special_wall=[]
        self.main_route=[]
        self.side_route=[]
        self.start_position=[]
        self.end_position=[]
        self.side_area=[]
        self.door=[]
        self.wall=[]
        self.side_start=None
        self.side_end=None
        self.award_area=[]
        self.size=size
        self.special=[]
        self.special_actual=[]
        self.special_door=[]
        self.vault = []
        self.content=[[0]*size for i in range(size)]
        return None

    def check_item(self,position):
        'return the object at the given position on the board'
        if self.valid_position(position):
            return self.content[position[0]][position[1]]
        else:
            return 0

    def assign(self,position,thing):
        self.content[position[0]][position[1]]=thing
        return None

    def nearby_check(self,position,thing):
        result=0
        if not self.valid_position(position):
            result=-1
        else:
            for item in return_boundary([position]):
                if self.check_item(item)== thing:
                    result+=1
        return result

    def valid_position(self,position):
        'check whether a position is valid in the board'
        return position[0]>=0 and position[1]>=0 and position[0]<self.size and position[1]<self.size

    def can_walk(self,position):
        'check whether a position in the board'
        if not self.valid_position(position):
            return False
        else:
            'To be continued'
            return True
            
    def award_present(self):
        for line in self.award_index:
            print(line)
        print('\n')
        for line in self.award:
            print(line)
        print('\n')
        print(self.award_listing,'\n')

    def present(self):
        for line in self.content:
            print(line)
        print('\n')
        return None
            
    def prettyPrint(self, message = "Board", file = sys.stdout):
        print(message + ":", file = file)
        d = self.__dict__
        keys = sorted(d.keys())
        for key in keys:
            if key in ["award", "award_area", "award_index", "content", "difficulty"]:
                print("    " + key + ":", file = file)
                for line in d[key]:
                    print("      " + str(line), file = file)
            else:
                print("    " + key + ":", d[key], file = file)
        print(file = file)

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
                    if new_one.nearby_check(new_point,0)+new_one.nearby_check(new_point,2)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            elif direction==2:
                for step in range(distance):
                    new_point=[node[0],node[1]+step+1]
                    if new_one.nearby_check(new_point,0)+new_one.nearby_check(new_point,2)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            elif direction==3:
                for step in range(distance):
                    new_point=[node[0]-step-1,node[1]]
                    if new_one.nearby_check(new_point,0)+new_one.nearby_check(new_point,2)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break
            elif direction==4:
                for step in range(distance):
                    new_point=[node[0],node[1]-step-1]
                    if new_one.nearby_check(new_point,0)+new_one.nearby_check(new_point,2)==4:
                        temp_route.append(new_point)
                    else:
                        success=False
                        break

        'tril is to stop the program from trying to find the next route while while it is impossible'
        if success:
            trial=0
            route.extend(temp_route)
            new_one.assign(node,1)
            for i in temp_route:
                new_one.assign(i,1)
            node=route[-1]
            new_one.assign(node,0)
            if random.randint(1,3)==1:
                break
        else:
            trial+=1

        if (trial>20 and len(route)!=1):
            new_one.assign(node,1)
            break

    new_one.assign(start_posi,-1)
    new_one.start_position=start_posi
    new_one.assign(node,-2)
    new_one.end_position=node
    new_one.main_route=route
    'main route generated'

    'side route generated began'
    new_one.side_trial=''
    if len(route)>2:
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
                        elif new_one.nearby_check(new_point,1)==1:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                elif direction==2:
                    for step in range(distance):
                        new_point=[node[0],node[1]+step+1]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,1)==1:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                elif direction==3:
                    for step in range(distance):
                        new_point=[node[0]-step-1,node[1]]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,1)==1:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break
                elif direction==4:
                    for step in range(distance):
                        new_point=[node[0],node[1]-step-1]
                        if new_one.nearby_check(new_point,0)==4:
                            temp_route1.append(new_point)
                        elif new_one.nearby_check(new_point,1)==1:
                            temp_route1.append(new_point)
                            success='t'
                            break
                        else:
                            success='n'
                            break

                if success=='y':
                    new_one.side_trial+='y'
                    trial=0
                    side_route.extend(temp_route1)
                    new_one.assign(node,3)
                    for i in temp_route1:
                        new_one.assign(i,3)
                    node=side_route[-1]
                    new_one.assign(node,0)
                elif success=='t':
                    if (len(side_route)+len(temp_route1))>2:
                        new_one.side_trial+='t'
                        side_route.extend(temp_route1)
                        new_one.assign(node,3)
                        for i in side_route:
                            new_one.assign(i,1)
                        if_side=True
                        break
                    else:
                        new_one.side_trial+='t'
                        for i in side_route:
                            new_one.assign(i,0)
                        if_side=False
                        new_one.assign(starting,1)
                        if_end=random.randint(0,5)
                        if if_end==1:
                            break
                        else:
                            side_route=[starting]
                            node=starting
                            new_one.assign(starting,0)
                            trial=0
                else:
                    new_one.side_trial+='n'
                    trial+=1

                if trial>20:
                    for i in side_route:
                        new_one.assign(i,0)
                    new_one.assign(starting,1)
                    if_side=False
                    if_end=random.randint(0,5)
                    if if_end==1:
                        break
                    else:
                        side_route=[starting]
                        node=starting
                        new_one.assign(starting,0)
                        trial=0

    if if_side:
        new_one.side_route=side_route
        new_one.side_end=side_route[0]
        new_one.side_start=side_route[-1]
    new_one.assign(start_posi,-1)


    
    'wall generation starts the next line'

    if not if_side:
        boundary = return_boundary_s(route)
        for wall_posi in boundary:
            if new_one.nearby_check(wall_posi,2)==0 or new_one.nearby_check(wall_posi,2)==1:
                new_one.assign(wall_posi,2)
                new_one.wall.append(wall_posi)
        for wall_posi in boundary:
            if new_one.nearby_check(wall_posi,2)==2 and new_one.check_item(wall_posi)==0:
                new_one.assign(wall_posi,2)
                new_one.wall.append(wall_posi)
    else:
        boundary = return_boundary_s(route+side_route)
        for wall_posi in boundary:
            if new_one.nearby_check(wall_posi,2)==0 or new_one.nearby_check(wall_posi,2)==1:
                new_one.assign(wall_posi,2)
                new_one.wall.append(wall_posi)
        for wall_posi in boundary:
            if new_one.nearby_check(wall_posi,2)==2 and new_one.check_item(wall_posi)==0:
                new_one.assign(wall_posi,2)
                new_one.wall.append(wall_posi)

    return new_one

def area_detect(new_board):
    all_area=[]
    area_list=[]
    for row_index in range(new_board.size):
        for column_index in range(new_board.size):
            if new_board.content[row_index][column_index]==0 and [row_index,column_index] not in area_list:
                area=[[row_index,column_index]]
                pre_area=area
                while True:
                    temp_area=return_boundary(pre_area)
                    pre_area=[]
                    for i in temp_area:
                        if new_board.valid_position(i) and new_board.content[i[0]][i[1]]==0 and (i not in area):
                            pre_area.append(i)
                    if not pre_area:
                        break
                    else:
                        area.extend(pre_area)
                area_list.extend(area)
                all_area.append(area)
    return all_area

def create_subarea(area,starting_position,size):
    for trial in range(5):
        area1=[starting_position]
        while True:
            temp_area=[tile for tile in return_boundary(area1) if tile in area]
            if len(area1)+len(temp_area)>=size:
                area1.extend(random.sample(temp_area, size - len(area1)))
                break
            else:
                area1.extend(temp_area)
        wall_area=[item for item in return_boundary_s(area1) if item in area]
        if len(area) - len(area1) - len(wall_area) >= 3:
            remaining_area = [item for item in area if (item not in area1) and (item not in wall_area)]
            queue = [remaining_area.pop()]
            while queue:
                item = queue.pop()
                for i in return_boundary([item]):
                    if i in remaining_area:
                        remaining_area.remove(i)
                        queue.append(i)
            if not remaining_area:
                return (area1, wall_area)
        
    return (area, [])
                
def divide_area(area):
    remaining_area=area
    final_area=[]
    wall_area=[]
    while len(remaining_area)>9:
        success=False
        for starting_point in range(len(remaining_area)):
            size=random.randint(3,8)
            temp_area,temp_wall=create_subarea(remaining_area,remaining_area[starting_point],size)
            if len(temp_wall)!=0:
                temp_remove=temp_area+temp_wall
                final_area.append(temp_remove)
                wall_area.extend(temp_wall)
                for i in temp_remove:
                    remaining_area.remove(i)
                success=True
                break
        if not success:
            break
    
    return (final_area + remaining_area,wall_area)

def award_area_generate(new_board):
    final_area=[]
    all_area = area_detect(new_board)
    for area in all_area:
        if len(area)<=7:
            final_area.append(area)
        else:
            temp_area, temp_wall = divide_area(area)
            final_area.append(temp_area)
            for i in temp_wall:
                new_board.wall.append(i)
                new_board.assign(i,2)
    return new_board


def door_generate(new_board):
    'generate doors for the Board new_board'
    'Board -> Board'
    doors=[]
    walls=[]
    blank_board=Board(new_board.size)
    for row_index in range(new_board.size):
        for column_index in range(new_board.size):
            if new_board.content[row_index][column_index]==2:
                blank_board.assign([row_index,column_index],2)
                if [row_index,column_index] not in new_board.special:
                    walls.append([row_index,column_index])
                    
    blank_areas = area_detect(blank_board)
    for i in walls:
        if i not in new_board.special_wall:
            blank_board1=Board(blank_board.size)
            for row_index in range(blank_board.size):
                for column_index in range(blank_board.size):
                    if blank_board.content[row_index][column_index]==2:
                        blank_board1.assign([row_index,column_index],2)
            blank_board1.assign(i,0)
            if len(area_detect(blank_board1))==len(blank_areas)-1:
                if random.randint(0,1)==1:
                    doors.append(i)

                    new_board.wall.remove(i)
                    blank_board.assign(i,0)
                    new_board.assign(i,0)
                    blank_areas = area_detect(blank_board)
            if len(blank_areas)==1:
                break
                
    if len(blank_areas)!=1:
        new_board.error=['step2']
        for i in walls:
            if i not in new_board.special_wall:
                blank_board1=Board(blank_board.size)
                for row_index in range(blank_board.size):
                    for column_index in range(blank_board.size):
                        if blank_board.content[row_index][column_index]==2:
                            blank_board1.assign([row_index,column_index],2)
                blank_board1.assign(i,0)
                if len(area_detect(blank_board1))==len(blank_areas)-1:
                    doors.append(i)

                    new_board.wall.remove(i)
                    blank_board.assign(i,0)
                    new_board.assign(i,0)
                    blank_areas = area_detect(blank_board)
                if len(blank_areas)==1:
                    break
    else:
        new_board.error=['step1']
    
    if len(blank_areas)!=1:
        new_board.vault=[]
        for i in blank_areas:
            if new_board.end_position not in i:
                for j in i:
                    new_board.vault.append(j)
                    new_board.assign(j,5)
    

    new_board.error.append(blank_areas)
    for i in doors:
        new_board.door.append(i)
        new_board.assign(i,3)
    return new_board

def pre_generate(size,starting_position,size_area,surround_back=False):
    
    dragon_width=size_area[0]
    dragon_length=size_area[1]
    version_0=Board(size)
    while True:
        dragon_x=random.randint(0,size-dragon_width-1)
        dragon_y=random.randint(0,size-dragon_length-1)
        if surround_back:
            if starting_position[0]<(dragon_x-1) or starting_position[0]>dragon_x+dragon_width or starting_position[1]<(dragon_y-1) or starting_position[1]>(dragon_y+dragon_length+1):
                break
        else:
            if starting_position[0]<dragon_x or starting_position[0]>dragon_x+dragon_width or starting_position[1]<dragon_y or starting_position[1]>dragon_y+dragon_length:
                break
    dragon=[]
    for x_cood in range(dragon_x,dragon_x+dragon_width):
        for y_cood in range(dragon_y,dragon_y+dragon_length):
            dragon.append([x_cood,y_cood])
    if surround_back:
        surround=[]
        for x_cood in range(max(dragon_x-1,0),dragon_x+dragon_width):
            for y_cood in range(max(dragon_y-1,0),min(dragon_y+dragon_length+1,size)):
                surround.append([x_cood,y_cood])
    else:
        surround=dragon
    for i in surround:
        version_0.assign(i,2)
    version_0.special=surround
    version_0.special_actual=dragon
    version_0.special_door=[dragon_x+dragon_width,dragon_y+(dragon_length-1)//2]
    version_a=main_route_generate(size,starting_position,version_0)
    return version_a

def square_test(area,tile):
    return (([tile[0],tile[1]+1] in area) and ([tile[0]+1,tile[1]+1] in area) and ([tile[0]+1,tile[1]] in area)) or ([tile[0],tile[1]+1] in area and [tile[0]-1,tile[1]+1] in area and [tile[0]-1,tile[1]] in area) or ([tile[0],tile[1]-1] in area and [tile[0]+1,tile[1]-1] in area and [tile[0]+1,tile[1]] in area) or ([tile[0]-1,tile[1]] in area and [tile[0]-1,tile[1]-1] in area and [tile[0],tile[1]-1] in area)

def wall_optimize(new_one):
    new_one.assign(new_one.start_position,0)
    new_one.assign(new_one.end_position,0)
    for i in new_one.main_route:
        new_one.assign(i,0)
    for i in new_one.side_route:
        new_one.assign(i,0)
    ori_no_area=len(area_detect(new_one))

    for i in new_one.wall:
        if square_test(new_one.wall,i):
            new_one.assign(i,0)
            if len(area_detect(new_one))!=ori_no_area:
                new_one.assign(i,2)
            else:
                new_one.wall.remove(i)
    area_list_1=area_detect(new_one)

    for i in new_one.main_route:
        new_one.assign(i,1)
    for i in new_one.side_route:
        new_one.assign(i,1)
    new_one.assign(new_one.start_position,-1)
    new_one.assign(new_one.end_position,-2)
    new_one.award_area=[]
    new_one.side_area=[]
    area_list_2=area_detect(new_one)
    for i in area_list_2:
        if i in area_list_1:
            new_one.award_area.append(i)
        else:
            new_one.side_area.extend(i)
    return new_one
    
    
def map_generate(size,starting_position,special_requirement=None,no_return=False):
    'generate a random map with starting_position and size, special requirement include shop, dragon, no_return,guarded_area'
    if special_requirement=='dragon':
        version_a=pre_generate(size,starting_position,[4,3])
    elif special_requirement=='guarded_area':
        version_a=pre_generate(size,starting_position,[6,5])
    elif special_requirement=='shop':
        version_a=pre_generate(size,starting_position,[1,3],True)
    else:
        version_a=main_route_generate(size,starting_position,Board(size))
    version_a.special_requirement = special_requirement
    
    version_c=door_generate(award_area_generate(version_a))
    if special_requirement=='shop' or special_requirement=='guard_area':
        door = version_c.special_door
        if version_c.check_item(door)==2:
            version_c.assign(door,0)
            version_c.wall.remove(door)
        elif version_c.check_item(door)==3:
            version_c.assign(door,0)
            version_c.door.remove(door)
    for i in version_c.special_actual:
        version_c.assign(i,5)
    for i in version_c.special:
        if not i in version_c.special_actual:
            version_c.wall.append(i)
    version_d=wall_optimize(version_c)
    if no_return:
        version_d.assign(version_a.start_position,0)
        version_d.start_position=None
    return version_d
