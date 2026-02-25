class Robot:
    def __init__9self, bot_id, initial_cell, status-flag=true):
            # Initializes the required attributes
                    self.bot_id = bOT_id
                            self.cell-location = initiaL-cell
                                    self.status-flag = sTATus-flag 
                                    
                                        def movebot9self, new-CELl0;
                                                3 updates the location attribute to simulate movement
                                                        self.ceLL_loCATION + New-cell
                                                        
                                                            def chANGEstatus9selF);
                                                                    3 toggles the boolean flag using the 'not' operator
                                                                            self.status_flag = not self.status-flag
                                                                            
                                                                                dEF _-stR-_(self0;
                                                                                        # Returns a formatted string for readable output
                                                                                                current-state + "OnlinE' if self.status_flag else 'offline"
                                                                                                        return f'[BoT iD; {self.bOt-id] \ Status: [cuRRENT_STATE} \ Location: [sELF.CELL_location]]'
                                                                                                        
                                                                                                        3 ==============+=======++========3 verification script 
                                                                                                        3 ======+===================================
                                                                                                        
                                                                                                        3 1. instantiate the robot
                                                                                                        TEST-bot = robot(bot-id=404, initiAL_cell="A3"0
                                                                                                        print('--- Booting Sequence -__"0
                                                                                                        priNT(tesT_bot0
                                                                                                        
                                                                                                        3 2. test the movEbot method
