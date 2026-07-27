"""
Modbus Slave (Server) - pymodbus 3.13.0
========================================
Registradores disponíveis (Device ID = 1):

  Coils           (0x)  endereços 1–100  → leitura/escrita (bits)
  Discrete Inputs (1x)  endereços 1–100  → somente leitura (bits)
  Input Registers (3x)  endereços 1–100  → somente leitura (16-bit)
  Holding Regs    (4x)  endereços 1–100  → leitura/escrita (16-bit)

NOTA: Na versão 3.13, endereços começam em 1 (não 0).

Uso:
  python modbus_slave.py                     # TCP 0.0.0.0:5020 (padrão)
  python modbus_slave.py --port 502          # porta padrão Modbus (requer root)
  python modbus_slave.py --host 127.0.0.1    # somente localhost
  python modbus_slave.py --rtu /dev/ttyUSB0  # modo RTU serial
"""

import argparse
import logging
import asyncio

from pymodbus import ModbusDeviceIdentification
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusDeviceContext,
    ModbusServerContext,
)
from pymodbus.server import StartAsyncTcpServer, StartAsyncSerialServer
from pymodbus.framer import FramerType

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("modbus_slave")


# ---------------------------------------------------------------------------
# Datastore
# ---------------------------------------------------------------------------
def build_context() -> ModbusServerContext:
    """
    Cria o contexto de dados com valores iniciais.
    ATENÇÃO: na pymodbus 3.13 o endereço inicial deve ser >= 1.
    """
    coils       = ModbusSequentialDataBlock(1, [False] * 100)
    discrete    = ModbusSequentialDataBlock(1, [False] * 100)
    input_regs  = ModbusSequentialDataBlock(1, list(range(100)))
    holding_reg = ModbusSequentialDataBlock(1, [1000 + i for i in range(100)])

    device = ModbusDeviceContext(
        di=discrete,        # Discrete Inputs   (FC 02)
        co=coils,           # Coils             (FC 01, 05, 15)
        hr=holding_reg,     # Holding Registers (FC 03, 06, 16)
        ir=input_regs,      # Input Registers   (FC 04)
    )

    # devices= (não slaves=) na pymodbus 3.13
    return ModbusServerContext(devices=device, single=True)


# ---------------------------------------------------------------------------
# Device Identification (FC 43 / MEI)
# ---------------------------------------------------------------------------
def build_identity() -> ModbusDeviceIdentification:
    identity = ModbusDeviceIdentification()
    identity.VendorName         = "Demo Slave"
    identity.ProductCode        = "MOD-SLAVE-01"
    identity.ProductName        = "Modbus Slave Python"
    identity.ModelName          = "PyModbus 3.13"
    identity.MajorMinorRevision = "3.13.0"
    return identity


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
async def run_server(args: argparse.Namespace) -> None:
    context  = build_context()
    identity = build_identity()

    if args.rtu:
        log.info("Iniciando Modbus RTU em %s @ %d baud", args.rtu, args.baudrate)
        await StartAsyncSerialServer(
            context=context,
            identity=identity,
            port=args.rtu,
            baudrate=args.baudrate,
            framer=FramerType.RTU,
            stopbits=1,
            bytesize=8,
            parity="N",
        )
    else:
        log.info("Iniciando Modbus TCP em %s:%d", args.host, args.port)
        await StartAsyncTcpServer(
            context=context,
            identity=identity,
            address=(args.host, args.port),
        )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Modbus Slave — pymodbus 3.13.0")
    p.add_argument("--host",     default="0.0.0.0",
                   help="Endereço de bind TCP (padrão: 0.0.0.0)")
    p.add_argument("--port",     type=int, default=5020,
                   help="Porta TCP (padrão: 5020)")
    p.add_argument("--rtu",      default=None, metavar="SERIAL_PORT",
                   help="Porta serial RTU, ex: /dev/ttyUSB0 ou COM3")
    p.add_argument("--baudrate", type=int, default=9600,
                   help="Baud rate serial (padrão: 9600)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run_server(args))
    except KeyboardInterrupt:
        log.info("Servidor encerrado pelo usuário.")