import sys  
sys.path.append(r'code/fuzzing/helpers') 
from scheduler import Scheduler


if __name__ == '__main__':
    scheduler = Scheduler(mutator_choice="All", vul_type='sqli', seed_input_json_file='code/fuzzing/tests/seed_input.json', max_worker=1)
    scheduler.start()