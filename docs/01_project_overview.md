# MCU Specification Schema (V1)

This document defines the **minimum viable specification schema** for MCU data cleaning and structuring in the ChipSelect Data Cleaning project.

The schema is designed for **constraint-based component selection**, not for exhaustive datasheet coverage.

---

## 1. Identification

| Field Name | Type   | Description                         |
| ---------- | ------ | ----------------------------------- |
| vendor     | string | MCU vendor (e.g. ST, NXP, TI)       |
| family     | string | Product family (e.g. STM32F4, S32K) |
| model      | string | Exact part number                   |
| status     | enum   | active / NRND / obsolete            |

---

## 2. Core & Performance

| Field Name   | Type | Description                                  |
| ------------ | ---- | -------------------------------------------- |
| architecture | enum | CPU architecture (e.g. Cortex-M4, Cortex-M7) |
| core_count   | int  | Number of CPU cores                          |
| max_freq_mhz | int  | Maximum operating frequency (MHz)            |

---

## 3. Memory

| Field Name | Type | Description              |
| ---------- | ---- | ------------------------ |
| flash_kb   | int  | On-chip Flash size (KB)  |
| ram_kb     | int  | On-chip RAM size (KB)    |
| eeprom     | bool | On-chip EEPROM available |

---

## 4. Peripherals

| Field Name | Type | Description                |
| ---------- | ---- | -------------------------- |
| can        | bool | CAN controller available   |
| lin        | bool | LIN interface available    |
| ethernet   | bool | Ethernet MAC available     |
| usb        | enum | none / device / host / otg |
| adc_bits   | int  | ADC resolution (bits)      |

---

## 5. Power & Electrical

| Field Name     | Type  | Description                       |
| -------------- | ----- | --------------------------------- |
| vdd_min        | float | Minimum supply voltage (V)        |
| vdd_max        | float | Maximum supply voltage (V)        |
| low_power_mode | bool  | Low power / sleep modes supported |

---

## 6. Package & Environment

| Field Name | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| package    | string | Package type (e.g. LQFP, QFN, BGA) |
| temp_min_c | int    | Minimum operating temperature (°C) |
| temp_max_c | int    | Maximum operating temperature (°C) |

---

## 7. Compliance & Safety

| Field Name       | Type | Description            |
| ---------------- | ---- | ---------------------- |
| automotive_grade | bool | AEC-Q100 qualified     |
| safety_support   | enum | none / ASIL-B / ASIL-D |

---