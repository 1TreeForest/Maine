class CodeBlock:
    '''
    A class to represent a code block.
    To store the code block information
    '''

    # A counter to generate unique id for each seed input
    _id_counter = 0

    def __init__(self, start_line, end_line, block_type):
        CodeBlock._id_counter += 1
        self.id = CodeBlock._id_counter
        self.start_line = start_line
        self.end_line = end_line
        self.block_type = block_type

    def __str__(self):
        return f"CodeBlock(id={self.id}, start_line={self.start_line}, end_line={self.end_line}, block_type={self.block_type})"

    def __repr__(self):
        return str(self)