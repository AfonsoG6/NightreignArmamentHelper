from lib.constants import *

RATINGS: list[int] = [
    S := 32,
    A := 16,
    B := 8,
    C := 4,
    D := 2,
    E := 1,
    _ := 0,
]


class ArmamentSpec:
    """
    Class representing an armament specification.
    """
    def __init__(self, name: str, modifiable_name: str, type: str, affinities: list[str], STR: int, DEX: int, INT: int, FAI: int, ARC: int):
        self.name: str = name
        self.modifiable_name: str = modifiable_name
        self.type: str = type
        self.affinities: list[str] = affinities
        self.STR: int = STR
        self.DEX: int = DEX
        self.INT: int = INT
        self.FAI: int = FAI
        self.ARC: int = ARC

    def get_best_stat(self) -> str:
        """
        Returns the name of the stat with the highest rating.
        """
        best_stat: int = max(self.STR, self.DEX, self.INT, self.FAI, self.ARC)
        res: list[str] = []
        if best_stat == self.STR:
            res.append("STR")
        if best_stat == self.DEX:
            res.append("DEX")
        if best_stat == self.INT:
            res.append("INT")
        if best_stat == self.FAI:
            res.append("FAI")
        if best_stat == self.ARC:
            res.append("ARC")
        return ", ".join(res)

    def get_stat_letter(self, stat_id: str) -> str:
        stat_value: int = getattr(self, stat_id)
        if stat_value == S:
            return "S"
        elif stat_value == A:
            return "A"
        elif stat_value == B:
            return "B"
        elif stat_value == C:
            return "C"
        elif stat_value == D:
            return "D"
        elif stat_value == E:
            return "E"
        else:
            return "-"

MODIFIERS = [
    FIRE_MODIFIER := "Fire",
    MAGIC_MODIFIER := "Magic",
    HOLY_MODIFIER := "Sacred",
    LIGHTNING_MODIFIER := "Lightning",
    BLEED_MODIFIER := "Blood",
    POISON_MODIFIER := "Poison",
    FROSTBITE_MODIFIER := "Cold",
]

