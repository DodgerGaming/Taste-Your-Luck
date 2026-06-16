def shoot(shooter, target, shotgun): # uses shotgun class and applies dmg to who

    shell = shotgun.fire()

    if shell == "live":
        damage = shotgun.damage * shooter.damage_multiplier
        
        target.take_damage(damage)

    return shell