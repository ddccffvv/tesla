

import pytesla
import rpyc

import time

class Account()


	def __init__(self, parent, accountid, username, updateinterval):
		self.parent = parent
		self.accountid = accountid
		self.username = username
		self.updateinterval = updateinterval
		self.running = False
		self.pyteslaobj = None
		self.dbhandler = self.parent.parent.getDatabaseHandler()
		self.vehicleid = None

	def prepareJob(self):
		c = rpyc.connect("localhost", 65123)
		self.pyteslaobj = c.root.getLoginToken(self.accountid)
		c.close()

	def runjob(self):
		for vehicle in self.pyteslaobj.vehicles():
			# Charge states
			charge_state_data = vehicle.charge_state
			self.dbhandler.executeQueryNoResult("INSERT INTO ChargeStates (carid, charging_state, charge_limit_soc, charge_limit_soc_std, charge_limit_soc_min, charge_limit_soc_max, charge_to_max_range, battery_heater_on, not_enough_power_to_heat, max_range_charge_counter, fast_charger_present, battery_range, est_battery_range, ideal_battery_range, battery_level, battery_current, charge_energy_added, charge_miles_added_rated, charge_miles_added_ideal, charger_voltage, charger_pilot_current, charger_actual_current, charger_power, time_to_full_charge, charge_rate, charge_port_door_open, scheduled_charging_start_time, scheduled_charging_pending, user_charge_enable_request, charge_enable_request, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.vehicleid, charge_state_data["charging_state"],charge_state_data["charge_limit_soc"],charge_state_data["charge_limit_soc_std"],charge_state_data["charge_limit_soc_min"],charge_state_data["charge_limit_soc_max"],charge_state_data["charge_to_max_range"],charge_state_data["battery_heater_on"],charge_state_data["not_enough_power_to_heat"],charge_state_data["max_range_charge_counter"],charge_state_data["fast_charger_present"],charge_state_data["battery_range"],charge_state_data["est_battery_range"],charge_state_data["ideal_battery_range"],charge_state_data["battery_level"],charge_state_data["battery_current"],charge_state_data["charge_energy_added"],charge_state_data["charge_miles_added_rated"],charge_state_data["charge_miles_added_ideal"],charge_state_data["charger_voltage"],charge_state_data["charger_pilot_current"],charge_state_data["charger_actual_current"],charge_state_data["charger_power"],charge_state_data["time_to_full_charge"],charge_state_data["charge_rate"],charge_state_data["charge_port_door_open"],charge_state_data["scheduled_charging_start_time"],charge_state_data["scheduled_charging_start_time"],charge_state_data["scheduled_charging_pending"],charge_state_data["user_charge_enable_request"],int(time.time())),commit=True)

			# Drive states 
			drive_state_data = vehicle.drive_state
			self.dbhandler.executeQueryNoResult("INSERT INTO DriveStates (carid, shift_state, speed, latitude, longitude, heading, gps_as_of, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(self.vehicleid, drive_state_data["shift_state"],drive_state_data["speed"],drive_state_data["latitude"],drive_state_data["longitude"],drive_state_data["heading"],drive_state_data["gps_as_of"], int(time.time())),commit=True)


		
	def runMetajob(self):			
		# Meta job, meta data
		for vehicle in self.pyteslaobj.vehicles():
			carid = vehicle.carid
			vinnumber = vehicle.vin
			try:
				carmobile = vehicle.mobile_enabled
			except:
				#ZZZZZzzzzzzZZZZZ
				time.sleep(60)
				try:
					carmobile = vehicle.mobile_enabled
				except:
					# log this!!
					break


			vehicleid = self.dbhandler.executeQuery("SELECT id from vehicles WHERE carid=% and vinnumber=%s and accountid=%s", (carid, vinnumber, self.accountid))
			if vehicleid == None:
				# Add it
				self.dbhandler.executeQueryNoResult("INSERT INTO vehicles (carid, vinnumber, accountid, mobile_enabled, updated, brandid, typeid, countryid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(carid, vinnumber, self.accountid, carmobile, int(time.time()), 1, 1, 1), commit=True)

				vehicleid = self.dbhandler.executeQuery("SELECT id from vehicles WHERE carid=%s and vinnumber=%s and accountid = %s", (carid, vinnumber, self.accountid))

			else:
				self.dbhandler.executeQueryNoResult("UPDATE vehicles SET mobile_enabled=%s and updated=%s", (carmobile, int(time.time())))

			# For later use
			self.vehicleid = vehicleid[0][0]

			climate_state_data = vehicle.climate_state
			climateid = self.dbhandler.executeQuery("SELECT id FROM ClimateStates WHERE carid=%s", (vehicleid[0][0]))
			if climateid == None:
				# Insert
				self.dbhandler.executeQueryNoResult("INSERT INTO ClimateStates (carid, inside_temp, outside_temp, driver_temp_settings, passenger_temp_setting, is_auto_conditioning_on, is_front_defroster_on, is_rear_defroster_on, fan_status, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vehicleid[0][0], climate_state_data["inside_temp"],climate_state_data["outside_temp"],climate_state_data["driver_temp_setting"],climate_state_data["passenger_temp_setting"],climate_state_data["is_auto_conditioning_on"],climate_state_data["is_front_defroster_on"],climate_state_data["is_rear_defroster_on"],climate_state_data["fan_status"],int(time.time())),commit=True)
			else:
				# Update
				self.dbhandler.executeQueryNoResult("UPDATE ClimateStates SET inside_temp=%s, outside_temp=%s, driver_temp_setting=%s, passenger_temp_setting=%s, is_auto_conditioning_on=%s, is_front_defroster_on=%s, is_rear_defroster_on=%s, fan_status=%s, updated=%s WHERE id=%s",(climate_state_data["inside_temp"],climate_state_data["outside_temp"],climate_state_data["driver_temp_setting"],climate_state_data["passenger_temp_setting"],climate_state_data["is_auto_conditioning_on"],climate_state_data["is_front_defroster_on"],climate_state_data["is_rear_defroster_on"],climate_state_data["fan_status"],int(time.time()), climateid[0][0]),commit=True)


			# Climate information added
			# Gui states
			gui_settings_data = vehicle.gui_settings
			guisettingsid = self.dbhandler.executeQuery("SELECT id FROM GUISettings WHERE carid=%s", (vehicleid[0][0]))

			if guisettingsid == None:
				# Adding
				self.dbhandler.executeQueryNoResult("INSERT INTO GUISettings (carid, gui_distance_units, gui_temperature_units, gui_charge_rate_units, gui_24_hour_time, gui_range_display, updated) VALUES (%s,%s,%s,%s,%s,%s,%s)", (int(vehicleid[0][0]), gui_settings_data["gui_distance_units"],gui_settings_data["gui_temperature_units"],gui_settings_data["gui_charge_rate_units"],gui_settings_data["gui_24_hour_time"],gui_settings_data["gui_range_display"],int(time.time())),commit=True)
			else:
				# Update
				self.dbhandler.executeQueryNoResult("UPDATE GUISettings SET gui_distance_units=%s, gui_temperature_units=%s, gui_charge_rate_units=%s, gui_24_hour_time=%s, gui_range_display=%s, updated=%s WHERE id=%s",(gui_settings_data["gui_distance_units"],gui_settings_data["gui_temperature_units"],gui_settings_data["gui_charge_rate_units"],gui_settings_data["gui_24_hour_time"],gui_settings_data["gui_range_display"],int(time.time()), guisettingsid[0][0]),commit=True)

			# GUI data added

			# Last of the static: vehicle data

			vehicle_state_data = vehicle.vehicle_state
			vehiclestateid = self.dbhandler.executeQuery("SELECT id FROM VehicleStates WHERE carid=%s", (vehicleid[0][0]))
			if vehiclestateid == None:
				# Insert
				self.dbhandler.executeQueryNoResult("INSERT INTO VehicleStates (carid, df, dr, pf, ft, rt, car_version, locked, sun_roof_installed, sun_roof_state, sun_roof_percent_open, dark_rims, wheel_type, has_spoiler, roof_color, perf_config, exterior_color, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(vehicleid[0][0], vehicle_state_data["df"], vehicle_state_data["dr"], vehicle_state_data["pf"], vehicle_state_data["ft"], vehicle_state_data["rt"], vehicle_state_data["car_version"], vehicle_state_data["locked"], vehicle_state_data["sun_roof_installed"], vehicle_state_data["sun_roof_state"], vehicle_state_data["sun_roof_percent_open"], vehicle_state_data["dark_rims"], vehicle_state_data["wheel_type"], vehicle_state_data["has_spoiler"], vehicle_state_data["roof_color"], vehicle_state_data["perf_config"], vehicle_state_data["exterior_color"],int(time.time())),commit=True)
			else:
				# Update
				self.dbhandler.executeQueryNoResult("UPDATE VehicleStates SET df=%s,dr=%s, pf=%s, ft=%s, rt=%s, car_version=%s, locked=%s, sun_roof_installed=%s, sun_roof_state=%s, sun_roof_percent_open=%s, dark_rims=%s, wheel_type=%s, has_spoiler=%s, roof_color=%s, perf_config=%s, exterior_color=%s, updated=%s WHERE id=%s",(vehicle_state_data["df"], vehicle_state_data["dr"], vehicle_state_data["pf"], vehicle_state_data["ft"], vehicle_state_data["rt"], vehicle_state_data["car_version"], vehicle_state_data["locked"], vehicle_state_data["sun_roof_installed"], vehicle_state_data["sun_roof_state"], vehicle_state_data["sun_roof_percent_open"], vehicle_state_data["dark_rims"],vehicle_state_data["wheel_type"], vehicle_state_data["has_spoiler"], vehicle_state_data["roof_color"], vehicle_state_data["perf_config"], vehicle_state_data["exterior_color"],int(time.time()), int(vehicleid[0][0])),commit=True)

