import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict
from models import Phone

# я зашла на сайт интернет-магазина МТС и выбрала
# самые популярные модели смартфонов в трёх категориях
# (Apple, Samsung и Honor), исключив информациию о
# корпусе телефона, т. к., это не является
# техническими характеристиками


def find_n(string, return_int=True):
    # вспомогательная функция, получающая на вход строку,
    # содержащую число, и возвращающая только число
    if string is None:
        return None
    n = re.search(r'[\d\.]+', string).group(0)
    return int(n) if return_int else float(n)


def create_model(slug):
    # функция, выгружающая с сайта shop.mts.ru
    # характеристики телефона и создающая модель
    with urlopen(f'https://shop.mts.ru/product/{slug}/specs') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    name = re.sub(r' [\wА-Яа-яЁё]* –', '', soup.title.string[:-62])
    price = int(soup.find(itemprop='price')['content'])
    phone = Phone.objects.create(name=name, price=price)
    specs_dict = defaultdict(lambda: None, {
        key.get_text().strip(' \n'): value.get_text()
        for key, value in [
            tag.find_all(class_='table-specs__td')
            for tag in soup.find_all(class_='table-specs__tr')
            ]
        })

    setattr(phone, 'screen_technology', specs_dict['Тип цветного экрана'])
    setattr(
        phone, 'screen_diagonal',
        float(find_n(specs_dict['Диагональ экрана']))
        )
    setattr(phone, 'display_resolution', specs_dict['Разрешение экрана'])
    setattr(phone, 'pixel_density', find_n(specs_dict['Разрешение экрана']))
    setattr(phone, 'contrast', find_n(specs_dict['Контрастность']))
    setattr(phone, 'brightness', find_n(specs_dict['Яркость']))

    setattr(phone, 'platform', specs_dict['Платформа'])
    setattr(phone, 'OS', specs_dict['Операционная система'])

    setattr(phone, 'CPU', specs_dict['Процессор'])
    setattr(phone, 'n_cores', find_n(specs_dict['Количество ядер']))
    setattr(
        phone, 'CPU_max_frequency',
        find_n(specs_dict['Максимальная частота процессора'], False)
        )

    if specs_dict['Камера'] == 'Да, двойная':
        setattr(phone, 'cam_modules', 2)
    elif specs_dict['Камера'] == 'Да, 4 модуля':
        setattr(phone, 'cam_modules', 4)
    setattr(
        phone, 'cam_1st_module_resolution',
        find_n(specs_dict['Разрешение основной камеры'])
        )
    setattr(
        phone, 'cam_2nd_module_resolution',
        find_n(specs_dict['Разрешение второй основной камеры'])
        )
    setattr(
        phone, 'cam_3rd_module_resolution',
        find_n(specs_dict['Разрешение третьей основной камеры'])
        )
    setattr(
        phone, 'cam_4th_module_resolution',
        find_n(specs_dict['Разрешение четвертой основной камеры'])
        )
    setattr(
        phone, 'cam_1st_module_aperture',
        find_n(specs_dict['Диафрагма основной камеры'], False)
        )
    setattr(
        phone, 'cam_2nd_module_aperture',
        find_n(specs_dict['Диафрагма второй камеры'], False)
        )
    setattr(
        phone, 'cam_3rd_module_aperture',
        find_n(specs_dict['Диафрагма третьей камеры'], False)
        )
    setattr(
        phone, 'cam_4th_module_aperture',
        find_n(specs_dict['Диафрагма четвертой камеры'], False)
        )
    setattr(
        phone, 'front_resolution',
        find_n(specs_dict['Разрешение фронтальной камеры'])
        )
    setattr(
        phone, 'front_aperture',
        find_n(specs_dict['Диафрагма фронтальной камеры'], False)
        )
    setattr(
        phone, 'video_resolution',
        specs_dict['Разрешение видеосъемки основной камеры (макс)']
        )
    setattr(
        phone, 'front_video_resolution',
        specs_dict['Разрешение видеосъемки фронтальной камеры (макс)']
        )
    setattr(
        phone, 'video_frame_rate',
        specs_dict['Частота кадров при видеосъемке']
        )
    setattr(
        phone, 'digital_zoom_photo',
        find_n(specs_dict['Цифровой Zoom при фотосъемке'])
        )
    setattr(
        phone, 'digital_zoom_video',
        find_n(specs_dict['Цифровой Zoom при видеосъемке'])
        )
    setattr(
        phone, 'optical_zoom_photo',
        find_n(specs_dict['Цифровой Zoom при фотосъемке'])
        )
    setattr(
        phone, 'optical_zoom_video',
        find_n(specs_dict['Оптический Zoom при видеосъемке'])
        )
    setattr(phone, 'cam_functions', specs_dict['Функции камеры'])

    setattr(phone, 'memory', find_n(specs_dict['Объем встроенной памяти']))
    setattr(
        phone, 'availiable_memory',
        find_n(specs_dict['Объем доступной памяти'])
        )
    setattr(phone, 'RAM', find_n(specs_dict['Объем оперативной памяти']))
    if specs_dict['Слот для карты памяти']:
        setattr(phone, 'cartridge', True)
        setattr(phone, 'cartridge_type', 'microSD (TransFlash)')
        setattr(
            phone, 'cartridge_max_capacity',
            find_n(specs_dict['Максимальный объем карты памяти'])
            )

    if specs_dict['Стереозвук']:
        setattr(phone, 'stereo_sound', True)

    setattr(phone, 'audio_formats', specs_dict['Поддержка звуковых форматов'])
    setattr(phone, 'video_formats', specs_dict['Поддержка видео форматов'])

    setattr(phone, 'sensors', specs_dict['Основные датчики'])
    setattr(phone, 'sensors_additional', specs_dict['Дополнительные датчики'])

    setattr(phone, 'cellular_standards', specs_dict['Стандарты сотовой связи'])
    setattr(phone, 'UMTS_3G_ranges', specs_dict['Диапазоны 3G (UMTS)'])
    setattr(phone, 'LTE_ranges', specs_dict['Диапазоны LTE'])
    setattr(phone, 'internet', specs_dict['Интернет'])
    setattr(phone, 'n_sim', find_n(specs_dict['Количество SIM-карт']))
    setattr(phone, 'sim_type', specs_dict['Тип SIM-карты'])
    setattr(phone, 'sim_work_mode', specs_dict['Режим работы SIM-карт'])

    setattr(phone, 'wireless', specs_dict['Беспроводное соединение'])
    setattr(phone, 'wifi', specs_dict['Wi-Fi'])
    if specs_dict['Wi-Fi Direct']:
        setattr(phone, 'wifi_direct', True)
    setattr(phone, 'bluetooth', find_n(specs_dict['Bluetooth'], False))
    setattr(phone, 'bluetooth_profiles', specs_dict['Профили Bluetooth'])
    setattr(phone, 'wired_connection', specs_dict['Проводное соединение'])
    setattr(phone, 'headphone_jack', specs_dict['Разъем для наушников'])

    setattr(phone, 'navigation', specs_dict['Навигация'])
    if specs_dict['digital_compass']:
        setattr(phone, 'Цифровой компас', True)

    setattr(phone, 'battery_type', specs_dict['Тип аккумулятора'])
    setattr(
        phone, 'battery_capacity',
        find_n(specs_dict['Емкость аккумулятора'])
        )
    setattr(
        phone, 'max_time_wifi',
        find_n(specs_dict['Время работы в интернете через Wi-Fi до:'])
        )
    setattr(
        phone, 'max_time_4G_talk',
        find_n(specs_dict['Время в режиме разговора в сети 4G до:'])
        )
    setattr(
        phone, 'max_time_4G',
        find_n(specs_dict['Время работы в интернете в сети 4G до:'])
        )
    setattr(
        phone, 'max_time_music',
        find_n(specs_dict['Время работы в режиме прослушивания музыки до'])
        )
    setattr(
        phone, 'max_time_video',
        find_n(specs_dict['Время работы в режиме просмотра видео до:'])
        )

    phone.save()


create_model('smartfon-apple-iphone-12-128gb-chjernyj')
create_model('smartfon-samsung-a217-galaxy-a21s-3-32gb-black')
create_model('smartfon-honor-7a-blue')
