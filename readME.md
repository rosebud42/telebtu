
<a id="readme-top"></a>




<br />
<div align="center">

<h3 align="center">Bursa Teknik Üniversitesi Yemekhanesi Telegram Botu</h3>

  <p align="center">
    Bursa Teknik Üniversitesi öğrencilerinin telegram üzerinden menüye ulaşamını kolaylaştıran bot.
    <br />
    <br />
</div>



## İçerik

1. [Proje Hakkında](#proje-hakkında)
   - [Ne ile Geliştirildi](#ne-ile-geliştirildi)
2. [Başlamadan Önce](#başlamadan-önce)
   - [Kurulum](#kurulum)
3. [Kullanım](#kullanım)
4. [İletişim](#iletişim)





<!-- ABOUT THE PROJECT -->
## Proje hakkında

![Proje Gösterimi][product-screenshot]

Proje temel olarak Bursa Teknik Üniversitesi yemekhane biriminin kendi sitesinde yayınladığı pdf'i okumakta ve menüyü kullanıcılara telegram üzerinden iletmeyi hedeflemektedir. Üstteki resimde basit komut örnekleri resmedilmiştir. Detaylı ve admin özel komutlar için <a href=#kullanım>Kullanım</a> kısmını inceleybilirsiniz.


<p align="right">(<a href="#readme-top">başa dön</a>)</p>



### Ne ile geliştirildi

* [![Python][Python.js]][Python-url]


<p align="right">(<a href="#readme-top">başa dön</a>)</p>




## Başlamadan önce

Bu adımları takip ederek bu projeyi kurabilirsiniz.


### Kurulum

1. Projeyi bilgisayarınıza klonlayın
   ```sh
   git clone https://github.com/rosebud42/telebtu
   ```
2. Virtual Environment kurun
   ```sh
   python -m venv venv
   ```
   Kurduğunuz ortamı aktif kale getirin <br/>
   Windows için:
   ```sh
   venv/Scripts/activate.ps1
   ``` 
   MacOS / Linux için:
    ```sh
   source venv/bin/activate
   ```
3. Gerekli paketleri yükleyin
   ```sh
   pip install -r requirements.txt
   ```
5. main.py üzerindeki tokeni güncelleyin 
   ```
   TOKEN = 'your-token'
   ```
   Telegram tokeniniz yoksa telegram içerisinde BotFather'dan alabilirsiniz.
6. Eğer projeyi şuan olduğu gibi Koyeb üzerinden çalıştırmak yerine kendi bilgisayarınızda çalıştıracaksanız main.py dosyasında 21 ile 28. satır arasını ve     298 ile 300. satır arasını silmeniz gerekmektedir.<br/>Silmeniz gerek kod parçaları : 
   ```sh
   app = Flask(__name__)

   @app.route('/health', methods=['GET'])
   def health_check():
     return 'OK', 200

   def run_flask():
     app.run(host='0.0.0.0', port=8000)
   ```
   <br/> Ve,
   ```sh
   flask_thread = Thread(target=run_flask)
   flask_thread.start()
   tm.sleep(40)
   ```
   
8. Projeyi çalıştırın
   ```sh
   python main.py
   ```
  Artık proje bilgisayarınızda çalışmaya hazır.

<p align="right">(<a href="#readme-top">başa dön</a>)</p>



## Kullanım

Projeyi çalıştırdıktan sonra kullanabilecek komutlar ve açıklamaları şu şekilde: <br/>
/start -> Botu başlatmak için kullanılır. <br/>
/komutlar -> Komutlara ulaşmak için kullanılır.<br/>
/menu 16 -> Ayın 16.günündeki menüyü iletir. Gün verilmeden '/menu' şeklinde kullanıldığında aynı günün menüsünü iletir.<br/>
/abonelik -> Database üzerinde kullanıcının kaydı oluşturulur ve hafta içi her gün 09.00'da günün menüsü iletilir.<br/>
/abonelikiptal -> Database üzerinden kullanıcının kaydı silinir.<br/>
/aylikmenu -> Ayın menüsü pdf ve resim olarak iletilir.<br/>

/idogren -> Kullanıcının telegram id'sini döndürür. Admin ekle ve çıkar işlemleri için ihtiyaç duyulabilmekte.<br/>
/adminekle -> Admin özel komuttur ve '/adminekle TELEGRAM-ID' şeklinde kullanılır. Admin eklemek için kullanılır.<br/>
/adminsil -> Admin özel komuttur ve '/adminsil TELEGRAM-ID' şeklinde kullanılır. Admin silmek için kullanılır.<br/>

/duyuruyap -> Admin özel komuttur ve '/duyuruyap Bu bir duyurudur.' şeklinde kullanılır. Bütün kullanıcılara duyuru iletilir.<br/>

Ayrıca internet sitesinden ayın menüsü çekilirken bir sorun olursa adminler maunel olarak pdf'i değiştiribilmektedir. Sohbete direkt olarak pdf'i atmaları yeterlidir.<br/>

Kullanıcıların aldığı çeşitli hatalarda adminlerin müdahale edebilmesi için alarm sistemi mevcut. Hata alındığında telegram üzerinden tüm adminlere bildirim gider.<br/>


<p align="right">(<a href="#readme-top">başa dön</a>)</p>

<!-- CONTACT -->
## İletişim

Efekan Aksoy - efekan_aksoy@hotmail.com <br/>
LinkedIn hesabıma ulaşmak için: <br/> [![LinkedIn][linkedin]][linkedin-url] <br/>
Proje linki: [https://github.com/rosebud42/telebtu](https://github.com/rosebud42/telebtu)<br/>

<p align="right">(<a href="#readme-top">başa dön</a>)</p>


[linkedin-url]: https://www.linkedin.com/in/efekanaksoy35/
[product-screenshot]: readme-photo.png
[Python.js]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org
[linkedin]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
