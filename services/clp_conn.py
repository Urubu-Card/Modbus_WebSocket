
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging
import asyncio

logging.getLogger('pymodbus').setLevel(logging.CRITICAL)


class Conexao:

    def __init__(self, ip: str, port: int):
        self.ip     = ip
        self.porta  = port
        self.cliente = None

    async def Conectar(self):
        "Faz a conexão com o CLP"
        
        try:
            self.cliente = AsyncModbusTcpClient(self.ip, port=self.porta)
            await self.cliente.connect()
            if self.cliente.connected:
                return self.cliente
            else:
                self.cliente = None
                return self.cliente
        except ModbusException:
            self.cliente = None
            return None

    def FecharConexao(self):
        if self.cliente is not None:
            self.cliente.close()

async def main():
    conexao_clp = Conexao("127.0.0.1", 5020)
    
    cliente = await conexao_clp.Conectar()
    print(cliente)
    


if __name__ =="__main__":
    async def main():
        conexao_clp = Conexao("127.0.0.1", 5020)
        
        cliente = await conexao_clp.Conectar()
        print(cliente)
    
    asyncio.run(main())