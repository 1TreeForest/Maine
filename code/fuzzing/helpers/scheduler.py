import sys  
sys.path.append(r'code/fuzzing')
from request_handler import RequestHandler
from coverage_processer import CoverageProcesser
from time import sleep
from mutators import StringMutator, ParameterMutator
from multiprocessing import Process, Manager
from definition.test_item import TestItem
from queue import Queue
import random
import math
import json

class Scheduler:
    def __init__(self, seed_input_json_file, mutator_choice="All", attack_type = "All", cooling_rate=0.1, max_iterations=5, max_worker=1):
        self.test_count = 0
        self.seed_input_set = set()
        with open(seed_input_json_file, 'r') as f:
            for item in json.load(f):
                seed_input = TestItem(
                    url=item["url"],
                    method=item["method"],
                    parameters=item["parameters"],
                    headers=item.get("headers", {})
                )
                self.seed_input_set.add(seed_input)
                
        self.max_worker = max_worker
        self.processes = []
        self.manager = Manager()
        self.num_workers = self.manager.Value('i', 0)
        self.lock = self.manager.Lock()
        self.running = True
        
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        
        self.test_input_queue = Queue()
        self.mutator_choice = mutator_choice
        self.attack_type = attack_type
        for seed_input in self.seed_input_set:
            self.test_input_queue.put(seed_input)
        
    def start(self):
        while self.running:
            # 如果当前worker数量小于max_worker，则启动新的worker
            with self.lock:
                if self.num_workers.value < self.max_worker:
                    self.num_workers.value += 1
                    p = Process(target=self.schedule_worker)
                    self.processes.append(p)
                    p.start()

            # 移除已经停止的worker
            for p in self.processes:
                if not p.is_alive():
                    with self.lock:
                        self.num_workers.value -= 1
                    self.processes.remove(p)

    def stop(self):
        self.running = False
        for p in self.processes:
            p.terminate()
    
    def schedule_worker(self):
        parent_seed_input = self.test_input_queue.get()
        print(parent_seed_input)
        # for item in self.test_input_queue.queue:
        #     print(item)
        # print("-" * 10)
        current_solution = TestItem(url=parent_seed_input.url, method=parent_seed_input.method, parameters=parent_seed_input.parameters, headers=parent_seed_input.headers)
        current_energy = self._calculate_energy(current_solution)
        # 初始化为100 - 0
        temperature = 100 / (1 + current_solution.usage_count)
        iterations = 0

        # 开始退火算法
        while temperature > 1 and iterations < self.max_iterations:
            parent_seed_input.increment_usage_count()
            # 变异当前解
            # print(current_solution)
            if self.mutator_choice == "StringMutator":
                new_solution = StringMutator().random_mutate(current_solution)
            elif self.mutator_choice == "ParameterMutator":
                new_solution = ParameterMutator().random_mutate(current_solution)
            else:  # All
                mutator = random.choice([StringMutator(), ParameterMutator()])
                new_solution = mutator.random_mutate(current_solution)
            # 发送变异后的解的请求
            self.test_count += 1
            request_handler = RequestHandler(self.attack_type)
            test_result = request_handler.handle_request(new_solution)
            if test_result is True:
                print("Success: ", new_solution)
                self.stop()
            # 收集变异后的解的距离信息
            coverage_processer = CoverageProcesser()
            feedback = coverage_processer.calculate_block_distance()
            distance_type = list(feedback.keys())[1]

            if distance_type == "smallest_distance":
                new_solution.smallest_distance = feedback[distance_type]
            elif distance_type == "average_distance":
                new_solution.average_distance = feedback[distance_type]
            new_energy = self._calculate_energy(new_solution)

            # 判断是否接受新解
            if new_energy < current_energy:
                current_solution = new_solution
                current_energy = new_energy
            else:
                interval = new_energy - current_energy
                if interval != 0:
                    acceptance_probability = math.exp(-(interval) / temperature)
                    # print("acceptance_probability: ", acceptance_probability)
                    if random.random() < acceptance_probability:
                        current_solution = new_solution
                        current_energy = new_energy

            # 降温
            temperature *= 1 - self.cooling_rate

            iterations += 1
            
        # 将本次变异后的解加入种子库
        current_solution.parent_id = parent_seed_input.id
        parent_seed_input.num_children += 1
        self.seed_input_set.add(current_solution)
        # 更新parent_seed_input的信息
        for item in self.seed_input_set:
            if item.id == parent_seed_input.id:
                self.seed_input_set.remove(item)
                break
        self.seed_input_set.add(parent_seed_input)
        # 从种子库中随机再选择一个种子加入测试队列
        self.test_input_queue.put(random.choice(list(self.seed_input_set)))
        

    def _calculate_energy(self, seed_input):
        # 将距离信息转化为能量
            return min(seed_input.smallest_distance, seed_input.average_distance)