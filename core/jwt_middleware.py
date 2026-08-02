from urllib.parse import parse_qs
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from asgiref.sync import sync_to_async

def busca_usuario(user_id):
    try:
        usuario = User.objects.get(id=user_id)
        return usuario
    
    except User.DoesNotExist:
        return AnonymousUser()
class JWTAuthMiddleware:
    
    
    def __init__(self,app):
        self.app = app
        
    async def __call__(self, scope,receive,send):
        query = scope['query_string'].decode('utf-8')
        dict_query = parse_qs(query)
        token = dict_query['token']
        print(token)
        
        try:
            validated_token = UntypedToken(token)
            user_Id = validated_token['user_id'] 
            usuario = await sync_to_async(busca_usuario)(user_Id)
            scope['user'] = usuario
            
        except (InvalidToken,TokenError):
            scope["user"]= AnonymousUser()
        
        return await self.app(scope, receive, send)
            