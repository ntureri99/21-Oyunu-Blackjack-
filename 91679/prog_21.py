import play  # play kütüphanesini içe aktarıyoruz (grafik ve etkileşim için)
from random import sample  # Rastgele kart seçmek için sample fonksiyonunu içe aktarıyoruz

# Oyunun başlangıç mesajını oluşturuyoruz
hello = play.new_text(words="Try to get 21 points and beat the comp!", x=0, y=200)

# Oyuncu ve bilgisayarın kartlarını tutacak listeler
you_cards = []
comp_cards = []

# Çekilen kart sayısını takip eden değişken
steps = 0
steps_txt1 = play.new_text(words="Çekilen kart sayısı: ", x=-20, y=-280, font_size=30)  # Bilgi metni
steps_txt2 = play.new_text(words=str(steps), x=80, y=-280, font_size=30)  # Güncellenen adım sayısı

# "Add Card" butonu (Sarı renkli)
button_add = play.new_box(color="yellow", border_width=1, border_color="grey", x=-130, y=-160, width=170, height=40)
# "Start me VS comp" butonu (Kırmızı renkli)
button_comp = play.new_box(color="red", border_width=1, border_color="grey", x=130, y=-160, width=170, height=40)

# Butonların üzerine gelecek metinleri oluşturuyoruz
add_txt = play.new_text(words="Add card", font_size=30, x=-130, y=-160, color="grey")
comp_txt = play.new_text(words="Start me VS comp", font_size=30, x=130, y=-160, color="grey")

# Skorları tutan metin nesneleri
you_score = play.new_text(words="0", x=-100, y=-230)
comp_score = play.new_text(words="0", x=100, y=-230)

# Kullanılabilir kart numaraları listesi (0-10 arası)
available_cards = list(range(11))
comp_available_cards = list(range(11))

@play.when_program_starts  # Program başladığında çalışacak fonksiyon
def start():
    for i in range(11):  # 0'dan 10'a kadar olan sayılar için dön
        # Oyuncunun kartlarını oluştur ve gizle
        card = play.new_image(image=f"card{i+1}.png", size=40, x=-150, y=20)
        card.hide()
        you_cards.append(card)
        
        # Bilgisayarın kartlarını oluştur ve gizle
        card1 = play.new_image(image=f"card{i+1}.png", size=40, x=150, y=20)
        card1.hide()
        comp_cards.append(card1)

@button_add.when_clicked  # "Add Card" butonuna tıklandığında çalışacak fonksiyon
async def add():
    global steps, available_cards  # Küresel değişkenleri kullanıyoruz
    if not available_cards:  # Eğer kart kalmadıysa işlemi durdur
        return
    
    # Rastgele bir kart seç ve oyuncuya ata
    number = available_cards.pop(available_cards.index(sample(available_cards, 1)[0]))
    you_cards[number].show()
    
    # Oyuncunun skorunu güncelle
    you_score.words = str(int(you_score.words) + (number + 1))
    steps += 1  # Çekilen kart sayısını artır
    steps_txt2.words = str(steps)  # Ekranda güncelle
    
    await play.timer(1.5)  # 1.5 saniye bekle
    you_cards[number].hide()  # Kartı tekrar gizle

@button_comp.when_clicked  # "Start me VS comp" butonuna tıklandığında çalışacak fonksiyon
async def stop():
    global steps, comp_available_cards  # Küresel değişkenler
    if not comp_available_cards:  # Eğer bilgisayarın kartları biterse işlemi durdur
        return
    
    for _ in range(steps):  # Oyuncunun çektiği kart kadar bilgisayar da kart çeker
        if not comp_available_cards:
            break
        number = comp_available_cards.pop(comp_available_cards.index(sample(comp_available_cards, 1)[0]))
        comp_cards[number].show()
        comp_score.words = str(int(comp_score.words) + (number + 1))
        await play.timer(1.5)
        comp_cards[number].hide()
    
    # Skorları karşılaştır ve kazananı belirle
    you_total = int(you_score.words)
    comp_total = int(comp_score.words)
    
    if you_total <= 21 and (comp_total > 21 or you_total > comp_total):
        you_score.color = "green"
        play.new_text(words="You win!", color="green", x=-210, y=-230)
        comp_score.color = "red"
    elif comp_total <= 21 and (you_total > 21 or comp_total > you_total):
        comp_score.color = "green"
        play.new_text(words="You lose!", color="red", x=-210, y=-230)
        you_score.color = "red"
    else:
        you_score.color = "red"
        comp_score.color = "red"

@play.repeat_forever  # Oyun süresince sürekli çalışan döngü
def do():
    if int(you_score.words) > 21:  # Eğer oyuncunun puanı 21'i geçerse kaybeder
        you_score.color = "red"
        play.new_text(words="You lose!", color="red", x=-210, y=-230)
    if int(comp_score.words) > 21:  # Eğer bilgisayarın puanı 21'i geçerse kaybeder
        comp_score.color = "red"
        play.new_text(words="Comp loses!", color="red", x=220, y=-230)
        you_score.color = "green"
        play.new_text(words="You win!", color="green", x=-210, y=-230)

play.start_program()  # Oyunu başlat