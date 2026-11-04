#!/usr/bin/env python3
"""Archived Android ANT HAL client security inventory; never runs or installs it."""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys
ROOT=Path(__file__).resolve().parents[1]
ANDROID="{http://schemas.android.com/apk/res/android}"
def check(ok,label):
    if not ok: raise AssertionError(label)
    print("PASS archived ANT client:",label)
try:
    bp=(ROOT/"Android.bp").read_text()
    manifest=ET.parse(ROOT/"AndroidManifest.xml").getroot()
    vintf=(ROOT/"vintf/compatibility_matrix.xml").read_text()
    policy=(ROOT/"sepolicy/ANTHALService.te").read_text()
    client=(ROOT/"src/com/dsi/ant/hidl/HidlClient.java").read_text()
    check('name: "AntHalService-Soong"' in bp and '"com.dsi.ant-V1.0-java"' in bp,
          "legacy system-ext app depends on HIDL 1.0 binding")
    check('certificate: "platform"' in bp and "system_ext_specific: true" in bp,
          "platform certificate and system_ext device privilege")
    check(manifest.get("package")=="com.dsi.ant.server"
          and manifest.get(ANDROID+"sharedUserId")=="android.uid.system",
          "archived system UID (not approved for Android17)")
    sdk=manifest.find("uses-sdk")
    check(sdk is not None and sdk.get(ANDROID+"targetSdkVersion")=="29",
          "outdated targetSDK 29")
    service=manifest.find("application/service")
    check(service is not None and service.get(ANDROID+"exported")=="true",
          "old exported ANT service requires security review")
    check('optional="false"' in vintf and "<name>com.dsi.ant</name>" in vintf
          and "<name>IAnt</name>" in vintf and "<instance>default</instance>" in vintf,
          "legacy VINTF unconditionally requires actual ANT HAL")
    check("hal_client_domain(system_server, hal_dsi_ant);" in policy,
          "archived SELinux system server HAL access")
    check("com.dsi.ant.V1_0.IAnt" in client and "KEEPALIVE_TIMEOUT" in client,
          "old HIDL client cannot create physical ANT radio")
    print("PASS source inventory only. No ANT service activated or hardware presence claimed.")
except (AssertionError,OSError,ET.ParseError) as e:
    print("FAIL:",e,file=sys.stderr)
    sys.exit(1)
