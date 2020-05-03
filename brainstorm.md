

Design outline

need components:
- position, movement
- area of effect
- tile properties like hardness etc
- tile transformations: empty to water / sand
- tile movement: sand is moved
- tile descruction and dropping of minerals etc
- UI, inventory, goals
- controllers: characters by players and AI, robots by scripts
- entity guis for robots, machines, factories, vehicles
- physics, maybe (flying bullets)

Ideas:
Visibility: 
Field called Light makes things (tiles, buildings, entities) visible
Character has a vision device with a range which is affected by available energy.
Some buildings can emit Light too.


=======================================================================================================================

nach rechts expanden
lokomotive, die autonom fährt und grabt, der man aber ressourcen und module nachschickt
hin und her von ressourcen
sie trifft auf monstersiedlungen
view von lokomotive zeigt sie immer, oder eine art minimap oder ein modell von allen wagen=modulen

verschiedene tech-strategien nach einiger zeit gameplay:
wahl zwischen
    - lokomotive
    - selber lasern
    - roboter
    - maulwürfe


situation:
miner, verschüttet. "links" ist geröll mit verschütteten geräten und technologie, "rechts" ist harter fels mit ressourcen.
geröll durchwühlbar, stein hart. braucht technologie (evtl vorübergehend gutes tool vorhanden, das sich aber abnutzt und rechtzeitig ersetzt werden muss)


=======================================================================================================================

## Train Mechanics
A train is composed of wagons, each of them enables certain abilities and benefits (e.g. speed, mining power, capacity) but might also require resources (e.g. energy).
Wagons can be chained together, for some of them the order might be relevant (e.g. the field created by an antenna might not reach all wagons).

### Wagons
- Engine
    - Determines speed and provides energy
    - Examples:
        - Manual (played needs to control it and press two keyboard buttons alternately xD)
        - Automated: steam engine, oil, nuclear power
- Boring head
    - Determines mining power
    - Examples: Automated pickaxe, crowbar, drills, laser (fast but no resources are mined), TNT (fast but needs to be refilled)
    - Durable tools might be built from different materials (stone, iron, diamond)
- Cart
    - Increases capacity / inventory size of train. If train is full, cannot mine further -> player needs to automate this to be efficient
- Energy Dissipator
    - Cart with an antenna
    - Draws energy (e.g. from engine)
    - Creates a field (e.g. a MiningField)
        - Crazy idea for late-game tech: portal field to teleport resources directly back to home basis (which can of course be misused by other players..^^)
- Computing Module
    - Cart with a computer (a simple one so it needs space ;)) to enable simple logic operations
    - Examples:
        - Based on sensory inputs from other carts (see below) determine in which direction the train should head
        - Based on capacity / amount of stuff in inventory decide which direction to ride (e.g. to head home to unload when full)
        - Weaponization: Explode all TNT if a building or player is in front of the train (in multiplayer mode)
        - Thief protection: When train is moving and someone tries to take something out of inventory, explode all TNT
- Sensor
    - Provides information to computing modules, e.g. in which direction the closest gold source is
    - Types: Resource radar (direction, distance, amount), Resource detector (e.g. to sort them into separate carts)
    - For simplification, sensors might just be a feature of the computing module which can be upgraded.
- Weapons
    - Cart with weapons to defend against monsters and other players
    - Examples:
        - Slingshot (the most natural weapon when you sit on a pile of stones, no?)
        - Catapult
        - Flame thrower
        - ATOMIC 
    - Could be funny in a survival mode (where more and more monsters appear) or in P2P
    
### Technology
- Wagons are built in factories
- Multiple trains can be built for different purposes (e.g. one that scouts, one that mines straight, one that destroys)
- Upgrades and technologies are researched / found while mining (ancient or foreign tech) / discovered (e.g. if an accident happens)
- Once part of a train, wagons can be upgraded

### Things to think about
- Initial goal why the player needs a train should be clear
    - e.g. manually mining certain resources is not possible or takes very long
    - Afterwards it's all about progress and exploration
    
- Meta Research
    - Research could be partially probabilistic: some techs have prerequisites (resources, other techs, buildings) but the exact time of discovery follows a random distribution (to simulate research)
        - Trade-off where to spend time researching: something easy with high probability for success (e.g. enhancing a drill material) vs. something very innovative with low probability for success (quantum-based computing module)
        - Player can increase success probability by investing more resources
    - Player decides which research practices to use (conservative vs. risky, fast vs. slow, cheap vs. expensive)
        - Need to design a scheme how these factors influence each other. E.g. fast is always more expensive, low-risk takes longer in average, risky could result in disaster
    - Meta research could be a general decision (affect all branches of the tech tree) or research-field related (affect only certain branches of the tech tree)

- Game modes:
    - Single player mode: find exit
    - Multiplayer mode: find exit together, or destroy each other


