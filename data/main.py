import random, pygame, sys, asyncio, pickle
from pygame.locals import *

datapath = "./data/dat.bin"
highscore = []
scoreds = 0

# hs = [0 for x in range(5)]
# with open(datapath, "wb") as file:
#     pickle.dump(hs, file)

with open(datapath, "rb") as file:
    highscore = pickle.load(file)

async def main():
    while (True):
        #             R    G    B
        WHITE     = (255, 255, 255)
        BLACK     = (  0,   0,   0)
        RED       = (255,   0,   0)
        GREEN     = (  0, 255,   0)
        DARKGREEN = (  0, 155,   0)
        YELLOW    = (255, 255,   0)

        randomApplecolor = RED
        randomWormcolor = GREEN
        randomScreencolor = BLACK
        mute = False
        paused = False
        pausedVar = 1

        UP = 'up'
        DOWN = 'down'
        LEFT = 'left'
        RIGHT = 'right'

        HEAD = 0 

        def musicOnOffToggle():
            nonlocal mute
            if (mute):
                pass
                bgObj.play(loops = -1)
            else:
                pass
                bgObj.stop()
            mute = not mute

        def PauseToggle():
            nonlocal paused, pausedVar
            if (paused):
                pausedVar = 1
            else:
                pausedVar = 0
            paused = not paused
        
        def showHighScore():
            global highscore
            hsFont = pygame.font.Font('freesansbold.ttf', 150)
            hsSurf = hsFont.render('HIGHSCORES', True, YELLOW)
            hsTRect = hsSurf.get_rect()
            hsTRect.midtop = (WINDOWWIDTH / 2, 10)
            DISPLAYSURF.blit(hsSurf, hsTRect)
            hssFont = pygame.font.Font('freesansbold.ttf', 60)
            hsSurfaces = [hssFont.render('{}'.format(x), True, WHITE) for x in highscore]; i = 0
            for hs in hsSurfaces:
                hsRect = hs.get_rect()
                hsRect.midtop = (WINDOWWIDTH/2, hsTRect.height + 100 + (70*i)); i+=1
                DISPLAYSURF.blit(hs, hsRect)

            drawPressKeyMsg("H")
            pygame.display.update()
            pygame.time.wait(500)
            checkForKeyPress()

            while True:
                if checkForKeyPress():
                    pygame.event.get()
                    return

        def runGame():
            nonlocal flag1
            # Set a random start point.
            startx = random.randint(5, CELLWIDTH // 2)
            starty = random.randint(5, CELLHEIGHT // 2)
            wormCoords = [{'x': startx,   'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
            direction = RIGHT

            # Start the apple in a random place.
            apple = getRandomLocation()
            
            while True: # main game loop
                nonlocal FPS, pausedVar
                for event in pygame.event.get(): # event handling loop
                    if event.type == QUIT:
                        terminate()
                    elif (pausedVar):
                        if event.type == KEYDOWN:
                            if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                                direction = LEFT
                            elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                                direction = RIGHT
                            elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                                direction = UP
                            elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                                direction = DOWN
                            elif (event.key == K_m):
                                musicOnOffToggle()
                            elif (event.key == K_h):
                                PauseToggle()
                                showHighScore()
                                PauseToggle()
                            elif (event.key == K_p):
                                PauseToggle()
                            elif (event.key == K_ESCAPE):
                                terminate()
                    elif (event.type == KEYDOWN and event.key == K_p):
                        PauseToggle()
                    elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                        terminate()

                # check if the worm has hit itself or the edge
                if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
                    dieObj.play()
                    FPS = FPS001
                    showGameOverScreen()
                    return # game over
                for wormBody in wormCoords[1:]:
                    if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                        dieObj.play()
                        FPS = FPS001
                        showGameOverScreen()
                        return # game over

                # check if worm has eaten an apple
                if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
                    FPS += 3            
                    eatObj.play()
                    apple = getRandomLocation() # set a new apple somewhere and set colors if needed
                else:
                    if (pausedVar):
                        del wormCoords[-1]

                if (pausedVar):
                    if direction == UP:
                        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - pausedVar}
                    elif direction == DOWN:
                        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + pausedVar}
                    elif direction == LEFT:
                        newHead = {'x': wormCoords[HEAD]['x'] - pausedVar, 'y': wormCoords[HEAD]['y']}
                    elif direction == RIGHT:
                        newHead = {'x': wormCoords[HEAD]['x'] + pausedVar, 'y': wormCoords[HEAD]['y']}

                # move the worm by adding a segment in the direction it is moving
                # if direction == UP:
                #     newHead = {'x': (wormCoords[HEAD]['x']) % CELLWIDTH, 'y': (wormCoords[HEAD]['y'] - 1) % CELLHEIGHT}
                # elif direction == DOWN:
                #     newHead = {'x': (wormCoords[HEAD]['x']) % CELLWIDTH, 'y': (wormCoords[HEAD]['y'] + 1) % CELLHEIGHT}
                # elif direction == LEFT:
                #     newHead = {'x': (wormCoords[HEAD]['x'] - 1) % CELLWIDTH, 'y': (wormCoords[HEAD]['y'] % CELLHEIGHT)}
                # elif direction == RIGHT:
                #     newHead = {'x': (wormCoords[HEAD]['x'] + 1) % CELLWIDTH, 'y': (wormCoords[HEAD]['y'] % CELLHEIGHT)}

                if (pausedVar):
                    wormCoords.insert(0, newHead)
                else:
                    wormCoords = wormCoords

                DISPLAYSURF.fill(randomScreencolor)
                drawGrid()
                drawWorm(wormCoords)
                drawApple(apple)
                global scoreds

                scoreds = len(wormCoords) - 3
                drawScore(len(wormCoords) - 3)
                
                pygame.display.update()
                FPSCLOCK.tick(FPS)

        def drawPressKeyMsg(key = "any key"):
            pressKeySurf = BASICFONT.render('Press {} to play.'.format(key), True, WHITE)
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
            DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        def checkForKeyPress():
            if len(pygame.event.get(QUIT)) > 0:
                terminate()

            keyUpEvents = pygame.event.get(KEYUP)
            if len(keyUpEvents) == 0:
                return None
            if keyUpEvents[0].key == K_ESCAPE:
                terminate()
            return keyUpEvents[0].key

        def showStartScreen():
            nonlocal randomScreencolor
            if (randomScreencolor == BLACK):
                r, g, b = 0, 100, 0
            else:
                r, g, b = randomScreencolor
            titleFont = pygame.font.Font('freesansbold.ttf', 100)
            titleSurf1 = titleFont.render('Snake', True, WHITE, (50 + r//2, 50 + g//2, 50 + b//2))
            titleSurf2 = titleFont.render('PRO', True, (155+ r, 155+ g, 155+ b))

            degrees1 = 0
            degrees2 = 0
            while True:
                DISPLAYSURF.fill(randomScreencolor)
                rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
                rotatedRect1 = rotatedSurf1.get_rect()
                rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
                DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

                rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
                rotatedRect2 = rotatedSurf2.get_rect()
                rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
                DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

                drawPressKeyMsg()

                if checkForKeyPress():
                    pygame.event.get() # clear event queue
                    runGame()
                    return
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                degrees1 += 3.5 
                degrees2 += 7 

        def terminate():
            pygame.quit()
            sys.exit()

        def getRandomLocation():
            nonlocal randomApplecolor, randomScreencolor, randomWormcolor
            randomWormcolor = randomApplecolor
            randomApplecolor = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

            if ((scoreds + 1) % 10 == 0):
                randomScreencolor = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
            return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

        def showGameOverScreen():
            nonlocal pausedVar
            global scoreds, highscore
            gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
            insultFont = pygame.font.Font('freesansbold.ttf', 80)
            gameSurf = gameOverFont.render('Game', True, RED)
            overSurf = gameOverFont.render('Over', True, RED)
            insultSurf = insultFont.render('YOUR SCORE: {}'.format(scoreds) ,True, WHITE)
                
            gameRect = gameSurf.get_rect()
            overRect = overSurf.get_rect()
            insultRect = insultSurf.get_rect()
            
            gameRect.midtop = (WINDOWWIDTH / 2, 10)
            overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 15)
            insultRect.midtop = (WINDOWWIDTH/2 ,overRect.height + 10 + 25 + 160)

            DISPLAYSURF.blit(gameSurf, gameRect)
            DISPLAYSURF.blit(overSurf, overRect)
            DISPLAYSURF.blit(insultSurf, insultRect)

            if (scoreds > highscore[0]):
                newhighschoreFont = pygame.font.Font('freesansbold.ttf', 80)
                newhighscoreSurf = newhighschoreFont.render("NEW HIGH SCORE!", True, YELLOW)
                newhighschoreRect = newhighscoreSurf.get_rect()
                newhighschoreRect.midtop = (WINDOWWIDTH/2 ,insultRect.height + 10 + 25 + 160 + 10 + 160)
                DISPLAYSURF.blit(newhighscoreSurf, newhighschoreRect)
            highscore.append(scoreds)
            highscore.sort(reverse=True)
            highscore = highscore[:5]
            with open(datapath, "wb") as file:
                pickle.dump(highscore, file)
            
            scoreds = 0
            pausedVar = 1
            drawPressKeyMsg()
            pygame.display.update()
            pygame.time.wait(500)
            checkForKeyPress()

            while True:
                if checkForKeyPress():
                    pygame.event.get()
                    return
                
        def drawScore(score):
            scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft = (WINDOWWIDTH - 120, 10)
            DISPLAYSURF.blit(scoreSurf, scoreRect)

            highscoreSurf = BASICFONT.render('Highscore: %s' % (highscore[0]), True, YELLOW)
            highscoreRect = highscoreSurf.get_rect()
            highscoreRect.topleft = (40, 10)
            DISPLAYSURF.blit(highscoreSurf, highscoreRect)

        def drawWorm(wormCoords):
            for coord in wormCoords:
                x = coord['x'] * CELLSIZE
                y = coord['y'] * CELLSIZE
                wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                r, g, b = randomWormcolor
                pygame.draw.rect(DISPLAYSURF, (r, g, b), wormSegmentRect)
                wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
                pygame.draw.rect(DISPLAYSURF, (r//2, g//2, b//2) , wormInnerSegmentRect)


        def drawApple(coord):
            nonlocal randomApplecolor
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, randomApplecolor, appleRect)


        def drawGrid():
            r, g, b = randomScreencolor
            for x in range(0, WINDOWWIDTH, CELLSIZE):
                pygame.draw.line(DISPLAYSURF, (r//2, g//2, b//2) , (x, 0), (x, WINDOWHEIGHT))
            for y in range(0, WINDOWHEIGHT, CELLSIZE):
                pygame.draw.line(DISPLAYSURF, (r//2, g//2, b//2), (0, y), (WINDOWWIDTH, y))


        flag1 = 0
        WINDOWWIDTH = 1280
        WINDOWHEIGHT = 640
        FPS = 20
        CELLSIZE = 16

        CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
        CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

        pygame.init()
        eatObj = pygame.mixer.Sound('./audio/eat.ogg')
        dieObj = pygame.mixer.Sound('./audio/die.ogg')
        bgObj = pygame.mixer.Sound('./audio/bgm.ogg')
        bgObj.play(loops = -1)
        bgObj.set_volume(0.5)

        FPS001 = FPS

        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Pro! Snake')

        while True:
            showStartScreen()
            await asyncio.sleep(0)
       

asyncio.run(main())
