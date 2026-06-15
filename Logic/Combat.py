def shoot(target, shotgun): # uses shotgun class and applies dmg to who

    shell = shotgun.fire()

    if shell == "live":
        target.take_damage(1)
        print("Boom")
    else:
        print("Nope")

    return shell