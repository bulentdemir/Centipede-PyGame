import pygame

from Enemy import Enemy
from Mushroom import Mushroom
from Player import Player
from Point import Point
from LevelManager import LevelManager

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Initializing pygame and pygame.mixer
pygame.init()
pygame.mixer.init()

screenwidth = 800
screenheight = 600

# Create an 800x600 sized screen
screen = pygame.display.set_mode([screenwidth, screenheight])

# Title of the window
pygame.display.set_caption('Centipede V1.1', 'Cntpd...')

# mouse disappear
pygame.mouse.set_visible(0)

# Font
font = pygame.font.Font("font/AtariClassic-gry3.ttf", 20)
titleFont = pygame.font.SysFont("comicsansms", 90)
authorFont = pygame.font.Font(None, 18)

# Surface
background = pygame.Surface(screen.get_size())

# Sprite Groups
bullets = pygame.sprite.Group()
allSprites = pygame.sprite.Group()

# Assignments
player = Player()
allSprites.add(player)
points = []
levelManager = LevelManager(3)

# Clock to limit speed
clock = pygame.time.Clock()

# Checking
game_over = False
win_screen = False
exit_program = False
initial_screen = True

heart = pygame.image.load("images/heart.gif")
liveInfo = font.render("Live: ", True, white)
initial_screen_image = pygame.image.load("images/initialScreen.gif")
mainSound = pygame.mixer.Sound("sounds/main.ogg")
mainSound.play(-1)

def addPoint(point, bullet):
    player.activeStuff.play()
    points.append(Point("+" + str(point), bullet.rect, red))
    bullets.remove(bullet)
    allSprites.remove(bullet)
    player.point += point

def initial_Screen():
    title = titleFont.render("CENTIPEDE", True, white)
    titlePos = title.get_rect(centerx=background.get_width() / 2, centery=250)
    screen.blit(title, titlePos)

    initial_screen_image_pos = (background.get_width() / 2 - 310, 160)
    screen.blit(initial_screen_image, initial_screen_image_pos)

    description = font.render("press any key to start", True, white)
    descriptionPos = description.get_rect(centerx=background.get_width() / 2, centery=330)
    screen.blit(description, descriptionPos)

    author = authorFont.render("This Game is completely codded by Bulent Demir", True, white)
    authorPos = author.get_rect(centerx=background.get_width() - author.get_width() / 2 - 10,
                                centery=background.get_height() - author.get_height() / 2 - 10)
    screen.blit(author, authorPos)

def addMushroom(level, x, y, dirX):
    posY = int(y / 25) * 25
    if dirX == 1:
        posX = int((x + 5) / 25) * 25
    else:
        posX = int((x - 5) / 25) * 25
    mushroom = Mushroom(posX, posY)
    level.MushroomList.add(mushroom)
    level.levelSprites.add(mushroom)

def removeEnemyPiece(level, enemy, i):
    level.levelSprites.remove(enemy.pieces[i].feet)
    level.EnemyPieces.remove(enemy.pieces[i])
    level.levelSprites.remove(enemy.pieces[i])
    enemy.pieces.remove(enemy.pieces[i])
# And the L(oop) including the E(vents)
# Main program loop

