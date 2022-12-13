try:
    resolve, fusion
except NameError:
    import DaVinciResolveScript

    resolve = DaVinciResolveScript.scriptapp("Resolve")
    fusion = resolve.Fusion()
