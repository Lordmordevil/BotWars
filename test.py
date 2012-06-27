import unittest
from pygamehelper import *
from pygame import *
from vec2d import vec2d
from animation import Animation
from drone import Drone
from resource import Ore
from buildings import Building, MainBase, UpgradeFactory, \
                    Generator, Whearhouse, Outpost, Medbay

class TestMain():
    def __init__(self):
        main = MainBase()
        main.pos = vec2d(300, 300)
        main.target = vec2d(main.pos[0] + 10, main.pos[1])
        out = Outpost()
        out.pos = vec2d(200, 200)
        out.target = vec2d(out.pos[0] + 10, out.pos[1])
        self.buildings = [main, out]
                    
class DronesTest(unittest.TestCase):      
    
    def test_init_main_base(self):
        firstbuild = MainBase()
        firstbuild.pos = vec2d(300, 300)
        firstbuild.target = vec2d(firstbuild.pos[0] + 10, firstbuild.pos[1])
        self.assertEqual(firstbuild.pos[0], 300)
        self.assertEqual(firstbuild.pos[1], 300)
        
    def test_vec2d(self):
        testvec = vec2d(200,300)
        self.assertEqual(testvec[0], 200)
        self.assertEqual(testvec[1], 300)
        
    def test_mine(self):
        p = TestMain()
        drone = Drone()
        drone.pos = vec2d(100, 100)
        target = vec2d(100, 100)
        drone.target.append(target)
        ore = Ore()
        ore.pos = vec2d(100, 100)
        ore.mine(p, drone)
        self.assertEqual(drone.inventory[1][1], 1)
        self.assertEqual(ore.quantity, 799999)
        
    def test_drone_update(self):
        drone = Drone()
        drone.pos = vec2d(100, 100)
        target = vec2d(200, 200)
        drone.target.append(target)
        drone.update()
        self.assertEqual(drone.pos, (103, 103))
        self.assertEqual(drone.power, 255-0.1)
        
    def test_mainbuilding_buy_drone(self):
        p = TestMain()
        example = Drone()
        created = p.buildings[0].buy_drone()
        self.assertEqual(p.buildings[0].inventory[1][1], 490000)
        self.assertEqual(type(created), type(example))

    def test_mainbuilding_buy_battery(self):
        p = TestMain()
        p.buildings[0].buy_battery()
        self.assertEqual(p.buildings[0].inventory[1][1], 495000)
        self.assertEqual(p.buildings[0].inventory[0][1], 3)
        
    def test_mainbuilding_update(self):
        p = TestMain()
        p.buildings[0].update()
        self.assertEqual(p.buildings[0].power, 100005)
        
    def test_outpost_upgrade(self):
        p = TestMain()
        self.assertEqual(p.buildings[1].level, 0)
        p.buildings[1].upgrade()
        self.assertEqual(p.buildings[1].level, 1)
        self.assertEqual(p.buildings[1].fire_target, p.buildings[1].pos)
        self.assertEqual(p.buildings[1].target, p.buildings[1].pos)
        
if __name__ == '__main__':
    unittest.main()
