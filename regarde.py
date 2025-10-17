def clamp(value: float, min_val: float, max_val: float) -> float:
    """Contraint une valeur dans un intervalle."""
    return max(min_val, min(value, max_val))

def contact(p, balle, n) -> str:
    """
    Détermine le type de contact ('ABOVE', 'LEFT', 'RIGHT', 'BELOW', ou '')
    entre une balle (cercle) et une plateforme rectangulaire.
    """
    # Point du rectangle le plus proche du centre du cercle
    closest_x = clamp(balle.x, p.x, p.x + p.lx)
    closest_y = clamp(balle.y, p.y, p.y + p.ly)

    # Différences
    dx = balle.x - closest_x
    dy = balle.y - closest_y
    dist_sq = dx * dx + dy * dy

    # Pas de collision
    if dist_sq > balle.radius ** 2:
        return ""

    # Détermination du côté de contact
    if abs(dy) > abs(dx):
        return "above" if dy < 0 else "below"
    else:
        return "left" if dx < 0 else "right"


def interactions(players, balle, n):#, simulation=False, coor=None):
    global last_r

    p =- 1
    if balle.x < players[0].x + players[0].lx + balle.radius + balle.vx + 10: p = 0
    elif balle.x > players[1].x - balle.radius - balle.vx - 10: p = 1
    if p != -1:
        c = contact(players[p], balle, n)
        if c: balle.rebond(players[p], n, c)
        else:
            s = False
            py = int(players[p].y)
            bx , by = int(balle.x), int(balle.y)
          #  print(f">>>Simulation {n}>>>")
            steps = int(max(abs(players[p].vy), abs(balle.vy), abs(balle.vx)))
            for simx in range(steps):
                players[p].y = int(py + (simx * players[p].vy / steps))
                balle.y = int(by + (simx * balle.vy / steps))
                balle.x = int(bx + (simx * balle.vx / steps))
                c = contact(players[p], balle, (n,1, steps))
             #   print((players[p].y, balle.y, balle.x), end ="; ")
                if c:
                   # print("")
                    balle.freeze()
                    players[p].freeze()
                    s = True
                    break
            if not s:
                players[p].y = py
                balle.x = bx
                balle.y = by
          #  print("<<<End<<<")


    #si la balle touche le haut ou la bas du terrain
    if balle.y - balle.radius <= 120:
        balle.rebond(players[p], n, "wallup")
    if balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(players[p], n, "walldown")

    #si la balle touche la gauche ou la droite du terrain
    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        #arreter le jeu
        return False

    #continuer le jeu
    return True
