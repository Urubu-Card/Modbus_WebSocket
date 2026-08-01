import asyncio
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from services.clp_control import Modbus_Control
from ...models import Clp
from asgiref.sync import sync_to_async


def busca_clps():
    dados = []
    resultado =  Clp.objects.filter(ativo=True)
    for clp in resultado:
        dados.append ( {
            "nome":clp.nome,
            "ip":clp.ip,
            "porta":clp.porta,
        })
    return dados
        

class Command(BaseCommand):
    
    help = "Comando Modbus para distrubuição dos WebSockets"
    
    async def poll_loop(self,nome,ip,port):
        channel_layer =get_channel_layer()
        client = Modbus_Control(ip,port)
        
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
                    
                    holding_result    =  await client.HoldingRegister(0,3)
                    data['nivel']        = holding_result[0]  
                    data['pressao']      = holding_result[1]  
                    data['velocidade']   = holding_result[2]  
                    
                    
                    if data:
                        await channel_layer.group_send(
                            f'plant_{nome}',
                            {'type':"plant.update",
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
        asyncio.run(self.main())
        
        
    async def main(self,):

        clps = await sync_to_async(busca_clps)()#? Genial isso ele primeiro transforma e depois chama
        lista_de_clps =[self.poll_loop(clp['nome'],clp['ip'],clp['porta']) for clp in clps]
        await asyncio.gather(*lista_de_clps)