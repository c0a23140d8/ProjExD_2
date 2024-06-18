import os
import time
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {# 移動量の辞書
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, +5), 
        pg.K_LEFT:(-5, 0), 
        pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gm_end(screen: any) -> None:
    """
    引数：全画面のscreen
    戻り値：なし
    画面が薄い黒になって、GAMEOVERの表示が5秒出る
    """
    black_b = pg.Surface((1600, 900))#黒い四角を作る
    pg.draw.rect(black_b,(0, 0, 0) , pg.Rect(0, 0, 1600, 900))
    black_b.set_alpha(100)
    screen.blit(black_b, [0, 0])
    
    font = pg.font.Font(None, 80)#文字の表示
    txt = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(txt, [650, 450])
    
    img_l = pg.image.load("fig/8.png")#左にこうかとんを表示
    enn_l = pg.Surface((20, 20))
    pg.draw.circle(enn_l, (255, 0, 0), (10, 10), 10)
    screen.blit(img_l, [600, 450])
    
    img_r = pg.image.load("fig/8.png")#右のこうかとんを表示
    enn_r = pg.Surface((20, 20))
    pg.draw.circle(enn_r, (255, 0, 0), (10, 10), 10)
    screen.blit(img_r, [1000, 450])

    pg.display.update()

    time.sleep(5)

def rotate_bird(img):
    FLIP = {
    (0, +5):pg.transform.rotozoom(img, 270, 2.0),
    (+5, +5):pg.transform.rotozoom(img, 225, 2.0),
    (+5, 0):pg.transform.rotozoom(img, 180, 2.0),
    (+5, -5):pg.transform.rotozoom(img, 135, 2.0),
    (0, -5):pg.transform.rotozoom(img, 90, 2.0),
    (-5, -5):pg.transform.rotozoom(img, 45, 2.0),
    (-5, 0):pg.transform.rotozoom(img, 0, 2.0),
    (-5, +5):pg.transform.rotozoom(img, 315, 2.0),
}

    return FLIP


def acca_exp(bob):
    accs = [a for a in range(1, 11)]
    
    for r in range(1, 11):
        bob = pg.Surface((20*r, 20*r))
        pg.draw.circle(bob, (255, 0, 0), (10*r, 10*r), 10*r)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #衝突判定
            gm_end(screen)
            return#ゲームオーバー
        
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        for y, t in rotate_bird(kk_img).items():
            if sum_mv == y:
                kk_img = t
        kk_rct.move_ip(sum_mv)
        if cheak_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(vx, vy)
        if cheak_bound(bb_rct) == (False, True):
            vx *= -1
        if cheak_bound(bb_rct) == (True, False):
            vy *= -1
        if cheak_bound(bb_rct) == (False, False):
            vx *= -1
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


def cheak_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル(横方向判定結果、縦判定結果)
    画面内ならTrue、画面外ならFlase
    """
    
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
