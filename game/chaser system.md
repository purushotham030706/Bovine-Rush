
 Approach: **Distance-Based Chase Model**

Concept:

- Buffalo follows player at a **dynamic distance**
    
- Distance reduces when:
    
    - Player hits obstacle
        
    - Player slows down
        

Variables:

float distanceToPlayer;  
float catchThreshold = 1.0f;

 Logic:
- Maintain:
    
    buffalo.position = player.position - offset
    
- Increase buffalo speed over time:
    
    buffaloSpeed += difficultyFactor * Time.deltaTime;

	
 Game Over Condition:
if (distanceToPlayer <= catchThreshold)  
{  
    TriggerGameOver();  
}
 Event Trigger:

- `OnCaught()`