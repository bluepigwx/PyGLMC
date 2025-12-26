from OpenGL.GL import *
import glm

# 一个Shader需要同时包含顶点着色器和片段着色器


def _CreateShader(ShaderCode: str, ShaderType: int) -> int:
    """
    Args:
        ShaderCode: 着色器源代码
        ShaderType: 着色器类型 (GL_VERTEX_SHADER 或 GL_FRAGMENT_SHADER)
    
    Returns:
        成功返回着色器句柄，失败返回 0
    """
    ShaderHandle = glCreateShader(ShaderType)
    glShaderSource(ShaderHandle, ShaderCode)
    glCompileShader(ShaderHandle)

    Success = glGetShaderiv(ShaderHandle, GL_COMPILE_STATUS)
    if not Success:
        ErrorInfo = glGetShaderInfoLog(ShaderHandle)
        ShaderTypeName = "Vertex" if ShaderType == GL_VERTEX_SHADER else "Fragment"
        print(f"Create {ShaderTypeName} Shader failed: {ErrorInfo.decode()}")
        glDeleteShader(ShaderHandle)
        return 0  # 返回 0 表示失败（OpenGL 标准）

    return ShaderHandle


class Shader:
    def __init__(self, VertexShader: str, FragmentShader: str):
        """
        Args:
            VertexShader: 顶点着色器文件路径
            FragmentShader: 片段着色器文件路径
        """
        self.ShaderProgram = 0
        self.IsValid = self._CompileSourceCode(VertexShader, FragmentShader) > 0


    def _CompileSourceCode(self, VertexShader: str, FragmentShader: str) -> int:
        """
        Args:
            VertexShader: 顶点着色器文件路径
            FragmentShader: 片段着色器文件路径
        
        Returns:
            成功返回程序句柄，失败返回 -1
        """
        ShaderProgramHandle = 0
        VertexHandle = 0
        FragmentHandle = 0

        try:
            # 处理定点着色器
            with open(VertexShader, 'r', encoding='utf-8') as vs:
                VertexShaderSource = vs.read()
                VertexHandle = _CreateShader(VertexShaderSource, GL_VERTEX_SHADER)
                if VertexHandle == 0:
                    raise RuntimeError(f"Failed to create vertex shader from {VertexShader}")

            # 处理片段着色器
            with open(FragmentShader, 'r', encoding='utf-8') as fs:
                FragmentShaderSource = fs.read()
                FragmentHandle = _CreateShader(FragmentShaderSource, GL_FRAGMENT_SHADER)
                if FragmentHandle == 0:
                    raise RuntimeError(f"Failed to create fragment shader from {FragmentShader}")

            # 创建着色器程序
            ShaderProgramHandle = glCreateProgram()
            glAttachShader(ShaderProgramHandle, VertexHandle)
            glAttachShader(ShaderProgramHandle, FragmentHandle)
            glLinkProgram(ShaderProgramHandle)
            Success = glGetProgramiv(ShaderProgramHandle, GL_LINK_STATUS)
            if not Success:
                ErrorInfo = glGetProgramInfoLog(ShaderProgramHandle)
                raise RuntimeError(f"Failed to link shader program: {ErrorInfo.decode()}")
            
            self.ShaderProgram = ShaderProgramHandle
            return ShaderProgramHandle

        except FileNotFoundError as e:
            if ShaderProgramHandle > 0:
                glDeleteProgram(ShaderProgramHandle)

            return -1
            
        except Exception as e:
            print(f"Shader compilation error: {e}")
            if ShaderProgramHandle > 0:
                glDeleteProgram(ShaderProgramHandle)

            return -1
            
        finally:
            if VertexHandle > 0:
                glDeleteShader(VertexHandle)
            if FragmentHandle > 0:
                glDeleteShader(FragmentHandle)


    def Use(self):
        """激活着色器"""
        if not self.IsValid:
            raise RuntimeError(f"Shader is not valid when Use")
        
        glUseProgram(self.ShaderProgram)

    
    def GetAttribLocation(self, name):
        return glGetAttribLocation(self.ShaderProgram, name)

    
    def Uniform4f(self, name:str, a:float, b:float, c:float, d:float):
        if not self.IsValid:
            raise RuntimeError(f"Shader is not valid when Uniform4f")
        
        Location = glGetUniformLocation(self.ShaderProgram, name)
        if Location < 0:
            raise RuntimeError(f"Uniform {name} not found in this shader")
        
        glUniform4f(Location, a, b, c, d)

    
    def Uniform1i(self, name:str, a:int):
        if not self.IsValid:
            raise RuntimeError(f"Shader is not valid when Uniform4f")
        
        Location = glGetUniformLocation(self.ShaderProgram, name)
        if Location < 0 :
            raise RuntimeError(f"Unifom {name} not found in this shader")
        
        glUniform1i(Location, a)

    
    def UniformMat4fv(self, name:str, mat4):
        if not self.IsValid:
            raise RuntimeError(f"Shader is not valid")
        
        Location = glGetUniformLocation(self.ShaderProgram, name)
        if Location < 0:
            raise RuntimeError(f"Uniform {name} not found")
        
        glUniformMatrix4fv(Location, 1, GL_FALSE, glm.value_ptr(mat4))


    def Release(self):
        if self.ShaderProgram > 0:
            glDeleteProgram(self.ShaderProgram)
            self.ShaderProgram = 0
            self.IsValid = False