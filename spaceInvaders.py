from core.base import Base 
from core.openGLUtils import OpenGLUtils 
from core.attribute import Attribute 
from core.uniform import Uniform
from core.matrix import Matrix 
from OpenGL.GL import * 
from math import pi
import numpy as np
import random

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

        ## defender lives object
        self.vaoLive = glGenVertexArrays(1)
        glBindVertexArray(self.vaoLive)
        positionDataLive=[[0.0,0.08,0.0],[0.04,0.0,0.0],[-0.04,0.0,0.0]]
        self.vertexCountLive = len(positionDataLive)
        positionAttributeLive = Attribute("vec3",positionDataLive)
        positionAttributeLive.associateVariable(self.programRef,"position")
        self.lives = []
        for i in np.arange(-0.5,-0.3,0.1):
            ## top row
            baseColorLive = Uniform("vec3",[1.0,1.0,0.0])
            baseColorLive.locateVariable(self.programRef,"baseColor")
            mMatrixLive = Matrix.makeTranslation(i, -0.55, -1) 
            modelMatrixLive = Uniform("mat4", mMatrixLive) 
            modelMatrixLive.locateVariable(self.programRef,"modelMatrix" )
            pMatrixLive = Matrix.makePerspective() 
            projectionMatrixLive = Uniform("mat4", pMatrixLive) 
            projectionMatrixLive.locateVariable(self.programRef,"projectionMatrix" )
            self.lives.append([baseColorLive,modelMatrixLive,projectionMatrixLive])

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

        ## bombs
        self.defenderBombs = []
        self.attackerBombs = []
        self.vaoBomb = glGenVertexArrays(1)
        self.positionDataBomb =[[0.0,0.0,0.0],[-0.01,0.01,0.0],[0.0,0.02,0.0],[0.01,0.01,0.0]]
        self.vertexCountBomb = len(self.positionDataBomb)
        self.spacePressedNow = False

        ## line object
        self.vaoLine = glGenVertexArrays(1)
        glBindVertexArray(self.vaoLine)
        positionDataLine =[[-0.7,-0.5,0.0],[0.7,-0.5,0.0],[0.7,-0.51,0.0],[-0.7,-0.51,0.0]]
        self.vertexCountLine = len(positionDataLine)
        glBindVertexArray(self.vaoLine)
        positionAttributeLine = Attribute("vec3",positionDataLine)
        positionAttributeLine.associateVariable(self.programRef,"position")
        self.baseColorLine = Uniform("vec3",[1.0,1.0,0.0])
        self.baseColorLine.locateVariable(self.programRef,"baseColor")
        mMatrixLine = Matrix.makeTranslation(0.0, 0.05, -1.0) 
        self.modelMatrixLine = Uniform("mat4", mMatrixLine) 
        self.modelMatrixLine.locateVariable(self.programRef,"modelMatrix" )
        pMatrixLine = Matrix.makePerspective() 
        self.projectionMatrixLine = Uniform("mat4", pMatrixLine) 
        self.projectionMatrixLine.locateVariable(self.programRef,"projectionMatrix" )

        ## move speed, units per second
        self.moveSpeedDef = 0.35
        self.moveSpeedEne = 0.002
        self.enemyDirection = 1
        ## game state
        self.playerAlive = True
        self.livesLeft = 3
        
    def update(self):
        ## left and right for defender
        moveAmountDef = self.moveSpeedDef * self.deltaTime
        if self.input.isKeyPressed("right") and self.playerAlive:  
            m = Matrix.makeTranslation(moveAmountDef,0, 0) 
            self.modelMatrixDef.data = m @ self.modelMatrixDef.data
        if self.input.isKeyPressed("left") and self.playerAlive: 
            m = Matrix.makeTranslation(-moveAmountDef,0, 0) 
            self.modelMatrixDef.data = m @ self.modelMatrixDef.data

        ## defender shooting with space
        if self.input.isKeyPressed("space") and self.playerAlive: 
            if not self.spacePressedNow:
                glBindVertexArray(self.vaoBomb)
                positionAttributeBomb = Attribute("vec3",self.positionDataBomb)
                positionAttributeBomb.associateVariable(self.programRef,"position")
                baseColorBomb = Uniform("vec3",[1.0,1.0,1.0])
                baseColorBomb.locateVariable(self.programRef,"baseColor")
                mMatrixBomb = Matrix.makeTranslation(self.modelMatrixDef.data[0][3], -0.3, -1.0) 
                modelMatrixBomb = Uniform("mat4", mMatrixBomb) 
                modelMatrixBomb.locateVariable(self.programRef,"modelMatrix" )
                pMatrixBomb = Matrix.makePerspective() 
                projectionMatrixBomb = Uniform("mat4", pMatrixBomb) 
                projectionMatrixBomb.locateVariable(self.programRef,"projectionMatrix")
                self.defenderBombs.append([baseColorBomb,modelMatrixBomb,projectionMatrixBomb])
                self.spacePressedNow=True
        else:
            if self.spacePressedNow:
                self.spacePressedNow = False

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
            if random.uniform(0.0,1.0) < 0.0035 and self.playerAlive:
                glBindVertexArray(self.vaoBomb)
                positionAttributeBomb = Attribute("vec3",self.positionDataBomb)
                positionAttributeBomb.associateVariable(self.programRef,"position")
                baseColorBomb = Uniform("vec3",[1.0,1.0,1.0])
                baseColorBomb.locateVariable(self.programRef,"baseColor")
                mMatrixBomb = Matrix.makeTranslation(enemy[1].data[0][3], enemy[1].data[1][3]-0.12, -1) 
                modelMatrixBomb = Uniform("mat4", mMatrixBomb) 
                modelMatrixBomb.locateVariable(self.programRef,"modelMatrix" )
                pMatrixBomb = Matrix.makePerspective() 
                projectionMatrixBomb = Uniform("mat4", pMatrixBomb) 
                projectionMatrixBomb.locateVariable(self.programRef,"projectionMatrix")
                self.attackerBombs.append([baseColorBomb,modelMatrixBomb,projectionMatrixBomb])  
            ## basic movement left or right
            if self.playerAlive:
                moveAmountEne = self.moveSpeedEne * self.enemyDirection
                m = Matrix.makeTranslation(moveAmountEne,0,0)
                enemy[1].data = m @ enemy[1].data

        ## bounds of defender bombs
        for bomb in self.defenderBombs:
            ## stop rendering if off screen
            if bomb[1].data[1][3]>=0.6:
                self.defenderBombs.remove(bomb)

            ## check if hitting an enemy
            for enemy in self.enemies:
                if bomb[1].data[1][3]<enemy[1].data[1][3]-0.02 and bomb[1].data[1][3]>enemy[1].data[1][3]-0.12:
                    ## since its a trianlge the x is sort of relavent to height
                    diff = bomb[1].data[1][3]-enemy[1].data[1][3]
                    diff += 0.12
                    diff = diff/2
                    if bomb[1].data[0][3]<enemy[1].data[0][3]+diff and bomb[1].data[0][3]>enemy[1].data[0][3]-diff and self.playerAlive:
                        self.enemies.remove(enemy)
                        self.defenderBombs.remove(bomb)
    
        ## buonds of attacker bombs
        for bomb in self.attackerBombs:
            ## stop rendering if off screen
            if bomb[1].data[1][3]<=-0.451:
                self.attackerBombs.remove(bomb)
            
            ## check if hitting defender
            if bomb[1].data[1][3]>-0.42 and bomb[1].data[1][3]<-0.32 and self.playerAlive:
                    ## since its a trianlge the x is sort of relavent to height
                    diff = bomb[1].data[1][3]+0.32
                    diff = -1*diff/2
                    if bomb[1].data[0][3]<self.modelMatrixDef.data[0][3]+diff+0.01 and bomb[1].data[0][3]>self.modelMatrixDef.data[0][3]-diff-0.01:
                        ## player lost/losses life
                        if self.livesLeft ==1:
                            ## player lost
                            self.playerAlive = False
                        else:
                            self.livesLeft-=1
                            self.attackerBombs.remove(bomb)
                            self.lives.pop()

        ## check if game won
        if self.enemies == []:
            ## could make this seperate than player alive to diff between player win and lose
            self.playerAlive = False
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
            if self.playerAlive:
                m = Matrix.makeTranslation(0,0.005,0)
                bomb[1].data = m @ bomb[1].data
            bomb[0].uploadData()
            bomb[1].uploadData()
            bomb[2].uploadData()
            glDrawArrays(GL_TRIANGLE_FAN,0,self.vertexCountBomb)
        for bomb in self.attackerBombs:
            if self.playerAlive:
                m = Matrix.makeTranslation(0,-0.005,0)
                bomb[1].data = m @ bomb[1].data
            bomb[0].uploadData()
            bomb[1].uploadData()
            bomb[2].uploadData()
            glDrawArrays(GL_TRIANGLE_FAN,0,self.vertexCountBomb)
        glBindVertexArray(self.vaoLive)
        for life in self.lives:
            life[0].uploadData()
            life[1].uploadData()
            life[2].uploadData()
            glDrawArrays(GL_TRIANGLES,0,self.vertexCountLive)
        glBindVertexArray(self.vaoLine)
        self.modelMatrixLine.uploadData()
        self.projectionMatrixLine.uploadData()
        self.baseColorLine.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN,0,self.vertexCountLine)
Test().run()