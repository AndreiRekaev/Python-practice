import requests
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Setting
from .form import ControllerForm

TOKEN = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {TOKEN}'}


def get_or_update(controller_name, label, value):
    try:
        entry = Setting.objects.get(controller_name=controller_name)
    except Setting.DoesNotExist:
        Setting.objects.create(
            controller_name=controller_name,
            label=label,
            value=value
        )
    else:
        entry.value = value
        entry.save()


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not context.get('data'):
            return self.render_to_response(context, status=502)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Получаем данные контроллеров один раз и сохраняем их в self.current_controller_raw,
        чтобы не выполнять повторный GET в form_valid.
        """
        context = super(ControllerView, self).get_context_data(**kwargs)
        try:
            current_controller_data = requests.get(
                settings.SMART_HOME_API_URL, headers=headers, timeout=5
            ).json()
            context['data'] = current_controller_data
            # Сохраняем внутрь экземпляра в виде списка контроллеров (или пустого списка)
            if isinstance(current_controller_data, dict):
                self.current_controller_raw = current_controller_data.get('data', []) or []
            else:
                self.current_controller_raw = []
        except Exception:
            context['data'] = {}
            self.current_controller_raw = []
        return context

    def get_initial(self):
        initial = super(ControllerView, self).get_initial()
        initial['bedroom_target_temperature'] = 21
        initial['hot_water_target_temperature'] = 80
        return initial

    def form_valid(self, form):
        # Сохраняем настройки в БД
        get_or_update(
            'bedroom_target_temperature',
            'Bedroom target temperature',
            form.cleaned_data['bedroom_target_temperature']
        )
        get_or_update(
            'hot_water_target_temperature',
            'Hot water target temperature value',
            form.cleaned_data['hot_water_target_temperature']
        )

        # Переиспользуем данные контроллеров, получённые в get_context_data.
        # Если их нет — делаем запасной GET (редко происходит).
        controller_data = getattr(self, 'current_controller_raw', None)
        if not controller_data:
            try:
                controller_data = requests.get(url, headers=headers, timeout=5).json().get('data', [])
            except Exception:
                controller_data = []

        if controller_data:
            # helper: найти значение по name
            def find_value(name):
                items = [x for x in controller_data if x.get('name') == name]
                return items[0].get('value') if items else None

            controller_bedroom_light = find_value('bedroom_light')
            controller_bathroom_light = find_value('bathroom_light')
            smoke_detector = find_value('smoke_detector')

            payload = {'controllers': []}

            # Только если нет дыма — разрешаем менять освещение
            if not smoke_detector:
                if form.cleaned_data.get('bedroom_light') != controller_bedroom_light:
                    payload['controllers'].append({
                        'name': 'bedroom_light',
                        'value': form.cleaned_data.get('bedroom_light')
                    })
                if form.cleaned_data.get('bathroom_light') != controller_bathroom_light:
                    payload['controllers'].append({
                        'name': 'bathroom_light',
                        'value': form.cleaned_data.get('bathroom_light')
                    })

                # Отправляем POST только при реальных изменениях
                if payload['controllers']:
                    # удалить дубликаты, сохранить порядок
                    unique = []
                    for item in payload['controllers']:
                        if item not in unique:
                            unique.append(item)
                    payload['controllers'] = unique
                    try:
                        requests.post(url, headers=headers, json=payload, timeout=5)
                    except Exception:
                        # Не прерываем обработку формы из-за ошибки внешнего API
                        pass

        # Возвращаем корректный ответ для form_valid — редирект на success_url
        return super(ControllerView, self).form_valid(form)

