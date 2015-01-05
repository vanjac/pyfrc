'''
    The primary purpose of these tests is to run through your code
    and make sure that it doesn't crash. If you actually want to test
    your code, you need to write your own custom tests to tease out
    the edge cases
    
    The tests are identical for :class:`wpilib.iterativerobot.IterativeRobot`
    and :class:`wpilib.samplerobot.SampleRobot` based robots.
'''

import math


def test_autonomous(control, fake_time, robot):
    '''Runs autonomous mode by itself'''
    
    # run autonomous mode for 15 seconds
    control.set_autonomous(enabled=True)
    control.run_test(lambda tm: tm < 15)
    
    # make sure autonomous mode ran for 15 seconds
    assert int(fake_time.get()) == 15


def test_disabled(control, fake_time, robot):
    '''Runs disabled mode by itself'''
    
    # run disabled mode for 5 seconds
    control.set_autonomous(enabled=False)
    control.run_test(lambda tm: tm < 5)
    
    # make sure disabled mode ran for 5 seconds
    assert int(fake_time.get()) == 5


def test_operator_control(control, fake_time, robot):
    '''Runs operator control mode by itself'''
    
    # run operator mode for 120 seconds
    control.set_operator_control(enabled=True)
    control.run_test(lambda tm: tm < 120)
    
    # make sure operator mode ran for 10 seconds
    assert int(fake_time.get()) == 120


def test_practice(control, fake_time, robot):
    '''Runs through the entire span of a practice match'''
    
    class TestController:
        
        def __init__(self):
            self.mode = None
            
            self.disabled = 0
            self.autonomous = 0
            self.teleop = 0
            
            
        def on_step(self, tm):
            
            mode = control.get_mode()
            if mode == self.mode:
                return
            
            if mode == 'autonomous':
                self.autonomous += 1
                assert int(math.floor(fake_time.get())) == 5
                
            elif mode == 'teleop':
                self.teleop += 1
                assert int(math.floor(fake_time.get())) == 21
            
            elif mode == 'disabled':
                self.disabled += 1
                
                if self.disabled == 1:
                    assert int(math.floor(fake_time.get())) == 0
                else:
                    assert int(math.floor(fake_time.get())) == 20
            else:
                assert False, "Internal error!"
            
            self.mode = mode
    
    control.set_practice_match()
    tc = control.run_test(TestController)
    
    assert int(math.floor(fake_time.get())) == 141
    
    # If an error occurs here, for some reason a mode got called too many times
    assert tc.disabled == 2
    assert tc.autonomous == 1
    assert tc.teleop == 1