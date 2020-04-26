import default
from entities.entities import Entity
from entities.inventories import Inventory
from entities.coordinates import Vector
TRAIN_SPRITE_SIZE = (default.TILE_SIZE / 2)


class Train(Entity):
    def __init__(self, direction: Vector, size=Vector(TRAIN_SPRITE_SIZE, TRAIN_SPRITE_SIZE), *args, **kwargs):
        super().__init__(size=size, *args, **kwargs)

        self.wagons = []
        self.direction = direction
        self.inventory = Inventory()

    @property
    def capacity(self):
        total_capacity = 0
        for wagon in self.wagons:
            total_capacity += wagon.capacity

        return total_capacity

    @property
    def mining_power(self):
        total_mining_power = 0
        for wagon in self.wagons:
            total_mining_power += wagon.mining_power

        return total_mining_power

    @property
    def speed(self):
        total_speed = 0
        for wagon in self.wagons:
            total_speed += wagon.speed

        return total_speed
    
    @property
    def length(self):
        total_length = 0
        for wagon in self.wagons:
            total_length += wagon.size.x

        return total_length

    def add_wagon(self, wagon):
        dx, dy = self.direction
        if dx:
            wagon.pos = self.pos + Vector(-dx * self.length, 0)
        elif dy:
            wagon.pos = self.pos + Vector(0, -dy * self.length)

        self.wagons.append(wagon)

    def ride(self):
        reach = self.pos + self.direction * self.size.x * 0.5

        tile = self.game.tile_grid.get_tile(reach)
        if tile and tile.is_mineable:
            self.mine(tile)
        elif tile and not tile.is_blocking and self.speed > 0:
            self.move(self.direction * self.speed)

    def mine(self, resource):
        resource.durability -= self.mining_power
        if resource.durability < 0:
            drops = resource.drops()
            self.inventory.add_items(drops)
            self.game.tile_grid.replace_tile(resource.pos, resource.reveals())

    def move(self, delta, *args, **kwargs):
        # First check if all wagons can be moved
        for wagon in self.wagons:
            if not wagon.is_valid_move(delta):
                return

        # Move train
        super().move(delta, *args, **kwargs)
        for wagon in self.wagons:
            wagon.move(delta, *args, **kwargs)

    def draw(self, *args, **kwargs):
        for wagon in self.wagons:
            wagon.draw(*args, **kwargs)


class Wagon(Entity):
    icon = 'w'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capacity = 0
        self.mining_power = 0
        self.speed = 0
        self.size = Vector(TRAIN_SPRITE_SIZE, TRAIN_SPRITE_SIZE)
        self.color = (127, 0, 255)

    def draw(self, surface):
        super().draw(surface)

        # TODO: Replace with proper art
        rendered_text = self.game.font.render(self.icon, True, (255, 255, 255))
        surface.blit(rendered_text, (self.pos.x, self.pos.y - self.size.x / 2))


class Engine(Wagon):
    icon = 'e'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capacity = 100
        self.speed = 1


class BoringHead(Wagon):
    icon = '>'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mining_power = 0.5


class Cart(Wagon):
    icon = 'c'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.capacity = 1000
