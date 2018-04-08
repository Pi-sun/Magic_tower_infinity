from mt_core import REF_KEY_ANY

from generate_section import floor2section

class ShopContentProvider:
    def __init__(self):
        self.purchases = 0

    def get(self, app, cell):
        section = floor2section(cell.floor)
        
        money = 10 * self.purchases * (self.purchases - 1) + 20
        health = (self.purchases + 1) * 100
        attack = section * 2
        defence = section * 2
        
        if app.hero.money.value >= money:
					def purchase(item, quantity):
						self.purchases += 1
						app.hero.money.update(-money)
						item.update(quantity)
						return True
				
					return ("Give me %d gold coins\nto increase one of your abilities\n\n<1> Health +%d\n\n<2> Attack +%d\n\n<3> Defence +%d\n\n<Any> No, thanks", {
						"1": lambda: True
						REF_KEY_ANY: lambda: True
					})

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
