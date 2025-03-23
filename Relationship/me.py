class RelationshipFSW:
    STATE = ['ACTIVE', 'STANDBY', 'TERMINATED']

    def __init__(self, last_days=5, ghosted=False):
        self.last_response_days = last_days
        self._ghosted = ghosted
        self.current_state = self.STATE[1] if self.check_5d_silence() else self.STATE[2]

    def check_5d_silence(self):
        if self.last_response_days <= 5 and not self.is_ghosted():
            return True
        elif self.last_response_days > 5 and not self.is_ghosted():
            return True
        elif self.last_response_days >= 10 or self.is_ghosted():
            return False

    def is_ghosted(self):
        return self._ghosted


# 测试用例
print(RelationshipFSW(last_days=5, ghosted=False).current_state)  # 输出: STANDBY
print(RelationshipFSW(last_days=5, ghosted=True).current_state)  # 输出: TERMINATED