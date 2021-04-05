# Experiments with the GDMC HTTP interface mod

These are experiments using the [Minecraft HTTP Interface Mod](https://github.com/nilsgawlik/gdmc_http_interface), and the example scripts in the [GDMC http Client Python](https://github.com/nilsgawlik/gdmc_http_client_python) repository.

# Hints

- To dynamically set the build area for testing, use the `setbuildarea` command from inside minecraft, and use `requestBuildArea` from interfaceUtils.py to get the area around your player. For example, the command below sets a 128x128 area around the player as the building area:

```
setbuildarea ~-64 0 ~-64 ~64 255 ~64
```

- Remember that you can add numpy array to lists and tuples of numbers of the same size.

# Experiments

## 1. Basic Experiments: `experiment_basic.py`

This script shows how to add some blocks, including a sign with text, and
a chest with items and books with text.

## 2. Heightmap Interface: `experiment_heightmap.py`

This script uses the "WorldSlice" object provided by the **GDMC http client python** repository and build a small beacon at the highest point in the building area.

## TODO: Nether invasion

- Choose an appropriate starting location and place a tumour
- Tumour expands to areas of same and lower heights, following biological blocks.
- Tumour increases as it expands
- Bone towers are built at appropriate places during the expancion.
- A human observation outpost is build in an appropriate location with a notebook.

# TODO:
- Improve the client library by providing a tuple-based set/get block command
- Improved "make book item" command that takes \p and \n into account.
