from mt_core import REF_KEY_ANY, LARGE_TEXT_GAP, SMALL_TEXT_GAP

from generate_section import floor2section

class ShopContentProvider:
    def __init__(self):
        self.purchases = 0

    def get(self, app, cell):
        section = floor2section(cell.floor)
        
        money = round(150*(1.07)**self.purchases)
        health = (section) * 200 + 200
        attack = section * 2
        defence = section * 2
        
        if app.hero.money.value >= money:
            def purchase(item, quantity):
                self.purchases += 1
                app.hero.money.update(-money)
                item.update(quantity)
                return True
            return ("Give me %d gold coins\nto increase one of your abilities" % money +
                LARGE_TEXT_GAP + "[ref=1]<1> Health +%d[/ref]" % health +
                SMALL_TEXT_GAP + "[ref=2]<2> Attack +%d[/ref]" % attack + 
                SMALL_TEXT_GAP + "[ref=3]<3> Defence +%d[/ref]" % defence +
                SMALL_TEXT_GAP + "[ref=" + REF_KEY_ANY + "]<Any> No, thanks[/ref]", {
                "1": lambda: purchase(app.hero.health, health),
                "2": lambda: purchase(app.hero.attack, attack),
                "3": lambda: purchase(app.hero.defence, defence),
                REF_KEY_ANY: lambda: True
            })
        else:
            return ("You need %d gold coins\nto make a purchase!" % money + 
                LARGE_TEXT_GAP + "Press any key to continue", {
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
