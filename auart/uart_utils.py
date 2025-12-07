import asyncio

import machine


class UARTUtil:
    """
    UART工具类，用于处理UART通信
    """

    def __init__(self, uart_id, baudrate=9600, tx_pin=None, rx_pin=None, bits=8, parity=None, stop=1):
        """
        初始化UART
        """
        if tx_pin is not None and rx_pin is not None:
            self.uart = machine.UART(
                uart_id,
                baudrate=baudrate,
                tx=tx_pin,
                rx=rx_pin,
                bits=bits,
                parity=parity,
                stop=stop
            )
        else:
            self.uart = machine.UART(
                uart_id,
                baudrate=baudrate,
                bits=bits,
                parity=parity,
                stop=stop
            )

        # 非阻塞清空缓冲区
        try:
            if self.uart.any():
                self.uart.read()
        except:
            pass

    def send(self, data):
        """发送数据"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.uart.write(data)

    def any(self):
        """返回缓冲区可读字节数"""
        try:
            return self.uart.any()
        except:
            return 0

    def read(self):
        """非阻塞读取"""
        try:
            if self.uart.any():
                return self.uart.read()
            return None
        except:
            return None

    def close(self):
        """关闭UART"""
        self.uart.deinit()


async def uart_reader(uart_util, callback):
    print("进入uart_reader")

    buffer = ""
    while True:
        # 先让出调度权
        await asyncio.sleep_ms(10)

        n = uart_util.any()
        if n and n > 0:
            data = uart_util.read()
            if data:
                try:
                    decoded_data = data.decode("utf-8")
                    buffer += decoded_data

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip("\r")
                        if line:
                            callback(line)
                except Exception as e:
                    print("解码错误:", e)
