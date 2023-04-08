class TestItem:
    '''
    To represent a test input item, which is a piece of data that is used to generate new inputs.
    A input can be appended as a child of another input, if it triggers a new path.
    A test input item can be selected for mutation, and the usage count will be recorded.
    A test input item will be removed if ... TODO
    '''

    _id_counter = 0
    def __init__(self, url, parent_id=None, method="", parameters="", headers={}, id=None):
        if id:
            self.id = id
        else:
            self.id = TestItem._id_counter  
            TestItem._id_counter += 1
        self.url = url
        self.method = method
        self.usage_count = 0
        self.num_children = 0
        self.parent_id = parent_id
        self.parameters = parameters
        self.headers = headers
        self.smallest_distance = float("inf")
        self.average_distance = float("inf")

    def __str__(self):
        return f"TestItem(id={self.id}, url={self.url}, method={self.method}, usage_count={self.usage_count}, num_children={self.num_children}, parent_id={self.parent_id}, parameters={self.parameters}, headers={self.headers}, smallest_distance={self.smallest_distance}, average_distance={self.average_distance})"

    def __repr__(self):
        return str(self)

    def increment_usage_count(self):
        self.usage_count += 1

    def increment_num_children(self):
        self.num_children += 1
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'method': self.method,
            'usage_count': self.usage_count,
            'num_children': self.num_children,
            'parent_id': self.parent_id,
            'parameters': self.parameters,
            'headers': self.headers,
            'smallest_distance': self.smallest_distance,
            'average_distance': self.average_distance,
        }

if __name__ == "__main__":
    import json
    seed1 = TestItem(url='http://localhost/index.php', method='GET', parameters='param1=value1', headers={})
    seed2 = TestItem(url='http://localhost/index.php', method='GET', parameters='action=file2', headers={})
    seed = [seed1.to_dict(), seed2.to_dict()]
    print(json.dumps(seed))