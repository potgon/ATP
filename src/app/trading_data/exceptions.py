class DuplicateAssetException(Exception):
    
    def __init__(self, asset, message="Asset is already being traded"):
        self.asset = asset
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"{self.asset} -> {self.message}"