# Extensions

**As of version 2.2.x, Nightreign Armament Helper supports extensions** to customize the information provided for each armament. Extensions allow you to define custom logic for displaying icons or text based on the detected armament/item/talisman and character, in order to better suit your preferences.

Unfortunately, you will have to be somewhat familiar with programming to create extensions, as they must be written in Python. However, I urge anyone to try creating their own extension, as it may be easier than you think!

## How Extensions Work

Extensions are Python files placed in the `extensions` folder. The mod automatically loads these files and checks for specific functions that match predefined specifications. If your extension implements these functions correctly, they will be used by the mod.

### Configuring Extensions with `extensions.json`

The `extensions.json` file is located in the `extensions` folder and is used to configure how extensions are loaded. If the file does not exist, the mod will create a template for you. Below is an explanation of the fields in the `extensions.json` file:

```json
{
    "mode_help": "Possible values: override/before/after - override means the extensions will replace the default functions, before means they will be called before the default functions, and after means they will be called after the default functions.",
    "mode": "override",
    "order_help": "Place the name of the extensions to load, in the order they should be loaded.",
    "order": []
}
```

#### Fields

1. **`mode`**:
   - Determines how the extensions interact with the default functions.
   - Possible values:
     - `"override"`: Extensions will replace the default functions entirely.
     - `"before"`: Extensions will be called before the default functions.
     - `"after"`: Extensions will be called after the default functions.
   - Default value: `"override"`.

2. **`order`**:
   - A list of extension filenames (without the `.py` extension) to load, in the order they should be loaded.
   - Example:

     ```json
     "order": ["my_extension", "another_extension"]
     ```

#### Example `extensions.json`

```json
{
    "mode": "before",
    "order": ["my_extension", "another_extension"]
}
```

In this example:

- The extensions `my_extension.py` and `another_extension.py` will be loaded in that order.
- The extensions will be executed **before** the default functions.

## Available Functions for Extensions

1. **`get_basic_label_icons(character_spec: dict, grabbable_spec: dict) -> list[str]`**
   - This function allows you to define custom icons to display for an armament based on the character and armament specifications.
   - **Return Value:** A list of strings representing the icons to display. Each string should correspond to an icon defined in the mod.

2. **`get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str`**
   - This function allows you to define custom text to display for an armament in advanced mode.
   - **Return Value:** A string representing the text to display.

## Format of parameters

- `character_spec`:

```py
{
    "name": str,  # Name of the character
    "armament_types": list[str],  # List of armament types the character prefers
    "STR": str,  # Strength rating of the character (E/D/C/B/A/S)
    "DEX": str,  # Dexterity rating of the character (E/D/C/B/A/S)
    "INT": str,  # Intelligence rating of the character (E/D/C/B/A/S)
    "FAI": str,  # Faith rating of the character (E/D/C/B/A/S)
    "ARC": str,  # Arcane rating of the character (E/D/C/B/A/S)
}
```

- `grabbable_spec`:

```py
{
    "id": str,  # Unique identifier
    "name": str,  # Name of the grabbable
    "type": str,  # Type of grabbable (armament | item | talisman)
    ################################# Armaments only: ##################################
    "armament_type": str,  # Armament type ("Straight Sword", "Greatsword", "Bow", etc.)
    "STR": int,  # Strength scaling (0-100)
    "DEX": int,  # Dexterity scaling (0-100)
    "INT": int,  # Intelligence scaling (0-100)
    "FAI": int,  # Faith scaling (0-100)
    "ARC": int,  # Arcane scaling (0-100)
}
```

## Example Extension

Below is an example of an extension file that adds custom logic for displaying icons and text:

```python
def get_basic_label_icons(character_spec: dict, grabbable_spec: dict) -> list[str]:
    icons = []
    if grabbable_spec["type"] == "armament":
        if grabbable_spec["STR"] >= 50:
            icons.append("💪")
        if grabbable_spec["DEX"] >= 50:
            icons.append("⚡")
    elif grabbable_spec["type"] == "item" and grabbable_spec["name"] == "Wending Grace":
        icons.append("⭐")
    elif grabbable_spec["type"] == "talisman" and grabbable_spec["name"] in ["Graven-School Talisman", "Radagon Icon", "Cerulean Amber Medallion"] and character_spec["name"] == "Recluse":
        icons.append("⭐")
    return icons

def get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str:
    if grabbable_spec["type"] == "armament":
        return f"STR: {grabbable_spec['STR']}, DEX: {grabbable_spec['DEX']}"
    return ""
```

## Adding Your Extension

1. Create a new Python file in the `extensions` folder located at:

    ```text
    %LOCALAPPDATA%\Nightreign Armament Helper\extensions
    ```

2. Implement one or multiple of the functions described above.
3. Add the filename (with or without `.py`) to the `order` field in the `extensions.json` file.
4. Restart the mod to load your extension.

## Debugging Extensions

If your extension is not working as expected:

- Ensure the function signatures match the specifications exactly.
- Check the control panel in the mod to see if your extension is listed under "Loaded Extensions"
- Use print statements or logging in your extension to debug its behavior.

## Notes

- Extensions are isolated and do not interfere with the core functionality of the mod.
- You can implement multiple extensions, and the mod will load all valid extensions in the `extensions` folder.
