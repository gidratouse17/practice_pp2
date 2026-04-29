class Reader: 
    def read(self): print("read")
class Writer: 
    def write(self): print("write")
class Doc(Reader, Writer): pass
d = Doc(); d.read(); d.write()


class Mammal:
    def mammal_info(self):
        print("Mammals can give direct birth.")
class WingedAnimal:
    def winged_animal_info(self):
        print("Winged animals can flap.")
class Bat(Mammal, WingedAnimal):
    pass


class P: 
    def show(self): print("P")
class Q(P):
    def show(self): print("Q"); super().show()
class R(P):
    def show(self): print("R"); super().show()
class S(Q, R):
    def show(self): print("S"); super().show()
S().show()


class PayCard:
    def pay_card(self): print("Paid by card")
class PayCash:
    def pay_cash(self): print("Paid by cash")
class Payment(PayCard, PayCash): pass
p = Payment(); p.pay_card(); p.pay_cash()


class Email:
    def send_email(self): print("Email sent")
class SMS:
    def send_sms(self): print("SMS sent")
class Notification(Email, SMS): pass
n = Notification(); n.send_email(); n.send_sms()