import sys  
sys.path.append(r'code/fuzzing/helpers') 
from scheduler import Scheduler


if __name__ == '__main__':
    scheduler = Scheduler(seed_input_json_file='code/fuzzing/tests/seed_input.json',)
    scheduler.start()