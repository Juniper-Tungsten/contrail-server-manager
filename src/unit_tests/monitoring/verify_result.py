import unittest

def checkQuantaData(self,output):
	self.assertEqual(output[0].sensor, 'MB1_Temp')
	self.assertEqual(output[0].sensor_type, 'temperature')
	self.assertEqual(output[0].reading, 28)
	self.assertEqual(output[0].unit, 'C')
	self.assertEqual(output[0].status, 'ok')
	self.assertEqual(output[1].sensor, 'PDB_FAN1A')
	self.assertEqual(output[1].sensor_type, 'fan')
	self.assertEqual(output[1].reading, 4700)
	self.assertEqual(output[1].unit, 'RPM')
	self.assertEqual(output[1].status, 'ok')
	self.assertEqual(output[2].sensor, 'PSU_Input_Power')
	self.assertEqual(output[2].sensor_type, 'power')
	self.assertEqual(output[2].reading, 0)
	self.assertEqual(output[2].unit, 'Watts')
	self.assertEqual(output[2].status, 'ok')

def checkSuperMicroData(self, output):
	self.assertEqual(output[0].sensor, 'System Temp')
	self.assertEqual(output[0].sensor_type, 'temperature')
	self.assertEqual(output[0].reading, 28)
	self.assertEqual(output[0].unit, 'C')
	self.assertEqual(output[0].status, 'ok')
	self.assertEqual(output[1].sensor, 'CPU Temp')
	self.assertEqual(output[1].sensor_type, 'temperature')
	self.assertEqual(output[1].reading, 0)
	self.assertEqual(output[1].unit, 'unspecified')
	self.assertEqual(output[1].status, 'ok')
	self.assertEqual(output[2].sensor, 'FAN 1')
	self.assertEqual(output[2].sensor_type, 'fan')
	self.assertEqual(output[2].reading, 3825)
	self.assertEqual(output[2].unit, 'RPM')
	self.assertEqual(output[2].status, 'ok')

def checkChassisData(self,output):
	self.assertEqual(output.system_power, 'on')
	self.assertFalse(output.power_overload)
	self.assertEqual(output.power_interlock, 'inactive')
	self.assertFalse(output.main_power_fault)
	self.assertFalse(output.power_control_fault)
	self.assertEqual(output.power_restore_policy, 'always-off')
	self.assertEqual(output.last_power_event, 'command')
	self.assertEqual(output.chassis_intrusion, 'inactive')
	self.assertEqual(output.front_panel_lockout, 'inactive')
	self.assertFalse(output.drive_fault)
	self.assertFalse(output.cooling_fan_fault)