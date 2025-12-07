import machine


def init_adc(pin_number=27):
    """
    初始化ADC
    
    Args:
        pin_number (int): ADC引脚号，默认为27（对应Pico的ADC1）
        
    Returns:
        machine.ADC: ADC对象
    """
    return machine.ADC(machine.Pin(pin_number))


def read_adc_value(adc):
    """
    读取ADC值并转换为电压
    
    Args:
        adc (machine.ADC): ADC对象
        
    Returns:
        tuple: (原始ADC值, 电压值)
    """
    # 读取ADC值 (Raspberry Pi Pico ADC是12位，范围0-4095)
    adc_value = adc.read_u16()  # Pico推荐使用read_u16()
    voltage = adc_value * 3.3 / 65535  # 转换为电压值
    
    return adc_value, voltage