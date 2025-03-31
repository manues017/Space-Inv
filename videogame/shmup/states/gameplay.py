import random
import pygame
from moviepy.editor import VideoFileClip
from states.state import State
from entities.rendergroup import RenderGroup
from entities.hero import Hero
from events import Events
from entities.projectiles.projectile_factory import ProjectileFactory
from entities.projectiles.projectile_type import ProjectileType
from config import cfg_item
from entities.enemies.enemy_factory import EnemyFactory, EnemyType
from entities.explosion import Explosion
from entities.movement_type import MovementType
from entities.enemies.boss import Boss
from entities.projectiles.laser_beam import LaserBeam
from importlib import resources



class GamePlay(State):

    ''' 
    Manages the gameplay state, including player, enemies, projectiles, explosions, and the boss.
    '''
    def __init__(self):
        super().__init__()

        self.__players = RenderGroup()
        self.__projectiles_allied = RenderGroup()
        self.__projectiles_enemy = RenderGroup()
        self.__enemies = RenderGroup()
        self.__explosions = RenderGroup()
        self.__boss = None
        self.__enemies_destroyed = 0
        self.__max_enemies_destroyed = 20
        self.__enemy_spawn = True

        self.next_state = "Intro"
        
        explosion_sound_path = resources.files("assets.sounds").joinpath('explosion.mp3')
        with resources.as_file(explosion_sound_path) as sound_path:
            self.__explosion_sound = pygame.mixer.Sound(sound_path)



    def enter(self):
        """
        Initializes the state when entered.
        """
        self.done = False
        self.__players.add(Hero(MovementType.HORIZONTAL))

    def exit(self):
        """
        Cleans up the state when exited.
        """
        self.__players.empty()
        self.__projectiles_allied.empty()
        self.__projectiles_enemy.empty()
        self.__enemies.empty()
        self.__explosions.empty()
        if self.__boss:
            self.__boss = None

    def handle_input(self, event):
        """
        Handles player input events.

        Args:
            event (pygame.event.Event): The input event to handle.
        """
        if event.type == pygame.KEYDOWN:
            self.__players.handle_input(event.key, True)
        elif event.type == pygame.KEYUP:
            self.__players.handle_input(event.key, False)

    def process_events(self, event):
        """
        Processes various game events.

        Args:
            event (pygame.event.Event): The game event to process.
        """
        self.__handle_events(event)
        self.__players.process_events(event)
        self.__projectiles_allied.process_events(event)
        self.__projectiles_enemy.process_events(event)
        self.__enemies.process_events(event)
        self.__explosions.process_events(event)

    def update(self, delta_time):
        """
        Updates the state with the given delta time.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        if not self.__boss:
            self.__spawn_enemy()
        
        self.__players.update(delta_time)
        self.__projectiles_allied.update(delta_time)
        self.__projectiles_enemy.update(delta_time)
        self.__enemies.update(delta_time)
        self.__explosions.update(delta_time)

        if self.__boss:
            self.__boss.update(delta_time)
            self.__boss.laser_beams.update(delta_time)

        self.__detect_collisions()

    def render(self, surface_dst):
        """
        Renders the state on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render the state on.
        """
        self.__players.render(surface_dst)
        self.__projectiles_allied.render(surface_dst)
        self.__projectiles_enemy.render(surface_dst)
        self.__enemies.render(surface_dst)
        self.__explosions.render(surface_dst)
        if self.__boss:
            self.__boss.render(surface_dst)
            self.__boss.laser_beams.draw(surface_dst)

    def release(self):
        """
        Releases resources for the state.
        """
        self.__players.release()
        self.__projectiles_allied.release()
        self.__projectiles_enemy.release()
        self.__enemies.release()
        self.__explosions.release()
        if self.__boss:
            self.__boss.release()

    def __handle_events(self, event):
        """
        Internal method to handle custom events.

        Args:
            event (pygame.event.Event): The custom event to handle.
        """
        if event.event == Events.HERO_FIRES:
            self.__spawn_projectile(ProjectileType.Allied, event.pos)
        elif event.event == Events.ENEMY_FIRES:
            self.__spawn_projectile(ProjectileType.Enemy, event.pos)
        elif event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__kill_projectile(event.proj)
        elif event.event == Events.ENEMY_END_POINT:
            self.__kill_enemy(event.enemy)
        elif event.event == Events.EXPLOSION_FINISHED:
            self.__kill_explosion(event.explosion)
        elif event.event == Events.BOSS_KILLED:
            self.__kill_boss(event.boss)

    def __spawn_projectile(self, proj_type, position):
        """
        Spawns a projectile of the given type at the specified position.

        Args:
            proj_type (ProjectileType): The type of projectile to spawn.
            position (tuple): The position to spawn the projectile at.
        """
        projectile = ProjectileFactory.create_projectile(proj_type, position)

        if proj_type == ProjectileType.Allied:
            self.__projectiles_allied.add(projectile)
        elif proj_type == ProjectileType.Enemy:
            self.__projectiles_enemy.add(projectile)

    def __kill_projectile(self, projectile):
        """
        Removes a projectile from the game.

        Args:
            projectile (Projectile): The projectile to remove.
        """
        if projectile.proj_type == ProjectileType.Allied:
            self.__projectiles_allied.remove(projectile)
        elif projectile.proj_type == ProjectileType.Enemy:
            self.__projectiles_enemy.remove(projectile)

    def __spawn_enemy(self):
        """
        Spawns an enemy if the conditions are met.
        """
        while self.__enemy_spawn:
            if len(self.__enemies) > 5:
                return
   
            enemy_list = [EnemyType.Avenger, EnemyType.Raptor]
            enemy_type = random.choice(enemy_list)

            padding = cfg_item("entities", "enemies", "enemy_padding")

            if enemy_type == EnemyType.Avenger:
                x = cfg_item("game", "screen_size")[0] / 2
                y_rows = [padding, padding + 80, padding + 160]
                y = random.choice(y_rows)
                position_init = (x, y)
                position_end = (x, cfg_item("game", "screen_size")[1] + padding)
            
            elif enemy_type == EnemyType.Raptor:
                x = random.randint(padding, cfg_item("game", "screen_size")[0] - padding)
                position_init = (x, -padding)
                position_end = (x, cfg_item("game", "screen_size")[1] + padding)

            enemy = EnemyFactory.create_enemy(enemy_type, position_init, position_end)
            self.__enemies.add(enemy)

    def __kill_enemy(self, enemy):
        """
        Removes an enemy from the game and checks for boss spawn conditions.

        Args:
            enemy (Enemy): The enemy to remove.
        """
        self.__enemies.remove(enemy)
        self.__enemies_destroyed += 1
        print(f"Enemies destroyed: {self.__enemies_destroyed}")
        if self.__enemies_destroyed >= self.__max_enemies_destroyed:
            self.__enemy_spawn = False
            if len(self.__enemies) == 0:
                print("Spawning Boss")
                self.__spawn_boss()

    def __spawn_boss(self):
        """
        Spawns the boss enemy.
        """
        boss_position_init = (40, -300)  # Initial position above the screen
        boss_position_end = (40, 0)  # Position in the game screen
        self.__boss = Boss(boss_position_init, boss_position_end)
        
    def __kill_boss(self, boss):
        """
        Removes the boss from the game.

        Args:
            boss (Boss): The boss to remove.
        """
        self.__boss = None
        print("Boss Killed")
        self.__enemies_destroyed = 0
        self.__enemy_spawn = True

    def __spawn_explosion(self, position):
        """
        Spawns an explosion at the specified position.

        Args:
            position (tuple): The position to spawn the explosion at.
        """
        self.__explosions.add(Explosion(position))
        self.__explosion_sound.play()  # Reproduce el sonido de explosión

    def __kill_explosion(self, explosion):
        """
        Removes an explosion from the game.

        Args:
            explosion (Explosion): The explosion to remove.
        """
        self.__explosions.remove(explosion)

    def __game_over(self):
        """
        Handles game over conditions.
        """
        print("Game Over")
        self.done = True
        self.__enemies_destroyed = 0
        self.__enemy_spawn = True

    def __detect_collisions(self):
        """
        Detects and handles collisions between various game objects.
        """
        for player in pygame.sprite.groupcollide(self.__players, self.__projectiles_enemy, True, True).keys():
            self.__spawn_explosion(player.pos)
            self.__game_over()

        for enemy in pygame.sprite.groupcollide(self.__enemies, self.__projectiles_allied, True, True).keys():
            self.__spawn_explosion(enemy.pos)
            self.__kill_enemy(enemy)
            print("Enemy Killed")

        if self.__boss:
            for player in self.__players:
                if pygame.sprite.spritecollide(player, self.__boss.laser_beams, True):
                    self.__spawn_explosion(player.pos)
                    self.__game_over()
                if pygame.sprite.spritecollide(self.__boss, self.__projectiles_allied, True):
                    self.__boss.take_damage(1)  # Reduce vida del jefe
                    print("Boss Hit")