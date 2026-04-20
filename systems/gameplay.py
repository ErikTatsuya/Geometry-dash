import math
import pygame


def spawn_trail(game):
    if not game.player or game.player.trail_timer % 3 != 0:
        return
    center = pygame.Vector2(game.player.hitbox.centerx - game.camera_x - 8, game.player.hitbox.centery)
    vel = pygame.Vector2(-1.2, 0.15 * math.sin(pygame.time.get_ticks() / 90))
    game.particles.append(
        {
            "pos": center,
            "vel": vel,
            "radius": 7,
            "life": 24,
            "color": (0, 220, 255),
        }
    )


def spawn_death_burst(game):
    if not game.player:
        return
    center = pygame.Vector2(game.player.hitbox.centerx - game.camera_x, game.player.hitbox.centery)
    for i in range(18):
        angle = (math.pi * 2 / 18) * i
        speed = 1.5 + (i % 3) * 0.6
        game.particles.append(
            {
                "pos": center.copy(),
                "vel": pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed),
                "radius": 4 + (i % 2),
                "life": 28,
                "color": (255, 90, 120) if i % 2 else (0, 220, 255),
            }
        )


def update_particles(game):
    alive = []
    for particle in game.particles:
        particle["pos"] += particle["vel"]
        particle["vel"].y += 0.02
        particle["radius"] *= 0.95
        particle["life"] -= 1
        if particle["life"] > 0 and particle["radius"] > 0.6:
            alive.append(particle)
    game.particles = alive


def draw_particles(game):
    for particle in game.particles:
        alpha = max(40, min(255, particle["life"] * 8))
        surf_size = max(4, int(particle["radius"] * 4))
        surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
        pygame.draw.circle(
            surf,
            (*particle["color"], alpha),
            (surf_size // 2, surf_size // 2),
            max(1, int(particle["radius"])),
        )
        game.screen.blit(surf, (particle["pos"].x - surf_size // 2, particle["pos"].y - surf_size // 2))


def resolve_solid_collisions(game):
    player_box = game.player.get_blue_hitbox()
    landed = False
    for block in game.blocks:
        solid = getattr(block, "blue_hitbox", block.rect)
        if player_box.colliderect(solid) and game.player.vel_y >= 0:
            player_box.bottom = solid.top + 1
            game.player.hitbox.bottom = player_box.bottom - 2
            game.player.pos_y = float(game.player.hitbox.y)
            game.player.vel_y = 0
            game.player.on_ground = True
            landed = True
    if landed:
        game.player.sync_visual()


def touches_hazard(game):
    player_box = game.player.get_red_hitbox()
    for hazard in game.hazards:
        hitbox = getattr(hazard, "red_hitbox", hazard.rect)
        if player_box.colliderect(hitbox):
            return True
    return False


def apply_portals(game):
    if game.player.portal_cooldown > 0:
        return

    player_box = game.player.get_blue_hitbox()
    for portal in game.portals:
        hitbox = getattr(portal, "portal_hitbox", portal.rect)
        if not player_box.colliderect(hitbox):
            continue

        if portal.type == "s":
            game.player.mode = "ship"
            game.player.image = game.player.original_image
        elif portal.type == "c":
            game.player.mode = "cube"
            game.player.image = game.player.original_image
            game.player.angle = round(game.player.angle / 90) * 90
        elif portal.type == "gi":
            game.player.gravity_dir = -1
        elif portal.type == "gn":
            game.player.gravity_dir = 1
        elif portal.type == "w":
            game.player.mode = "ship"

        game.player.portal_cooldown = 18
        game.player.sync_visual()
        return
