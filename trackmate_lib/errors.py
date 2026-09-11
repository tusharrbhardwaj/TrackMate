class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class AllocationExceededError(Exception):
    def __init__(self, current_weight: int):
        self.current_weight = current_weight
        super().__init__("Task allocation cannot exceed 100%.")
