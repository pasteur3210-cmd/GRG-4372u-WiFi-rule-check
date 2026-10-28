# Shipping Data Validation Tool V1.2.0

Windows 10/11 GUI tool. Select Excel shipment or DT writing log mode. Choose input and output directory, review editable rules, click RUN VALIDATION. Outputs Summary, Detail, Failures and Rule Settings sheets plus EXECUTION and DEBUG logs.

## Build EXE (no local Python required)
1. Upload all files/folders in the Clean GitHub ZIP to a GitHub repo (including `.github/workflows/build.yml`).
2. Select Actions > Build Windows EXE > Run workflow.
3. Download `ShippingDataValidation_V1.2.0` artifact and run the EXE on Windows.

## Rule notes
- SN/MAC must be within inclusive configurable boundaries; sequence gaps are allowed, but MAC addresses must correspond to SN positions using the configured allocation count.
- Duplicate SSIDs across devices are allowed; formatting and 2.4G/5G suffix pairing remain checked.
- MAC allocation defaults to 10 addresses/device. MAC block boundaries, overlap, alignment, and expected start MAC computed from SN number are validated.
- The MAC-to-SN mapping is a production-specific rule inferred from this batch; disable `check_mac_sn_mapping` if another shipment uses a different allocation scheme.
- SSID default is DIGIFIBRA-xxxx / DIGIFIBRA-PLUS-xxxx, alphanumeric four-character shared suffix. Exact suffix specification is a configurable **assumption** not independently established by the supplied message.
- WiFi 2.4G and 5G keys can be equal within a device; cross-device reuse is rejected. Additional Admin/User passwords can be included with `check_other_password_fields`.
- `~` is not allowed by default because source formatting struck it out; `# @ < >` are allowed. Edit setting when confirmed.
- Random generation and independence from fixed identifiers cannot be proven by inspecting exported values. Only obvious full substring reuse is flagged.
- Uniqueness checks are limited to rows in the imported file, not prior manufacturing batches.
- The password policy is applied to WiFi fields only by default. Admin/User password requirements may differ.
- Original Excel is read-only; outputs are new files. Reports contain actual passwords: handle as controlled confidential material.

## V1.2.0 Windows GitHub Actions fix
The read-only Excel input workbook is explicitly closed in a `finally` block, even when validation errors occur. The report workbook and unit-test fixture workbooks are also closed. This prevents Windows `PermissionError: [WinError 32]` when temporary directories are deleted.

## DT writing log mode (V1.2.0)
Select **DT writing log**, browse a `.log` or `.txt` file, and run. The parser reads MES field `cst7` (complete 2.4G SSID), WiFiSSIDSuffix `nvram set/get`, MES `cst10` (WiFi WPA key), and WiFiPwd `nvram set/get`. It verifies complete SSID prefix/suffix rules, key composition, and write/readback consistency. Missing evidence and conflicting values are FAIL. Log mode does not use shipment SN/MAC range settings. It does not prove the actual broadcast 5G SSID, randomness of password generation, or uniqueness across other devices. Source file is never overwritten. Exported workbook includes WPA keys and must be handled as confidential.
