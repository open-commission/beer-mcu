import uasyncio as asyncio
from uart.uart_utils import UARTUtil


# ---------------- UART 回调 ----------------
def uart_callback(data):
    print("✅ 收到UART数据:", data)


# ---------------- UART 接收任务 ----------------
async def uart_rx_task(uart_util, callback):
    buf = ""
    while True:
        n = uart_util.any()
        if n > 0:
            data = uart_util.safe_read()
            if data:
                try:
                    txt = data.decode()
                    buf += txt

                    # 按行拆包
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip("\r")
                        if line:
                            callback(line)

                except Exception as e:
                    print("❌ 串口解码异常:", e)

        await asyncio.sleep_ms(2)


# ---------------- UART 发送任务 ----------------
async def uart_tx_task(uart_util):
    i = 0
    while True:
        msg = "Hello {}\n".format(i)
        uart_util.send(msg)
        print("📤 发送数据:", msg.strip())
        i += 1
        await asyncio.sleep(1)


# ---------------- 主函数 ----------------
async def main():
    print("🚀 测试程序开始运行...")

    # 初始化 UART
    uart_point = UARTUtil(
        uart_id=1,
        baudrate=115200,
        tx_pin=4,
        rx_pin=5
    )

    print("✅ UART 初始化完成")

    # 并发启动接收和发送任务
    asyncio.create_task(uart_rx_task(uart_point, uart_callback))
    asyncio.create_task(uart_tx_task(uart_point))

    # 主协程挂起，不退出
    while True:
        await asyncio.sleep(10)


# ---------------- 入口 ----------------
asyncio.run(main())
