import random
import logging
import sys
from threading import Thread
import os
import time
from abc import ABC, abstractmethod


stop=True

class event(ABC):
  def __init__(self, plane, sleep):
    self.plane=plane
    self.sleep=sleep
  
  @abstractmethod
  def update(self):
    pass


class envimpact(event):
  def update(self,env):
    global stop
    while stop:
      self.plane.roll+=env.roll
      self.plane.pitch+=env.pitch
      self.plane.yaw+=env.yaw
      time.sleep(self.sleep)


class correction(event):
  def __init__(self, plane, sleep, roll, pitch, yaw, roc):
    self.plane=plane
    self.sleep=sleep
    self.roll = roll
    self.pitch = pitch
    self.yaw = yaw
    self.roc=roc

  def update(self):
    global stop
    while stop:
      os.system('clear')
      logging.info("\nBefore Correction: {},  {},  {}".format(self.plane.roll,self.plane.pitch,self.plane.yaw))

      self.plane.roll += self.roc*int((self.roll-self.plane.roll)/self.roc)
      self.plane.pitch += self.roc*int((self.pitch-self.plane.pitch)/self.roc)
      self.plane.yaw += self.roc*int((self.yaw-self.plane.yaw)/self.roc)

      logging.info("\nAfter correction {},  {},  {} \n\nPress Enter to land\n\n\n".format(self.plane.roll,self.plane.pitch,self.plane.yaw))
      time.sleep(self.sleep)


class Plane:
  def __init__(self, roll, pitch, yaw, windres):
    self.roll = roll
    self.pitch = pitch
    self.yaw = yaw
    self.windres= windres


  def tryplane(self):
    global stop
    while stop:
      if abs(self.roll)>self.windres or abs(self.pitch)>self.windres or abs(self.yaw)>self.windres :
        logging.warning("\nToo much turbulence, the plane crashed!\nLast Position: {},  {},  {} \n\nPress Enter to end ".format(self.roll,self.pitch,self.yaw))
        stop=False
        
      


class Environment:
  def __init__(self, windforce,maxwind):
    self.roll = 0
    self.pitch = 0
    self.yaw = 0
    self.windforce=windforce
    self.maxwind=maxwind

  def envirchange(self):
    global stop
    while stop:
      self.roll+=random.gauss(0, self.windforce)
      if self.roll>self.maxwind:
        self.roll-=0.1*self.maxwind
      if self.roll<-self.maxwind:
        self.roll+=0.1*self.maxwind

      self.pitch+=random.gauss(0, self.windforce)
      if self.pitch>self.maxwind:
        self.pitch-=0.1*self.maxwind
      if self.pitch<-self.maxwind:
        self.pitch+=0.1*self.maxwind

      self.yaw+=random.gauss(0, self.windforce)
      if self.yaw>self.maxwind:
        self.yaw-=0.1*self.maxwind
      if self.yaw<-self.maxwind:
        self.yaw+=0.1*self.maxwind


def inputstop():
  global stop
  input()
  stop=False


if __name__ == "__main__":

  logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
  plane = Plane(0,0,0,20)
  env = Environment(0.01,5)
  envimp=envimpact(plane,0.03)
  correct=correction(plane,0.1,0,0,0,1)

  envpr = Thread(target=env.envirchange)
  planech = Thread(target=envimp.update,args=(env,))
  planecor = Thread(target=correct.update)
  planeig = Thread(target=plane.tryplane)
  instop=Thread(target=inputstop)

  envpr.start()
  planech.start()
  planecor.start()
  planeig.start()
  instop.start()

  instop.join()
  envpr.join()
  planech.join()
  planecor.join()
  planeig.join()

  plane.tryplane()

  logging.info('Landed') 
