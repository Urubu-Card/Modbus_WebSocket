import asyncio
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from services.clp_control import Modbus_Control

class Command(BaseCommand):
    
    help = "Comando Modbus para distrubuição dos WebSockets"
    
    async def poll_loop(self):
        channel_layer =get_channel_layer()
        client = Modbus_Control("127.0.0.1",5020)
        
        await client.Conectar()
        
        
            
        if client.isConnected():
            try:
                while True:
                    data = {}
                    #* Coil
                    coil_result     =  await client.Ler_Coil(0,3)
                    
                    data['motor_status'] = coil_result[0]  
                    data['alerta']       = coil_result[1]  
                    data['bobina']       = coil_result[2]  
                    
                    #* Input Status
                    inputstaus_result =  await client.InputStatus(0,3)
                    data['temperatura']  = inputstaus_result[0]  
                    data['volume']       = inputstaus_result[1]  
                    data['vazao']        = inputstaus_result[2]  


                    #* Holding Register
                    
                    holding_result    =  await client.InputStatus(0,3)
                    data['nivel']        = holding_result[0]  
                    data['pressao']      = holding_result[1]  
                    data['velocidade']   = holding_result[2]  
                    
                    
                    if data:
                        await channel_layer.group_send(
                            'plant_data',
                            {'type':"plant_update",
                            'data':data}
                        )
                        self.stdout.write(f"Enviando data:{data}")
                        
                    else:
                        self.stdout.write(self.style.WARNING("Deu merda"))
                        
                    await asyncio.sleep(1)
                    
            finally:
                client.conexao.FecharConexao()
        
        else:
            self.stdout.write(self.style.ERROR("Não foi possivel conectar ao servidor"))
                
    def handle(self, *args, **options):
        asyncio.run(self.poll_loop())