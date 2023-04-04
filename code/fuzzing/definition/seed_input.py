class SeedInput:
    '''
    To represent a seed input, which is a piece of data that is used to generate new inputs.
    A input can be appended as a child of another input, if it triggers a new path.
    A seed input can be selected for mutation, and the usage count will be recorded.
    A seed input will be removed if ... TODO
    '''

    # A counter to generate unique id for each seed input
    _id_counter = 0

    def __init__(self, url, parent_id=None, method="", parameters="", headers={}):
        SeedInput._id_counter += 1
        self.id = SeedInput._id_counter
        self.url = url
        self.method = method
        self.usage_count = 0
        self.num_children = 0
        self.parent_id = parent_id
        self.parameters = parameters
        self.headers = headers

    def __str__(self):
        return f"SeedInput(id={self.id}, url={self.url}, method={self.method}, usage_count={self.usage_count}, parent_id={self.parent_id}, num_children={self.num_children}, parameters={self.parameters}, headers={self.headers})"

    def __repr__(self):
        return str(self)

    def increment_usage_count(self):
        self.usage_count += 1

    def increment_num_children(self):
        self.num_children += 1