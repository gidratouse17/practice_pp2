#1
day = int(input())

match day:
    case 8:
        print("Happy International Womens day!")
    case 21 | 22 | 23:
        print("Nauryz day!")
    case _:
        print("Its a work day :(")  

#2
season = int(input("Whats your favorite spongebob season? "))
match season:
    case 1 | 2 | 3:
        print("You know peak!")
    case 4 | 5:
        print("Mid seasons")
    case 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14:
        print("Very unusual choice....")
    case _:
        print("There are only 14 seasons in Spongebob! Write again")

#3
fav_char = input("Tell me whos ur fav character! ")
match fav_char:
    case "Twilight Sparkle":
        print("I love her sm! Especially when she was an alicorn")
    case "Isagi Yoichi":
        print("I really want to have a mindset like his!")
    case "Fluttershy":
        print("I relate to her sm. And shes so adorable!")
    case _:
        print("Tell me about her/him!") 

#4
lang = input("Whats your native language? ")
match lang:
    case "English":
        print("Thats awesome!")
    case "Russian":
        print("Это замечательно!")
    case "Kazakh":
        print("Өте керемет!")
    case _:
        print("Oh, thats interesting!")

#5
time_of_year = input("Try to guess my fav time of year: ")
match time_of_year:
    case "Winter":
        print("I absolutely hate winter cuz of very cold weather, black ice and Im feeling some sort of depression")
    case "Spring":
        "I like spring, but not in Aktau, its not my most fav season."
    case "Summer":
        "I really like summer because of holidays and Caspian sea, but weather is too hot"
    case "Fall":
        "YES, I LOVE FALL! Its very beautiful, especially in Almaty"
    case _:
        print("Try to write again")   
        