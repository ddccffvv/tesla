
import threading
import time

import pytesla

import rpyc

class TeslaThread(threading.Thread):

	def __init__(self, account, parent):
		threading.Thread.__init__(self)
		self.account = account
		#self.credentials = self.account.TeslaCredentials
		self.parent = parent
		self.starttime = time.time()

		# Every 30 minutes we check the metadata
		self.metadata_interval = 60*30

		self.update_interval = self.account.getUpdateInterval()
	
		self.firstrun = True
		self.rpyconnection = rpyc.connect("localhost", 65123)

		

	def run(self):
		print "Startin the thread for account " + str(self.account.Accountid)
		#self.parent.log("Starting the thread for account: " + str(self.account.Accountid))
		self.account.startRunning()
		# Before we start looping we start with the setup of the connection to make sure it all is ready to go
		#all_vehicles = pytesla.Connection(self.credentials[0], self.credentials[1])
		all_vehicles = self.rpyconnection.root.getLoginToken(self.account.Accountid)
		
		
		self.starttime = time.time()

		# Now we are logged in, we can start looping through the data
		while self.parent.KeepRunning():
			diff = float(time.time()) - float(self.starttime)
			if self.firstrun or int(diff % float(self.metadata_interval)) == 0:
				# We fetch everything
				for vehicle in all_vehicles.vehicles():
					carid = vehicle.id
					vinnumber = vehicle.vin
					try:
						carmobile = vehicle.mobile_enabled
					except:
						# Most likely asleep
						print "mobile failed"
						time.sleep(120)
						try:
							carmobile = vehicle.mobile_enabled
						except:
							#self.parent.log("Fetching carmobile failed twice for " + self.account.Accountid)
							print "Mobile failed again!"							
							break
							# TODO Fix this so we can catch this and report it!



					vehicleid = self.parent.getDatabaseHandler().executeQuery("SELECT id from vehicles WHERE accountid=%s and carid=%s and vinnumber=%s",(self.account.Accountid, carid, vinnumber))

					if vehicleid == None:
						# This is rare, but it does happen
						self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO vehicles (accountid, carid, vinnumber, mobile_enabled, updated, brandid, typeid, countryid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (self.account.Accountid, carid, vinnumber, carmobile, int(time.time()), 1, 1, 1),commit=True)
						# TODO Fix the hardcoded brand & country
						
						vehicleid = self.parent.getDatabaseHandler().executeQuery("SELECT id from vehicles WHERE accountid=%s and carid=%s and vinnumber=%s",(self.account.Accountid, carid, vinnumber))



					else:
						# modify the mobile enabled, might be redundant but is the quickest
						self.parent.getDatabaseHandler().executeQueryNoResult("UPDATE vehicles SET mobile_enabled=%s, updated=%s WHERE accountid=%s and carid=%s and vinnumber=%s",(carmobile, int(time.time()), self.account.Accountid, carid, vinnumber),commit=True)

					# The car data has been updated


					# Next bit of the static data: Climate State
					climate_state_data = vehicle.climate_state
					climateid = self.parent.getDatabaseHandler().executeQuery("SELECT id FROM ClimateStates WHERE carid=%s", (vehicleid[0][0]))
					if climateid == None:
						# Insert
						self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO ClimateStates (carid, inside_temp, outside_temp, driver_temp_settings, passenger_temp_setting, is_auto_conditioning_on, is_front_defroster_on, is_rear_defroster_on, fan_status, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vehicleid[0][0], climate_state_data["inside_temp"],climate_state_data["outside_temp"],climate_state_data["driver_temp_setting"],climate_state_data["passenger_temp_setting"],climate_state_data["is_auto_conditioning_on"],climate_state_data["is_front_defroster_on"],climate_state_data["is_rear_defroster_on"],climate_state_data["fan_status"],int(time.time())),commit=True)
					else:
						# Update
						self.parent.getDatabaseHandler().executeQueryNoResult("UPDATE ClimateStates SET inside_temp=%s, outside_temp=%s, driver_temp_setting=%s, passenger_temp_setting=%s, is_auto_conditioning_on=%s, is_front_defroster_on=%s, is_rear_defroster_on=%s, fan_status=%s, updated=%s WHERE id=%s",(climate_state_data["inside_temp"],climate_state_data["outside_temp"],climate_state_data["driver_temp_setting"],climate_state_data["passenger_temp_setting"],climate_state_data["is_auto_conditioning_on"],climate_state_data["is_front_defroster_on"],climate_state_data["is_rear_defroster_on"],climate_state_data["fan_status"],int(time.time()), climateid[0][0]),commit=True)


					# Climate information added

					# Gui states
					gui_settings_data = vehicle.gui_settings
					guisettingsid = self.parent.getDatabaseHandler().executeQuery("SELECT id FROM GUISettings WHERE carid=%s", (vehicleid[0][0]))

					if guisettingsid == None:
						# Adding
						self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO GUISettings (carid, gui_distance_units, gui_temperature_units, gui_charge_rate_units, gui_24_hour_time, gui_range_display, updated) VALUES (%s,%s,%s,%s,%s,%s,%s)", (int(vehicleid[0][0]), gui_settings_data["gui_distance_units"],gui_settings_data["gui_temperature_units"],gui_settings_data["gui_charge_rate_units"],gui_settings_data["gui_24_hour_time"],gui_settings_data["gui_range_display"],int(time.time())),commit=True)
					else:
						# Update
						self.parent.getDatabaseHandler().executeQueryNoResult("UPDATE GUISettings SET gui_distance_units=%s, gui_temperature_units=%s, gui_charge_rate_units=%s, gui_24_hour_time=%s, gui_range_display=%s, updated=%s WHERE id=%s",(gui_settings_data["gui_distance_units"],gui_settings_data["gui_temperature_units"],gui_settings_data["gui_charge_rate_units"],gui_settings_data["gui_24_hour_time"],gui_settings_data["gui_range_display"],int(time.time()), guisettingsid[0][0]),commit=True)

					# GUI data added

					# Last of the static: vehicle data

					vehicle_state_data = vehicle.vehicle_state
					vehiclestateid = self.parent.getDatabaseHandler().executeQuery("SELECT id FROM VehicleStates WHERE carid=%s", (vehicleid[0][0]))
					if vehiclestateid == None:
						# Insert
						self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO VehicleStates (carid, df, dr, pf, ft, rt, car_version, locked, sun_roof_installed, sun_roof_state, sun_roof_percent_open, dark_rims, wheel_type, has_spoiler, roof_color, perf_config, exterior_color, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(vehicleid[0][0], vehicle_state_data["df"], vehicle_state_data["dr"], vehicle_state_data["pf"], vehicle_state_data["ft"], vehicle_state_data["rt"], vehicle_state_data["car_version"], vehicle_state_data["locked"], vehicle_state_data["sun_roof_installed"], vehicle_state_data["sun_roof_state"], vehicle_state_data["sun_roof_percent_open"], vehicle_state_data["dark_rims"], vehicle_state_data["wheel_type"], vehicle_state_data["has_spoiler"], vehicle_state_data["roof_color"], vehicle_state_data["perf_config"], vehicle_state_data["exterior_color"],int(time.time())),commit=True)
					else:
						# Update
						self.parent.getDatabaseHandler().executeQueryNoResult("UPDATE VehicleStates SET df=%s,dr=%s, pf=%s, ft=%s, rt=%s, car_version=%s, locked=%s, sun_roof_installed=%s, sun_roof_state=%s, sun_roof_percent_open=%s, dark_rims=%s, wheel_type=%s, has_spoiler=%s, roof_color=%s, perf_config=%s, exterior_color=%s, updated=%s WHERE id=%s",(vehicle_state_data["df"], vehicle_state_data["dr"], vehicle_state_data["pf"], vehicle_state_data["ft"], vehicle_state_data["rt"], vehicle_state_data["car_version"], vehicle_state_data["locked"], vehicle_state_data["sun_roof_installed"], vehicle_state_data["sun_roof_state"], vehicle_state_data["sun_roof_percent_open"], vehicle_state_data["dark_rims"],vehicle_state_data["wheel_type"], vehicle_state_data["has_spoiler"], vehicle_state_data["roof_color"], vehicle_state_data["perf_config"], vehicle_state_data["exterior_color"],int(time.time()), int(vehicleid[0][0])),commit=True)

			
			# All data
			# First time should have been handled 
			diff = float(time.time()) - float(self.starttime)			
			
			if int(diff % float(self.update_interval)) == 0:
				print "Adding charging data and more"
				# We can add the data
				for vehicle in all_vehicles.vehicles():
					# Get the minimal data
					carid = vehicle.id
					vinnumber = vehicle.vin						
					vehicleid = self.parent.getDatabaseHandler().executeQuery("SELECT id from vehicles WHERE accountid=%s and carid=%s and vinnumber=%s",(self.account.Accountid, carid, vinnumber))
					# Charge states
					charge_state_data = vehicle.charge_state
					self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO ChargeStates (carid, charging_state, charge_limit_soc, charge_limit_soc_std, charge_limit_soc_min, charge_limit_soc_max, charge_to_max_range, battery_heater_on, not_enough_power_to_heat, max_range_charge_counter, fast_charger_present, battery_range, est_battery_range, ideal_battery_range, battery_level, battery_current, charge_energy_added, charge_miles_added_rated, charge_miles_added_ideal, charger_voltage, charger_pilot_current, charger_actual_current, charger_power, time_to_full_charge, charge_rate, charge_port_door_open, scheduled_charging_start_time, scheduled_charging_pending, user_charge_enable_request, charge_enable_request, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(int(vehicleid[0][0]), charge_state_data["charging_state"],charge_state_data["charge_limit_soc"],charge_state_data["charge_limit_soc_std"],charge_state_data["charge_limit_soc_min"],charge_state_data["charge_limit_soc_max"],charge_state_data["charge_to_max_range"],charge_state_data["battery_heater_on"],charge_state_data["not_enough_power_to_heat"],charge_state_data["max_range_charge_counter"],charge_state_data["fast_charger_present"],charge_state_data["battery_range"],charge_state_data["est_battery_range"],charge_state_data["ideal_battery_range"],charge_state_data["battery_level"],charge_state_data["battery_current"],charge_state_data["charge_energy_added"],charge_state_data["charge_miles_added_rated"],charge_state_data["charge_miles_added_ideal"],charge_state_data["charger_voltage"],charge_state_data["charger_pilot_current"],charge_state_data["charger_actual_current"],charge_state_data["charger_power"],charge_state_data["time_to_full_charge"],charge_state_data["charge_rate"],charge_state_data["charge_port_door_open"],charge_state_data["scheduled_charging_start_time"],charge_state_data["scheduled_charging_start_time"],charge_state_data["scheduled_charging_pending"],charge_state_data["user_charge_enable_request"],int(time.time())),commit=True)

					# Drive states 
					drive_state_data = vehicle.drive_state
					self.parent.getDatabaseHandler().executeQueryNoResult("INSERT INTO DriveStates (carid, shift_state, speed, latitude, longitude, heading, gps_as_of, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(vehicleid[0][0]), drive_state_data["shift_state"],drive_state_data["speed"],drive_state_data["latitude"],drive_state_data["longitude"],drive_state_data["heading"],drive_state_data["gps_as_of"], int(time.time())),commit=True)


			self.firstrun = False # Reset for the firstrun
