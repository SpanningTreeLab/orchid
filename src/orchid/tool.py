import re

from .input import Input
from .util import fusion_list_process


class Tool(object):
    def __init__(self, tool):
        """
        Create a new tool object.

        Arguments:
            tool : BlackmagicFusion.Tool - tool object
        """
        if tool is None:
            raise Exception("Tool cannot be None")
        self._tool = tool

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tool ({self.name})>"

    @property
    def composition(self):
        """Composition associated with the tool."""
        from .composition import Composition

        return Composition(self._tool.Composition)

    @property
    def name(self):
        """Name for the tool."""
        return self._tool.Name

    @name.setter
    def name(self, name):
        """Set name for the tool."""
        self._tool.SetAttrs({"TOOLS_Name": name})

    def inputs(self):
        """
        Return a list of all Inputs associated with a given tool.

        Returns:
            List[Input] - All inputs associated with tool
        """
        inputs = fusion_list_process(self._tool.GetInputList)()
        return [Input(i) for i in inputs]

    def get_input(self, name):
        """
        Return an Input object by its name.

        Arguments:
            name -- name of the input

        Returns:
            Input | None -- Input object if found on the tool, None otherwise
        """
        for inp in self.inputs():
            if inp.name == name:
                return inp
        return None

    def children(self):
        """
        Return children tools of the current tool.

        Returns:
            List[Tool] - List of all children tools
        """
        tools = fusion_list_process(self._tool.GetChildrenList)()
        return [Tool(t) for t in tools]

    def get_child_by_pattern(self, regex):
        """
        Get first child matching a particular name pattern.
        """
        for child in self.children():
            if re.match(regex, child.name):
                return child
        return None

    def is_attr_animated(self, attr_name):
        """
        Checks if tool's attribute is animated.

        Arguments:
            attr_name : str - Name of attribute to check

        Returns:
            Bool - True if tool's attribute is animated, False otherwise
        """
        return getattr(self._tool, attr_name).GetConnectedOutput() is not None

    def set_attr(self, attr_name, attr_value, keyframe=None):
        """
        Set an input's value for the tool.
        If a keyframe is provided, value is set for the given frame.
        If no keyframe provided, keyframe is added for the current frame
        if the attribute is already animated.

        Arguments:
            attr_name : str - Name of attribute to set
            attr_value : Any - Value of attribute

        Optional arguments:
            keyframe : int - Keyframe to associate with value
        """
        is_animated = self.is_attr_animated(attr_name)
        if is_animated:
            if keyframe is None:
                # Set value for the current keyframe
                frame = self.composition.frame
                self._tool.SetInput(attr_name, attr_value, frame)
            else:
                # Set value fir indicated keyframe
                self._tool.SetInput(attr_name, attr_value, keyframe)
        else:
            if keyframe is None:
                # Set value, no keyframe
                self._tool.SetInput(attr_name, attr_value)
            else:
                # Set value, add keyframe after
                self._tool.SetInput(attr_name, attr_value)
                comp = self.composition
                stored_time = comp.frame
                comp.frame = keyframe
                self._tool.SetInput(attr_name, comp._composition.BezierSpline())
                comp.frame = stored_time

    def get_attr(self, attr_name, keyframe=None):
        """
        Get an input's value at a given keyframe.

        Arguments:
            attr_name : str - Name of attribute to read

        Optional arguments:
            keyframe : int - Keyframe for time to access value, defaults to current
        """
        frame = keyframe or self.composition.frame
        return self._tool.GetInput(attr_name, frame)

    def set_color(self, red, green, blue, alpha=None, keyframe=None):
        """
        Set color attributes for tool.

        Arguments:
            red : float - Red value in range [0, 1]
            green : float - Green value in range [0, 1]
            blue : float - Blue value in range [0, 1]

        Optional arguments:
            alpha : float - Alpha value in range [0, 1]
            keyframe : int - Keyframe to associate with color
        """
        self.set_attr("TopLeftRed", red, keyframe=keyframe)
        self.set_attr("TopLeftGreen", green, keyframe=keyframe)
        self.set_attr("TopLeftBlue", blue, keyframe=keyframe)
        if alpha != None:
            self.set_attr("TopLeftAlpha", alpha, keyframe=keyframe)
