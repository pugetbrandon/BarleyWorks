import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
lineSize = 5

lineMaster = []
lineMaster.append([blue, [0, 0], [0, 0], 0])
lineMaster.append([blue, [266, 270], [266, 346], lineSize])
lineMaster.append([blue, [0, 0], [0, 0], 0])
lineMaster.append([blue, [266, 346], [288, 346], lineSize])
lineMaster.append([blue, [287, 330], [321, 330], lineSize])
lineMaster.append([blue, [350, 330], [368, 330], lineSize])
lineMaster.append([blue, [388, 349], [388, 424], lineSize])
lineMaster.append([blue, [388, 424], [189, 424], lineSize])
lineMaster.append([blue, [189, 424], [189, 67], lineSize])
lineMaster.append([blue, [189, 67], [278, 67], lineSize])
lineMaster.append([blue, [408, 330], [497, 330], lineSize])
lineMaster.append([blue, [587, 330], [587, 280], lineSize])
lineMaster.append([blue, [497, 330], [587, 330], lineSize])
lineMaster.append([blue, [732, 280], [732, 440], lineSize])
lineMaster.append([blue, [732, 440], [710, 440], lineSize])
lineMaster.append([blue, [710, 424], [672, 424], lineSize])
lineMaster.append([blue, [594, 424], [580, 424], lineSize])
lineMaster.append([blue, [541, 424], [517, 424], lineSize])
lineMaster.append([blue, [497, 330], [497, 405], lineSize])
lineMaster.append([blue, [441, 424], [479, 424], lineSize])
lineMaster.append([blue, [388, 424], [415, 424], lineSize])
lineMaster.append([blue, [561, 444], [561, 581], lineSize])
lineMaster.append([blue, [658, 440], [658, 489], lineSize])  #cooler
lineMaster.append([blue, [608, 440], [608, 489], lineSize])  #cooler

def changeGraphics(gameDisplay, component):

    if component[0] is True and component[1] is False:
        tLines = [1, 3, 4, 5, 6, 7, 8, 9]

    if component[0] is True and component[1] is True and component[3] is False:
        tLines = [1, 3, 4, 5, 10, 11, 12]

    if component[2] is True and component[3] is False and component[4] is False:
        tLines = [11, 12, 13, 14, 15, 16, 17, 18]

    if component[2] is True and component[3] is True and component[4] is False and component[0] is False:
        tLines = [7, 8, 9, 13, 14, 15, 16, 17, 19, 20]

    if component[2] is True and component[3] is False and component[4] is True:
        tLines = [13, 14, 15, 16, 21, 22, 23]

    if component[0] is False and component[2] is False:
        tLines = []

    if component[2] is True and component[0] is True:
        tLines = [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20]


    for iLines in tLines:
        pygame.draw.line(gameDisplay, *lineMaster[iLines])







