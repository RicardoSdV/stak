"""
Should CompressionFormatList inherit from list or should it contain a list??

Pro inheritance arguments

"""


class CompressionFormatList(list):
    def __init__(self, *args, cnt: int = 1, rep: str = '') -> None:
        super().__init__(*args)
        self.cnt = cnt
        self.rep = rep


CompressionRecursive = CompressionFormatList[str, CompressionFormatList]
