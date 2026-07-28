from pymodbus.exceptions import ModbusException
import asyncio
import time
try:
    from .clp_conn  import Conexao 
except ImportError:
    from clp_conn import Conexao


class Modbus_Control:

    def __init__(self, ip: str, port: int):
        self.conexao  = Conexao(ip, port)
        self.cliente  = None

    async def Conectar(self):
        conector = await self.conexao.Conectar()
        self.cliente = conector
        return self.cliente

    def isConnected(self):
        return self.cliente is not None and self.cliente.connected

    async def Ler_Coil(self, address: int, count :int = 1):
        try:
            leitor = await self.cliente.read_coils(address=address,count=count)
            if not leitor.isError():
                if count>1:
                    return [bool(bits) for bits in leitor.bits]
                else:
                    return [leitor.bits[0]]
            return f'Erro ao ler: {leitor}'
        except ModbusException as e:
            return f'Erro: {e}'

    async def Escrever_Coil(self, address: int, value: bool):
        try:
            resultado = await self.cliente.write_coil(address=address, value=value)
            if bool(resultado):
                return f'Valor {value} registrado na coil {address}'
            return f'Erro ao escrever na coil: {resultado}'
        except ModbusException as e:
            return f'Erro: {e}'
        


    async def InputStatus(self, address: int ,count :int =1):
        try:
            leitor =  await self.cliente.read_discrete_inputs(address=address,count=count)
            if not leitor.isError():
                if count >1:
                    return [bool(bits)for bits in leitor.bits]
                else:
                    return [bool(leitor.bits[0])]
            return f'Erro: {leitor}'
        except ModbusException as e:
            return f'Erro: {e}'


    async def HoldingRegister(self, address: int,count:int =1):
        try:
            leitor = await self.cliente.read_holding_registers(address,count=count)
            if not leitor.isError():
                if count>1:
                    return [registros for registros in leitor.registers]
                else:
                    return [leitor.registers[0]]
            return f'Erro: {leitor}'
            
        except ModbusException as e:
            return f'Erro: {e}'
        
            
    async def Write_Register(self,address:int,value):
        
        try:
            resultado = await self.cliente.write_register(address,value)
            if not resultado.isError():
                return f"Valor({value} foi inserido com sucesso no endereço:{address} ) "
            else:
                return f"Occoreu um erro :{resultado}"
            
        
        except ModbusException as e:
            return f"Ocoreu um erro: {e}"    
            
     
        

if __name__ == "__main__":
    async def main():
        client = Modbus_Control("127.0.0.1",5020)
        await client.Conectar()
        print(await client.HoldingRegister(1,8))
        #valor = int(input("Insira valor:"))
        #while True:
        #    print(await client.Escrever_Coil(0,valor))
        #    valor += 1
        #    time.sleep(1)

    asyncio.run(main())