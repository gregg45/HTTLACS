import pygame

my_clock = pygame.time.Clock()
gravity = 0.02

class QueenSprite:

    def __init__(self,img,target_posn):
        """Create and initialise a queen for this 
           target position on the board
        """
        self.image = img
        self.target_posn = target_posn
        (x,y) = target_posn
        self.posn = (x,0)
        self.y_velocity = 0

    def update(self):
        self.y_velocity += gravity
        (x,y) = self.posn
        new_y_posn = y + self.y_velocity
        (target_x, target_y) = self.target_posn
        dist_to_go = target_y - new_y_posn

        if dist_to_go < 0:
            self.y_velocity = -0.65* self.y_velocity
            new_y_posn = target_y + dist_to_go
        self.posn = (x, new_y_posn)

    def draw(self,target_surface):
        target_surface.blit(self.image,self.posn)

    def contains_point(self,pt):
        """Return True if my sprite rectangle contains point pt """
        (my_x, my_y) = self.posn
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x,y) = pt
        return ( x >= my_x and x < my_x + my_width
            and y >= my_y and y < my_y + my_height)

    def handle_click(self):
        self.y_velocity += -2

class DukeSprite:
    def __init__(self,img,target_posn):
        self.image = img
        self.posn = target_posn
        self.anim_frame_count = 0
        self.curr_patch_num = 0

    def update(self):
        if self.anim_frame_count >0:
            self.anim_frame_count = (self.anim_frame_count + 1) % 60
            self.curr_patch_num = self.anim_frame_count // 6

    def draw(self,target_surface):
        patch_rect = (self.curr_patch_num * 50, 0, 50, self.image.get_height())
        target_surface.blit(self.image,self.posn,patch_rect)

    def handle_click(self):
        if self.anim_frame_count == 0:
            self.anim_frame_count = 5

    def contains_point(self,pt):
         """Return True if my sprite rectangle contains point pt """
         (my_x, my_y) = self.posn
         my_width = self.image.get_width()
         my_height = self.image.get_height()
         (x,y) = pt
         return ( x >= my_x and x < my_x + my_width
            and y >= my_y and y < my_y + my_height)

def draw_board(the_board):
    """ Draw a chess board with queens, from the_board. """

    pygame.init()
    colors = [(255,0,0),(0,0,0)]  # Set up the colors [red,black]
    all_sprites = []

    n = len(the_board)  # This is an N x N chess board.
    surface_sz = 480    # Proposed physical surface size.
    sq_sz = surface_sz // n # sq_sz is the length of a square.
    surface_sz = n * sq_sz  # Adjust to exactly fit n squares.

    # Create the surface of (width,height), and its window.
    surface = pygame.display.set_mode((surface_sz,surface_sz))
    
    # Load Zelda
    zelda = pygame.image.load("zelda.png")
    # Load duke
    duke_sprite_sheet = pygame.image.load("duke_spritesheet.png")

    # Instantiate two duke instances, put them on the chessboard
    duke1 = DukeSprite(duke_sprite_sheet,(sq_sz*2,0))
    duke2 = DukeSprite(duke_sprite_sheet,(sq_sz*5,sq_sz))
    # Add tem to the list of sprites
    all_sprites.append(duke1)
    all_sprites.append(duke2)

    # Use an extra offset to centre the zelda in its square.
    ball_offset = (sq_sz-zelda.get_width()) // 2

    for (col, row) in enumerate(the_board):
        a_queen = QueenSprite(zelda,(col*sq_sz+ball_offset,row*sq_sz+ball_offset))
        all_sprites.append(a_queen)
        #surface.blit(zelda,(col*sq_sz+ball_offset, row*sq_sz+ball_offset))

    while True:
        # Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:   # Window close button clicked?
            break 
        if ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == 27:
                break
            if key == ord("r"):
                colors[0] = (255,0,0)
            elif key == ord("g"):
                colors[0] = (0,255,0)
            elif key == ord("b"):
                colors[0] = (0,0,255)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            posn_of_click = ev.dict["pos"]
            for sprite in all_sprites:
                if sprite.contains_point(posn_of_click):
                    sprite.handle_click()
                    break

        # Draw a fresh background (a blank chess board)
        for row in range(n):  # Draw each row of the board
            c_indx = row % 2  # Change starting color on each row
            for col in range(n):
                the_square = (col*sq_sz,row*sq_sz,sq_sz,sq_sz)
                surface.fill(colors[c_indx],the_square)
                # now flip the color index for the next square
                c_indx = (c_indx + 1) % 2

        for sprite in all_sprites:
            sprite.update()

        for sprite in all_sprites:
            sprite.draw(surface)

        my_clock.tick(60)
        pygame.display.flip()

draw_board([4, 0, 3, 5, 7, 2, 6, 2])