
class VertexAttrib:
    def __init__(self):
        self.Name = None
        self.Num = 0
        self.Span = 0
        self.Offset = None


class CreateMeshContext:
    def __init__(self):
        self.Attribs = []


class Mesh:
    def __init__(self):
        self.VAO = None

    
    def Setup(self, Context): ...

    def Render(self): ...
        