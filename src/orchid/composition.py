from .davinci_resolve import fusion
from .tool import Tool


class Composition(object):
    def __init__(self, composition=None):
        """
        Create a new composition.

        Arguments:
            composition : BlackmagicFusion.Composition - composition object
        """
        if composition is None:
            composition = fusion.CurrentComp
        self._composition = composition

    @property
    def frame(self):
        """Current keyframe number."""
        return self._composition.CurrentTime

    @frame.setter
    def frame(self, new_frame):
        """Update current keyframe number."""
        self._composition.CurrentTime = new_frame

    @property
    def active_tool(self):
        """Active tool for the composition."""
        tool = self._composition.ActiveTool
        return Tool(tool) if tool is not None else None

    def selected_tools(self):
        """
        Return the selected tools in the composition.

        Returns:
            List[Tool] - list of selected tools
        """
        return [Tool(tool) for tool in self._composition.GetToolList(True)]

    def add_tool(self, tool_type, name=None):
        """
        Create a new tool by tool type.

        Arguments:
            tool_type : str - identifier for tool type (e.g. "Background")

        Optional arguments:
            name : str - name for the tool

        Returns:
            Tool - newly created tool
        """
        tool = Tool(self._composition.AddTool(tool_type))
        if name is not None:
            tool.name = name
        return tool
