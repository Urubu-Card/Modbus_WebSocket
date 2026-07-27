import asyncio
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from services.clp_control import Modbus_Control

class Command(BaseCommand):
    
    help = "Comando Modbus para distrubuição dos WebSockets"
    
    async def poll_loop(self):
        channel_layer =get_channel_layer()
        client = Modbus_Control("127.0.0.1",5020)
        
        
        if client.isConnected():
            while True:
                value = client.HoldingRegister(0)
                
                if value:
                    await channel_layer.group_send(
                        'plant_data',
                        {'type':"plant_update",
                        'data':{"Endereco_0":value}}
                    )
                    self.stdout.write(f"Leitura Completa:{value}")
                    
                else:
                    self.stdout.write(self.style.WARNING(value))
                    
                await asyncio.sleep(1)
        
        else:
            self.stdout.write(self.style.ERROR("Não foi possivel conectar ao servidor"))
                
    def handle(self, *args, **options):
        asyncio.run(self.poll_loop())