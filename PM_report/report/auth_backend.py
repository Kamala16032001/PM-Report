# myapp/auth_backend.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ldap3 import Server, Connection, ALL, NTLM

class LDAPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None

        # LDAP server configuration
        server_address = '10.212.70.10'  # Your AD server IP address
        base_dn = 'CN=Users,DC=DS,DC=INDIANOIL,DC=IN'  # Your AD base DN (replace this with actual structure)
        user_dn_template = 'CN={username},CN=Users,DC=DS,DC=INDIANOIL,DC=IN'  # Adjust according to your AD structure
        domain = 'IOC'  # Replace with your domain name

        # Establish connection to the LDAP server
        server = Server(server_address, get_info=ALL)
        conn = Connection(server, user=f'{domain}\\{username}', password=password, authentication=NTLM)

        # Attempt to bind to the LDAP server using the credentials
        if conn.bind():
            # If bind is successful, check if the user exists in Django or create a new one
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If user doesn't exist, create a new user in Django's User model
                user = User.objects.create_user(username=username)
            return user
        else:
            # If authentication fails
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