ARMAMENT_SPECS: set[ArmamentSpec] = set([
    ############ DAGGERS ############
    ArmamentSpec("Duchess' Dagger",              "Duchess' Dagger",              DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Dagger",                       "{} Dagger",                    DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Parrying Dagger",              "{} Parrying Dagger",              DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Great Knife",                  "{} Great Knife",                  DAGGER,               [BLEED],              E, S, _, _, _),
    ArmamentSpec("Miséricorde",                  "{} Miséricorde",               DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Bloodstained Dagger",          "{} Bloodstained Dagger",          DAGGER,               [BLEED],              E, S, _, _, _),
    ArmamentSpec("Erdsteel Dagger",              "{} Erdsteel Dagger",              DAGGER,               [],                   E, A, _, D, _),
    ArmamentSpec("Wakizashi",                    "{} Wakizashi",                 DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Celebrant's Sickle",           "Celebrant's {} Sickle",           DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Ivory Sickle",                 "{} Ivory Sickle",                 DAGGER,               [MAGIC],              E, A, D, _, _),
    ArmamentSpec("Crystal Knife",                "{} Crystal Knife",                DAGGER,               [MAGIC],              E, A, D, _, _),
    ArmamentSpec("Scorpion's Stinger",           "Scorpion's {} Stinger",           DAGGER,               [SCARLET_ROT],        E, S, _, _, _),
    ArmamentSpec("Cinquedea",                    "{} Cinquedea",                 DAGGER,               [],                   E, S, _, _, _),
    ArmamentSpec("Glintstone Kris",              "{} Glintstone Kris",              DAGGER,               [MAGIC],              E, A, D, _, _),
    ArmamentSpec("Reduvia",                      "{} Reduvia",                   DAGGER,               [BLEED],              E, A, _, _, C),
    ArmamentSpec("Blade Of Calling",             "{} Blade Of Calling",             DAGGER,               [HOLY],               E, A, _, D, _),
    ArmamentSpec("Black Knife",                  "{} Black Knife",                  DAGGER,               [HOLY],               E, A, _, D, _),
    ############ STRAIGHT SWORDS ############
    ArmamentSpec("Short Sword",                  "{} Short Sword",                  STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Longsword",                    "{} Longsword",                 STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Broadsword",                   "{} Broadsword",                STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Weathered Straight Sword",     "Weathered {} Straight Sword",     STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Noble's Slender Sword",        "Noble's {} Slender Sword",        STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Lordsworn's Straight Sword",   "Lordsworn's {} Straight Sword",   STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Cane Sword",                   "{} Cane Sword",                   STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Warhawk's Talon",              "Warhawk's {} Talon",              STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Lazuli Glintstone Sword",      "{} Lazuli Glintstone Sword",      STRAIGHT_SWORD,       [MAGIC],              C, C, C, _, _),
    ArmamentSpec("Carian Knight's Sword",        "Carian Knight's {} Sword",        STRAIGHT_SWORD,       [MAGIC],              C, C, C, _, _),
    ArmamentSpec("Crystal Sword",                "{} Crystal Sword",                STRAIGHT_SWORD,       [MAGIC],              C, C, C, _, _),
    ArmamentSpec("Rotten Crystal Sword",         "{} Rotten Crystal Sword",         STRAIGHT_SWORD,       [MAGIC, SCARLET_ROT], C, C, C, _, _),
    ArmamentSpec("Miquellan Knight's Sword",     "Miquellan Knight's {} Sword",     STRAIGHT_SWORD,       [HOLY],               C, C, _, C, _),
    ArmamentSpec("Ornamental Straight Sword",    "Ornamental {} Straight Sword",    STRAIGHT_SWORD,       [],                   B, B, _, _, _),
    ArmamentSpec("Golden Epitaph",               "{} Golden Epitaph",               STRAIGHT_SWORD,       [HOLY],               C, C, _, C, _),
    ArmamentSpec("Sword Of St. Trina",           "{} Sword Of St. Trina",           STRAIGHT_SWORD,       [MAGIC, SLEEP],       C, C, C, _, _),
    ArmamentSpec("Regalia Of Eochaid",           "{} Regalia Of Eochaid",           STRAIGHT_SWORD,       [MAGIC],              C, C, _, _, B),
    ArmamentSpec("Coded Sword",                  "{} Coded Sword",                  STRAIGHT_SWORD,       [HOLY],               _, _, _, S, _),
    ArmamentSpec("Sword Of Night And Flame",     "{} Sword Of Night And Flame",     STRAIGHT_SWORD,       [MAGIC, FIRE],        C, C, C, C, _),
    ############ GREATSWORDS ############
    ArmamentSpec("Wylder's Greatsword",          "Wylder's Greatsword",          GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Bastard Sword",                "{} Bastard Sword",                GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Iron Greatsword",              "{} Iron Greatsword",              GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Lordsworn's Greatsword",       "Lordsworn's {} Greatsword",       GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Claymore",                     "{} Claymore",                  GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Knight's Greatsword",          "Knight's {} Greatsword",          GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Banished Knight's Greatsword", "Banished Knight's {} Greatsword", GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Forked Greatsword",            "Forked {} Greatsword",            GREATSWORD,           [BLEED],              B, C, _, _, _),
    ArmamentSpec("Flamberge",                    "{} Flamberge",                 GREATSWORD,           [BLEED],              B, C, _, _, _),
    ArmamentSpec("Inseparable Sword",            "Inseparable {} Sword",            GREATSWORD,           [HOLY],               B, C, _, C, _),
    ArmamentSpec("Gargoyle's Greatsword",        "Gargoyle's {} Greatsword",        GREATSWORD,           [],                   B, C, _, _, _),
    ArmamentSpec("Gargoyle's Blackblade",        "Gargoyle's {} Blackblade",        GREATSWORD,           [HOLY],               B, C, _, C, _),
    ArmamentSpec("Sword Of Milos",               "{} Sword Of Milos",               GREATSWORD,           [BLEED],              B, C, _, _, _),
    ArmamentSpec("Ordovis's Greatsword",         "Ordovis's {} Greatsword",         GREATSWORD,           [HOLY],               B, C, _, C, _),
    ArmamentSpec("Alabaster Lord's Sword",       "Alabaster Lord's {} Sword",       GREATSWORD,           [MAGIC],              B, C, C, _, _),
    ArmamentSpec("Death's Poker",                "Death's {} Poker",                GREATSWORD,           [MAGIC, FROSTBITE],   B, C, C, _, _),
    ArmamentSpec("Helphen's Steeple",            "Helphen's {} Steeple",            GREATSWORD,           [MAGIC],              B, C, C, _, _),
    ArmamentSpec("Marais Executioner's Sword",   "Marais Executioner's {} Sword",   GREATSWORD,           [MAGIC],              B, C, _, _, B),
    ArmamentSpec("Blasphemous Blade",            "{} Blasphemous Blade",            GREATSWORD,           [FIRE],               B, C, _, C, _),
    ArmamentSpec("Golden Order Greatsword",      "Golden Order {} Greatsword",      GREATSWORD,           [HOLY],               B, C, _, C, _),
    ArmamentSpec("Dark Moon Greatsword",         "Dark Moon {} Greatsword",         GREATSWORD,           [MAGIC, FROSTBITE],   B, C, C, _, _),
    ArmamentSpec("Sacred Relic Sword",           "{} Sacred Relic Sword",           GREATSWORD,           [HOLY],               B, C, _, C, _),
    ############ COLLOSAL SWORDS ############
    ArmamentSpec("Zweihander",                   "{} Zweihander",                COLOSSAL_SWORD,       [],                   A, C, _, _, _),
    ArmamentSpec("Greatsword",                   "{} Greatsword",                COLOSSAL_SWORD,       [],                   A, C, _, _, _),
    ArmamentSpec("Watchdog's Greatsword",        "Watchdog's {} Greatsword",        COLOSSAL_SWORD,       [],                   A, C, _, _, _),
    ArmamentSpec("Troll's Golden Sword",         "Troll's {} Golden Sword",         COLOSSAL_SWORD,       [],                   A, C, _, _, _),
    ArmamentSpec("Troll Knight's Sword",         "Troll Knight's {} Sword",         COLOSSAL_SWORD,       [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Royal Greatsword",             "Royal Greatsword",             COLOSSAL_SWORD,       [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Godslayer's Greatsword",       "Godslayer's {} Greatsword",       COLOSSAL_SWORD,       [FIRE],               B, D, _, D, _),
    ArmamentSpec("Grafted Blade Greatsword",     "Grafted Blade Greatsword",     COLOSSAL_SWORD,       [],                   A, C, _, _, _),
    ArmamentSpec("Ruins Greatsword",             "Ruins {} Greatsword",             COLOSSAL_SWORD,       [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Starscourge Greatsword",       "Starscourge {} Greatsword",       COLOSSAL_SWORD,       [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Maliketh's Black Blade",       "Maliketh's {} Black Blade",       COLOSSAL_SWORD,       [HOLY],               B, D, _, D, _),
    ############ THRUSTING SWORDS ############
    ArmamentSpec("Rapier",                       "{} Rapier",                    THRUSTING_SWORD,      [],                   E, S, _, _, _),
    ArmamentSpec("Estoc",                        "{} Estoc",                     THRUSTING_SWORD,      [],                   E, S, _, _, _),
    ArmamentSpec("Noble's Estoc",                "Noble's {} Estoc",                THRUSTING_SWORD,      [],                   E, S, _, _, _),
    ArmamentSpec("Cleanrot Knight's Sword",      "Cleanrot Knight's {} Sword",      THRUSTING_SWORD,      [],                   E, S, _, _, _),
    ArmamentSpec("Rogier's Rapier",              "Rogier's {} Rapier",              THRUSTING_SWORD,      [],                   E, S, _, _, _),
    ArmamentSpec("Antspur Rapier",               "Antspur {} Rapier",               THRUSTING_SWORD,      [SCARLET_ROT],        E, S, _, _, _),
    ArmamentSpec("Frozen Needle",                "{} Frozen Needle",                THRUSTING_SWORD,      [FROSTBITE],          E, S, _, _, _),
    ############ HEAVY THRUSTING SWORDS ############
    ArmamentSpec("Great Épée",                   "Great {} Épée",                   HEAVY_THRUSTING_SWORD, [],                  C, B, _, _, _),
    ArmamentSpec("Godskin Stitcher",             "{} Godskin Stitcher",             HEAVY_THRUSTING_SWORD, [],                  C, B, _, _, _),
    ArmamentSpec("Bloody Helice",                "Bloody {} Helice",                HEAVY_THRUSTING_SWORD, [BLEED],             C, B, _, _, C),
    ArmamentSpec("Dragon King's Cragblade",      "Dragon King's {} Cragblade",      HEAVY_THRUSTING_SWORD, [],                  C, B, _, _, _),
    ############ CURVED SWORDS ############
    ArmamentSpec("Scimitar",                     "{} Scimitar",                  CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Falchion",                     "{} Falchion",                  CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Bandit's Curved Sword",        "Bandit's {} Curved Sword",        CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Shotel",                       "{} Shotel",                    CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Shamshir",                     "{} Shamshir",                  CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Grossmesser",                  "{} Grossmesser",               CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Scavenger's Curved Sword",     "Scavenger's {} Curved Sword",     CURVED_SWORD,         [BLEED],              D, A, _, _, _),
    ArmamentSpec("Mantis Blade",                 "{} Mantis Blade",                 CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Beastman's Curved Sword",      "Beastman's {} Curved Sword",      CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Serpent-God's Curved Sword",   "Serpent-God's {} Curved Sword",   CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Flowing Curved Sword",         "Flowing {} Curved Sword",         CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Magma Blade",                  "{} Magma Blade",                  CURVED_SWORD,         [FIRE],               D, B, _, D, _),
    ArmamentSpec("Nox Flowing Sword",            "{} Nox Flowing Sword",            CURVED_SWORD,         [],                   D, A, _, _, _),
    ArmamentSpec("Wing Of Astel",                "{} Wing Of Astel",                CURVED_SWORD,         [MAGIC],              D, B, D, _, _),
    ArmamentSpec("Eclipse Shotel",               "{} Eclipse Shotel",               CURVED_SWORD,         [HOLY],               D, B, _, D, _),
    ############ CURVED GREATSWORDS ############
    ArmamentSpec("Dismounter",                   "{} Dismounter",                   CURVED_GREATSWORD,    [],                   B, B, _, _, _),
    ArmamentSpec("Omen Cleaver",                 "{} Omen Cleaver",                 CURVED_GREATSWORD,    [],                   B, B, _, _, _),
    ArmamentSpec("Monk's Flameblade",            "Monk's {} Flameblade",            CURVED_GREATSWORD,    [],                   B, B, _, _, _),
    ArmamentSpec("Beastman's Cleaver",           "Beastman's {} Cleaver",           CURVED_GREATSWORD,    [],                   B, B, _, _, _),
    ArmamentSpec("Bloodhound's Fang",            "Bloodhound's {} Fang",            CURVED_GREATSWORD,    [BLEED],              B, B, _, _, _),
    ArmamentSpec("Onyx Lord's Greatsword",       "Onyx Lord's {} Greatsword",       CURVED_GREATSWORD,    [MAGIC],              C, C, C, _, _),
    ArmamentSpec("Zamor Curved Sword",           "Zamor {} Curved Sword",           CURVED_GREATSWORD,    [FROSTBITE],          B, B, _, _, _),
    ArmamentSpec("Magma Wyrm's Scalesword",      "Magma Wyrm's {} Scalesword",      CURVED_GREATSWORD,    [FIRE],               C, C, _, C, _),
    ArmamentSpec("Morgott's Cursed Sword",       "Morgott's {} Cursed Sword",       CURVED_GREATSWORD,    [BLEED],              C, C, _, _, B),
    ############ KATANAS ############
    ArmamentSpec("Executor's Blade",             "Executor's Blade",          KATANA,               [BLEED],              E, S, _, _, _),
    ArmamentSpec("Uchigatana",                   "{} Uchigatana",                KATANA,               [BLEED],              E, S, _, _, _),
    ArmamentSpec("Nagakiba",                     "{} Nagakiba",                  KATANA,               [BLEED],              E, S, _, _, _),
    ArmamentSpec("Serpentbone Blade",            "{} Serpentbone Blade",            KATANA,               [POISON],             E, S, _, _, _),
    ArmamentSpec("Meteoric Ore Blade",           "{} Meteoric Ore Blade",           KATANA,               [MAGIC, BLEED],       E, A, D, _, _),
    ArmamentSpec("Moonveil",                     "{} Moonveil",                     KATANA,               [MAGIC, BLEED],       E, A, D, _, _),
    ArmamentSpec("Rivers Of Blood",              "{} Rivers Of Blood",              KATANA,               [FIRE, BLEED],        E, A, _, _, C),
    ArmamentSpec("Dragonscale Blade",            "{} Dragonscale Blade",            KATANA,               [],                   E, S, _, _, _),
    ArmamentSpec("Hand Of Malenia",              "{} Hand Of Malenia",              KATANA,               [BLEED],              E, S, _, _, _),
    ############ TWINBLADES ############
    ArmamentSpec("Twinblade",                    "{} Twinblade",                 TWINBLADE,            [],                   C, B, _, _, _),
    ArmamentSpec("Twinned Knight Swords",        "{} Twinned Knight Swords",        TWINBLADE,            [],                   C, B, _, _, _),
    ArmamentSpec("Godskin Peeler",               "{} Godskin Peeler",               TWINBLADE,            [],                   C, B, _, _, _),
    ArmamentSpec("Gargoyle's Twinblade",         "Gargoyle's {} Twinblade",         TWINBLADE,            [],                   C, B, _, _, _),
    ArmamentSpec("Gargoyle's Black Blades",      "Gargoyle's {} Black Blades",      TWINBLADE,            [HOLY],               C, B, _, C, _),
    ArmamentSpec("Eleonora's Poleblade",         "Eleonora's {} Poleblade",         TWINBLADE,            [FIRE, BLEED],        C, B, _, _, B),
    ############ AXES ############
    ArmamentSpec("Hand Axe",                     "{} Hand Axe",                  AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Forked Hatchet",               "{} Forked Hatchet",               AXE,                  [BLEED],              B, C, _, _, _),
    ArmamentSpec("Battle Axe",                   "{} Battle Axe",                AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Jawbone Axe",                  "{} Jawbone Axe",               AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Warped Axe",                   "{} Warped Axe",                AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Iron Cleaver",                 "{} Iron Cleaver",              AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Highland Axe",                 "{} Highland Axe",              AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Celebrant's Cleaver",          "Celebrant's {} Cleaver",          AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Ripple Blade",                 "{} Ripple Blade",                 AXE,                  [],                   _, _, _, _, S),
    ArmamentSpec("Icerind Hatchet",              "{} Icerind Hatchet",              AXE,                  [FROSTBITE],          B, C, _, _, _),
    ArmamentSpec("Sacrificial Axe",              "Sacrificial {} Axe",              AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Stormhawk Axe",                "{} Stormhawk Axe",                AXE,                  [],                   B, C, _, _, _),
    ArmamentSpec("Rosus' Axe",                   "Rosus' {} Axe",                   AXE,                  [MAGIC],              C, B, D, _, _),
    ############ GREATAXES ############
    ArmamentSpec("Greataxe",                     "{} Greataxe",                  GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Crescent Moon Axe",            "{} Crescent Moon Axe",         GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Longhaft Axe",                 "{} Longhaft Axe",              GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Executioner's Greataxe",       "Executioner's {} Greataxe",    GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Great Omenkiller Cleaver",     "Great Omenkiller {} Cleaver",     GREATAXE,             [BLEED],              S, E, _, _, _),
    ArmamentSpec("Rusted Anchor",                "{} Rusted Anchor",             GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Gargoyle's Great Axe",         "Gargoyle's {} Great Axe",         GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Gargoyle's Black Axe",         "Gargoyle's {} Black Axe",         GREATAXE,             [HOLY],               A, E, _, D, _),
    ArmamentSpec("Butchering Knife",             "{} Butchering Knife",             GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Winged Greathorn",             "{} Winged Greathorn",             GREATAXE,             [],                   S, E, _, _, _),
    ArmamentSpec("Axe of Godrick",               "{} Axe of Godrick",               GREATAXE,             [],                   S, E, _, _, _),
    ############ HAMMERS ############
    ArmamentSpec("Club",                         "{} Club",                      HAMMER,               [],                   S, _, _, _, _),
    ArmamentSpec("Curved Club",                  "{} Curved Club",               HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Stone Club",                   "{} Stone Club",                HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Mace",                         "{} Mace",                      HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Spiked Club",                  "{} Spiked Club",               HAMMER,               [BLEED],              A, D, _, _, _),
    ArmamentSpec("Morning Star",                 "{} Morning Star",              HAMMER,               [BLEED],              A, D, _, _, _),
    ArmamentSpec("Warpick",                      "{} Warpick",                   HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Hammer",                       "{} Hammer",                    HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Monk's Flamemace",             "Monk's {} Flamemace",             HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Varré's Bouquet",              "Varré's {} Bouquet",              HAMMER,               [BLEED],              B, D, _, _, C),
    ArmamentSpec("Envoy's Horn",                 "Envoy's {} Horn",                 HAMMER,               [HOLY],               B, D, _, D, _),
    ArmamentSpec("Nox Flowing Hammer",           "{} Nox Flowing Hammer",           HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Ringed Finger",                "{} Ringed Finger",                HAMMER,               [],                   A, D, _, _, _),
    ArmamentSpec("Scepter Of The All-Knowing",   "{} Scepter Of The All-Knowing",   HAMMER,               [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Marika's Hammer",              "Marika's {} Hammer",              HAMMER,               [HOLY],               B, D, _, D, _),
    ############ FLAILS ############
    ArmamentSpec("Flail",                        "{} Flail",                     FLAILS,               [BLEED],              C, B, _, _, _),
    ArmamentSpec("Nightrider Flail",             "{} Nightrider Flail",          FLAILS,               [BLEED],              C, B, _, _, _),
    ArmamentSpec("Chainlink Flail",              "{} Chainlink Flail",           FLAILS,               [BLEED],              B, C, _, _, _),
    ArmamentSpec("Family Heads",                 "{} Family Heads",                 FLAILS,               [MAGIC],              C, B, D, _, _),
    ArmamentSpec("Bastard's Stars",              "Bastard's {} Stars",              FLAILS,               [MAGIC],              C, B, D, _, _),
    ############ GREAT HAMMERS ############
    ArmamentSpec("Large Club",                   "{} Large Club",                GREAT_HAMMER,         [],                   S, _, _, _, _),
    ArmamentSpec("Curved Great Club",            "{} Curved Great Club",         GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Great Mace",                   "{} Great Mace",                GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Pickaxe",                      "{} Pickaxe",                   GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Brick Hammer",                 "{} Brick Hammer",              GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Battle Hammer",                "{} Battle Hammer",             GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Rotten Battle Hammer",         "{} Rotten Battle Hammer",         GREAT_HAMMER,         [SCARLET_ROT],        S, E, _, _, _),
    ArmamentSpec("Celebrant's Skull",            "Celebrant's {} Skull",            GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Great Stars",                  "{} Great Stars",                  GREAT_HAMMER,         [BLEED],              S, E, _, _, _),
    ArmamentSpec("Greathorn Hammer",             "Greathorn {} Hammer",             GREAT_HAMMER,         [],                   S, E, _, _, _),
    ArmamentSpec("Envoy's Long Horn",            "Envoy's {} Long Horn",            GREAT_HAMMER,         [HOLY],               A, E, _, D, _),
    ArmamentSpec("Cranial Vessel Candlestand",   "{} Cranial Vessel Candlestand",   GREAT_HAMMER,         [FIRE],               A, E, _, D, _),
    ArmamentSpec("Beastclaw Greathammer",        "Beastclaw {} Greathammer",        GREAT_HAMMER,         [HOLY],               A, E, _, D, _),
    ArmamentSpec("Devourer's Scepter",           "Devourer's {} Scepter",           GREAT_HAMMER,         [FIRE],               A, E, _, D, _),
    ############ COLOSSAL WEAPONS ############
    ArmamentSpec("Raider's Greataxe",            "Raider's Greataxe",            COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Duelist Greataxe",             "Duelist {} Greataxe",             COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Rotten Greataxe",              "{} Rotten Greataxe",              COLOSSAL_WEAPON,      [SCARLET_ROT],        S, _, _, _, _),
    ArmamentSpec("Golem's Halberd",              "Golem's {} Halberd",              COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Giant-Crusher",                "{} Giant-Crusher",                COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Great Club",                   "{} Great Club",                   COLOSSAL_WEAPON,      [HOLY],               A, _, _, D, _),
    ArmamentSpec("Troll's Hammer",               "Troll's {} Hammer",               COLOSSAL_WEAPON,      [FIRE],               A, _, _, D, _),
    ArmamentSpec("Prelate's Inferno Crozier",    "Prelate's {} Inferno Crozier",    COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Dragon Greatclaw",             "{} Dragon Greatclaw",             COLOSSAL_WEAPON,      [LIGHTNING],          S, _, _, _, _),
    ArmamentSpec("Watchdog's Staff",             "Watchdog's {} Staff",             COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ArmamentSpec("Staff Of The Avatar",          "{} Staff Of The Avatar",          COLOSSAL_WEAPON,      [HOLY],               A, _, _, D, _),
    ArmamentSpec("Rotten Staff",                 "{} Rotten Staff",                 COLOSSAL_WEAPON,      [SCARLET_ROT],        S, _, _, _, _),
    ArmamentSpec("Envoy's Greathorn",            "Envoy's {} Greathorn",            COLOSSAL_WEAPON,      [HOLY],               A, _, _, D, _),
    ArmamentSpec("Ghiza's Wheel",                "Ghiza's {} Wheel",                COLOSSAL_WEAPON,      [BLEED],              S, _, _, _, _),
    ArmamentSpec("Fallingstar Beast Jaw",        "{} Fallingstar Beast Jaw",        COLOSSAL_WEAPON,      [MAGIC],              A, _, D, _, _),
    ArmamentSpec("Axe Of Godfrey",               "{} Axe Of Godfrey",               COLOSSAL_WEAPON,      [],                   S, _, _, _, _),
    ############ SPEARS ############
    ArmamentSpec("Short Spear",                  "{} Short Spear",               SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Iron Spear",                   "{} Iron Spear",                SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Spear",                        "{} Spear",                     SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Partisan",                     "{} Partisan",                  SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Pike",                         "{} Pike",                      SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Spiked Spear",                 "{} Spiked Spear",              SPEAR,                [BLEED],              C, B, _, _, _),
    ArmamentSpec("Cross-Naginata",               "{} Cross-Naginata",               SPEAR,                [BLEED],              C, B, _, _, _),
    ArmamentSpec("Clayman's Harpoon",            "Clayman's {} Harpoon",            SPEAR,                [MAGIC],              C, B, C, _, _),
    ArmamentSpec("Celebrant's Rib-Rake",         "Celebrant's {} Rib-Rake",         SPEAR,                [],                   C, B, _, _, _),
    ArmamentSpec("Torchpole",                    "{} Torchpole",                 SPEAR,                [FIRE],               C, B, _, _, _),
    ArmamentSpec("Crystal Spear",                "{} Crystal Spear",                SPEAR,                [MAGIC],              C, B, C, _, _),
    ArmamentSpec("Rotten Crystal Spear",         "{} Rotten Crystal Spear",         SPEAR,                [MAGIC, SCARLET_ROT], C, B, C, _, _),
    ArmamentSpec("Inquisitor's Girandole",       "Inquisitor's {} Girandole",       SPEAR,                [FIRE, BLEED],        C, B, _, C, _),
    ArmamentSpec("Cleanrot Spear",               "{} Cleanrot Spear",               SPEAR,                [HOLY],               C, B, _, C, _),
    ArmamentSpec("Death Ritual Spear",           "Death Ritual {} Spear",           SPEAR,                [MAGIC],              C, B, C, _, _),
    ArmamentSpec("Bolt Of Gransax",              "{} Bolt Of Gransax",              SPEAR,                [LIGHTNING],          C, B, _, _, _),
    ############ GREAT SPEARS ############
    ArmamentSpec("Lance",                        "{} Lance",                     GREAT_SPEAR,          [],                   B, C, _, _, _),
    ArmamentSpec("Treespear",                    "{} Treespear",                    GREAT_SPEAR,          [HOLY],               C, B, _, D, _),
    ArmamentSpec("Serpent-Hunter",               "{} Serpent-Hunter",            GREAT_SPEAR,          [],                   B, C, _, _, _),
    ArmamentSpec("Siluria's Tree",               "Siluria's {} Tree",               GREAT_SPEAR,          [HOLY],               B, C, _, D, _),
    ArmamentSpec("Vyke's War Spear",             "Vyke's {} War Spear",             GREAT_SPEAR,          [FIRE, MADNESS],      B, C, _, D, _),
    ArmamentSpec("Mohgwyn's Sacred Spear",       "Mohgwyn's {} Sacred Spear",       GREAT_SPEAR,          [FIRE, BLEED],        B, C, _, _, C),
    ############ HALBERDS ############
    ArmamentSpec("Guardian's Halberd",           "Guardian's Halberd",           HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Halberd",                      "{} Halberd",                   HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Banished Knight's Halberd",    "Banished Knight's {} Halberd",    HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Lucerne",                      "{} Lucerne",                   HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Glaive",                       "{} Glaive",                    HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Vulgar Militia Shotel",        "{} Vulgar Militia Shotel",        HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Vulgar Militia Saw",           "{} Vulgar Militia Saw",           HALBERD,              [BLEED],              B, C, _, _, _),
    ArmamentSpec("Guardian's Swordspear",        "Guardian's {} Swordspear",        HALBERD,              [],                   E, S, _, _, _),
    ArmamentSpec("Nightrider Glaive",            "Nightrider Glaive",            HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Pest's Glaive",                "Pest's {} Glaive",                HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Ripple Crescent Halberd",      "Ripple Crescent {} Halberd",      HALBERD,              [],                   _, _, _, _, S),
    ArmamentSpec("Gargoyle's Halberd",           "Gargoyle's {} Halberd",           HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Gargoyle's Black Halberd",     "Gargoyle's {} Black Halberd",     HALBERD,              [HOLY],               B, C, _, C, _),
    ArmamentSpec("Golden Halberd",               "Golden {} Halberd",               HALBERD,              [HOLY],               B, C, _, C, _),
    ArmamentSpec("Dragon Halberd",               "{} Dragon Halberd",               HALBERD,              [],                   B, C, _, _, _),
    ArmamentSpec("Loretta's War Sickle",         "Loretta's {} War Sickle",         HALBERD,              [MAGIC],              B, C, C, _, _),
    ArmamentSpec("Commander's Standard",         "Commander's {} Standard",         HALBERD,              [],                   B, C, _, _, _),
    ############ REAPERS ############
    ArmamentSpec("Scythe",                       "{} Scythe",                    REAPER,               [BLEED],              D, A, _, _, _),
    ArmamentSpec("Grave Scythe",                 "{} Grave Scythe",              REAPER,               [BLEED],              D, A, _, _, _),
    ArmamentSpec("Halo Scythe",                  "{} Halo Scythe",                  REAPER,               [HOLY, BLEED],        D, B, _, D, _),
    ArmamentSpec("Winged Scythe",                "{} Winged Scythe",                REAPER,               [HOLY, BLEED],        D, B, _, D, _),
    ############ WHIPS ############
    ArmamentSpec("Whip",                         "{} Whip",                      WHIP,                 [],                   D, A, _, _, _),
    ArmamentSpec("Thorned Whip",                 "{} Thorned Whip",              WHIP,                 [BLEED],              D, A, _, _, _),
    ArmamentSpec("Urumi",                        "{} Urumi",                     WHIP,                 [],                   D, A, _, _, _),
    ArmamentSpec("Hoslow's Petal Whip",          "Hoslow's {} Petal Whip",          WHIP,                 [BLEED],              D, A, _, _, _),
    ArmamentSpec("Magma Whip Candlestick",       "{} Magma Whip Candlestick",       WHIP,                 [FIRE],               D, A, _, D, _),
    ArmamentSpec("Giant's Red Braid",            "Giant's {} Red Braid",            WHIP,                 [FIRE],               D, A, _, D, _),
    ############ FISTS ############
    ArmamentSpec("Revenant's Cursed Claws",      "Revenant's Cursed Claws",      FIST,                 [MAGIC],              E, _, _, S, _),
    ArmamentSpec("Katar",                        "{} Katar",                     FIST,                 [],                   B, C, _, _, _),
    ArmamentSpec("Caestus",                      "{} Caestus",                   FIST,                 [],                   B, C, _, _, _),
    ArmamentSpec("Spiked Caestus",               "{} Spiked Caestus",            FIST,                 [BLEED],              B, C, _, _, _),
    ArmamentSpec("Iron Ball",                    "{} Iron Ball",                 FIST,                 [],                   B, C, _, _, _),
    ArmamentSpec("Star Fist",                    "{} Star Fist",                 FIST,                 [BLEED],              B, C, _, _, _),
    ArmamentSpec("Clinging Bone",                "{} Clinging Bone",                FIST,                 [MAGIC],              B, C, _, _, B),
    ArmamentSpec("Veteran's Prosthesis",         "Veteran's {} Prosthesis",         FIST,                 [LIGHTNING],          B, C, _, _, _),
    ArmamentSpec("Cipher Pata",                  "{} Cipher Pata",                  FIST,                 [HOLY],               _, _, _, S, _),
    ArmamentSpec("Grafted Dragon",               "{} Grafted Dragon",               FIST,                 [FIRE],               B, C, _, C, _),
    ############ CLAWS ############
    ArmamentSpec("Hookclaws",                    "{} Hookclaws",                 CLAWS,                [BLEED],              D, A, _, _, _),
    ArmamentSpec("Bloodhound Claws",             "{} Bloodhound Claws",          CLAWS,                [BLEED],              D, A, _, _, _),
    ArmamentSpec("Venomous Fang",                "{} Venomous Fang",             CLAWS,                [POISON],             D, A, _, _, _),
    ArmamentSpec("Raptor Talons",                "{} Raptor Talons",             CLAWS,                [BLEED],              D, A, _, _, _),
    ############ BOWS ############
    ArmamentSpec("Ironeye's Bow",                "Ironeye's Bow",                BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Shortbow",                     "{} Shortbow",                  BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Misbegotten Shortbow",         "{} Misbegotten Shortbow",         BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Longbow",                      "{} Longbow",                   BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Composite Bow",                "{} Composite Bow",             BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Red Branch Shortbow",          "{} Red Branch Shortbow",          BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Harp Bow",                     "{} Harp Bow",                     BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Albinauric Bow",               "{} Albinauric Bow",               BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Horn Bow",                     "{} Horn Bow",                     BOW,                  [MAGIC],              E, A, D, _, _),
    ArmamentSpec("Black Bow",                    "{} Black Bow",                    BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Pulley Bow",                   "{} Pulley Bow",                   BOW,                  [],                   E, S, _, _, _),
    ArmamentSpec("Serpent Bow",                  "{} Serpent Bow",                  BOW,                  [POISON],             E, A, _, _, C),
    ArmamentSpec("Erdtree Bow",                  "{} Erdtree Bow",                  BOW,                  [HOLY],               E, A, _, D, _),
    ############ GREATBOWS ############
    ArmamentSpec("Greatbow",                     "{} Greatbow",                  GREATBOW,             [],                   B, C, _, _, _),
    ArmamentSpec("Golem Greatbow",               "{} Golem Greatbow",            GREATBOW,             [],                   B, C, _, _, _),
    ArmamentSpec("Erdtree Greatbow",             "{} Erdtree Greatbow",             GREATBOW,             [HOLY],               C, C, _, C, _),
    ArmamentSpec("Lion Greatbow",                "{} Lion Greatbow",                GREATBOW,             [],                   B, C, _, _, _),
    ############ CROSSBOWS ############
    ArmamentSpec("Soldier's Crossbow",           "Soldier's {} Crossbow",           CROSSBOW,             [],                   _, _, _, _, _),
    ArmamentSpec("Light Crossbow",               "{} Light Crossbow",            CROSSBOW,             [],                   _, _, _, _, _),
    ArmamentSpec("Heavy Crossbow",               "{} Heavy Crossbow",            CROSSBOW,             [],                   _, _, _, _, _),
    ArmamentSpec("Arbalest",                     "{} Arbalest",                  CROSSBOW,             [],                   _, _, _, _, _),
    ArmamentSpec("Crepus's Black-Key Crossbow",  "Crepus's {} Black-Key Crossbow",  CROSSBOW,             [],                   _, _, _, _, _),
    ArmamentSpec("Full Moon Crossbow",           "{} Full Moon Crossbow",           CROSSBOW,             [MAGIC],              _, _, _, _, _),
    ArmamentSpec("Pulley Crossbow",              "{} Pulley Crossbow",              CROSSBOW,             [],                   _, _, _, _, _),
    ############ BALLISTAS ############
    ArmamentSpec("Hand Ballista",                "{} Hand Ballista",             BALLISTA,             [],                   _, _, _, _, _),
    ArmamentSpec("Jar Cannon",                   "{} Jar Cannon",                BALLISTA,             [],                   _, _, _, _, _),
    ############ TORCHES ############
    ArmamentSpec("Torch",                        "{} Torch",                     TORCH,                [FIRE],               B, B, _, _, _),
    ArmamentSpec("Beast-Repellent Torch",        "Beast-Repellent {} Torch",        TORCH,                [FIRE],               B, B, _, _, _),
    ArmamentSpec("Steel-Wire Torch",             "Steel-Wire {} Torch",             TORCH,                [FIRE],               B, B, _, _, _),
    ArmamentSpec("Sentry's Torch",               "Sentry's {} Torch",               TORCH,                [FIRE, HOLY],         C, C, _, D, _),
    ArmamentSpec("Ghostflame Torch",             "Ghostflame {} Torch",             TORCH,                [MAGIC, FROSTBITE],   C, C, D, _, _),
    ArmamentSpec("St. Trina's Torch",            "St. Trina's {} Torch",            TORCH,                [FIRE, SLEEP],        C, C, _, D, _),
    ############ SMALL SHIELDS ############
    ArmamentSpec("Wylder's Small Shield",        "Wylder's Small Shield",        SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Rickety Shield",               "{} Rickety Shield",            SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Riveted Wooden Shield",        "{} Riveted Wooden Shield",     SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Blue-White Wooden Shield",     "{} Blue-White Wooden Shield",  SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Scripture Wooden Shield",      "{} Scripture Wooden Shield",   SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Red Thorn Roundshield",        "{} Red Thorn Roundshield",     SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Pillory Shield",               "{} Pillory Shield",            SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Buckler",                      "{} Buckler",                   SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Iron Roundshield",             "{} Iron Roundshield",          SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Gilded Iron Shield",           "{} Gilded Iron Shield",        SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Man-Serpent's Shield",         "Man-Serpent's {} Shield",         SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Ice Crest Shield",             "Ice Crest {} Shield",             SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Rift Shield",                  "Rift {} Shield",                  SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Perfumer's Shield",            "Perfumer's {} Shield",            SMALL_SHIELD,         [],                   B, C, _, _, _),
    ArmamentSpec("Shield Of The Guilty",         "{} Shield Of The Guilty",         SMALL_SHIELD,         [BLEED],              B, C, _, _, _),
    ArmamentSpec("Spiralhorn Shield",            "Spiralhorn {} Shield",            SMALL_SHIELD,         [BLEED],              B, C, _, _, _),
    ArmamentSpec("Smoldering Shield",            "Smoldering {} Shield",            SMALL_SHIELD,         [FIRE],               B, C, _, D, _),
    ArmamentSpec("Coil Shield",                  "{} Coil Shield",                  SMALL_SHIELD,         [POISON],             B, C, _, _, _),
    ############ MEDIUM SHIELDS ############
    ArmamentSpec("Hawk Crest Wooden Shield",     "{} Hawk Crest Wooden Shield",  MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Horse Crest Wooden Shield",    "{} Horse Crest Wooden Shield", MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Candletree Wooden Shield",     "{} Candletree Wooden Shield",  MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Flame Crest Wooden Shield",    "{} Flame Crest Wooden Shield", MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Marred Wooden Shield",         "{} Marred Wooden Shield",         MEDIUM_SHIELD,        [BLEED],              A, D, _, _, _),
    ArmamentSpec("Round Shield",                 "{} Round Shield",              MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Marred Leather Shield",        "{} Marred Leather Shield",        MEDIUM_SHIELD,        [BLEED],              A, D, _, _, _),
    ArmamentSpec("Heater Shield",                "{} Heater Shield",             MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Blue Crest Heater Shield",     "{} Blue Crest Heater Shield",  MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Red Crest Heater Shield",      "{} Red Crest Heater Shield",   MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Beast Crest Heater Shield",    "{} Beast Crest Heater Shield", MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Inverted Hawk Heater Shield",  "{} Inverted Hawk Heater Shield", MEDIUM_SHIELD,      [],                   A, D, _, _, _),
    ArmamentSpec("Eclipse Crest Heater Shield",  "{} Eclipse Crest Heater Shield", MEDIUM_SHIELD,      [],                   A, D, _, _, _),
    ArmamentSpec("Sun Realm Shield",             "{} Sun Realm Shield",          MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Large Leather Shield",         "{} Large Leather Shield",      MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Black Leather Shield",         "{} Black Leather Shield",      MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Kite Shield",                  "{} Kite Shield",               MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Blue-Gold Kite Shield",        "{} Blue-Gold Kite Shield",     MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Scorpion Kite Shield",         "{} Scorpion Kite Shield",      MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Twinbird Kite Shield",         "{} Twinbird Kite Shield",      MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Brass Shield",                 "{} Brass Shield",              MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Banished Knight's Shield",     "Banished Knight's {} Shield",     MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Albinauric Shield",            "{} Albinauric Shield",            MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Beastman's Jar-Shield",        "Beastman's {} Jar-Shield",        MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ArmamentSpec("Carian Knight's Shield",       "Carian Knight's {} Shield",       MEDIUM_SHIELD,        [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Silver Mirrorshield",          "{} Silver Mirrorshield",          MEDIUM_SHIELD,        [MAGIC],              B, D, D, _, _),
    ArmamentSpec("Great Turtle Shell",           "Great Turtle Shell",           MEDIUM_SHIELD,        [],                   A, D, _, _, _),
    ############ GREATSHIELDS ############
    ArmamentSpec("Guardian's Greatshield",       "Guardian's {} Greatshield",       GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Wooden Greatshield",           "{} Wooden Greatshield",        GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Lordsworn's Shield",           "Lordsworn's {} Shield",           GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Manor Towershield",            "{} Manor Towershield",            GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Crossed-Tree Towershield",     "{} Crossed-Tree Towershield",     GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Inverted Hawk Towershield",    "{} Inverted Hawk Towershield",    GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Dragon Towershield",           "{} Dragon Towershield",           GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Briar Greatshield",            "{} Briar Greatshield",            GREATSHIELD,          [BLEED],              A, D, _, _, _),
    ArmamentSpec("Spiked Palisade Shield",       "{} Spiked Palisade Shield",       GREATSHIELD,          [BLEED],              A, D, _, _, _),
    ArmamentSpec("Icon Shield",                  "{} Icon Shield",                  GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Golden Beast Crest Shield",    "{} Golden Beast Crest Shield",    GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Distinguished Greatshield",    "{} Distinguished Greatshield",    GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Gilded Greatshield",           "{} Gilded Greatshield",           GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Cuckoo Greatshield",           "{} Cuckoo Greatshield",           GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Redmane Greatshield",          "{} Redmane Greatshield",          GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Golden Greatshield",           "{} Golden Greatshield",           GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Haligtree Crest Greatshield",  "{} Haligtree Crest Greatshield",  GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Eclipse Crest Greatshield",    "{} Eclipse Crest Greatshield",    GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Crucible Hornshield",          "{} Crucible Hornshield",          GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Dragonclaw Shield",            "{} Dragonclaw Shield",            GREATSHIELD,          [LIGHTNING],          A, D, _, _, _),
    ArmamentSpec("Fingerprint Stone Shield",     "{} Fingerprint Stone Shield",     GREATSHIELD,          [MADNESS],            A, D, _, _, _),
    ArmamentSpec("Ant's Skull Plate",            "Ant's {} Skull Plate",            GREATSHIELD,          [POISON],             A, D, _, _, _),
    ArmamentSpec("Erdtree Greatshield",          "{} Erdtree Greatshield",          GREATSHIELD,          [HOLY],               A, D, _, D, _),
    ArmamentSpec("Jellyfish Shield",             "{} Jellyfish Shield",             GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("Visage Shield",                "{} Visage Shield",                GREATSHIELD,          [],                   A, D, _, _, _),
    ArmamentSpec("One-Eyed Shield",              "{} One-Eyed Shield",              GREATSHIELD,          [],                   A, D, _, _, _),
    ############ GLINTSTONE STAFFS ############
    ArmamentSpec("Recluse's Staff",              "Recluse's Staff",              GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Astrologer's Staff",           "Astrologer's Staff",           GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Glintstone Staff",             "Glintstone Staff",             GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Academy Glintstone Staff",     "Academy Glintstone Staff",     GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Digger's Staff",               "Digger's Staff",               GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Demi-Human Queen's Staff",     "Demi-Human Queen's Staff",     GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Carian Glintstone Staff",      "Carian Glintstone Staff",      GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Carian Glintblade Staff",      "Carian Glintblade Staff",      GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Albinauric Staff",             "Albinauric Staff",             GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Staff Of Loss",                "Staff Of Loss",                GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Gelmir Glintstone Staff",      "Gelmir Glintstone Staff",      GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Crystal Staff",                "Crystal Staff",                GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Rotten Crystal Staff",         "Rotten Crystal Staff",         GLINTSTONE_STAFF,     [SCARLET_ROT],        _, _, S, _, _),
    ArmamentSpec("Staff Of The Guilty",          "Staff Of The Guilty",          GLINTSTONE_STAFF,     [BLEED],              _, _, S, _, _),
    ArmamentSpec("Azur's Glintstone Staff",      "Azur's Glintstone Staff",      GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Lusat's Glintstone Staff",     "Lusat's Glintstone Staff",     GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Meteorite Staff",              "Meteorite Staff",              GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Prince Of Death's Staff",      "Prince Of Death's Staff",      GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ArmamentSpec("Carian Regal Scepter",         "Carian Regal Scepter",         GLINTSTONE_STAFF,     [],                   _, _, S, _, _),
    ############ SACRED SEALS ############
    ArmamentSpec("Finger Seal",                  "Finger Seal",                  SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Gravel Stone Seal",            "Gravel Stone Seal",            SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Giant's Seal",                 "Giant's Seal",                 SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Godslayer's Seal",             "Godslayer's Seal",             SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Clawmark Seal",                "Clawmark Seal",                SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Erdtree Seal",                 "Erdtree Seal",                 SACRED_SEAL,          [HOLY],               _, _, _, S, _),
    ArmamentSpec("Golden Order Seal",            "Golden Order Seal",            SACRED_SEAL,          [],                   _, _, _, S, _),
    ArmamentSpec("Frenzied Flame Seal",          "Frenzied Flame Seal",          SACRED_SEAL,          [MADNESS],            _, _, _, S, _),
    ArmamentSpec("Dragon Communion Seal",        "Dragon Communion Seal",        SACRED_SEAL,          [],                   _, _, _, S, _),
])

EXPANDED_ARMAMENT_SPECS: set[ArmamentSpec] = set()
for armament in ARMAMENT_SPECS:
    if armament.modifiable_name != armament.name:
        # Expand the name using the modifiable name format
        for modifier in MODIFIERS:
            expanded_name = armament.modifiable_name.format(modifier)
            EXPANDED_ARMAMENT_SPECS.add(ArmamentSpec(expanded_name, armament.modifiable_name, armament.type, armament.affinities, armament.STR, armament.DEX, armament.INT, armament.FAI, armament.ARC))
    EXPANDED_ARMAMENT_SPECS.add(armament)