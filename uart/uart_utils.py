import machine


class UARTUtil:
    def __init__(self, uart_id, baudrate=115200, tx_pin=12, rx_pin=13, bits=8, parity=None, stop=1):
        self.uart = machine.UART(
            uart_id,
            baudrate=baudrate,
            tx=machine.Pin(tx_pin),
            rx=machine.Pin(rx_pin),
            bits=bits,
            parity=parity,
            stop=stop
        )

        # 清空缓冲区
        try:
            if self.uart.any():
                self.uart.read()
        except:
            pass

    # 发送数据
    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.uart.write(data)

    # 查询缓冲区
    def any(self):
        try:
            return self.uart.any()
        except:
            return 0

    # 读取数据
    def read(self):
        try:
            if self.uart.any():
                return self.uart.read()
            return None
        except:
            return None

    # 安全读（适用于异步任务）
    def safe_read(self):
        return self.read()
