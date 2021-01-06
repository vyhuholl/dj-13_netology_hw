import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict
from django.core.management.base import BaseCommand
from phones.models import Phone

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
    params = defaultdict(lambda: None)
    params['name'] = re.sub(r' [\wА-Яа-яЁё]* –', '', soup.title.string[:-62])
    params['price'] = int(soup.find(itemprop='price')['content'])
    specs_dict = defaultdict(lambda: None, {
        key.get_text().strip(' \n'): value.get_text()
        for key, value in [
            tag.find_all(class_='table-specs__td')
            for tag in soup.find_all(class_='table-specs__tr')
            ]
        })
    params['screen_technology'] = specs_dict['Тип цветного экрана']
    params['screen_diagonal'] = find_n(specs_dict['Диагональ экрана'], False)
    params['display_resolution'] = specs_dict['Разрешение экрана']
    params['pixel_density'] = find_n(specs_dict['Плотность точек'])
    params['contrast'] = find_n(specs_dict['Контрастность'])
    params['brightness'] = find_n(specs_dict['Яркость'])

    params['platform'] = specs_dict['Платформа']
    params['OS'] = specs_dict['Операционная система']

    params['CPU'] = specs_dict['Процессор']
    params['n_cores'] = find_n(specs_dict['Количество ядер'])
    params['CPU_max_frequency'] = find_n(
        specs_dict['Максимальная частота процессора'], False)

    params['cam_1st_module_resolution'] = find_n(
        specs_dict['Разрешение основной камеры'])
    params['cam_1st_module_aperture'] = find_n(
        specs_dict['Диафрагма основной камеры'], False)
    if specs_dict['Камера'] != 'Да':
        params['cam_modules'] = 2
        params['cam_2nd_module_resolution'] = find_n(
            specs_dict['Разрешение второй основной камеры'])
        params['cam_2nd_module_aperture'] = find_n(
            specs_dict['Диафрагма второй камеры'], False)
        if specs_dict['Камера'] == 'Да, 4 модуля':
            params['cam_modules'] = 4
            params['cam_3rd_module_resolution'] = find_n(
                specs_dict['Разрешение третьей основной камеры'])
            params['cam_3rd_module_aperture'] = find_n(
                specs_dict['Диафрагма третьей камеры'], False)
            params['cam_4th_module_resolution'] = find_n(
                specs_dict['Разрешение четвертой основной камеры'])
            params['cam_4th_module_aperture'] = find_n(
                specs_dict['Диафрагма четвертой камеры'], False)
    params['front_resolution'] = find_n(
        specs_dict['Разрешение фронтальной камеры'])
    params['front_aperture'] = find_n(
        specs_dict['Диафрагма фронтальной камеры'], False)
    params['video_resolution'] = specs_dict[
        'Разрешение видеосъемки основной камеры (макс)']
    params['front_video_resolution'] = specs_dict[
        'Разрешение видеосъемки фронтальной камеры (макс)']
    params['video_frame_rate'] = specs_dict['Частота кадров при видеосъемке']
    params['digital_zoom_photo'] = find_n(
        specs_dict['Цифровой Zoom при фотосъемке'])
    params['digital_zoom_video'] = find_n(
        specs_dict['Цифровой Zoom при видеосъемке'])
    params['optical_zoom_photo'] = find_n(
        specs_dict['Оптический Zoom при фотосъемке'])
    params['optical_zoom_video'] = find_n(
        specs_dict['Оптический Zoom при видеосъемке'])
    params['cam_functions'] = specs_dict['Функции камеры']

    params['memory'] = find_n(specs_dict['Объем встроенной памяти'])
    params['availiable_memory'] = find_n(specs_dict['Объем доступной памяти'])
    params['RAM'] = find_n(specs_dict['Объем оперативной памяти'])
    if specs_dict['Слот для карты памяти']:
        params['cartridge'] = True
        params['cartridge_type'] = 'microSD (TransFlash)'
        params['cartridge_max_capacity'] = find_n(
            specs_dict['Максимальный объем карты памяти'])

    if specs_dict['Стереозвук']:
        params['stereo_sound'] = True

    params['audio_formats'] = specs_dict['Поддержка звуковых форматов']
    params['video_formats'] = specs_dict['Поддержка видео форматов']

    params['sensors'] = specs_dict['Основные датчики']
    params['sensors_additional'] = specs_dict['Дополнительные датчики']

    params['cellular_standards'] = specs_dict['Стандарты сотовой связи']
    params['UMTS_3G_ranges'] = specs_dict['Диапазоны 3G (UMTS)']
    params['LTE_ranges'] = specs_dict['Диапазоны LTE']
    params['internet'] = specs_dict['Интернет']
    params['n_sim'] = find_n(specs_dict['Количество SIM-карт'])
    params['sim_type'] = specs_dict['Тип SIM-карты']
    params['sim_work_mode'] = specs_dict['Режим работы SIM-карт']

    params['wireless'] = specs_dict['Беспроводное соединение']
    params['wifi'] = specs_dict['Wi-Fi']
    if specs_dict['Wi-Fi Direct']:
        params['wifi_direct'] = True
    params['bluetooth'] = find_n(specs_dict['Bluetooth'], False)
    params['bluetooth_profiles'] = specs_dict['Профили Bluetooth']
    params['wired_connection'] = specs_dict['Проводное соединение']
    params['headphone_jack'] = specs_dict['Разъем для наушников']

    params['navigation'] = specs_dict['Навигация']
    if specs_dict['Цифровой компас']:
        params['digital_compass'] = True

    params['battery_type'] = specs_dict['Тип аккумулятора']
    params['battery_capacity'] = find_n(specs_dict['Емкость аккумулятора'])
    params['max_time_wifi'] = find_n(
        specs_dict['Время работы в интернете через Wi-Fi до:'])
    params['max_time_4G_talk'] = find_n(
        specs_dict['Время в режиме разговора в сети 4G до:'])
    params['max_time_4G'] = find_n(
        specs_dict['Время работы в интернете в сети 4G до:'])
    params['max_time_music'] = find_n(
        specs_dict['Время работы в режиме прослушивания музыки до'])
    params['max_time_video'] = find_n(
        specs_dict['Время работы в режиме просмотра видео до:'])

    phone = Phone.objects.create(**params)
    phone.save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        create_model('smartfon-apple-iphone-12-128gb-chjernyj')
        create_model('smartfon-samsung-a217-galaxy-a21s-3-32gb-black')
        create_model('smartfon-honor-7a-blue')
