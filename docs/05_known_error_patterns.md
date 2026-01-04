## STM32F407VG Known Error Patterns

1. max_freq_mhz
- Wrong value: 432 MHz
- Reason: PLL / internal clock mistaken as CPU frequency

2. flash_kb
- Wrong value: 524288
- Reason: Address space / bit count mistaken as capacity

3. ram_kb
- Same as flash_kb

4. vdd
- Wrong range: 0.1–8.5 V
- Reason: Absolute maximum rating used instead of operating condition
