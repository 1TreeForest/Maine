import json
import os

class CoverageProcesser():
    def __init__(self, coverage_dir_path="/var/www/html/tmp/coverage", distance_file_path="/home/fuzz/Desktop/Projects/Maine/info/distance/index.php.json"):
        self.coverage_dir_path = coverage_dir_path
        self.distance_file_path = distance_file_path
        self.code_block_map = {}
    
    def get_coverage(self):
        coverage_files = os.listdir(self.coverage_dir_path)

        # 没有文件则应该在核心引擎中调整这个部件实例的数量 TODO
        if not coverage_files:
            raise FileNotFoundError("No coverage file found.")

        # 找到创建时间最早的文件
        earliest_file = min(coverage_files, key=lambda x: os.path.getctime(os.path.join(self.coverage_dir_path, x)))

        with open(os.path.join(self.coverage_dir_path, earliest_file), 'r') as f:
            coverage_json = json.load(f)

        os.remove(os.path.join(self.coverage_dir_path, earliest_file))

        return coverage_json
    
    def get_distance(self):
        try:
            with open(self.distance_file_path, 'r') as f:
                distance_json = json.load(f)
        except:
            raise FileNotFoundError("No distance file found.")
        
        return distance_json
    
    def build_code_block_map(self):
        distances = self.get_distance()
        for node in distances['nodes']:
            node_file = node['node_file']
            node_lineno = str(node['node_lineno'])
            node_distance = node['node_distance']
            if node_file not in self.code_block_map:
                self.code_block_map[node_file] = {}
            self.code_block_map[node_file][node_lineno] = node_distance
            
    def calculate_block_distance(self, choice="smallest"):
        covered_block_and_distance = {}
        covers = self.get_coverage()
        for node_file, node_lines in covers['coverage'].items():
            if node_file not in covered_block_and_distance.keys():
                covered_block_and_distance[node_file] = {}

            for lineno in node_lines.keys():
                if lineno in self.code_block_map[node_file].keys():
                    distance = self.code_block_map[node_file][lineno]
                else:
                    block = None
                    smallest_interval = float('inf')
                    for start_lineno in self.code_block_map[node_file]:
                        interval = int(lineno) - int(start_lineno)
                        if interval > 0 and interval < smallest_interval:
                            block = start_lineno
                            smallest_interval = interval
                    distance = self.code_block_map[node_file][block]
                    
                covered_block_and_distance[node_file][lineno] = distance

        if choice == "smallest":
            smallest_distance = float('inf')
            for node_file, node_lines in covered_block_and_distance.items():
                for lineno, distance in node_lines.items():
                    if float(distance) < float(smallest_distance):
                        smallest_distance = distance
            return {"seed_id": covers['test_input']["seed_id"], "input_distance": smallest_distance}
        elif choice == "average":
            total_distance = 0
            total_lines = 0
            for node_file, node_lines in covered_block_and_distance.items():
                for lineno, distance in node_lines.items():
                    total_distance += float(distance) if float(distance) != float('inf') else 0
                    total_lines += 1
            return {"seed_id": covers['test_input']["seed_id"], "input_distance": total_distance / total_lines}
        else:
            raise ValueError("Invalid choice for calculating input_distance.")
    
if __name__ == "__main__":
    test = CoverageProcesser()
    test.build_code_block_map()
    print(test.calculate_block_distance())
