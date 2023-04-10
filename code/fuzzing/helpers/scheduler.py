from request_handler import RequestHandler
from coverage_processer import CoverageProcesser
from mutators import StringMutator, ParameterMutator
from multiprocessing import Process, Manager
from definition.test_item import TestItem
import os
from datetime import datetime
import time
import json
import math
import random


class Scheduler:
    def __init__(self, mutator_choice="All", vul_type="All", extra_cooling_rate=0.02, max_iterations=100, max_worker=1, coverage_dir_path="/var/www/html/tmp/coverage", distance_file_path="/home/fuzz/Desktop/Projects/Maine/info/distance/index.php.json", seed_input_json_file='code/fuzzing/tests/seed_input.json'):
        self.manager = Manager()
        self.seed_input_dict = self.manager.dict()
        self.coverage_dir_path = coverage_dir_path
        self.distance_file_path = distance_file_path
        self.seed_input_json_file = seed_input_json_file
        self.id_counter = self.manager.Value('i', 0)
        self.test_input_queue = self.manager.Queue()
        self.max_worker = max_worker
        self.num_workers = self.manager.Value('i', 0)
        self.distance_record = self.manager.Value('f', float("inf"))
        self.test_count = self.manager.Value('i', 0)
        self.processes = []
        self.lock = self.manager.Lock()
        self.running = True
        self.start_time = datetime.now()
        self.log_file_path = f"code/fuzzing/logs/{self.start_time.strftime('%Y-%m-%d-%H-%M-%S')}.log"

        self.extra_cooling_rate = extra_cooling_rate
        self.max_iterations = max_iterations
        self.mutator_choice = mutator_choice
        self.vul_type = vul_type
        self.request_handler = RequestHandler(self.vul_type)
        self.coverage_processer = CoverageProcesser(
            self.coverage_dir_path, self.distance_file_path)

        if self.mutator_choice == "All":
            self.mutators = [
                StringMutator(),
                ParameterMutator(self.vul_type)
            ]
        elif self.mutator_choice == "String":
            self.mutators = [
                StringMutator()
            ]
        elif self.mutator_choice == "Parameter":
            self.mutators = [
                ParameterMutator(self.vul_type)
            ]

    def clear_coverage_dir(self):
        if os.path.exists(self.coverage_dir_path):
            coverage_files = os.listdir(self.coverage_dir_path)
            for file_to_rm in coverage_files:
                os.remove(os.path.join(self.coverage_dir_path, file_to_rm))
            print("Coverage dir cleared")
        else:
            print("Coverage dir not found")

    def start(self):
        # 防止以前的结果影响本次测试
        self.clear_coverage_dir()
        # 读入用户提供的种子输入
        with open(self.seed_input_json_file, 'r') as f:
            for item in json.load(f):
                seed_input = TestItem(
                    id=self.id_counter.value,
                    url=item["url"],
                    method=item["method"],
                    parameters=item["parameters"],
                    headers=item.get("headers", {}),
                    smallest_distance=item.get(
                        "smallest_distance", float("inf")),
                    average_distance=item.get("average_distance", float("inf"))
                )
                self.id_counter.value += 1
                # 如果距离未初始化，则需要进行一次测试并更新距离
                if seed_input.smallest_distance == float("inf") and seed_input.average_distance == float("inf"):
                    maine_test_id = self.test_count.value
                    self.test_count.value += 1
                    self.request_handler.handle_request(
                        seed_input, maine_test_id=maine_test_id)
                    feedback = self.coverage_processer.calculate_block_distance(
                        maine_test_id=maine_test_id)
                    distance_type = list(feedback.keys())[1]
                    if distance_type == "smallest_distance":
                        seed_input.smallest_distance = feedback[distance_type]
                    elif distance_type == "average_distance":
                        seed_input.average_distance = feedback[distance_type]
                # 将种子加入种子库并加入测试队列
                self.seed_input_dict[seed_input.id] = seed_input
                self.test_input_queue.put(seed_input)

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
                    print("worker-{} stopped".format(p.pid))
                    with self.lock:
                        self.num_workers.value -= 1
                    self.processes.remove(p)
                if p.exitcode == 0:
                    self.stop()

    def stop(self):
        self.running = False
        for p in self.processes:
            p.terminate()

    def schedule_worker(self):
        while self.running:
            # sum_use = 0
            # for item in self.seed_input_dict.values():
            #     sum_use += item.usage_count
            # print(self.test_count.value, sum_use, self.id_counter.value)
            parent_seed_input = self.test_input_queue.get()
            current_solution = TestItem(url=parent_seed_input.url, method=parent_seed_input.method,
                                        parameters=parent_seed_input.parameters, headers=parent_seed_input.headers)
            current_energy = self._calculate_energy(current_solution)
            # 初始化为100 - 1
            temperature = 100 * \
                (1 - (parent_seed_input.usage_count /
                 (parent_seed_input.usage_count + 1000)))
            # print("temperature: ", temperature)
            iterations = 0

            # 开始退火算法
            while temperature > 1 and iterations < self.max_iterations:
                # 变异当前解
                new_solution = random.choice(self.mutators).random_mutate(
                    current_solution, self.vul_type)
                if new_solution is None:
                    # print("error")
                    continue
                # 发送变异后的解的请求
                maine_test_id = self.test_count.value
                self.test_count.value += 1
                test_result = self.request_handler.handle_request(
                    new_solution, maine_test_id=maine_test_id)
                # 收集变异后的解的距离信息

                feedback = self.coverage_processer.calculate_block_distance(
                    maine_test_id=maine_test_id)
                distance_type = list(feedback.keys())[1]
                if distance_type == "smallest_distance":
                    new_solution.smallest_distance = feedback[distance_type]
                elif distance_type == "average_distance":
                    new_solution.average_distance = feedback[distance_type]

                # 判断是否成功触发漏洞，如果成功则记录并停止
                if test_result is True:
                    new_solution.id = self.id_counter.value
                    self.id_counter.value += 1
                    new_solution.parent_id = parent_seed_input.id
                    print("Success: ", new_solution)
                    with open(self.log_file_path, "a") as f:
                        f.write("\nSuccess\n")
                        f.write("---------------------\n")
                        f.write("\t".join(["Time cost: %s" % (datetime.now() - self.start_time), "Test count: %s" % maine_test_id,
                                "Distance: %s" % new_solution.smallest_distance, "Solution: %s" % new_solution]) + "\n")
                    return 0

                new_energy = self._calculate_energy(new_solution)
                energy_delta = new_energy - current_energy
                acceptance_probability = math.exp(
                    -(energy_delta) / temperature) - 0.8
                # print(acceptance_probability, temperature, cooling_rate, parent_seed_input.usage_count)
                # 判断是否接受新解
                if new_energy < current_energy:
                    current_solution = new_solution
                    current_energy = new_energy
                elif random.random() < acceptance_probability:
                    current_solution = new_solution
                    current_energy = new_energy

                # 降温
                temperature *= 1 - self.extra_cooling_rate
                iterations += 1

            if current_solution.average_distance < parent_seed_input.average_distance or current_solution.smallest_distance < parent_seed_input.smallest_distance:
                # 将本次变异后的解加入种子库
                current_solution.parent_id = parent_seed_input.id
                # 更新parent_seed_input的孩子数量
                self.seed_input_dict[parent_seed_input.id].num_children += 1
                current_solution.id = self.id_counter.value
                self.id_counter.value += 1
                self.seed_input_dict[current_solution.id] = current_solution
                # 如果distance比最优记录好，则输出到log文件
                if current_solution.smallest_distance < self.distance_record.value:
                    self.distance_record.value = current_solution.smallest_distance
                    with open(self.log_file_path, "a") as f:
                        f.write("\t".join(["Time cost: %s" % (datetime.now() - self.start_time), "Test count: %s" % maine_test_id,
                                "Distance: %s" % current_solution.smallest_distance, "Solution: %s" % current_solution]) + "\n")

            print("\t".join(["Time cost: %s" % (datetime.now() - self.start_time), "Test count: %s" % maine_test_id,
                  "Seed count: %s" % len(self.seed_input_dict), "Params: %s" % current_solution.parameters]))

            # if parent_seed_input.num_children > len(self.seed_input_dict) * 0.2:
            #     # 如果parent_seed_input的子节点数量大于种子库的20%，则删除该种子，防止污染种子库
            #     self.seed_input_dict.pop(parent_seed_input.id)
            #     print("Delete seed: ", parent_seed_input.id)
            # else:
            
            # 更新parent_seed_input的使用次数
            self.seed_input_dict[parent_seed_input.id].usage_count += iterations

            # 从种子库中随机再选择一个种子加入测试队列
            self.test_input_queue.put(
                random.choice(self.seed_input_dict.values()))

    def _calculate_energy(self, seed_input):
        # 将距离信息转化为能量
        return min(seed_input.smallest_distance, seed_input.average_distance)
