from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Setting


TOKEN = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {TOKEN}'}


@task()
def smart_home_manager():
    # Получаем данные контроллеров
    resp = requests.get(url, headers=headers)
    controller_data_raw = resp.json().get('data', []) if resp is not None else []
    controller_data = {x['name']: x for x in controller_data_raw}

    payload = {'controllers': []}
    changes_required = False

    def add_control(name, value):
        nonlocal changes_required
        # избегаем добавления команды, если текущее значение уже такое же
        current = controller_data.get(name, {}).get('value')
        # обычное сравнение; для булевых и строковых значений это работает
        if current != value:
            payload['controllers'].append({'name': name, 'value': value})
            changes_required = True

    # ---- Обработка протечки ----
    if controller_data.get('leak_detector', {}).get('value'):
        # если есть протечка — перекрываем холодную/горячую воду, если они открыты
        if controller_data.get('cold_water', {}).get('value'):
            add_control('cold_water', False)

        if controller_data.get('hot_water', {}).get('value'):
            add_control('hot_water', False)

        # отправляем уведомление на почту
        email = EmailMessage(
            'leak detector',
            'text',
            settings.EMAIL_HOST,
            [settings.EMAIL_RECEPIENT],
        )
        email.send(fail_silently=False)

    # если протечка или нет холодной воды — выключаем бойлер и стиралку (если работают/сломаны)
    if controller_data.get('leak_detector', {}).get('value') or \
            not controller_data.get('cold_water', {}).get('value'):
        if controller_data.get('boiler', {}).get('value'):
            add_control('boiler', False)
        wm_val = controller_data.get('washing_machine', {}).get('value')
        if wm_val in ('on', 'broken'):
            add_control('washing_machine', 'off')

    # ---- Температурные настройки ----
    boiler_temperature = controller_data.get('boiler_temperature', {}).get('value')
    try:
        hot_water_target_temperature = float(
            Setting.objects.get(controller_name='hot_water_target_temperature').value
        )
    except Exception:
        hot_water_target_temperature = None

    bedroom_temperature = controller_data.get('bedroom_temperature', {}).get('value')
    try:
        bedroom_target_temperature = float(
            Setting.objects.get(controller_name='bedroom_target_temperature').value
        )
    except Exception:
        bedroom_target_temperature = None

    # ---- Дым ----
    if controller_data.get('smoke_detector', {}).get('value'):
        # если есть дым — выключаем кондиционер, бойлер и свет, но только если они включены
        if controller_data.get('air_conditioner', {}).get('value'):
            add_control('air_conditioner', False)
        if controller_data.get('bathroom_light', {}).get('value'):
            add_control('bathroom_light', False)
        if controller_data.get('bedroom_light', {}).get('value'):
            add_control('bedroom_light', False)
        if controller_data.get('boiler', {}).get('value'):
            add_control('boiler', False)
        wm_val = controller_data.get('washing_machine', {}).get('value')
        if wm_val in ('on', 'broken'):
            add_control('washing_machine', 'off')

    # ---- Возможность включения устройств ----
    can_turn_on = {
        'boiler': controller_data.get('cold_water', {}).get('value') and
                  not controller_data.get('leak_detector', {}).get('value') and
                  not controller_data.get('smoke_detector', {}).get('value') and
                  not controller_data.get('boiler', {}).get('value'),
        'air_conditioner': not controller_data.get('smoke_detector', {}).get('value')
    }

    # Бойлер: включаем/выключаем только если это действительно необходимо
    if (hot_water_target_temperature is not None) and (isinstance(boiler_temperature, (int, float))):
        if (boiler_temperature < hot_water_target_temperature * 0.9) and can_turn_on['boiler']:
            # включаем бойлер только если он сейчас выключен
            add_control('boiler', True)

        if boiler_temperature > hot_water_target_temperature * 1.1:
            # выключаем бойлер только если он сейчас включен
            if controller_data.get('boiler', {}).get('value'):
                add_control('boiler', False)

    # Кондиционер (логика: если слишком холодно — выключаем, если слишком жарко — включаем)
    if (bedroom_target_temperature is not None) and (isinstance(bedroom_temperature, (int, float))):
        if (bedroom_temperature < bedroom_target_temperature * 0.9) and can_turn_on['air_conditioner']:
            # выключаем кондиционер, если он включён
            if controller_data.get('air_conditioner', {}).get('value'):
                add_control('air_conditioner', False)

        if bedroom_temperature > bedroom_target_temperature * 1.1:
            # включаем кондиционер, если он выключен и нет дыма
            if not controller_data.get('air_conditioner', {}).get('value') and can_turn_on['air_conditioner']:
                add_control('air_conditioner', True)

    # ---- Шторы (curtains) ----
    outdoor_light = controller_data.get('outdoor_light', {}).get('value')
    bedroom_light = controller_data.get('bedroom_light', {}).get('value')
    curtains_state = controller_data.get('curtains', {}).get('value')

    if curtains_state != 'slightly_open':
        # открываем, если на улице темно и в спальне нет света
        if (isinstance(outdoor_light, (int, float)) and outdoor_light < 50) and not bedroom_light:
            if curtains_state != 'open':
                add_control('curtains', 'open')
        # закрываем, если светло снаружи или в спальне включён свет
        elif (isinstance(outdoor_light, (int, float)) and outdoor_light > 50) or bedroom_light:
            if curtains_state != 'close':
                add_control('curtains', 'close')

    # ---- Отправка команд только при реальных изменениях ----
    if changes_required and payload['controllers']:
        # удаляем дубликаты, сохраняя порядок
        unique = []
        for item in payload['controllers']:
            if item not in unique:
                unique.append(item)
        payload['controllers'] = unique
        requests.post(url, headers=headers, json=payload)

