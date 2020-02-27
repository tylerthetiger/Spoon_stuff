#!/usr/bin/env python2
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
    inst = Instruction(symbol0*2+symbol1*2,self.whileEnd)
    self.instructionList.append(inst)
  
  #  inst = Instruction()
   # i = 
    #self.instructionMapping = dict()
    #self.instructionMapping['']
  def executeOneInstruction(self):
    #make sure our mem array is large enough to be referenced
    while(len(self.a)<=self.ptr):
      self.a.append(0)
    for i in self.instructionList:
      if self.code[self.PC:self.PC+len(i.instructionStr)] == i.instructionStr:
        return i.handler()
    raise Exception("I dont know how to decode instruction: {}".format(self.code[self.PC:]))
  #a[ptr]++
  def incMem(self):
   # print "look at me, i'm the incHandler!"
    self.a[self.ptr]+=1
    self.PC+=1
  #a[ptr]--
  def decMem(self):
    self.a[self.ptr]-=1
  #  print "look at me, i'm the decHandler!"
    self.PC+=3
  def incPtr(self):
    self.ptr+=1
    self.PC+=3
  def decPtr(self):
    self.ptr-=3
    self.PC+=3
  def putChar(self):
    letter=self.a[self.ptr]
    letter=chr(letter)
    print letter,
    self.PC+=6
  def getChar(self):
    char = raw_input()[0]
    #print b
    self.a[self.ptr] = ord(char)
    self.PC+=7
  def whileStart(self):
    raise Exception("TODO, write while start")
  def whileEnd(self):
    raise Exception("TODO, write while end")
  def printState(self):
    print "PC: {}\na:{}\nptr:{}".format(self.PC,self.a,self.ptr)
    print "Code: {}".format(self.code[self.PC:])
  def runIt(self):
    #a = Instruction("1001",self.incHandler)
    #print a
    #a.handler()
    while self.PC<len(self.code):
      self.printState()
      self.executeOneInstruction()

if __name__ == "__main__":
  j = Spoon("code.bin")
  #j = Spoon("test.bin")
  j.runIt()
