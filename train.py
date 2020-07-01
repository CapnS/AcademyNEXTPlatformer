import pygame
import random
import sys
from generator import Generator
from character import Character
from platformclass import Platform
from enemy import Enemy
import neat
import os

#init pygame and create screen
pygame.init()
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])


#create a list of things to call move function on...
#all platforms should be moved by a set amount left every time the game loop continues


#create an instance of the Generator class to create platforms and enemies
#given the width of the screen
PLATFORM_WIDTH, PLATFORM_HEIGHT = 150, 20
GENERATOR = Generator(WIDTH, HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)

#simple bg art
X = 600
Y = 600
ground_tiles = pygame.image.load(os.path.join('sprite_art','Multi_Platformer_Tileset_v2','Grassland','Background','GrassLand_Background_3.png'))
background = pygame.image.load(os.path.join('sprite_art','Multi_Platformer_Tileset_v2','Grassland','Background','GrassLand_Background_2.png'))
further_background = pygame.image.load(os.path.join('sprite_art','Multi_Platformer_Tileset_v2','Grassland','Background','GrassLand_Background_1.png'))
sky = (173, 216, 230)

#add basic platforms
def main(genomes, config):
    running = True
    platforms = []
    bullets = []
    
    platforms.append(Platform(0, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    platforms.append(Platform(300, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    platforms.append(Platform(600, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    platforms.append(Platform(800, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT))

    nets = []
    ge = []
    characters = []
    characterz = pygame.sprite.Group()
    for g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g[1], config)
        nets.append(net)
        char = Character(platforms, bullets)
        characters.append(char)
        characterz.add(char)
        g[1].fitness = 0
        ge.append(g[1])



    #loop vars
    counter = 0
    last_platform_height = 300
    new_platform_mod = 15
    score = 0
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        if not len(characters):
            running = False
            break

        tick = clock.tick(30)
        for i in range(len(platforms)):
            try:
                if platforms[i].move(tick):
                    platforms.remove(platforms[i])
                    i -= 1
            except:
                pass

        SCREEN.fill(sky)
        SCREEN.blit(further_background, (0, Y - 520))
        SCREEN.blit(background, (0, Y - 460))
        SCREEN.blit(ground_tiles, (0, Y - 400))
        

        #generate new platforms
        counter += 1
        if (counter % new_platform_mod == 0):
            plat = GENERATOR.add_platform(last_platform_height)
            last_platform_height = plat.rect.y
            platforms.append(plat)
            new_platform_mod = random.randint(50,80)
            counter = 0
            score += 1
            print(score)

        #blit platforms
        for o in platforms:
            SCREEN.blit(o.image, o.rect)
        

        for i, character in enumerate(characters):
            ge[i].fitness += character.rect.x / 200
            p_index = 0
            for p in platforms:
                if character.rect.x > p.rect.left:
                    p_index += 1
                    ge[i].fitness += .1
                else:
                    break

            ge[i].fitness += .01

            output = nets[i].activate((character.rect.x, character.rect.y, platforms[p_index].rect.left, platforms[p_index].rect.right, platforms[p_index].rect.y, 600 - character.rect.x))[0]

            if output < .25:
                pass
            elif output > .25 and output < .75:
                character.move(10, 0)
            else:
                if not character.jumping and character.can_jump:
                    character.jumping = True

            
            character.update()
            
            if character.rect.y > HEIGHT:
                ge[i].fitness -= 1
                char = characters.pop(i)
                nets.pop(i)
                ge.pop(i)
                characterz.remove(char)


            if character.rect.x > 600:
                ge[i].fitness -=.1
                char = characters.pop(i)
                nets.pop(i)
                ge.pop(i)
                characterz.remove(char)


            if character.rect.x == 0:
                ge[i].fitness -=5
                char = characters.pop(i)
                nets.pop(i)
                ge.pop(i)
                characterz.remove(char)

            SCREEN.blit(character.image, character.rect)

        characterz.draw(SCREEN)
        pygame.display.flip()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)