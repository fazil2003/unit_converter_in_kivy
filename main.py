from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

class KeyPad(GridLayout):

	def __init__(self, *args, **kwargs):
		super(KeyPad, self).__init__(*args, **kwargs)
		self.cols = 4
		self.rows = 4
		self.create_buttons()

	def create_buttons(self):
		buttons = [7, 8, 9, '<-', 4, 5, 6, 'C', 1, 2, 3 ,'E', 0, '.', '+/-', '-E']

		loop_i=0
		for button in buttons:
			loop_i=loop_i+1
			if((loop_i%4)==0):
				self.add_widget(Button(text=str(button), background_color=(0,0,1,1), color=(1,1,1,1), on_release=self.on_button_pressed))
			elif(button=='+/-'):
				self.add_widget(Button(text=str(button), background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), on_release=self.on_button_pressed))
			else:
				self.add_widget(Button(text=str(button), on_release=self.on_button_pressed))

	def on_button_pressed(self, btn):
		text = App.get_running_app().root.user_input_form.input_box.text

		if btn.text.isdigit():
			text = text + str(btn.text)
		elif btn.text == '<-':
			text = text[:-1]
		elif btn.text == 'C':
			text = ''
		elif btn.text == '+/-':
			text = str(float(text) * -1)
		elif btn.text == '.' and '.' not in text:
			text = text + btn.text
		elif btn.text == 'E':
			text = str(float(text) * 10)
		elif btn.text == '-E':
			text = str(float(text) / 10)

		App.get_running_app().root.user_input_form.input_box.text = text


class ResultList(RecycleView):
	pass


class UserInputForm(BoxLayout):
	input_box = ObjectProperty()
	unit_menu = ObjectProperty()
	metric_menu = ObjectProperty()

	def select_metric(self, spinner):
		if spinner.text == 'Length':
			self.unit_menu.text = 'Meter (m)'
			self.unit_menu.values = ('Meter (m)', 'Kilometer (km)', 'Centimeter (cm)', 'Milimeter (mm)', 'Mile (mile)', 'Yard (yd)', 'Feet (ft)', 'Inch (in)', 'Nautical Mile (nmi)', 'Nautical League (league)') #Decimeter (dm), Furlong, Rod, Chain
		elif spinner.text == 'Area':
			self.unit_menu.text = 'Square Meter (m[sup]2[/sup])'
			self.unit_menu.values = ('Square Meter (m[sup]2[/sup])', 'Square Kilometer (km[sup]2[/sup])', 'Square Centimeter (cm[sup]2[/sup])', 'Square Milimeter (mm[sup]2[/sup])', 'Square Mile (mile[sup]2[/sup])', 'Acre (acre)', 'Hectare (ha)', 'Square Yard (yd[sup]2[/sup])', 'Square Feet (ft[sup]2[/sup])', 'Square Inch (in[sup]2[/sup])')
		elif spinner.text == 'Volume':
			self.unit_menu.text = 'Cubic Meter (m[sup]3[/sup])'
			self.unit_menu.values = ('Cubic Meter (m[sup]3[/sup])', 'Liter (l)', 'Mililiter (ml)', 'Cubic Millimeter (mm[sup]3[/sup])', 'Tablespoon-UK (tblspn)', 'Teaspoon-UK (tspn)', 'Gallon-UK (gal)', 'Ounce-UK (oz)', 'Pint-UK (pint)', 'Quart-UK (quart)')
		elif spinner.text == 'Temparature':
			self.unit_menu.text = 'Celcius ([sup]o[/sup]C)'
			self.unit_menu.values = ('Celcius ([sup]o[/sup]C)', 'Fahrenheit ([sup]o[/sup]F)', 'Kelvin (K)') #rankine
		elif spinner.text == 'Weight':
			self.unit_menu.text = 'Gram (g)'
			self.unit_menu.values = ('Gram (g)', 'Kilogram (kg)', 'Miligram (mg)', 'Pound (lb)', 'Ounce (oz)', 'Tonne-UK (ton)') #short ton, long ton
		elif spinner.text == 'Pressure':
			self.unit_menu.text = 'Pascal (Pa)'
			self.unit_menu.values = ('Pascal (Pa)', 'Kilopascal (kPa)', 'Pound per Sq Inch (psi)', 'Pound per Sq Foot (psf)', 'Atmospheric (atm)', 'Inch Mercury (in Hg)', 'Milimeter Mercury (mm Hg)') # Bar, milibar, megapascal
		elif spinner.text == 'Speed':
			self.unit_menu.text = 'Meter per Second (m/s)'
			self.unit_menu.values = ('Meter per Second (m/s)', 'Kilometer per Hour (km/h)', 'Mile per Hour (mile/h)', 'Feet per Minute (ft/min)', 'Feet per Second (ft/s)', 'Knot (knot)') #, 'Speed of Light (m/s)', 'Speed of Sound (m/s)') 
		elif spinner.text == 'Time':
			self.unit_menu.text = 'Seconds (s)'
			self.unit_menu.values = ('Seconds (s)', 'Minute (min)', 'Hour (hr)', 'Day (day)', 'Week (wk)', 'Month (mo)', 'Year (yr)', 'Decade (dec)', 'Century (c)')
		elif spinner.text == 'Bytes':
			self.unit_menu.text = 'Bit (b)'
			self.unit_menu.values = ('Bit (b)', 'Byte (B)', 'Kilobyte (KB)', 'Megabyte (MB)', 'Gigabyte (GB)', 'Terabyte (TB)')


	def change_unit(self):
		App.get_running_app().root.calculate()


