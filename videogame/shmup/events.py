from enum import Enum

class Events(Enum):
    HERO_FIRES = 0,  #pos = position of projectile to spawn
    PROJECTILE_OUT_OF_SCREEN = 1   #proj = instance of projectile
    ENEMY_END_POINT = 2   #enemy = instance of enemy
    ENEMY_FIRES = 3,  #pos = position of projectile to spawn
    EXPLOSION_FINISHED = 4   #explosion = instance of explosion
    BOSS_KILLED = 5