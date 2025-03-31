
from shmup.entities.projectiles.projectile_allied import ProjectileAllied
from shmup.entities.projectiles.projectile_enemy import ProjectileEnemy
from shmup.entities.projectiles.projectile_type import ProjectileType

class ProjectileFactory:
    """Factory class for creating projectiles."""

    @staticmethod
    def create_projectile(projectile_type, position):
        """Creates a projectile based on the given type and position.

        Args:
            projectile_type (ProjectileType): The type of the projectile to create (Allied or Enemy).
            position (tuple): The initial position of the projectile.

        Returns:
            Projectile: An instance of the projectile class corresponding to the given type.

        Raises:
            ValueError: If an invalid projectile type is provided.
        """
        if projectile_type == ProjectileType.Allied:
            return ProjectileAllied(position)
        elif projectile_type == ProjectileType.Enemy:
            return ProjectileEnemy(position)
        else:
            raise ValueError(f"Invalid projectile type: {projectile_type}")
