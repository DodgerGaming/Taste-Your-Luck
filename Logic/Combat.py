def shoot(shooter, target, shotgun): # uses shotgun class and applies dmg to who

    shell = shotgun.fire()

    if shell == "live":
        damage = 1 * shooter.damage_multiplier # flexible logic so even if user use hacksaw, dmg calculation is still right.
        
        target.take_damage(damage)

    return shell