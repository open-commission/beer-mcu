from adc.adc_utils import init_adc, read_adc_value
import utime

def adc_task():
    adc = init_adc(27)

    print("开始读取ADC值...")

    while True:
        adc_value, voltage = read_adc_value(adc)

        # 输出ADC值和电压
        print("ADC值:", adc_value, "电压: {:.2f}V".format(voltage))

        utime.sleep(1)