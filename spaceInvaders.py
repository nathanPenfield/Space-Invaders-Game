from core.base import Base 
from core.openGLUtils import OpenGLUtils 
from core.attribute import Attribute 
from core.uniform import Uniform
from core.matrix import Matrix 
from OpenGL.GL import * 
from math import pi
import numpy as np

class Test(Base):
    def initialize(self):
        print("initializing program")
        vsCode = """
            in vec3 position;
            uniform mat4 modelMatrix;
            uniform mat4 projectionMatrix;
            void main(){
                gl_Position = projectionMatrix*modelMatrix*vec4(position, 1.0);
            }"""
        fsCode = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main(){
                fragColor = vec4(baseColor.r,baseColor.g,baseColor.b,1.0);
            }"""
        self.programRef = OpenGLUtils.initializeProgram(vsCode,fsCode)

        ## defender object
        self.vaoDef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoDef)
        positionDataDef =[[0.0,0.1,0.0],[0.05,0.0,0.0],[-0.05,0.0,0.0]]
        self.vertexCountDef = len(positionDataDef)
        positionAttributeDef = Attribute("vec3",positionDataDef)
        positionAttributeDef.associateVariable(self.programRef,"position")
        self.baseColorDef = Uniform("vec3",[1.0,1.0,0.0])
        self.baseColorDef.locateVariable(self.programRef,"baseColor")
        mMatrixDef = Matrix.makeTranslation(0, -0.4, -1) 
        self.modelMatrixDef = Uniform("mat4", mMatrixDef) 
        self.modelMatrixDef.locateVariable(self.programRef,"modelMatrix" )
        pMatrixDef = Matrix.makePerspective() 
        self.projectionMatrixDef = Uniform("mat4", pMatrixDef) 
        self.projectionMatrixDef.locateVariable(self.programRef,"projectionMatrix" )

        
        ## enemy object
        self.vaoEne = glGenVertexArrays(1)
        glBindVertexArray(self.vaoEne)
        positionDataEne=[[0.0,-0.1,0.0],[0.05,0.0,0.0],[-0.05,0.0,0.0]]
        self.vertexCountEne = len(positionDataEne)
        positionAttributeEne = Attribute("vec3",positionDataEne)
        positionAttributeEne.associateVariable(self.programRef,"position")
        self.enemies = []
        for i in np.arange(-0.5,0.2,0.15):
            ## top row
            baseColorEne = Uniform("vec3",[1.0,0.0,0.0])
            baseColorEne.locateVariable(self.programRef,"baseColor")
            mMatrixEne = Matrix.makeTranslation(i, 0.55, -1) 
            modelMatrixEne = Uniform("mat4", mMatrixEne) 
            modelMatrixEne.locateVariable(self.programRef,"modelMatrix" )
            pMatrixEne = Matrix.makePerspective() 
            projectionMatrixEne = Uniform("mat4", pMatrixEne) 
            projectionMatrixEne.locateVariable(self.programRef,"projectionMatrix" )
            self.enemies.append([baseColorEne,modelMatrixEne,projectionMatrixEne])

            ## middle row
            baseColorEne = Uniform("vec3",[1.0,0.0,0.0])
            baseColorEne.locateVariable(self.programRef,"baseColor")
            mMatrixEne = Matrix.makeTranslation(i+0.075, 0.4, -1) 
            modelMatrixEne = Uniform("mat4", mMatrixEne) 
            modelMatrixEne.locateVariable(self.programRef,"modelMatrix" )
            MatrixEne = Matrix.makePerspective() 
            projectionMatrixEne = Uniform("mat4", pMatrixEne) 
            projectionMatrixEne.locateVariable(self.programRef,"projectionMatrix" )
            self.enemies.append([baseColorEne,modelMatrixEne,projectionMatrixEne])

            ## middle row
            baseColorEne = Uniform("vec3",[1.0,0.0,0.0])
            baseColorEne.locateVariable(self.programRef,"baseColor")
            mMatrixEne = Matrix.makeTranslation(i, 0.25, -1) 
            modelMatrixEne = Uniform("mat4", mMatrixEne) 
            modelMatrixEne.locateVariable(self.programRef,"modelMatrix" )
            MatrixEne = Matrix.makePerspective() 
            projectionMatrixEne = Uniform("mat4", pMatrixEne) 
            projectionMatrixEne.locateVariable(self.programRef,"projectionMatrix" )
            self.enemies.append([baseColorEne,modelMatrixEne,projectionMatrixEne])

        self.defenderBombs = []
        self.vaoBomb = glGenVertexArrays(1)
        self.positionDataBomb =[[0.0,0.0,0.0],[-0.01,0.01,0.0],[0.0,0.02,0.0],[0.01,0.01,0.0]]
        self.vertexCountBomb = len(self.positionDataBomb)
        self.spacePressedNow = False
        ## move speed, units per second
        self.moveSpeedDef = 0.35
        self.moveSpeedEne = 0.002
        self.enemyDirection = 1
        
    def update(self):
        ## left and right for defender
        moveAmountDef = self.moveSpeedDef * self.deltaTime
        if self.input.isKeyPressed("right"):  
            m = Matrix.makeTranslation(moveAmountDef,0, 0) 
            self.modelMatrixDef.data = m @ self.modelMatrixDef.data
        if self.input.isKeyPressed("left"): 
            m = Matrix.makeTranslation(-moveAmountDef,0, 0) 
            self.modelMatrixDef.data = m @ self.modelMatrixDef.data

        ## defender shooting with space
        if self.input.isKeyPressed("space"): 
            if not self.spacePressedNow:
                glBindVertexArray(self.vaoBomb)
                positionAttributeBomb = Attribute("vec3",self.positionDataBomb)
                positionAttributeBomb.associateVariable(self.programRef,"position")
                baseColorBomb = Uniform("vec3",[1.0,1.0,1.0])
                baseColorBomb.locateVariable(self.programRef,"baseColor")
                mMatrixBomb = Matrix.makeTranslation(0.0, 0.0, -1) 
                modelMatrixBomb = Uniform("mat4", mMatrixBomb) 
                modelMatrixBomb.locateVariable(self.programRef,"modelMatrix" )
                pMatrixBomb = Matrix.makePerspective() 
                projectionMatrixBomb = Uniform("mat4", pMatrixBomb) 
                projectionMatrixBomb.locateVariable(self.programRef,"projectionMatrix")
                self.defenderBombs.append([baseColorBomb,modelMatrixBomb,projectionMatrixBomb])
                self.spacePressedNow=True
        
        ## movement of enemies. Left to right when changes goes down 0.2 units
        for enemy in self.enemies:
            ## change directions and go down
            if enemy[1].data[0][3]>=0.53:
                self.enemyDirection = -1
                for enemy1 in self.enemies:
                    m = Matrix.makeTranslation(0,-0.1,0)
                    enemy1[1].data = m @ enemy1[1].data
            if enemy[1].data[0][3]<=-0.53:
                self.enemyDirection = 1
                for enemy1 in self.enemies:
                    m = Matrix.makeTranslation(0,-0.05,0)
                    enemy1[1].data = m @ enemy1[1].data  
            ## maybe drop bomb
             
            ## basic movement left or right
            moveAmountEne = self.moveSpeedEne * self.enemyDirection
            m = Matrix.makeTranslation(moveAmountEne,0,0)
            enemy[1].data = m @ enemy[1].data

            
        ## render scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.programRef)
        glBindVertexArray(self.vaoDef)
        self.modelMatrixDef.uploadData()
        self.projectionMatrixDef.uploadData()
        self.baseColorDef.uploadData()
        glDrawArrays(GL_TRIANGLES,0,self.vertexCountDef)
        glBindVertexArray(self.vaoEne)
        for enemy in self.enemies:
            enemy[0].uploadData()
            enemy[1].uploadData()
            enemy[2].uploadData()
            glDrawArrays(GL_TRIANGLES,0,self.vertexCountEne)
        glBindVertexArray(self.vaoBomb)
        for bomb in self.defenderBombs:

            bomb[0].uploadData()
            bomb[1].uploadData()
            bomb[2].uploadData()
            glDrawArrays(GL_TRIANGLE_FAN,0,self.vertexCountBomb)
        
Test().run()