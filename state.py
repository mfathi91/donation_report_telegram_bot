class State:

    def __init__(self, name, next_input_request, validate_input):
        self.name = name
        self.next_input_request = next_input_request
        self.validate_input = validate_input


    @staticmethod
    def validate_nothing(state_input):
        return True


    @staticmethod
    def validate_euro_format(state_input):
        # To be implemented
        return True


    @staticmethod
    def validate_toman_format(state_input):
        # To be implemented
        return True

