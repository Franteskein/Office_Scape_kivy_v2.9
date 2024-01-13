from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.clock import Clock

class ControlTiempoOcio(BoxLayout):
    def __init__(self, **kwargs):
        super(ControlTiempoOcio, self).__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.tiempo_maximo_trabajo = 0
        self.tiempo_maximo_ocio = 30  # 30 minutos de tiempo de ocio máximo
        self.tiempo_trabajado = 0
        self.tiempo_ocio = 0
        self.alerta_mostrada = False

        # Campo de entrada para el tiempo de trabajo en minutos
        self.label_tiempo_trabajo = Label(text="Selecciona el tiempo de trabajo en minutos:", color=(1, 0, 0, 1), font_size=16)
        self.add_widget(self.label_tiempo_trabajo)
        self.slider_tiempo_trabajo = Slider(min=0, max=120, value=0, step=1)
        self.slider_tiempo_trabajo.bind(value=self.actualizar_label_trabajo)
        self.add_widget(self.slider_tiempo_trabajo)
        self.label_tiempo_trabajo_seleccionado = Label(text="0", color=(1, 0, 0, 1), font_size=18)
        self.add_widget(self.label_tiempo_trabajo_seleccionado)

        # Campo de entrada para el tiempo de ocio en minutos
        self.label_tiempo_ocio = Label(text="Selecciona el tiempo de ocio en minutos:", color=(0, 0, 1, 1), font_size=16)
        self.add_widget(self.label_tiempo_ocio)
        self.slider_tiempo_ocio = Slider(min=0, max=120, value=0, step=1)
        self.slider_tiempo_ocio.bind(value=self.actualizar_label_ocio)
        self.add_widget(self.slider_tiempo_ocio)
        self.label_tiempo_ocio_seleccionado = Label(text="0", color=(0, 0, 1, 1), font_size=18)
        self.add_widget(self.label_tiempo_ocio_seleccionado)

        # Botones de inicio y detención
        self.boton_iniciar = Button(text="Iniciar", on_press=self.iniciar_tiempo)
        self.add_widget(self.boton_iniciar)

        self.boton_detener = Button(text="Detener", on_press=self.detener_tiempo)
        self.add_widget(self.boton_detener)

        # Barra de progreso para el tiempo de trabajo y etiqueta de tiempo restante
        self.barra_progreso = ProgressBar(max=100)
        self.add_widget(self.barra_progreso)

        self.etiqueta_tiempo = Label(text="")
        self.add_widget(self.etiqueta_tiempo)

    def iniciar_tiempo(self, instance):
        self.tiempo_maximo_trabajo = int(self.slider_tiempo_trabajo.value) * 60
        self.tiempo_maximo_ocio = int(self.slider_tiempo_ocio.value) * 60
        self.tiempo_trabajado = 0
        self.tiempo_ocio = 0
        self.barra_progreso.value = 0  # Restablecer la barra de progreso
        self.alerta_mostrada = False  # Restablecer la variable de alerta
        self.actualizar_tiempo(None)

    def detener_tiempo(self, instance):
        Clock.unschedule(self.actualizar_tiempo)

    def actualizar_tiempo(self, dt):
        tiempo_total = self.tiempo_maximo_trabajo + self.tiempo_maximo_ocio

        if self.tiempo_trabajado + self.tiempo_ocio < tiempo_total:
            if self.tiempo_trabajado < self.tiempo_maximo_trabajo:
                self.tiempo_trabajado += 1
                porcentaje_trabajo = (self.tiempo_trabajado / self.tiempo_maximo_trabajo) * 100
                self.barra_progreso.value = porcentaje_trabajo

                tiempo_restante_trabajo = self.tiempo_maximo_trabajo - self.tiempo_trabajado
                self.etiqueta_tiempo.text = f"Tiempo de trabajo restante: {tiempo_restante_trabajo // 60} minutos {tiempo_restante_trabajo % 60} segundos"

                if tiempo_restante_trabajo == 0 and not self.alerta_mostrada:
                    self.alerta_mostrada = True
                    self.mostrar_alerta("¡Descanso necesario!", "Has trabajado lo suficiente. ¡Es hora de disfrutar de tu tiempo de ocio!")
            else:
                self.tiempo_ocio += 1
                porcentaje_ocio = (self.tiempo_ocio / self.tiempo_maximo_ocio) * 100
                self.barra_progreso.value = porcentaje_ocio

                tiempo_restante_ocio = self.tiempo_maximo_ocio - self.tiempo_ocio
                self.etiqueta_tiempo.text = f"Tiempo de ocio restante: {tiempo_restante_ocio // 60} minutos {tiempo_restante_ocio % 60} segundos"

                if self.tiempo_ocio == 1:
                    self.mostrar_alerta("¡Tiempo de ocio!", "¡Comenzó tu tiempo de ocio!")

            Clock.schedule_once(self.actualizar_tiempo, 1)
        else:
            self.mostrar_alerta("¡Descanso necesario!", "Has disfrutado de suficiente tiempo de ocio hoy.")
            self.tiempo_trabajado = 0
            self.tiempo_ocio = 0
            self.barra_progreso.value = 0

    def mostrar_alerta(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

    def actualizar_label_trabajo(self, instance, value):
        self.label_tiempo_trabajo_seleccionado.text = str(int(value))

    def actualizar_label_ocio(self, instance, value):
        self.label_tiempo_ocio_seleccionado.text = str(int(value))

class ControlTiempoOcioApp(App):
    def build(self):
        return ControlTiempoOcio()

if __name__ == '__main__':
    ControlTiempoOcioApp().run()