while not exit_program:
    # Limit to 30 fps
    clock.tick(70)
    # Clear the screen
    screen.fill(black)
    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit_program = True
            initial_screen = False

    if initial_screen:
        initial_Screen()

    else:
        screen.blit(background, background.get_rect())
        pygame.draw.line(background, white, (0, background.get_height() / 2),
                         (background.get_width(), background.get_height() / 2), 1)
        if not (game_over or win_screen):
            level = levelManager.Levels[player.level - 1]

            if levelManager.inTransition:
                text = font.render("Press enter to next level", True, white)
                textPos = text.get_rect(centerx=background.get_width() / 2,
                                        centery=background.get_height() - text.get_height() / 2)
                screen.blit(text, textPos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        levelManager.inTransition = False
            else:
                if levelManager.levelTime < levelManager.levelTimeMax:
                    levelManager.update()
                    text = font.render("Level: " + str(player.level), True, white)
                    textPos = text.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 2)
                    screen.blit(text, textPos)
                player.handle_event(event, bullets, allSprites, level.MushroomList)

                level.SpyderSprites.update(level.MushroomList)
                level.MushroomerSprites.update(level)
                level.GhostSprites.update(level)
                level.update()

                if not player.isReborn:
                    if pygame.sprite.spritecollide(player, level.SpyderSprites, False) \
                            or pygame.sprite.spritecollide(player, level.EnemyPieces, False)\
                            or pygame.sprite.spritecollide(player, level.MushroomerSprites, False)\
                            or pygame.sprite.spritecollide(player, level.GhostSprites, False):
                        player.liveReduce.play()
                        player.live -= 1
                        player.isReborn = True
                        player.rebornCounter = 0
                        if player.live == 0:
                            game_over = True
                        player.resetPosition()
                else:
                    player.reborn()

                if len(level.EnemyList):
                    for enemy in level.EnemyList:
                        if len(enemy.pieces):
                            enemy.update(level.MushroomList)
                        else:
                            level.EnemyList.remove(enemy)
                            level.levelSprites.remove(enemy)

                if len(level.EnemyList):
                    if len(bullets):
                        for bullet in bullets:
                            deadMushrooms = pygame.sprite.spritecollide(bullet, level.MushroomList, False)
                            if len(deadMushrooms):
                                bullets.remove(bullet)
                                allSprites.remove(bullet)
                            for mushroom in deadMushrooms:
                                if mushroom.live != 1:
                                    mushroom.live -= 1
                                    mushroom.changeImage()
                                else:
                                    player.mushroomSound.play()
                                    points.append(Point("+1", mushroom.rect, yellow))
                                    level.MushroomList.remove(mushroom)
                                    level.levelSprites.remove(mushroom)
                                    player.point += 1
                            if pygame.sprite.spritecollide(bullet, level.SpyderSprites, True):
                                addPoint(600, bullet)
                                break
                            elif pygame.sprite.spritecollide(bullet, level.MushroomerSprites, True):
                                addPoint(200, bullet)
                                break
                            elif pygame.sprite.spritecollide(bullet, level.GhostSprites, True):
                                addPoint(1000, bullet)
                                break

                            for enemy in level.EnemyList:
                                if len(enemy.pieces):
                                    for i in range(len(enemy.pieces)):
                                        if bullet.rect.colliderect(enemy.pieces[i].rect):
                                            player.activeStuff.play()
                                            bullets.remove(bullet)
                                            allSprites.remove(bullet)
                                            if i == 0:
                                                addMushroom(level, enemy.pieces[i].rect.x, enemy.pieces[i].rect.y, enemy.pieces[i].directionX)
                                                points.append(Point("+100", enemy.pieces[i].rect, red))
                                                removeEnemyPiece(level, enemy, i)

                                                if len(enemy.pieces) > 0:
                                                    enemy.pieces[0].updateImageWAngle("Head")
                                                player.point += 100
                                                break
                                            elif 0 < i < len(enemy.pieces) - 1:
                                                level.levelSprites.remove(enemy.pieces[i].feet)
                                                addMushroom(level, enemy.pieces[i].rect.x, enemy.pieces[i].rect.y, enemy.pieces[i].directionX)

                                                points.append(Point("+10", enemy.pieces[i].rect, blue))

                                                enemy2 = Enemy(enemy.velocity, enemy.directionX, enemy.directionY)
                                                enemy2.pieces = enemy.pieces[i + 1:]
                                                enemy2.pieces[0].updateImageWAngle("Head")
                                                enemy.pieces = enemy.pieces[:i + 1]
                                                level.EnemyList.append(enemy2)

                                                removeEnemyPiece(level, enemy, i)
                                                player.point += 10
                                                break
                                            elif i == len(enemy.pieces) - 1:
                                                addMushroom(level, enemy.pieces[i].rect.x, enemy.pieces[i].rect.y, enemy.pieces[i].directionX)
                                                points.append(Point("+10", enemy.pieces[i].rect, blue))
                                                removeEnemyPiece(level, enemy, i)
                                                player.point += 10
                                                break
                            bullet.update()
                            if bullet.rect.y <= 25:
                                bullets.remove(bullet)
                                allSprites.remove(bullet)
                                break
                else:
                    if len(levelManager.Levels) > player.level:
                        player.levelPassing.play()
                        player.level += 1
                        player.resetPosition()
                        levelManager.inTransition = True
                        levelManager.levelTime = 0
                        for bul in bullets:
                            allSprites.remove(bul)
                        bullets.empty()
                    else:
                        win_screen = True

                if len(points):
                    for point in points[::-1]:
                        if point.counter < point.counterMax:
                            screen.blit(point.font, point.pos)
                            point.update()
                        else:
                            points.remove(point)

        allSprites.draw(screen)
        level.levelSprites.draw(screen)

        # If we are done, print game over
        if game_over:
            text = font.render("Game Over", True, white)
            textPos = text.get_rect(centerx=background.get_width() / 2)
            textPos.top = 300
            screen.blit(text, textPos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    allSprites.empty()
                    player = Player()
                    allSprites.add(player)
                    levelManager = LevelManager(3)
                    game_over = False

        if win_screen:
            text = font.render("You Won The Centipede!", True, white)
            textPos = text.get_rect(centerx=background.get_width() / 2)
            textPos.top = 300
            screen.blit(text, textPos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    allSprites.empty()
                    player = Player()
                    allSprites.add(player)
                    levelManager = LevelManager(3)
                    win_screen = False

        # Information will be edited
        screen.blit(liveInfo, (0, 0))
        for i in range(player.live):
            screen.blit(heart, (i * 30 + 100, 0))

        pointInfo = font.render("Score:" + str(player.point).zfill(8), True, white)
        pointInfoPos = pointInfo.get_rect(centerx=background.get_width() / 2)
        screen.blit(pointInfo, pointInfoPos)

        # level
        levelInfo = font.render("Level:" + str(player.level), True, white)
        levelInfoPos = levelInfo.get_rect(centerx=background.get_width() - levelInfo.get_size()[0] / 2)
        screen.blit(levelInfo, levelInfoPos)
        # End of information

    # Flip the screen and show what we've drawn
    pygame.display.flip()

# This is to ensure the termination of the game
pygame.quit()
quit()
