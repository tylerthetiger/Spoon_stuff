#!/usr/bin/env python2
import sys

class Instruction:
  def __init__(self,instructionStr,handler):
    self.instructionStr = instructionStr
    self.handler = handler

class Spoon:
  def __init__(self,code,symbol0="0",symbol1="1"):
    with open(code,"r") as f:
      self.code = f.read().rstrip()
    self.symbol0 = symbol0
    self.symbol1 = symbol1
    self.PC = 0
    self.ptr = 0
    self.a = list()
    self.instructionList = list()
    inst = Instruction(symbol1,self.incMem)
    self.instructionList.append(inst)
    inst = Instruction(symbol0*3,self.decMem)
    self.instructionList.append(inst)

    inst = Instruction(symbol0+symbol1+symbol0,self.incPtr)
    self.instructionList.append(inst)
    inst = Instruction(symbol0+symbol1+symbol1,self.decPtr)
    self.instructionList.append(inst)
    
    inst = Instruction(symbol0*2+symbol1+symbol0+symbol1+symbol0,self.putChar)
    self.instructionList.append(inst)
    inst = Instruction(symbol0*2+symbol1+symbol0+symbol1*2+symbol0,self.getChar)
    self.instructionList.append(inst)
    
    inst = Instruction(symbol0*2+symbol1+symbol0*2,self.whileStart)
    self.instructionList.append(inst)
    #we don't actually look for the while end here
  #  inst = Instruction(symbol0*2+symbol1*2,self.whileEnd)
  #  self.instructionList.append(inst)
  def executeOneInstruction(self):
    #make sure our mem array is large enough to be referenced
    while(len(self.a)<=self.ptr):
      self.a.append(0)
    for i in self.instructionList:
      if self.code[self.PC:self.PC+len(i.instructionStr)] == i.instructionStr:
        return i.handler()
    self.code = self.code.replace("_","0")
    self.code = self.code.replace("-","1")
    raise Exception("I dont know how to decode instruction: {}".format(self.code[self.PC:]))
  def incMem(self):
    self.a[self.ptr]+=1
    self.PC+=1
  def decMem(self):
    self.a[self.ptr]-=1
    self.PC+=3
  def incPtr(self):
    self.ptr+=1
    self.PC+=3
  def decPtr(self):
    self.ptr-=1
    self.PC+=3
  def putChar(self):
    letter=self.a[self.ptr]
    letter=chr(letter)
    sys.stdout.write(letter)
    sys.stdout.flush()
    self.PC+=6
  def getChar(self):
    char = raw_input()[0]
    self.a[self.ptr] = ord(char)
    self.PC+=7
  def executeUntilLoopEnd(self):
    loopEndInstr = self.symbol0*2+self.symbol1*2
    while True:
      if self.code[self.PC:self.PC+len(loopEndInstr)]==loopEndInstr:
        newPC =  self.PC+len(loopEndInstr)
        return newPC
      else:
        self.printState()
        self.executeOneInstruction()

  def whileStart(self):
    loopStart = self.PC+5
    self.PC+=5
    while (self.a[self.ptr]!=0):
      loopEnd = self.executeUntilLoopEnd()
      self.PC = loopStart
    self.PC = loopEnd#jump out of the loop!
    #loop end needs to be just after the loop end instruction

 # def whileEnd(self):
  #  raise Exception("TODO, write while end")
  def printState(self):
    return
    print "PC: {}\na:{}\nptr:{}".format(self.PC,self.a,self.ptr)
    print "Code: {}".format(self.code[self.PC:])
  def runIt(self):
    while self.PC<len(self.code):
      self.printState()
      self.executeOneInstruction()

if __name__ == "__main__":
  #j = Spoon("code.bin")
  j = Spoon("test.bin",symbol0="_",symbol1="-")
  j.runIt()
