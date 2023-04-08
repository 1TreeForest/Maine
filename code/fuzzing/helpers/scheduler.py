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
    def __init__(self, seed_input_json_file, mutator_choice="All", attack_type = "login", extra_cooling_rate=0, max_iterations=100, max_worker=1):
        self.manager = Manager()
        self.seed_input_dict = self.manager.dict()
        with open(seed_input_json_file, 'r') as f:
            for item in json.load(f):
                seed_input = TestItem(
                    url=item["url"],
                    method=item["method"],
                    parameters=item["parameters"],
                    headers=item.get("headers", {})
                )
                self.seed_input_dict[seed_input.id] = seed_input
                
        self.test_input_queue = self.manager.Queue()
        for seed_input in self.seed_input_dict.values():
            self.test_input_queue.put(seed_input)   
        self.max_worker = max_worker
        self.num_workers = self.manager.Value('i', 0)
        self.test_count = self.manager.Value('i', 0)
        self.processes = []
        self.lock = self.manager.Lock()
        self.running = True
        
        self.extra_cooling_rate = extra_cooling_rate
        self.max_iterations = max_iterations
        self.mutator_choice = mutator_choice
        self.attack_type = attack_type
        
        
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
        current_solution = TestItem(url=parent_seed_input.url, method=parent_seed_input.method, parameters=parent_seed_input.parameters, headers=parent_seed_input.headers)
        print(current_solution.id)
        current_energy = self._calculate_energy(current_solution)
        # 初始化为1000 - 0
        temperature = 1000 / (1 + parent_seed_input.usage_count)
        print("temperature: ", temperature)
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
            self.test_count.value += 1
            request_handler = RequestHandler(self.attack_type)
            test_result = request_handler.handle_request(new_solution)
            if test_result is True:
                print("Success: ", new_solution)
                sleep(10)
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
            energy_delta = new_energy - current_energy
            acceptance_probability = math.exp(-(energy_delta) / temperature)
            # 判断是否接受新解
            if new_energy < current_energy:
                current_solution = new_solution
                current_energy = new_energy
                # 如果新解的距离更小，则直接结束退火算法
                break
            elif random.random() < acceptance_probability:
                current_solution = new_solution
                current_energy = new_energy

            # 降温
            temperature *= 1 - self.extra_cooling_rate
            iterations += 1
        
        if current_solution.average_distance < parent_seed_input.average_distance or current_solution.smallest_distance < parent_seed_input.smallest_distance:
            # 将本次变异后的解加入种子库
            current_solution.parent_id = parent_seed_input.id
            parent_seed_input.num_children += 1
            print(current_solution.id)
            print('*' * 10)
            self.seed_input_dict[current_solution.id] = current_solution
        
            # 更新parent_seed_input的信息
            parent_seed_input.increment_usage_count()
            self.seed_input_dict[parent_seed_input.id] = parent_seed_input

        # print(self.seed_input_dict)
        # print(len(self.seed_input_dict), self.test_count)
        # 从种子库中随机再选择一个种子加入测试队列
        while True:
            try:
                self.test_input_queue.put(random.choice(self.seed_input_dict.values()))
                break
            except IndexError:
                continue
        # for item in self.seed_input_dict.values():
        #     print(item)
        # print('*' * 10)

    def _calculate_energy(self, seed_input):
        # 将距离信息转化为能量
            return min(seed_input.smallest_distance, seed_input.average_distance)