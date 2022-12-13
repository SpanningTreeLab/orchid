# Orchid

A Python animation library for the Blackmagic Fusion API

Built for [Spanning Tree](https://youtube.com/spanningtree)

## Installation

Requires `hatchling` to build.

```
$ pip install -e .
```

## Usage

Requires Blackmagic Fusion or Blackmagic Fusion Studio.

```python
from orchid import Composition

comp = Composition()
comp.add_tool("RectangleMask")
```

## Related Links

- [Fusion Scripting Guide](https://documents.blackmagicdesign.com/UserManuals/Fusion8_Scripting_Guide.pdf)
- [Script Reference](https://www.steakunderwater.com/VFXPedia/96.0.243.189/index8c76.html?title=Eyeon:Script/Reference/Applications/Fusion/Classes)
