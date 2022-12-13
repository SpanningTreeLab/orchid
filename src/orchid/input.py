class Input(object):
    def __init__(self, input):
        """
        Create a new input object.

        Arguments:
            input : BlackmagicFusion.Input -- input object
        """
        self._input = input

    def __str__(self):
        return self._input.Name

    def __repr__(self):
        return f"<Input ({self._input.Name})>"

    @property
    def name(self):
        return self._input.Name
