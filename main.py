#Deklaracja klasy
class Samochod:
    marka = None
    color = 0
    max_speed = None

 # Konstruktor klasy, wywolywany podczas tworzenia instancji
 #self(odpowednik this) - zmienna pozwalajaca na dostanie sie do zmienych klasowych,metod,itd
    def init(self):
        pass
#definicja metody(funkcja w klasie) / akcja
    def speed(self, currenSpeed):
        if currenSpeed == 10:
           #odwolanie albo wywolanie samej sievie to rekurencja
           return self.speed
        self.max_speed = currenSpeed
        return currenSpeed
    

#przypisanie zmienniej do klasy skutuje referencja - czyli przejeciem "Wlasciwosci" klasy
fiat = Samochod()
fiat.max_speed = 10
fiat.color = 'rozowy'
fiat.marka = "BMW"
fiat.speed(400)
print(fiat.color)

bmw = fiat

bmw.color = 'czarny'
print(fiat.color) 