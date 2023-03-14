from agent_based.models.base_model import Model
import time

if __name__ == "__main__":
    
    model = Model(2000000, dt=0.1)
    
    tstart = time.time()
    for i in range(10):
        model.step()
    
    tend = time.time()
    
    print(tend-tstart)