class UnitConverterRoot(BoxLayout):
	user_input_form = ObjectProperty()
	result_list = ObjectProperty()

	def calculate(self):
		if self.user_input_form.metric_menu.text == 'Length':
			self.result_list.data = self.length_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Area':
			self.result_list.data = self.area_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Volume':
			self.result_list.data = self.volume_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Temparature':
			self.result_list.data = self.temparature_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Weight':
			self.result_list.data = self.weight_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Pressure':
			self.result_list.data = self.pressure_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Speed':
			self.result_list.data = self.speed_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Time':
			self.result_list.data = self.time_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)
		elif self.user_input_form.metric_menu.text == 'Bytes':
			self.result_list.daa = self.byte_conversion(self.user_input_form.unit_menu.text, self.user_input_form.input_box.text)

	def length_conversion(self, in_unit, in_num):
		unit_list = ['m', 'km', 'cm', 'mm', 'mile', 'yd', 'ft', 'in', 'nmi', 'league']
		
		if in_num == '':
			return [{'text': '0 m'}, {'text': '0 km'}, {'text': '0 cm'}, {'text': '0 mm'}, {'text': '0 mile'}, {'text': '0 yd'}, {'text': '0 ft'}, {'text': '0 in'}, {'text': '0 nmi'}, {'text': '0 league'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Meter (m)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 1) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.001) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 100) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 1000) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.000621371) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 1.09361) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 3.28084) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 39.3701) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.000539957) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.000179986) + ' league'})

		elif in_unit == 'Kilometer (km)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 1000) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 1) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 100000) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 1000000) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.621371) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 1093.61) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 3280.84) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 39370.1) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.539957) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.179986) + ' league'})

		elif in_unit == 'Centimeter (cm)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 0.01) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.00001) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 1) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 10) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.0000062137) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 0.0109361) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 0.0328084) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 0.393701) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.0000053996) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.0000017999) + ' league'})

		elif in_unit == 'Milimeter (mm)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 0.001) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.000001) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 0.1) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 1) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.00000062137) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 0.00109361) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 0.00328084) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 0.0393701) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.00000053996) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.00000017999) + ' league'})

		elif in_unit == 'Mile (mile)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 1609.34) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 1.60934) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 160934) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 1609340) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 1) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 1760) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 5280) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 63360) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.868976) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.289659) + ' league'})

		elif in_unit == 'Yard (yd)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 0.91440029260800004263) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.000914400292608) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 91.4400292608) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 914.400292608) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.000568182) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 1) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 3) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 36) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.000493737) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.000164579) + ' league'})

		elif in_unit == 'Feet (ft)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 0.3048) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.0003048) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 30.48) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 304.8) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.000189394) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 0.33333344) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 1) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 12) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.000164579) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.00005486) + ' league'})

		elif in_unit == 'Inch (in)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 0.0254) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 0.0000254) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 2.54) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 25.4) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 0.000015783) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 0.0277778) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 0.0833333) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 1) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 0.000013715) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.0000045716) + ' league'})

		elif in_unit == 'Nautical Mile (nmi)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 1852) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 1.852) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 185200) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 1852000) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 1.15078) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 2025.37) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 6076.12) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 72913.4) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 1) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 0.333333) + ' league'})

		elif in_unit == 'League (league)':
			for unit in unit_list:
				if unit == 'm':
					_list.append({'text' : str(in_num * 5556) + ' m'})
				elif unit == 'km':
					_list.append({'text' : str(in_num * 5.556) + ' km'})
				elif unit == 'cm':
					_list.append({'text' : str(in_num * 555600) + ' cm'})
				elif unit == 'mm':
					_list.append({'text' : str(in_num * 5556000) + ' mm'})
				elif unit == 'mile':
					_list.append({'text' : str(in_num * 3.45234) + ' mile'})
				elif unit == 'yd':
					_list.append({'text' : str(in_num * 6076.12) + ' yd'})
				elif unit == 'ft':
					_list.append({'text' : str(in_num * 18228.33333228) + ' ft'})
				elif unit == 'in':
					_list.append({'text' : str(in_num * 218740) + ' in'})
				elif unit == 'nmi':
					_list.append({'text' : str(in_num * 3) + ' nmi'})
				elif unit == 'league':
					_list.append({'text' : str(in_num * 1) + ' league'})

		return _list;

	def area_conversion(self, in_unit, in_num):
		unit_list = ['m[sup]2[/sup]', 'km[sup]2[/sup]', 'cm[sup]2[/sup]', 'mm[sup]2[/sup]', 'mile[sup]2[/sup]', 'acre', 'ha', 'yd[sup]2[/sup]', 'ft[sup]2[/sup]', 'in[sup]2[/sup]']

		if in_num == '':
			return [{'text': '0 m[sup]2[/sup]'}, {'text': '0 km[sup]2[/sup]'}, {'text': '0 cm[sup]2[/sup]'}, {'text': '0 mm[sup]2[/sup]'}, {'text': '0 mile[sup]2[/sup]'}, {'text': '0 acre'}, {'text': '0 ha'}, {'text': '0 yd[sup]2[/sup]'}, {'text': '0 ft[sup]2[/sup]'}, {'text': '0 in[sup]2[/sup]'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Square Meter (m[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.000001) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10000) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0000003861) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.000247105) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.0001) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1.19599) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10.7639) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1550) + ' ' + unit})

		elif in_unit == 'Square Kilometer (km[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10000000000) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1000000000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.386102) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 247.105) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 100) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1196000) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10760000) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1549440000) + ' ' + unit})

		elif in_unit == 'Square Centimeter (cm[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0001) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0000000001) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000000003861) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.000000024711) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.00000001) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.000119599) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00107639) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.155) + ' ' + unit})

		elif in_unit == 'Square Milimeter (mm[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.000001) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.000000000001) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.01) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0000000000003861) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.00000000024711) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.0000000001) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000119599) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0000107639) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00155) + ' ' + unit})

		elif in_unit == 'Square Mile (mile[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 2590000) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 2.58999) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 25900000000) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 2590000000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 640) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 258.999) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 3098000) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 27880000) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 4014000000) + ' ' + unit})

		elif in_unit == 'Acre (acre)':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 4046.86) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00404686) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 40470000) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 4047000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0015625) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.404686) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 4840) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 43560) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 6272999.9993549) + ' ' + unit})

		elif in_unit == 'Hectare (ha)':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10000) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.01) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 100000000) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 10000000000) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00386102) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 2.47105) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 11959.9) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 107639) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 15500015.996032) + ' ' + unit})

		elif in_unit == 'Square Yard (yd[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.836127) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000083613) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 8361.27) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 836127) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000032283) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.000206612) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.000083613) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 9) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1296) + ' ' + unit})

		elif in_unit == 'Square Feet (ft[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.092902873703559998853) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000009290287370356000264) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 929.03) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 92902.87370356) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000003587) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.000022957) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.0000092903) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.111111) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 144) + ' ' + unit})

		elif in_unit == 'Square Inch (in[sup]2[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00064516) + ' ' + unit})
				elif unit == 'km[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.00000000064516) + ' ' + unit})
				elif unit == 'cm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 6.4516) + ' ' + unit})
				elif unit == 'mm[sup]2[/sup]':
					_list.append({'text' : str(in_num * 645.16) + ' ' + unit})
				elif unit == 'mile[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.0000000002491) + ' ' + unit})
				elif unit == 'acre':
					_list.append({'text' : str(in_num * 0.00000015942) + ' ' + unit})
				elif unit == 'ha':
					_list.append({'text' : str(in_num * 0.000000064516) + ' ' + unit})
				elif unit == 'yd[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.000771605) + ' ' + unit})
				elif unit == 'ft[sup]2[/sup]':
					_list.append({'text' : str(in_num * 0.006944445) + ' ' + unit})
				elif unit == 'in[sup]2[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def volume_conversion(self, in_unit, in_num):
		unit_list = ['m[sup]3[/sup]', 'litre', 'ml', 'mm[sup]3[/sup]', 'tblspn', 'tspn', 'gal', 'oz', 'pint', 'quart']

		if in_num == '':
			return [{'text':'0 m[sup]3[/sup]'}, {'text': '0 litre'}, {'text': '0 ml'}, {'text': '0 mm[sup]3[/sup]'}, {'text': '0 tblspn'}, {'text': '0 tspn'}, {'text': '0 gal'}, {'text': '0 oz'}, {'text': '0 pint'}, {'text': '0 quart'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Cubic Meter (m[sup]3[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1000000000) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 56312.1) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 168936.299991511) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 219.96923151543467156) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 35195.077042469543812) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 1759.7538521234771451) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 879.87692606173857257) + ' ' + unit})

		elif in_unit == 'Liter (l)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 56.3121) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 168.936299991511) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.21996923151543462671) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 35.19507704246954205) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 1.7597538521234770137) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.87987692606173850685) + ' ' + unit})

		elif in_unit == 'Mililiter (ml)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.000001) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 0.0563121) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 0.16893629999049697) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.00021996923151411431068) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 0.035195077042258285371) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 0.0017597538521129144854) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.0008798769260564572427) + ' ' + unit})

		elif in_unit == 'Cubic Millimeter (mm[sup]3[/sup])':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.000000001) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.000001) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 0.0000563121) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 0.00016893629999049697) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.000000021996923151411431068) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 3.5195077042258285371) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 1.7597538521129144854) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 8.798769260564572427) + ' ' + unit})

		elif in_unit == 'Tablespoon-UK (tblspn)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.00001775820000841400059) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.017758200008414000426) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 17.758200008414) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 17758.2) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 3) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.0039062500000002550044) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 0.62500000000004074519) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 0.03125000000000204) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.015625) + ' ' + unit})

		elif in_unit == 'Teaspoon-UK (tspn)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.0000059194) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.005919399997219) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 5.9193999972190001202) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 5919.3999972189994878) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 0.333333) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.00130208) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 0.208332800000004037) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 0.010416679999999024) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.00520834) + ' ' + unit})

		elif in_unit == 'Gallon-UK (gal)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.00454609) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 4.54609) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 4546.09) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 4546000) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 256) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 768) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 160) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 8) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 4) + ' ' + unit})

		elif in_unit == 'Ounce-UK (oz)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.000028413) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.0284129999913) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 28.412999991300004865) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 28413.1) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 1.6) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 4.8) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.00625) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 0.05) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.025) + ' ' + unit})

		elif in_unit == 'Pint-UK (pint)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.000568261) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 0.568261) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 568.2609999991457) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 568260.99999914562795) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 32) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 96) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.125) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 20) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 0.5) + ' ' + unit})

		elif in_unit == 'Quart-UK (quart)':
			for unit in unit_list:
				if unit == 'm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 0.00113651999999146) + ' ' + unit})
				elif unit == 'litre':
					_list.append({'text' : str(in_num * 1.13652) + ' ' + unit})
				elif unit == 'ml':
					_list.append({'text' : str(in_num * 1136.9999996997) + ' ' + unit})
				elif unit == 'mm[sup]3[/sup]':
					_list.append({'text' : str(in_num * 1137000) + ' ' + unit})
				elif unit == 'tblspn':
					_list.append({'text' : str(in_num * 64) + ' ' + unit})
				elif unit == 'tspn':
					_list.append({'text' : str(in_num * 192) + ' ' + unit})
				elif unit == 'gal':
					_list.append({'text' : str(in_num * 0.25) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 40) + ' ' + unit})
				elif unit == 'pint':
					_list.append({'text' : str(in_num * 2) + ' ' + unit})
				elif unit == 'quart':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def temparature_conversion(self, in_unit, in_num):
		unit_list = ['[sup]o[/sup]C', '[sup]o[/sup]F', 'K']

		if in_num == '':
			return [{'text': '0 [sup]o[/sup]C'}, {'text': '0 [sup]o[/sup]F'}, {'text': '0 K'}]

		in_num = float(in_num)

		_list = list()
		if in_unit == 'Celcius ([sup]o[/sup]C)':
			for unit in unit_list:
				if unit == '[sup]o[/sup]C':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == '[sup]o[/sup]F':
					_list.append({'text' : str(in_num * 9/5 + 32) + ' ' + unit})
				elif unit == 'K':
					_list.append({'text' : str(in_num + 273.15) + ' ' + unit})
				
		elif in_unit == 'Fahrenheit ([sup]o[/sup]F)':
			for unit in unit_list:
				if unit == '[sup]o[/sup]C':
					_list.append({'text' : str((in_num - 32) * 5/9) + ' ' + unit})
				elif unit == '[sup]o[/sup]F':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'K':
					_list.append({'text' : str((in_num + 459.67) * 5/9) + ' ' + unit})

		elif in_unit == 'Kelvin (K)':
			for unit in unit_list:
				if unit == '[sup]o[/sup]C':
					_list.append({'text' : str(in_num - 273.15) + ' ' + unit})
				elif unit == '[sup]o[/sup]F':
					_list.append({'text' : str((in_num * 9/5) - 459.67) + ' ' + unit})
				elif unit == 'K':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def weight_conversion(self, in_unit, in_num):
		unit_list = ['g', 'kg', 'mg', 'lb', 'oz', 'ton']

		if in_num == '':
			return [{'text': '0 g'}, {'text': '0 kg'}, {'text': '0 mg'}, {'text': '0 lb'}, {'text': '0 oz'}, {'text': '0 ton'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Gram (g)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 0.00220462) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 0.035274) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 0.00000098421) + ' ' + unit})
				
		elif in_unit == 'Kilogram (kg)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 2.20462) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 35.274) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 0.000984207) + ' ' + unit})

		elif in_unit == 'Miligram (mg)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 0.000001) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 0.00000220462) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 0.000035274) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 0.000000000984207) + ' ' + unit})

		elif in_unit == 'Pound (lb)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 453.592) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 0.453592) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 453592) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 16) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 0.000446429) + ' ' + unit})

		elif in_unit == 'Ounce (oz)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 28.3495) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 0.028349500000294) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 28349.500000294003257) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 0.0625) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 0.000027902) + ' ' + unit})

		elif in_unit == 'Tonne-UK (ton)':
			for unit in unit_list:
				if unit == 'g':
					_list.append({'text' : str(in_num * 1016000) + ' ' + unit})
				elif unit == 'kg':
					_list.append({'text' : str(in_num * 1016.05) + ' ' + unit})
				elif unit == 'mg':
					_list.append({'text' : str(in_num * 1016000000) + ' ' + unit})
				elif unit == 'lb':
					_list.append({'text' : str(in_num * 2240) + ' ' + unit})
				elif unit == 'oz':
					_list.append({'text' : str(in_num * 35840) + ' ' + unit})
				elif unit == 'ton':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def pressure_conversion(self, in_unit, in_num):

		unit_list = ['Pa', 'kPa', 'psi', 'psf', 'atm', 'in Hg', 'mm Hg']

		if in_num == '':
			return [{'text': '0 Pa'}, {'text': '0 kPa'}, {'text': '0 psi'}, {'text': '0 psf'}, {'text': '0 atm'}, {'text': '0 in Hg'}, {'text': '0 mm Hg'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Pascal (Pa)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 0.001) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 0.000145038) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 0.021) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.00000986923) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 0.0002953) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 0.00750062) + ' ' + unit})
				
		elif in_unit == 'Kilopascal (kPa)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 0.145038) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 20.885434273039) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.00986923) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 0.2953) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 7.50062) + ' ' + unit})

		elif in_unit == 'Pound per Sq Inch (psi)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 6894.76) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 6.89476) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 144) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.068046) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 2.03602) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 51.714925105101) + ' ' + unit})

		elif in_unit == 'Pound per Sq Foot (psf)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 47.880258888889) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 0.047880258888889) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 0.006944444444444444) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.000472541) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 0.014139) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 0.35913142434098) + ' ' + unit})

		elif in_unit == 'Atmospheric (atm)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 101325) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 101.325) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 14.6959) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 2116.22) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 29.9213) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 760) + ' ' + unit})

		elif in_unit == 'Inch Mercury (in Hg)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 3386.39) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 3.38639) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 0.491154) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 70.726197920632) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.0334211) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 25.400002697664) + ' ' + unit})

		elif in_unit == 'Milimeter Mercury (mm Hg)':
			for unit in unit_list:
				if unit == 'Pa':
					_list.append({'text' : str(in_num * 133.322387415) + ' ' + unit})
				elif unit == 'kPa':
					_list.append({'text' : str(in_num * 0.133322387415) + ' ' + unit})
				elif unit == 'psi':
					_list.append({'text' : str(in_num * 0.019336777496394) + ' ' + unit})
				elif unit == 'psf':
					_list.append({'text' : str(in_num * 2.7844959594807) + ' ' + unit})
				elif unit == 'atm':
					_list.append({'text' : str(in_num * 0.0013157895567935) + ' ' + unit})
				elif unit == 'in Hg':
					_list.append({'text' : str(in_num * 0.039370078434096) + ' ' + unit})
				elif unit == 'mm Hg':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def speed_conversion(self, in_unit, in_num):

		unit_list = ['m/s', 'km/h', 'mile/h', 'ft/min', 'ft/s', 'knot']

		if in_num == '':
			return [{'text': '0 m/s'}, {'text': '0 km/h'}, {'text': '0 mile/h'}, {'text': '0 ft/min'}, {'text': '0 ft/s'}, {'text': '0 knot'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Meter per Second (m/s)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 3.6) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 2.23694) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 196.85) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 3.28084) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 1.94384) + ' ' + unit})
				
		elif in_unit == 'Kilometer per Hour (km/h)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 0.277778) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 0.621371) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 54.6807) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 0.911344) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 0.539957) + ' ' + unit})

		elif in_unit == 'Mile per Hour (mile/h)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 0.44704) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 1.60934) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 88) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 1.46667) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 0.868976) + ' ' + unit})

		elif in_unit == 'Feet per Minute (ft/min)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 0.00508) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 0.018288) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 0.0113636) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 0.0166667) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 0.00987473) + ' ' + unit})

		elif in_unit == 'Feet per Second (ft/s)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 0.3048) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 1.09728) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 0.681818) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 60) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 0.592484) + ' ' + unit})

		elif in_unit == 'Knot (knot)':
			for unit in unit_list:
				if unit == 'm/s':
					_list.append({'text' : str(in_num * 0.514444) + ' ' + unit})
				elif unit == 'km/h':
					_list.append({'text' : str(in_num * 1.852) + ' ' + unit})
				elif unit == 'mile/h':
					_list.append({'text' : str(in_num * 1.15078) + ' ' + unit})
				elif unit == 'ft/min':
					_list.append({'text' : str(in_num * 101.269) + ' ' + unit})
				elif unit == 'ft/s':
					_list.append({'text' : str(in_num * 1.68781) + ' ' + unit})
				elif unit == 'knot':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def time_conversion(self, in_unit, in_num):

		unit_list = ['s', 'min', 'hr', 'day', 'wk', 'mo', 'yr', 'dec', 'c']

		if in_num == '':
			return [{'text': '0 s'}, {'text': '0 min'}, {'text': '0 hr'}, {'text': '0 day'}, {'text': '0 wk'}, {'text': '0 mo'}, {'text': '0 yr'}, {'text': '0 dec'}, {'text': '0 c'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Seconds (s)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 0.0166667) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 0.00027777833333) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 0.00001157409722208333465) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 0.0000016534) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 0.000000380508076156) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.0000000317090410959293262) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.00000000317090410959293262) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.0000000003170904109592932516) + ' ' + unit})

		elif in_unit == 'Minute (min)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 60) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 0.0166667) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 0.000694444) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 0.0000992062857143) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 0.000022831) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.000001902585418569) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.0000001902585418568999935) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.00000001902585418568999803) + ' ' + unit})

		elif in_unit == 'Hour (hr)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 3600) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 60) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 0.0416667) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 0.00595238) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 0.00136986) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.00011415512510136986) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.00001141551251013698563) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.000001141551251013698521) + ' ' + unit})

		elif in_unit == 'Day (day)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 86400) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 1440) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 24) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 0.142857) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 0.032876643423) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.0027397232876831892345) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.00027397232876831892345) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.00002739723287683189167) + ' ' + unit})

		elif in_unit == 'Week (wk)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 604800) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 10080) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 168) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 7) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 0.230137) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.019178104350137) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.0019178104350136998026) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.00019178104350136998568) + ' ' + unit})

		elif in_unit == 'Month (mo)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 2628000) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 43800) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 730.001) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 30.4167) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 4.34524) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 0.0833334) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.008333340000000723) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.000833334) + ' ' + unit})

		elif in_unit == 'Year (yr)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 31540000) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 525600) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 8760) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 365) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 52.1429) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 12) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 0.1) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.01) + ' ' + unit})

		elif in_unit == 'Decade (dec)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 315400000) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 5256000) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 87600) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 3650) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 521.429) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 120) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 10) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 0.1) + ' ' + unit})

		elif in_unit == 'Century (c)':
			for unit in unit_list:
				if unit == 's':
					_list.append({'text' : str(in_num * 3154000000) + ' ' + unit})
				elif unit == 'min':
					_list.append({'text' : str(in_num * 52560000) + ' ' + unit})
				elif unit == 'hr':
					_list.append({'text' : str(in_num * 876000) + ' ' + unit})
				elif unit == 'day':
					_list.append({'text' : str(in_num * 36500) + ' ' + unit})
				elif unit == 'wk':
					_list.append({'text' : str(in_num * 5214.29) + ' ' + unit})
				elif unit == 'mo':
					_list.append({'text' : str(in_num * 1200) + ' ' + unit})
				elif unit == 'yr':
					_list.append({'text' : str(in_num * 100) + ' ' + unit})
				elif unit == 'dec':
					_list.append({'text' : str(in_num * 10) + ' ' + unit})
				elif unit == 'c':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

	def byte_conversion(self, in_unit, in_num):

		unit_list = ['b', 'B', 'KB', 'MB', 'GB', 'TB']

		if in_num == '':
			return [{'text': '0 b'}, {'text': '0 B'}, {'text': '0 KB'}, {'text': '0 MB'}, {'text': '0 GB'}, {'text': '0 TB'}]

		in_num = float(in_num)

		_list = list()

		if in_unit == 'Bit (b)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num / 8) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num / (8*1000)) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num / (8*1000000)) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num / (8*1000000000)) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num / (8*1000000000000)) + ' ' + unit})

		elif in_unit == 'Byte (B)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 8) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num / 1000) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num / 1000000) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num / 1000000000) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num / 1000000000000) + ' ' + unit})

		elif in_unit == 'Kilobyte (KB)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 8 * 1000) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num / 1000) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num / 1000000) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num / 1000000000) + ' ' + unit})

		elif in_unit == 'Megabyte (MB)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 8 * 1000000) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num / 1000) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num / 1000000) + ' ' + unit})

		elif in_unit == 'Gigabyte (GB)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 8 * 1000000000) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num * 1000000000) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num / 1000) + ' ' + unit})

		elif in_unit == 'Terabyte (TB)':
			for unit in unit_list:
				if unit == 'b':
					_list.append({'text' : str(in_num * 8 * 1000000000000) + ' ' + unit})
				elif unit == 'B':
					_list.append({'text' : str(in_num * 1000000000000) + ' ' + unit})
				elif unit == 'KB':
					_list.append({'text' : str(in_num * 1000000000) + ' ' + unit})
				elif unit == 'MB':
					_list.append({'text' : str(in_num * 1000000) + ' ' + unit})
				elif unit == 'GB':
					_list.append({'text' : str(in_num * 1000) + ' ' + unit})
				elif unit == 'TB':
					_list.append({'text' : str(in_num * 1) + ' ' + unit})

		return _list;

			
class UnitConverterApp(App):
	pass

if __name__ == '__main__':
	UnitConverterApp().run()