# AI in videogames project

### Report by snake game project

Author: Artyom Sakhabutdinov, group 145

### Using technologies: ###
  - Python
  - Pygame

### Game rules ###

At the beginning of the game, we have a one dot - square 1x1 on the table of 20x20, which located in the center - (10; 10).It's our snake. Also, we spawn an apple on the random postition of the table, which is not marked as our snake. Snake can not bump into walls and itself. If snake doing something like that forbidden rules, game over have comming. Aim of the game for snake - eat as much apples as possible. And in addition, we have only increasing apples - when snake ate an apple, the length of the snake will increase to 1 square.

### Algorithm ###

I've used wave algorithm which starts at the respawned food. At the first step we want to see from which legal positions apple can be reached. All this positions we put in the queue, in destination graph for this positions we assign value 1. Then I repeat this procedure for all elements in the queue and give distance by 1 bigger then parent of the element have. After this actions, our snake can be moved to the position, which have minimal distance in distance graph and are allowded - snake can not move back, I mean that example when snake was moved up and the next step was moving down(it will lead to game over, because snake will bump into itself). When snake reach the food position, we delete old eaten food and spawn new, also we increase points.

The main problem of this algorithm - snake can't think about locked areas, which appeared when our player will grow and for example, snake fold in the circle and then new apple respawn in this circle, but head of the snake is out. It leads to game over.

Youtube link:
https://youtu.be/eIcdcLMp5wk