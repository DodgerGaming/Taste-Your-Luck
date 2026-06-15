def shoot(target, shotgun): # uses shotgun class and applies dmg to who

    shell = shotgun.shoot()

    if shell == "live":
        target.take_damage(1)

    return shell