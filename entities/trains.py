import default
from entities.entities import Entity
from entities.inventories import Inventory


TRAIN_SPRITE_SIZE = (default.TILE_SIZE / 2)


class Train(Entity):
    def __init__(self, direction=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wagons = []
        self.direction = direction
        self.inventory = Inventory()
        self.size = TRAIN_SPRITE_SIZE

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
            total_length += wagon.size

        return total_length

    def add_wagon(self, wagon):
        dx, dy = self.direction
        if dx:
            wagon.x = self.x - dx * self.length
            wagon.y = self.y
        elif dy:
            wagon.x = self.x
            wagon.y = self.y - dy * self.length

        self.wagons.append(wagon)

    def ride(self):
        dx, dy = self.direction
        reach_x = self.x + dx * self.size / 2
        reach_y = self.y + dy * self.size / 2

        tile = self.game.tile_grid.get_tile(reach_x, reach_y)
        if tile and tile.is_minable:
            self.mine(tile)
        elif tile and not tile.is_blocking and self.speed > 0:
            self.move(dx * self.speed, dy * self.speed)

    def mine(self, resource):
        resource.durability -= self.mining_power
        if resource.durability < 0:
            drops = resource.drops()
            self.inventory.add_items(drops)

            self.game.tile_grid.replace_tile(resource.x, resource.y, resource.reveals())

    def move(self, dx, dy, *args, **kwargs):
        # First check if all wagons can be moved
        for wagon in self.wagons:
            if not wagon.is_valid_move(dx, dy):
                return

        # Move train
        super().move(dx, dy, *args, **kwargs)
        for wagon in self.wagons:
            wagon.move(dx, dy, *args, **kwargs)

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
        self.size = TRAIN_SPRITE_SIZE
        self.color = (127, 0, 255)

    def draw(self, surface):
        super().draw(surface)

        # TODO: Replace with proper art
        rendered_text = self.game.font.render(self.icon, True, (255, 255, 255))
        surface.blit(rendered_text, (self.x, self.y - self.size / 2))


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
