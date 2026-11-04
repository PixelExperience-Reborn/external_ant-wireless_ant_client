# P2 — ANT+ client/HIDL bridge on AOSP17, native PE-Reborn mondrian

Date: 2026-11-04. **Source-only audit; legacy ANT app/HIDL is NOT selected for base ROM.**

## Provenance and architecture

- Archive `PixelExperience-Reborn/external_ant-wireless_ant_client` `seventeen` HEAD `9598c3df9cd82abb1922d9fb35525d247bf78f14`, last merge 2021, upstream CAF ANT HAL Service and HIDL bindings (Android 12 era).
- Root `Android.bp` defines `AntHalService-Soong` system-ext app, platform-signed, `platform_apis: true`, statically linked `com.dsi.ant-V1.0-java`. This is not an AOSP17 core module or Bluetooth generic HAL.
- `AndroidManifest.xml`: package `com.dsi.ant.server`, `sharedUserId="android.uid.system"`, `targetSdkVersion="29"`, process `system`, **exported** `.AntService`, boot-completed receiver and broad user-management privileges. On Android17 this is a substantial app/permission/attack-surface compatibility risk.
- `vintf/compatibility_matrix.xml`: **`optional="false"`** HIDL `com.dsi.ant@1.0::IAnt/default`. Importing it would make a HAL implementation mandatory for VINTF without evidence that mondrian has an ANT+ radio or compatible vendor firmware. `sepolicy/ANTHALService.te` makes `system_server` an ANT HAL client. These must not be injected in a clean ROM.
- Source `HidlClient.java` binds to `com.dsi.ant.V1_0.IAnt` and maintains a keepalive/retry flow. It cannot supply a missing physical radio or old HIDL HAL implementation by itself.

## Decision and test gates

- **No** `external/ant-wireless/ant_client`, `ant_native`, `ant_service` or `hidl` archive selected by staged official AOSP17 manifest. Do not add ANT packages, privileged sharedUID, `optional=false` compatibility declarations, boot receivers, or SELinux exception simply to satisfy matrix.
- Native PE-Reborn `device/xiaomi/mondrian` must first prove genuine ANT+ hardware/radio (vendor blob/firmware driver and service/VINTF on the physical device), and then separately evaluate if the feature is necessary. Current LF52406 Lineage-based device trees are hardware references only.
- If hardware exists, choose an appropriate modern Android17 app permission and HAL integration model; verify radio coexistence, users/permission boundaries, HIDL/AIDL APIs, VINTF FCM, SELinux, CTS/VTS and functional ANT traffic. Explicitly redesign system UID and exported service handling rather than blindly porting an Android 10-targeted APK.
- No full Soong/HAL build or actual mondrian ANT+ test has occurred. The archive is classified **inactive and hardware-unproven**, not a valid feature port.

## Current audit gates

- [x] Historical app/build/permission and mandatory HAL declaration identified.
- [x] Host-only static source validation workflow authored, with no service installation.
- [ ] Real mondrian vendor ANT capability and installed HAL proven.
- [ ] Modern AOSP17 app/Soong/VINTF/SELinux/CTS integration, if genuinely required.
