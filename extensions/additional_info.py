TYPE_MATCH_ICON = "\U0001f9e4"

def _fmt(v) -> str:
    return str(round(v)) if v is not None else "0"


def get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str:
    if grabbable_spec.get("type") != "armament":
        return ""

    arm_type = str(grabbable_spec.get("armament_type"))

    cut_icons = {
        "physGuardCutRate": "⚔️",
        "magGuardCutRate": "🌀",
        "fireGuardCutRate": "🔥",
        "thunGuardCutRate": "⚡",
        "holyGuardCutRate": "✨",
    }

    resist_icons = {
        "poisonGuardResist": "🧪",
        "scarletRotGuardResist": "🫧",
        "bloodGuardResist": "🩸",
        "curseGuardResist": "💀",
        "sleepGuardResist": "💤",
        "madnessGuardResist": "☀️",
        "freezeGuardResist": "❄️",
    }

    attack_icons = {
        "attackBasePhysics": "⚔️",
        "attackBaseMagic": "🌀",
        "attackBaseFire": "🔥",
        "attackBaseThunder": "⚡",
        "attackBaseHoly": "✨",
    }

    # Shields: show guard cut rates and guard resists (compact emoji tokens)
    if "shield" in arm_type.lower():
        cuts = []
        for key, emoji in cut_icons.items():
            if key in grabbable_spec:
                cuts.append(f"{emoji}{_fmt(grabbable_spec.get(key))}")

        resists = []
        for key, emoji in resist_icons.items():
            if key in grabbable_spec:
                resists.append(f"{emoji}{_fmt(grabbable_spec.get(key))}")

        cut_line = " ".join(cuts)
        resist_line = " ".join(resists)

        if cut_line and resist_line:
            return f"{cut_line}\n{resist_line}"
        return cut_line or resist_line or ""

    is_staff_or_seal = arm_type in ["Glintstone Staff", "Sacred Seal"]

    attacks = []
    for key, emoji in attack_icons.items():
        if is_staff_or_seal:
            continue
        if key in grabbable_spec:
            attacks.append(f"{emoji}{_fmt(grabbable_spec.get(key))}")

    stamina = grabbable_spec.get("attackBaseStamina")
    poise = grabbable_spec.get("poiseDamage")
    revive = grabbable_spec.get("reviveDamage")

    parts = []
    if attacks:
        parts.append(" ".join(attacks))
    parts.append(f"🍏{_fmt(stamina)} | 🪨{_fmt(poise)} | ❤️{_fmt(revive)}")

    return " | ".join(parts) if parts else ""
