from mt_core import REF_KEY_ANY

class ShopContentProvider:
    def get(self, cell):
        return ("Hi!", {REF_KEY_ANY: lambda: True})

def sharedShopContentProvider():
    return _shop_provider

def getState():
    return {"shopProvider": _shop_provider}

def setState(state):
    global _shop_provider
    _shop_provider = state["shopProvider"]
    
def newState():
    global _shop_provider
    _shop_provider = ShopContentProvider()
