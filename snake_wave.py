import pygame
import random


def blit_grid():
	for x in range(block_width):
		pygame.draw.aaline(screen, (255, 255, 255), (x * block_width,0),(x * block_width, 400))
	for y in range(block_width):
		pygame.draw.aaline(screen, (255, 255, 255), (0, y * block_width),(400, y * block_width))


def make_graph():
	queue = [food]
	marked = []
	for i in range(block_width):
		for j in range(block_width):
			distances[i][j] = max_dest
	distances[food[0]][food[1]] = 0
	while len(queue) != 0:
		parent = queue[0]
		marked.append(parent)
		sides = []
		for i, j in shifts.items():
			sides.append([parent[0] + j[0], parent[1] + j[1]])
		for dest in sides:
			if reliable_neighbour(dest, marked, queue):
				if distances[dest[0]][dest[1]] != max_dest + 1:
					distances[dest[0]][dest[1]] = distances[parent[0]][parent[1]] + 1
				queue.append(dest)
		queue.pop(0)


def reliable_neighbour(dest, marked, queue):
	if dest in queue or dest in marked or tuple(dest) in list(zip(snake_x, snake_y)) or dest[0] < 0 or \
	dest[0] >= block_width or dest[1] < 0 or dest[1] >= block_width:
		return False
	else:
		return True

def calc_dest_for_shift(key, value):
	new_pos_x, new_pos_y = snake_x[0] + value[0], snake_y[0] + value[1]

	if new_pos_y >= block_width or new_pos_y < 0 or new_pos_x >= block_width or new_pos_x < 0 or \
	[new_pos_x, new_pos_y] in zip(snake_x[1:], snake_y[1:]):
		return key, max_dest + 1
	else:
		return key, distances[new_pos_x][new_pos_y]

def move_snake():
	new_x = 0
	new_y = 0
	for i, j in dirs.items():
		if direction == j:
			new_x = snake_x[0] + shifts[i][0]
			new_y = snake_y[0] + shifts[i][1]

	if new_x < 0 or new_x >= 20 or new_y < 0 or new_y >= 20 or \
	tuple([new_x, new_y]) in list(zip(snake_x, snake_y)):
		main()

	snake_x.insert(0, new_x)
	snake_y.insert(0, new_y)

	global food, point

	if [new_x, new_y] != food:
		snake_x.pop()
		snake_y.pop()
	else:
		food = list(spawn_food())
		point += 1

def spawn_snake():
	for i in range(len(snake_x)):
		x_, y_ = snake_x[i] * block_width, snake_y[i] * block_width
		if i == 0:
			rect = pygame.Rect(snake_x[0] * block_width, snake_y[0] * block_width, 20, 20)
			pygame.draw.rect(screen, (0, 255, 0), rect)
		else:
			rect = pygame.Rect(x_, y_, 20, 20)
			pygame.draw.rect(screen,(255, 255, 255),rect)
	pygame.display.update()

def spawn_food():
	food_x, food_y = random.randint(0, 19), random.randint(0, 19)

	while tuple([food_x, food_y]) in list(zip(snake_x, snake_y)):
		food_x, food_y = random.randint(0, 19), random.randint(1, 19)

	rect = pygame.Rect(food_x * block_width, food_y * block_width, 20, 20)
	pygame.draw.rect(screen,(255, 0, 0), rect)
	return food_x, food_y

def update():
	move_snake()
	spawn_snake()
	make_graph()


def main():

	global block_width, screen, snake_x, snake_y, food, max_dest, distances, shifts, dirs, direction, point
	block_width = 20
	width = 400
	height = 400
	pygame.init()

	start = True
	screen = pygame.display.set_mode((width, height), 0, 32)
	clock = pygame.time.Clock()
	point = 0
	snake_x, snake_y = [10], [10]
	distances = []
	max_dest = 1000
	direction = ""
	shifts = {0: [-1, 0], 
				1: [1, 0],
				2: [0, -1],
				3: [0, 1]}

	forbidden_dirs = {0: "right",
						1: "left",
						2: "down",
						3: "up",
						4: ""}
	
	dirs = {0: "left",
			1:"right",
			2:"up",
			3:"down"}

	for i in range(block_width):
		distances.append([])
		for j in range(block_width):
			distances[i].append([])


	screen.fill((0,0,0))
	blit_grid()
	font = pygame.font.SysFont('Comic Sans MS',30)
	point_ = font.render(str(point),True,(255,255,255))
	screen.blit(point_,(0,0))
	food = list(spawn_food())
	pygame.display.update()
	make_graph()

	while True:

		clock.tick(15)

		if not start:
			screen.fill((0,0,0))
			blit_grid()
			font = pygame.font.SysFont('Comic Sans MS',30)
			point_ = font.render(str(point),True,(255,255,255))
			screen.blit(point_,(0,0))
			rect = pygame.Rect(food[0] * block_width, food[1] * block_width, 20, 20)
			pygame.draw.rect(screen,(255, 0, 0), rect)

		start = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		sides = 4
		# shifts = {0: [-1, 0], 1: [1, 0], 2: [0, -1], 3: [0, 1]}
		# {0: "left", 1:"right", 2:"up", 3:"down"}
		best_shift_dests = [max_dest + 1 for i in range(sides)]

		for i, j in shifts.items():
			tmp_key, tmp_val = calc_dest_for_shift(i, j)
			best_shift_dests[tmp_key] = tmp_val


		for i in range(len(best_shift_dests)):
			if best_shift_dests[i] != max_dest and best_shift_dests[i] != max_dest + 1 and \
			distances[snake_x[0] + shifts[i][0]][snake_y[0] + shifts[i][1]] == min(best_shift_dests) and \
			direction != forbidden_dirs[i]:
				direction = dirs[i]
				break

		update()

main()