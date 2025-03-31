from enum import Enum

from shmup.entities.enemies.enemy_avenger import EnemyAvenger
from shmup.entities.enemies.enemy_raptor import EnemyRaptor

class EnemyType(Enum):
    Avenger = 0,
    Raptor = 1

class EnemyFactory:

    @staticmethod
    def create_enemy(enemy_type, position_init, position_end):
        if enemy_type == EnemyType.Avenger:
            return EnemyAvenger(position_init, position_end)
        elif enemy_type == EnemyType.Raptor:
            return EnemyRaptor(position_init, position_end)