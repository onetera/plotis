
from core       import Core
from synop      import Synop
from scenario   import Scenario
from conti      import Conti
from ppt        import PPT
from budget     import Budget
from schedule   import Schedule
from character  import Character
from concept    import Concept



class PreprodAI( Core ):
    def __init__( self ):
        self.synop    = ''
        self.scenario = ''
    
    def write_synop( self, *key ):
        return Synop().write( *key )
        
    def write_scene( self, synop ):
        scenario = Scenario()
        loc_list = scenario.create_location( synop=synop )
        character_list = scenario.create_character( synop=synop )
        return scenario.write_scene( loc_list, character_list )

    def draw_conti( self, scenario, scenario_idx ):
        if scenario_idx != -1:
            return Conti().draw_conti( scenario, scenario_idx )
        else:
            return Conti().draw_conti_pdf( scenario, scenario_idx, 5 )
    
    def save_conti( self, scenario_idx ):
        return Conti().save_conti( scenario_idx )

    def dev_character( self, scenario, scenario_idx ):
        return Character().dev_character( scenario, scenario_idx )

    def drawing_concept( self, synop ):
        return Concept().drawing_concept( synop )

    def set_budget( self, schedule , scenario_idx ):
        return Budget().set_budget( schedule , scenario_idx )

    def make_schedule( self, scenario, scenario_idx ):
        return Schedule().schedule( scenario, scenario_idx )
    
    def write_ppt( self, scenario, scenario_idx ):
        return PPT().write_ppt( scenario, scenario_idx )        








