def shoot(target, shotgun): # uses shotgun class and applies dmg to who

    shell = shotgun.fire()

    if shell == "live":
        target.take_damage()
        print("Boom")
    else:
        print("Nope")

    return shell