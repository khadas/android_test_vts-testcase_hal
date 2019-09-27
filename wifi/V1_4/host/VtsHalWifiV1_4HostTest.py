#!/usr/bin/env python
#
# Copyright (C) 2019 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

from vts.runners.host import const
from vts.runners.host import test_runner
from vts.testcases.template.hal_hidl_gtest import hal_hidl_gtest

class VtsHalWifiV1_4Host(hal_hidl_gtest.HidlHalGTest):
    """Host test class to run the WiFi V1.4 HAL's VTS tests."""

    WIFI_AWARE_FEATURE_NAME = "android.hardware.wifi.aware"
    WIFI_SOFTAP_FEATURE_NAME = "android.hardware.wifi.hostapd"

    def setUpClass(self):
        """Disable android framework."""
        super(VtsHalWifiV1_4Host, self).setUpClass()
        self.dut = self.android_devices[0]
        self.shell = self.dut.shell
        self.dut.stop(True)

    def tearDownClass(self):
        """Enable android framework."""
        self.dut.start()
        super(VtsHalWifiV1_4Host, self).tearDownClass()

    def CreateTestCases(self):
        """Get all registered test components and create test case objects."""
        pm_list = self.shell.Execute("pm list features")
        self._nan_on = self.WIFI_AWARE_FEATURE_NAME in pm_list[const.STDOUT][0]
        logging.info("Wifi NaN Feature Supported: %s", self._nan_on)
        vintf_list = self.shell.Execute("grep android\\.hardware\\.wifi\\.hostapd /vendor/etc/vintf/manifest.xml")
        self._softap_on = self.WIFI_SOFTAP_FEATURE_NAME in vintf_list[const.STDOUT][0]
        logging.info("Wifi SoftAP Feature Supported: %s", self._softap_on)
        super(VtsHalWifiV1_4Host, self).CreateTestCases()

    # @Override
    def CreateTestCase(self, path, tag=''):
        """Create a list of VtsHalWifiV1_4TestCase objects.

        Args:
            path: string, absolute path of a gtest binary on device
            tag: string, a tag that will be appended to the end of test name

        Returns:
            A list of VtsHalWifiV1_4TestCase objects
        """
        gtest_cases = super(VtsHalWifiV1_4Host, self).CreateTestCase(path, tag)
        for gtest_case in gtest_cases:
            if self._nan_on:
                gtest_case.args += " --nan_on"
            if self._softap_on:
                gtest_case.args += " --softap_on"
            logging.info("Added args for test case: %s", gtest_case.args)
        return gtest_cases


if __name__ == "__main__":
    test_runner.main()
