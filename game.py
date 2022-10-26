import pygame, sys, random



# convert giúp chuyển hình ảnh thành file nhẹ hơn- ko bắt buộc
#Tạo hàm cho trò chơi
# hàm cho sàn chạy lùi về sau
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
# hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos)) #tạo hình chữ nhật bao quanh ống và chiều cao ống  dưới
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-650))# như trên và chiều cao ống từ trên xuống
    return bottom_pipe, top_pipe
# hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 5
    return pipes
# Vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : # => đây là ống dưới
            screen.blit(pipe_surface,pipe)
        else: # => đây là ống trên
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)# quay ngược ống lại( trục x, y=> muốn quay theo trục nào thì true trục ý)
            screen.blit(flip_pipe,pipe)
# Xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # nếu va chạm
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: # nếu vượt qua màn hình
            return False
    return True 
#xoay bird (xuay lên xuống)
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)# (tên  ,xoay , kích thước ảnh)
    return new_bird
# Hàm tạo hiệu ứng đập cánh
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
# điểm
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
# Set màn hình()
screen= pygame.display.set_mode((432,768))
# set thời gian 
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',35)# font chữ(tên font,font-size)
#Tạo các biến cho trò chơi
gravity = 0.25 #trọng lực
bird_movement = 0 # chuyển động của bird 
game_active = True # biến thoát trò chơi(game có hoạt động hay ko - false thì game kết thức)
score = 0# diểm 
high_score = 0 # diểm cao
#chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)# phóng to bg lên X2
#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0  # tọa độ sàn pos:posison- khi Bird di chuyển thì sàn cũng đi theo 
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]# thích bird nào thì đổi index sang đấy
#bird= pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))# tạo hình chữ nhật bao quanh con chim để kiểm tra có chạm cột ko
# cách trục x=100 ,y=384

#tạo timer cho bird
birdflap = pygame.USEREVENT + 1# + 1 là để phân biệt bới cái  của cột
pygame.time.set_timer(birdflap,200)
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[] # lưu các ống tạo ra
#tạo timer  cho ống
# xuất hiện ống liên tục
spawnpipe= pygame.USEREVENT
# Mốc thời gian
pygame.time.set_timer(spawnpipe, 1200)# sau 1.2s thì nó tạo ống mới
pipe_height = [200,300,400]# chiều dài ống
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
# while loop của trò chơi- vòng lặp game (hình ảnh game hienj trên mnaf hình là sự 
#  chớp chớp liên tục của màn hình)
while True:
    # lấy tất cả sự kiện pygame xảy ra
    for event in pygame.event.get():
        # tạo sự kiện phím ấn vào và thoát cửa sổ game ra
        if event.type == pygame.QUIT:
            pygame.quit()
            # thoát hệ thống
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 # set lại =0
                bird_movement =-11 # làm cho trọng lực hướng lên( y âm là đi lên)
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True 
                pipe_list.clear()# xóa ống cũ đi ko thì sẽ gây rối
                bird_rect.center = (100,384) # reset con bird 
                bird_movement = 0  # reset chuyển động bird
                score = 0 
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())# thêm ống vào danh sách các ống
            # create_pipe : cho py biết mình tạo ống tiếp theo
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation()    
    # thêm hình ảnh lên màn hình (vẽ chèn hình ảnh này lên màn hình)       
    screen.blit(bg,(0,0))# (0,0) góc tọa độ
    if game_active: # nếu game hoạt động
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)       
        bird_rect.centery += bird_movement # chim tự động bay xuống dưới do có trọng lực
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision(pipe_list)# kiểm tra có va chạm để kết thức ko
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #sàn
    floor_x_pos -= 1 # sàn di chuyển về phí bên trái
    draw_floor()
    if floor_x_pos <= -432:# khi sàn vượt qua sàn thứ 2 thì sàn 1 lập tức thay thế vào
        floor_x_pos =0
    # hiện lên màn hình
    pygame.display.update()
    # set tốc độ trò chơi
    clock.tick(60)